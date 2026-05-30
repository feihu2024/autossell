import ast
import re
from pathlib import Path
from typing import Optional, Tuple, List, Dict, Union

root_dir = Path(__file__).parents[1]
model_dir = root_dir / 'model'

model_file = model_dir / 'm_schema.py'
router_file = root_dir / 'router' / 'r_schema.py'
dao_file = root_dir / 'dao' / 'd_db.py'


def main():
    with open(str(model_dir / 'schema.py'), 'r') as f:
        cml = ast.parse(f.read(), str(model_dir / 'schema.py'))

    write_model_header(str(model_file))
    write_dao_header(str(dao_file))
    write_router_header(str(router_file))

    classes = [item for item in cml.body if isinstance(item, ast.ClassDef)]
    for c in classes:
        transfer_sqlalchemy_pydantic(c)
    # print(classes)
    pass


def write_model_header(file: str):
    with open(file, 'w') as f:
        header = \
            """from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from fastapi.exceptions import HTTPException

"""
        f.write(header)


def write_dao_header(file: str):
    with open(file, 'w') as f:
        header = """from common import Dao
from common.db import SessionLocal
from typing import List
from model.m_schema import *
from model.schema import *
from fastapi.exceptions import HTTPException

def model2dict(item) -> dict:
    return {key: val for key, val in item.dict().items() if val is not None}
"""
        f.write(header)


def write_router_header(file: str):
    with open(file, 'w') as f:
        header = """from fastapi import APIRouter
from typing import List
from dao import d_db
from model.m_schema import *
from fastapi.exceptions import HTTPException
import re

router = APIRouter()
"""
        f.write(header)


def transfer_sqlalchemy_pydantic(c: ast.ClassDef) -> str:
    class_name = c.name[1:]
    primary = None
    cols = []
    col_names = []
    col_types = []
    for assign in c.body:
        assign: ast.Assign
        if not isinstance(assign.value, ast.Call):
            continue
        col, is_primary, col_name, col_type = extract_col(assign)
        col_names.append(col_name)
        col_types.append(col_type)
        if is_primary:
            primary = col
        else:
            cols.append(col)
    print(class_name)
    create_class_str = \
        f"""
class Create{class_name}(BaseModel):
    """ + '    '.join(cols)

    class_str = \
        f"""
        
class S{class_name}(Create{class_name}):
    {primary}
    class Config:
        orm_mode = True

class {class_name}(Create{class_name}):
    id: Optional[int] = None
    class Config:
        orm_mode = True

class FilterRes{class_name}(BaseModel):
    data: List[S{class_name}]
    total: int
    """

    model_code = create_class_str + class_str

    create_router, create_dao = create_code(class_name)
    update_router, update_dao = update_code(class_name)
    delete_router, delete_dao = delete_code(class_name)
    get_router, get_dao = get_code(class_name)
    filter_router, filter_dao = filter_code(class_name, cols=col_names, types=col_types)

    #router_code = create_router + delete_router + update_router + get_router + filter_router
    router_code = create_router + update_router + get_router + filter_router
    dao_code = create_dao + delete_dao + update_dao + get_dao + filter_dao

    with open(str(model_file), 'a') as f:
        f.write(model_code)

    with open(str(router_file), 'a') as f:
        f.write(router_code)

    with open(str(dao_file), 'a') as f:
        f.write(dao_code)
    return class_str


def create_code(class_name: str) -> Tuple[str, str]:
    l_class_name = re.sub(r'([A-Z])', lambda m: '_' + m.group(1), class_name).lower().strip('_')

    router_code = f"""
    
@router.post(f'/{l_class_name}/create', response_model=S{class_name})
async def create_{l_class_name}(item: Create{class_name}) -> S{class_name}:
    dict_item = dict(item)
    for k,v in dict_item.items():
        if v is not None:
            v = str(v)
            v = v.replace(" ", "")
            get_search = re.search(r"'", v, flags=0)
            get_search2 = re.search(r'%27', v, flags=0)
            get_search3 = re.search(r'unionselect', v, flags=0)
            if get_search or get_search2 or get_search3:
               raise HTTPException(status_code=404, detail='bad way~~~~~~')

    return d_db.insert_{l_class_name}(item)
        """

    dao_code = f"""
    
def insert_{l_class_name}(item: Create{class_name}, db: Optional[SessionLocal] = None) -> S{class_name}:
    data = model2dict(item)
    t = T{class_name}(**data)
    if db:
        db.add(t)
        db.flush()
        db.refresh(t)
        return SAddress.parse_obj(t.__dict__)
    with Dao() as db:
        db.add(t)
        db.commit()
        db.refresh(t)
    return S{class_name}.parse_obj(t.__dict__)
"""

    return router_code, dao_code


def update_code(class_name: str) -> Tuple[str, str]:
    l_class_name = re.sub(r'([A-Z])', lambda m: '_' + m.group(1), class_name).lower().strip('_')
    router_code = f"""
    
@router.post(f'/{l_class_name}/update', response_model=str)
async def update_{l_class_name}(item: S{class_name}) -> str:
    d_db.update_{l_class_name}(item)
    return "success"
"""

    dao_code = f"""
    
def update_{l_class_name}(item: S{class_name}, db: Optional[SessionLocal] = None):
    data = model2dict(item)
    data.pop('id')
    if db:
        db.query(T{class_name}).where(T{class_name}.id == item.id).update(data)
        db.flush()
        return
    
    with Dao() as db:
        db.query(T{class_name}).where(T{class_name}.id == item.id).update(data)
        db.commit()
"""
    return router_code, dao_code


def delete_code(class_name: str) -> Tuple[str, str]:
    l_class_name = re.sub(r'([A-Z])', lambda m: '_' + m.group(1), class_name).lower().strip('_')
    router_code = f"""
    
@router.post(f'/{l_class_name}/delete', response_model=str)
async def delete_{l_class_name}({l_class_name}_id: int) -> str:
    d_db.delete_{l_class_name}({l_class_name}_id)
    return "success"
"""

    dao_code = f"""
    
def delete_{l_class_name}({l_class_name}_id: int, db: Optional[SessionLocal] = None):
    if db:
        db.query(T{class_name}).where(T{class_name}.id == {l_class_name}_id).delete()
        db.flush()
        return
    
    with Dao() as db:
        db.query(T{class_name}).where(T{class_name}.id == {l_class_name}_id).delete()
        db.commit()
"""
    return router_code, dao_code


def get_code(class_name: str) -> Tuple[str, str]:
    l_class_name = re.sub(r'([A-Z])', lambda m: '_' + m.group(1), class_name).lower().strip('_')
    router_code = f"""
    
@router.get(f'/{l_class_name}/get', response_model=S{class_name})
async def get_{l_class_name}({l_class_name}_id: int) -> S{class_name}:
    return d_db.get_{l_class_name}({l_class_name}_id)
"""

    dao_code = f"""
    
def get_{l_class_name}({l_class_name}_id: int) -> Optional[S{class_name}]:
    with Dao() as db:
        t = db.query(T{class_name}).where(T{class_name}.id == {l_class_name}_id).first()
        if t:
            return S{class_name}.parse_obj(t.__dict__)
        else:
            return None
"""
    return router_code, dao_code


def filter_code(class_name: str, cols: List[str], types: List[str]) -> Tuple[str, str]:
    search_cols = [col for col, t in zip(cols, types) if t == 'str']
    col_queries = [
        f'''
        {col}: Optional[str] = None''' for col in cols
    ]
    col_searches = [
        f'''
        s_{col}: Optional[str] = None''' for col in search_cols
    ]
    col_sets = [
        f'''
        l_{col}: Optional[str] = None''' for col in cols
    ]

    query_str = ', '.join(col_queries)
    search_str = ', '.join(col_searches)
    set_str = ', '.join(col_sets)

    if len(col_searches) > 0:
        search_str = search_str + ','

    l_class_name = re.sub(r'([A-Z])', lambda m: '_' + m.group(1), class_name).lower().strip('_')

    format_strs = []
    set_format_strs = []
    for col, t in zip(cols, types):
        convert_str = ''
        if t == 'int':
            convert_str = 'int(val)'
        elif t == 'str':
            convert_str = 'val'
        elif t == 'float':
            convert_str = 'float(val)'
        elif t == 'datetime':
            convert_str = 'datetime.fromtimestamp(int(val))'
        else:
            raise Exception(f'unknown type: {t}')

        block_str = f"""
    if {col} is not None:
        values = {col}.split(',')
        if len(values) == 1:
            val = values[0]
            items['{col}'] = {convert_str}
        else:
            val = values[0]
            if val != '':
                items['{col}_start'] = {convert_str}
            
            val = values[1]
            if val != '':
                items['{col}_end'] = {convert_str}
        """
        format_strs.append(block_str)

        set_block_str = f"""
    if l_{col} is not None:
        values = l_{col}.split(',')
        values = [{convert_str} for val in values]
        set_items['{col}'] = values
        """
        set_format_strs.append(set_block_str)

    format_str = ''.join(format_strs)
    set_format_str = ''.join(set_format_strs)
    search_format_str = ''.join([
        f"""
    if s_{col} is not None:
        search_items['{col}'] = '%' + s_{col} + '%'
        """
        for col in search_cols
    ])

    router_doc_code = f'''
    """
    1. 按照字段查询`?field1=value1&field2=value2`
    2. 按照范围查询，大于某个值`?field=value,`, 表示filed大于value
    3. 按照范围查询，小于某个值`?field=,value`， 表示field小于value
    4. 按照范围查询，范围值`?field=value1,value2`，表示搜索field大于等于value1，小于等于value2
    5. page是页数，第一页为1
    6. page_size为每一页大小， 默认20
    7. 如果是日期，请使用时间戳，十位的时间戳，单位：秒
    8. 所有字符串字段均可搜索，需要在字段前加个前缀`s_`,例如搜索`username`包含`zhang`， 则可以这样`s_username=zhang`写,这里只是一个假设
    9. 字段的多选择（in关系），需要在字段前加前缀`l_`,并且以逗号`,`隔开,例如要找出`id=2`或者`id=3`的样本，可以这样写`?l_id=2,3`
    """
    '''
    router_condition_code = f"""
    items = dict()
    search_items = dict()
    set_items = dict()
{format_str}
{search_format_str}
{set_format_str}    
    """

    router_code = f"""

@router.get(f'/{l_class_name}/filter', response_model=FilterRes{class_name})
async def filter_{l_class_name}({query_str}, {set_str}, {search_str}
        order_by: Optional[str] = None,
        page: int = 1, 
        page_size: int = 20) -> FilterRes{class_name}:
{router_doc_code}
{router_condition_code}
    
    order_items = dict()
    if order_by is not None:
        orders = order_by.split(',')
        for order in orders:
            if order.startswith('-'):
                order_items[order[1:]] = 'desc'
            else:
                order_items[order] = 'asc'
    data = d_db.filter_{l_class_name}(items, search_items, set_items, order_items, page, page_size)
    c = d_db.filter_count_{l_class_name}(items, search_items, set_items)
    
    return FilterRes{class_name}(data=data, total=c)
"""

    router_code2 = f"""

@router.get(f'/{l_class_name}/fast_filter', response_model=FilterRes{class_name})
async def fast_filter_{l_class_name}({query_str}, {set_str}, {search_str}
        page: int = 1, 
        page_size: int = 20) -> FilterRes{class_name}:
{router_doc_code}
{router_condition_code}
    data = d_db.filter_{l_class_name}(items, search_items, set_items, page, page_size)
    return FilterRes{class_name}(data=data, total=-1)
"""

    filter_code = ''.join([
        f"""
        if '{col}' in items:
            q = q.where(T{class_name}.{col} == items['{col}'])
        if '{col}_start' in items:
            q = q.where(T{class_name}.{col} >= items['{col}_start'])
        if '{col}_end' in items:
            q = q.where(T{class_name}.{col} <= items['{col}_end'])
        """
        for col in cols
    ])

    set_filter_code = ''.join([
        f"""
        if '{col}' in set_items:
            q = q.where(T{class_name}.{col}.in_(set_items['{col}']))
        """
        for col in cols
    ])

    search_filter_code = ''.join([
        f"""
        if '{col}' in search_items:
            q = q.where(T{class_name}.{col}.like(search_items['{col}']))
        """
        for col in search_cols
    ])

    order_code = \
        f"""
        orders = []
        for col, val in order_items.items():
            if val == 'asc':          
                #orders.append(T{class_name}.{col}.asc())
                orders.append(T{class_name}.id.asc())
            elif val == 'desc':
                #orders.append(T{class_name}.{col}.desc())
                orders.append(T{class_name}.id.desc())
            else:
                raise HTTPException(400, 'order value must be asc or desc')
        if len(order_items) > 0:
            q = q.order_by(*orders)
        """

    dao_condition_code = f"""
{filter_code}
{set_filter_code}
{search_filter_code}
    """

    empty_set = '{}'

    dao_code = f"""

def filter_{l_class_name}(
    items: dict, 
    search_items: dict={empty_set}, 
    set_items: dict={empty_set}, 
    order_items: dict={empty_set},
    page: int = 1,
    page_size: int = 20) -> List[S{class_name}]:
    with Dao() as db:
        q = db.query(T{class_name})
{dao_condition_code}
{order_code}
        t_{l_class_name}_list = q.offset(page*page_size-page_size).limit(page_size).all()
        return [S{class_name}.parse_obj(t.__dict__) for t in t_{l_class_name}_list]


def filter_count_{l_class_name}(items: dict, search_items: dict={empty_set}, set_items: dict={empty_set}) -> int:
    with Dao() as db:
        q = db.query(T{class_name})
{dao_condition_code}
        c = q.count()
        return c
"""

    router_code += router_code2
    return router_code.replace("'''", '"""'), dao_code


def extract_col(col: ast.Assign) -> Tuple[str, bool]:
    name = extract_name(col.targets[0])
    t, is_primary, raw_t = extract_type(col.value)
    field = extract_comment(col.value)

    if field:
        col = f'{name}: {t} = {field}\n'
    else:
        col = f'{name}: {t}\n'

    return col, is_primary, name, raw_t


def extract_name(c: Union[ast.expr, ast.Name]) -> str:
    return c.id


def extract_args(c: Union[ast.expr, ast.Call]) -> List[str]:
    args = []
    for arg in c.args:
        if isinstance(arg, ast.Name):
            args.append(arg.id)
        elif isinstance(arg, ast.Call):
            func: ast.expr = arg.func
            args.append(func.id)
    return args


def extract_keywords(c: Union[ast.expr, ast.Call]) -> Dict[str, str]:
    keywords = {
        keyword.arg: None if isinstance(keyword.value, ast.Call) else keyword.value.value
        for keyword in c.keywords
    }
    return keywords


def extract_type(c: Union[ast.expr, ast.Call]) -> Tuple[str, bool]:
    keywords = extract_keywords(c)
    args = extract_args(c)
    m = {
        'Integer': 'int',
        'TINYINT': 'int',
        'String': 'str',
        'TIMESTAMP': 'datetime',
        'Float': 'float',
        'VARCHAR': 'str',
        'text': 'str',
        'TEXT': 'str',
        'Text': 'str',
        'mediumtext': 'str',
        'MEDIUMTEXT': 'str',
        'LONGTEXT': 'str',
        'DECIMAL': 'float',
        'CHAR': 'str',
    }

    t = args[0]
    t = m[t]

    if 'primary_key' in keywords:
        return t, True, t
    else:
        return f'Optional[{t}]', False, t


def extract_comment(c: Union[ast.expr, ast.Call]) -> Optional[str]:
    keywords = extract_keywords(c)
    # keywords = {keyword.arg: keyword.value.value for keyword in c.keywords}
    comment = keywords.get('comment', None)
    if comment is None:
        return None
    return f"Field(title='{comment}')"


if __name__ == '__main__':
    main()
