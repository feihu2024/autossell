import sys
from typing import List, Optional, Literal

import mysql.connector
from urllib.parse import urlparse
from pydantic import BaseModel, Field



class Link(BaseModel):
    table_name: str = Field(..., title='表名')
    relation: Literal['one', 'many']  = Field(..., title='关系')

class DBColumn(BaseModel):
    name: str = Field(..., title='字段名')
    type: str = Field(..., title='字段类型')
    is_primary: bool = Field(..., title='是否主键')
    is_null: bool = Field(..., title='是否允许为空')
    default: Optional[str] = Field(..., title='默认值')
    comment: str = Field(..., title='字段注释')
    is_foreign: bool = Field(default=False, title='是否外键')


class DBTable(BaseModel):
    name: str = Field(..., title='表名')
    alias: str = Field(..., title='表别名')
    camel_name: str = Field(..., title='驼峰命名')
    columns: List[DBColumn] = Field(..., title='字段列表')
    comment: str = Field(..., title='表注释')
    links: List[Link] = Field(default=[], title='关联关系')




def main():
    if len(sys.argv) < 2:
        print('请输入连接字符串')
        exit(0)

    tables = get_tables_from_db(sys.argv[1])
    tables = add_foreign(tables)
    tables = add_one_link(tables)
    tables = add_many_link(tables)
    # for table in tables:
    #     print(table.name, table.links)

    schema_code = generate_schema(tables)
    with open('./model/linked_schema.py', 'w') as f:
        f.write(schema_code)
    # print(schema_code)

    model_code = generate_model(tables)
    with open('./model/linked_model.py', 'w') as f:
        f.write(model_code)

    router_code = generate_router(tables)

    dao_code = generate_dao(tables)


def generate_router(tables: List[DBTable]) -> str:
    code = f"""from typing import List, Optional"""
    return code

def generate_dao(tables: List[DBTable]) -> str:
    code = f"""from common import Dao
from model.linked_schema import *
from model.linked_model import *
"""
    pass
    # for table in tables:

    print('end')


def generate_model(tables: List[DBTable]) -> str:
    code = f"""from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
"""
    for table in tables:
        code += generate_model_table(table)
    return code


def generate_model_table(table: DBTable) -> str:
    code = f"""
    
class {table.camel_name[1:]}Base(BaseModel):
"""
    for column in table.columns:
        code += generate_model_column(column)

    for link in table.links:
        code += generate_model_link(link)

    return code


def generate_model_link(link: Link) -> str:
    code = ''
    model_name = convert_to_camel_case(link.table_name) + 'Base'
    if link.relation == 'one':
        code += f"""    {link.table_name}: Optional['{model_name}'] = None\n"""
    elif link.relation == 'many':
        code += f"""    {link.table_name}_list: Optional[List['{model_name}']] = None\n"""
    return code


def generate_model_column(column: DBColumn) -> str:
    python_type = mysql_type_to_python_type(column.type)
    code = f"""    {column.name}: Optional[{python_type}] = Field(None, title='{column.comment}')\n"""
    return code



def generate_schema(tables: List[DBTable]) -> str:
    code = f"""from sqlalchemy import Column, Float, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT, VARCHAR
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List

Base = declarative_base()
metadata = Base.metadata
"""
    code += generate_schema_tables(tables)
    return code


def generate_schema_tables(tables: List[DBTable]) -> str:
    code = ''
    for table in tables:
        code += generate_schema_table(table)
    return code

def generate_schema_table(table: DBTable) -> str:
    code = f"""
    
class {table.camel_name}(Base):
    __tablename__ = '{table.name}'
    __table_args__ = {{'comment': '{table.comment}'}}
    
"""
    for column in table.columns:
        code += generate_schema_column(column)
    code += '\n'

    for link in table.links:
        code += generate_schema_link(table.alias, link)

    return code

def generate_schema_column(column: DBColumn) -> str:
    tmp = ''
    if column.is_foreign:
        link_table_name = 't_' + column.name[:-3]
        tmp = f" ForeignKey('{link_table_name}.id'),"
    primary_key = ''
    if column.is_primary:
        primary_key = ' primary_key=True,'

    code = f'    {column.name} = Column({mysql_type_to_sqlalchemy_type(column.type)},{tmp} nullable={column.is_null}, server_default=text("{column.default}"),{primary_key} comment="{column.comment}")\n'
    return code

def generate_schema_link(table_name: str, link: Link) -> str:
    model_name = convert_to_camel_case('t_' + link.table_name)
    if link.relation == 'one':
        code = f'    {link.table_name} = relationship("{model_name}", uselist=False, back_populates="{table_name}_list", lazy="select")\n'
    elif link.relation == 'many':
        code = f'    {link.table_name}_list = relationship("{model_name}", uselist=True, back_populates="{table_name}", lazy="select")\n'
    else:
        raise Exception('未知的关系类型')
    return code


def add_foreign(tables: List[DBTable]) -> List[DBTable]:
    table_names = [table.name[2:] for table in tables]
    for table in tables:
        for column in table.columns:
            if len(column.name) > 3 and column.name[-3:] == '_id':
                if column.name[:-3] in table_names:
                    column.is_foreign = True
                else:
                    print(f'外键 {column.name} 没有对应的表')
    return tables


def add_one_link(tables: List[DBTable]) -> List[DBTable]:
    for table in tables:
        for column in table.columns:
            if column.is_foreign:
                table.links.append(Link(table_name=column.name[:-3], relation='one'))
    return tables


def add_many_link(tables: List[DBTable]) -> List[DBTable]:
    one_links = {}
    for table in tables:
        for link in table.links:
            if link.relation == 'one':
                if link.table_name in one_links:
                    one_links[link.table_name].append(table.alias)
                else:
                    one_links[link.table_name] = [table.alias]

    for table in tables:
        if table.alias in one_links:
            for link_table in one_links[table.alias]:
                table.links.append(Link(table_name=link_table, relation='many'))
    return tables


def get_tables_from_db(db: str) -> List[DBTable]:
    """
    从数据库获取所有表
    :return:
    """
    # 解析 MySQL 连接字符串
    url = urlparse(db)
    db_config = {
        "host": url.hostname,
        "user": url.username,
        "password": url.password,
        "database": url.path[1:]
    }

    # 创建数据库连接
    mydb = mysql.connector.connect(**db_config)

    # 创建游标对象
    mycursor = mydb.cursor()

    # 执行SQL查询语句
    mycursor.execute("select table_name, table_comment from information_schema.tables where table_schema = '{}'".format(db_config['database']))

    # 获取查询结果
    tables = mycursor.fetchall()

    # 输出所有表的名称
    tables = [table for table in tables]

    # 遍历所有表的名称
    tabs = []
    for table in tables:
        table_name = table[0]
        assert table_name[:2] == 't_', '表名必须以t_开头'

        # 获取当前表的字段信息
        mycursor.execute("select column_name, data_type, column_key, is_nullable, column_default, column_comment from information_schema.columns where table_schema = '{}' and table_name = '{}'".format(db_config['database'], table_name))
        columns = mycursor.fetchall()

        # 输出当前表的字段信息
        cols = []
        for column in columns:
            col = DBColumn(name=column[0], type=column[1], is_primary=column[2] == 'PRI', is_null=column[3] == 'YES', default=column[4], comment=column[5])
            cols.append(col)
        tab = DBTable(name=table_name, alias=table_name[2:], camel_name=convert_to_camel_case(table_name), columns=cols, comment=table[1])
        tabs.append(tab)

    # 关闭游标和连接对象
    mycursor.close()
    mydb.close()
    return tabs


def convert_to_camel_case(s):
    # 首先将字符串按照下划线分割成一个列表
    words = s.split('_')

    # 对于每个单词，将首字母大写，其他字母小写
    capitalized_words = [word.capitalize() for word in words]

    # 将所有单词连接起来并返回
    return ''.join(capitalized_words)

def mysql_type_to_sqlalchemy_type(mysql_type):
    if mysql_type == 'int':
        return 'Integer'
    elif mysql_type == 'varchar':
        return 'String'
    elif mysql_type == 'float':
        return 'Float'
    elif mysql_type == 'timestamp':
        return 'TIMESTAMP'
    elif mysql_type == 'tinyint':
        return 'TINYINT'
    else:
        return 'VARCHAR(255)'

def mysql_type_to_python_type(mysql_type):
    if mysql_type == 'int':
        return 'int'
    elif mysql_type == 'varchar':
        return 'str'
    elif mysql_type == 'float':
        return 'float'
    elif mysql_type == 'timestamp':
        return 'datetime'
    elif mysql_type == 'tinyint':
        return 'bool'
    else:
        return 'str'


if __name__ == '__main__':
    main()