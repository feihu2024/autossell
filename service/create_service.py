import re
from typing import Literal, Union, Tuple

from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Query, Session

from common import Dao, global_function
from model.m_schema import *
from model.schema import Base
from dao.d_query import to_datetime
from datetime import datetime

router = APIRouter()


def camel_to_snake(camel_str):
    _camel_str = camel_str[1:]
    components = re.findall(r'[A-Z][^A-Z]*', _camel_str)
    return '_'.join(x.lower() for x in components)


def get_table_map():
    from model.schema import __dict__ as schema_dict
    t_map = {key: val for key, val in schema_dict.items() if isinstance(val, type) and issubclass(val, Base)}
    t_map = {key: val for key, val in t_map.items() if key != 'Base'}
    t_map = {camel_to_snake(key): val for key, val in t_map.items()}
    return t_map

def get_model_map():
    from model.m_schema import __dict__ as m_dict
    t_map = {key: val for key, val in m_dict.items() if isinstance(val, type) and issubclass(val, BaseModel)}
    t_map = {key: val for key, val in t_map.items() if key[0] == 'S'}
    t_map = {camel_to_snake(key): val for key, val in t_map.items()}
    return t_map



table_map = get_table_map()
model_map = get_model_map()

def get_table(table_name):
    table = table_map[table_name]
    return table

def get_model(table_name):
    model = model_map[table_name]
    return model

def clean_dict(item: dict) -> dict:
    return {key: val for key, val in item.items() if val is not None}

class UpdateItem(BaseModel):
    table: str
    id: int
    data: dict

def get_ref_field_values(name: str, db: Session, new_data: dict, data: dict):
    vals = name.split('.')
    if len(vals) == 3:
        table_name = f'{vals[0]}.{vals[1]}'
        field_name = vals[2]
    elif len(vals) == 2:
        table_name = vals[0]
        field_name = vals[1]
    else:
        raise Exception(f'Invalid ref of field name: {name}')
    inst = new_data.get(table_name, None)
    if inst is None:
        table_values = data.pop(table_name)
        inst = create_item(table_name, table_values, db, new_data, data)
    new_data[table_name] = inst
    return getattr(inst, field_name)


def create_item(table_name, table_values: dict, db: Session, new_data: dict, data: dict):
    new_table_values = {}
    for key, val in table_values.items():
        if key[-1] == '@':
            new_table_values[key[:-1]] = get_ref_field_values(val, db, new_data, data)
        else:
            new_table_values[key] = val

    names = table_name.split('.')
    if len(names) == 2:
        new_table_name = names[0]
    elif len(names) == 1:
        new_table_name = table_name
    else:
        raise Exception(f'Invalid table name: {table_name}')

    table = get_table(new_table_name)
    new_table_values = clean_dict(new_table_values)
    if 'id' in new_table_values:
        data.pop('id')
    new_table_values = {
        key: to_datetime(val) if getattr(table, key).type.python_type == datetime else val
        for key, val in new_table_values.items()
    }
    inst = table(**new_table_values)
    db.add(inst)
    db.flush()

    model = get_model(new_table_name)
    return model.parse_obj(inst.__dict__)

def create(items: dict) -> dict:
    data = {}
    for key, item in items.items():
        if isinstance(item, dict):
            data[key] = item
        elif isinstance(item, list):
            for i, v in enumerate(item):
                data[f'{key}.{i}'] = v
        else:
            raise Exception(f'Invalid data type: {type(item)}')

    data = global_function.reversed_dict(data)
    new_data = {}
    with Dao() as db:
        try:
            while data:
                table_name, val = data.popitem()
                new_data[table_name] = create_item(table_name, val, db, new_data, data)
            db.commit()
        except Exception as e:
            db.rollback()
            raise e

    new_data = {k: new_data[k] for k in sorted(new_data)}
    formetted_data = {}
    for key, val in new_data.items():
        names = key.split('.')
        if len(names) == 2:
            table_name, idx = names[0], int(names[1])
            if table_name not in formetted_data:
                formetted_data[table_name] = [val]
            else:
                formetted_data[table_name].append(val)
        elif len(names) == 1:
            formetted_data[key] = val
        else:
            raise Exception(f'Invalid table name: {key}')

    return formetted_data
