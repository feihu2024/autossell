import re
from typing import Literal, Union, Tuple
from dao import d_query

from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Query
from sqlalchemy.orm.util import AliasedClass

from common import Dao
from model.m_schema import *
from model.schema import Base

router = APIRouter()


def camel_to_snake(camel_str):
    _camel_str = camel_str[1:]
    components = re.findall(r'[A-Z][^A-Z]*', _camel_str)
    return '_'.join(x.lower() for x in components)


def get_table_map():
    from model.schema import __dict__ as schema_dict
    from model.alias_schema import __dict__ as alias_dict
    local_dict = {**schema_dict, **alias_dict}
    t_map = {key: val for key, val in local_dict.items() if isinstance(val, AliasedClass) or isinstance(val, type) and issubclass(val, Base)}
    t_map = {key: val for key, val in t_map.items() if key != 'Base'}
    t_map = {camel_to_snake(key): val for key, val in t_map.items()}
    return t_map


table_map = get_table_map()


class FilterData(BaseModel):
    field: str = Field(..., title='字段名')
    op: Literal['==', '>', '<', 'between', 'in', 'like', 'is null', 'is not null'] = Field('==', title='操作符')
    value: Union[str, int, List[Union[str, int]]] = Field(..., title='值')


class OrderByData(BaseModel):
    field: str = Field(..., title='字段名')
    order: Literal['desc', 'asc'] = Field('asc', title='排序方式')


class JoinData(BaseModel):
    table: str = Field(..., title='表名')
    on_left: str = Field(..., title='左表字段')
    on_right: str = Field("id", title='右表字段')
    method: Literal['left', 'right', 'inner'] = Field('left', title='连接类型')


class QueryData(BaseModel):
    table: str = Field(..., title='表名')
    joins: Optional[List[JoinData]] = Field([], title='关联表')
    filters: Optional[List[FilterData]] = Field([], title='过滤条件')
    order_by: Optional[List[OrderByData]] = Field([], title='排序字段')


class FilterQueryData(QueryData):
    page: int = Field(1, title='页码')
    page_size: int = Field(10, title='每页数量')


class GroupQueryData(QueryData):
    group_by: Optional[List[str]] = Field([], title='分组字段')
    having: Optional[List[str]] = Field([], title='分组条件')
    selects: List[str] = Field([], title='返回数据')


class FilterGroupQueryData(GroupQueryData):
    page: int = Field(1, title='页码')
    page_size: int = Field(10, title='每页数量')


def get_table(table_name):
    table = table_map[table_name]
    return table

def is_int(val) -> bool:
    try:
        return True if int(val) else False
    except:
        return False

def to_datetime(value: Union[int, datetime, str]) -> datetime:
    if isinstance(value, int) or is_int(value):
        return datetime.fromtimestamp(int(value))
    elif isinstance(value, str):
        if 'T' in value:
            value = value.replace('T', ' ')
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    elif isinstance(value, datetime):
        return value
    else:
        raise ValueError('value must be int or str')


def filter_query(query: Query, main_table, filters: List[FilterData]) -> Query:
    filter_items

    for _filter in filters:
        if not isinstance(_filter.value, List):
            _filter.value = [_filter.value]

        filed_names = _filter.field.split('.')
        if len(filed_names) > 1:
            table = get_table(filed_names[0])
            field = getattr(table, filed_names[1])
        else:
            field = getattr(main_table, _filter.field)

        if field.type.python_type == datetime:
            _filter.value = [to_datetime(v) for v in _filter.value]

        if _filter.op == '==':
            query = query.filter(field == _filter.value[0])
        elif _filter.op == '>':
            query = query.filter(field > _filter.value[0])
        elif _filter.op == '<':
            query = query.filter(field < _filter.value[0])
        elif _filter.op == 'between':
            query = query.filter(field.between(_filter.value[0], _filter.value[1]))
        elif _filter.op == 'in':
            query = query.filter(field.in_(_filter.value))
        elif _filter.op == 'like':
            query = query.filter(field.like(_filter.value[0]))
        elif _filter.op == 'is null':
            query = query.filter(field.is_(None))
        elif _filter.op == 'is not null':
            query = query.filter(field.isnot(None))
    return query


def join_query(query: Query, main_table, joins: List[JoinData]) -> Query:
    for join in joins:
        right_table = get_table(join.table)
        left_field = getattr(main_table, join.on_left)
        right_field = getattr(right_table, join.on_right)
        if join.method == 'left':
            query = query.outerjoin(right_table, left_field == right_field)
        elif join.method == 'right':
            query = query.join(right_table, left_field == right_field)
        elif join.method == 'inner':
            query = query.join(right_table, left_field == right_field)
    return query


def order_query(query: Query, main_table, order_by: List[OrderByData]) -> Query:
    for order_by_data in order_by:
        field = order_by_data.field
        order = order_by_data.order

        field_names = field.split('.')
        if len(field_names) > 1:
            table = get_table(field_names[0])
            field = getattr(table, field_names[1])
        else:
            field = getattr(main_table, field)
        if order == 'desc':
            query = query.order_by(field.desc())
        elif order == 'asc':
            query = query.order_by(field.asc())
    return query


def group_by_query(query: Query, main_table, group_by: List[str]) -> Query:
    fields = [field.split('.') for field in group_by]
    fields = [getattr(get_table(field[0]), field[1]) if len(field) == 2 else getattr(main_table, field[0]) for
              field in fields]
    query = query.group_by(*fields)
    return query


def having_query(query: Query, stats, _having: List[str]) -> Query:
    for having in _having:
        stat_name, op_name, op_value = resolve_having(having)
        if stat_name in stats:
            stat_value = stats[stat_name]
        else:
            stat_value = get_select_value_by_name(stat_name)[1]

        if op_name == '==':
            query = query.having(stat_value == op_value)
        elif op_name == '>':
            query = query.having(stat_value > op_value)
        elif op_name == '<':
            query = query.having(stat_value < op_value)
        elif op_name == '>=':
            query = query.having(stat_value >= op_value)
        elif op_name == '<=':
            query = query.having(stat_value <= op_value)
    return query


@router.post('/get')
async def get(query_data: QueryData) -> dict:
    return d_query.get(query_data=query_data)

    tables = [query_data.table]
    if query_data.joins:
        tables.extend([join.table for join in query_data.joins])
    tables = [get_table(table) for table in tables]
    main_table = tables[0]

    with Dao() as db:
        query: Query = db.query(*tables)
        if query_data.joins:
            query = join_query(query, main_table, query_data.joins)

        if query_data.filters:
            query = filter_query(query, main_table, query_data.filters)

        if query_data.order_by:
            query = order_query(query, main_table, query_data.order_by)

        item = query.first()

        return {
            "code": 0,
            "data": item,
        }


@router.post('/filter')
async def filter_items(query_data: d_query.FilterQueryData) -> dict:
    return d_query.filter_items(query_data=query_data)


table_regex = re.compile(r"[a-z_]+")
filed_regex = re.compile(r"([a-z_]+)\.([a-z_]+)")
stat_regex = re.compile(r"(\w+)\(([a-z_]+)\.([a-z_]+)\)")
having_regex = re.compile(r"(\w+\([a-z_]+\.[a-z_]+\))(==|>|<|>=|<=)(\d+)")


def get_select_value_by_name(name: str):
    table_value = re.fullmatch(table_regex, name)
    if table_value:
        return 'table', get_table(table_value.group(0)), name

    filed_value = re.fullmatch(filed_regex, name)
    if filed_value:
        return 'filed', getattr(get_table(filed_value.group(1)), filed_value.group(2)), name

    stat_value = re.fullmatch(stat_regex, name)
    if stat_value:
        op_name = stat_value.group(1)
        table_name = stat_value.group(2)
        field_name = stat_value.group(3)
        field = getattr(get_table(table_name), field_name)
        stat_method = getattr(func, op_name)
        value = stat_method(field).label(f"{op_name}_{table_name}_{field_name}")
        return 'stat', value, name


def resolve_having(having: str) -> Tuple[str, str, int]:
    value = re.fullmatch(having_regex, having)
    if value:
        stat_name = value.group(1)
        op_name = value.group(2)
        op_value = int(value.group(3))
        return stat_name, op_name, op_value
    else:
        raise Exception(f"不支持的having条件：{having}")


@router.post('/group/filter')
async def group_filter(query_data: FilterGroupQueryData) -> dict:
    main_table = get_table(query_data.table)

    tables = {}
    fields = {}
    stats = {}
    for select in query_data.selects:
        item = get_select_value_by_name(select)
        if item[0] == 'table':
            tables[item[2]] = item[1]
        elif item[0] == 'filed':
            fields[item[2]] = item[1]
        elif item[0] == 'stat':
            stats[item[2]] = item[1]
        else:
            raise Exception(f"不支持的查询字段：{select}")

    selects = list(tables.values()) + list(fields.values()) + list(stats.values())

    with Dao() as db:
        query: Query = db.query(*selects)
        if query_data.joins:
            query = join_query(query, main_table, query_data.joins)

        if query_data.filters:
            query = filter_query(query, main_table, query_data.filters)

        if query_data.group_by:
            query = group_by_query(query, main_table, query_data.group_by)
            fields = [field.split('.') for field in query_data.group_by]
            fields = [getattr(get_table(field[0]), field[1]) if len(field) == 2 else getattr(main_table, field[0]) for
                      field in fields]
            query = query.group_by(*fields)

        if query_data.having:
            query = having_query(query, stats, query_data.having)

        if query_data.order_by:
            query = order_query(query, main_table, query_data.order_by)

        total = query.count()
        query = query.offset((query_data.page - 1) * query_data.page_size).limit(query_data.page_size)
        data = query.all()
        return {
            "data": data,
            "total": total
        }


@router.post('/group/get')
async def group_get(query_data: GroupQueryData) -> dict:
    main_table = get_table(query_data.table)

    tables = {}
    fields = {}
    stats = {}
    for select in query_data.selects:
        item = get_select_value_by_name(select)
        if item[0] == 'table':
            tables[item[2]] = item[1]
        elif item[0] == 'filed':
            fields[item[2]] = item[1]
        elif item[0] == 'stat':
            stats[item[2]] = item[1]
        else:
            raise Exception(f"不支持的查询字段：{select}")

    selects = list(tables.values()) + list(fields.values()) + list(stats.values())

    with Dao() as db:
        query: Query = db.query(*selects)
        if query_data.joins:
            query = join_query(query, main_table, query_data.joins)

        if query_data.filters:
            query = filter_query(query, main_table, query_data.filters)

        if query_data.group_by:
            query = group_by_query(query, main_table, query_data.group_by)

        if query_data.having:
            query = having_query(query, stats, query_data.having)

        if query_data.order_by:
            query = order_query(query, main_table, query_data.order_by)

        item = query.first()
        return {
            "code": 0,
            "data": item
        }
