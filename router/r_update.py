import re
from typing import Dict, Literal, Union, Tuple
import logging

from fastapi import APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Query, Session
from fastapi.exceptions import HTTPException

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
    t_map = {key: val for key, val in schema_dict.items() if isinstance(val, type) and issubclass(val, Base)}
    t_map = {key: val for key, val in t_map.items() if key != 'Base'}
    t_map = {camel_to_snake(key): val for key, val in t_map.items()}
    return t_map


table_map = get_table_map()

def get_table(table_name):
    table = table_map[table_name]
    return table

def clean_dict(item: dict) -> dict:
    return {key: val for key, val in item.items() if val is not None}

def update_item(table_name, id: int, item: dict, db: Session):
    table = get_table(table_name)
    data = clean_dict(item)
    if 'id' in data:
        data.pop('id')
    db.query(table).where(table.id == id).update(data)


def update_item_v2(table_name, item: dict, db: Session):
    table = get_table(table_name)
    if 'id' not in item:
        db.add(table(**item))
    table_id = item['id']
    res = db.query(table).where(table.id == table_id).update(item)
    if res == 0:
        logging.error(f'update failed: res={res}, table={table_name}, id={table_id}')
        raise HTTPException(400, f'invalid table and id: {table_name}, {table_id}')


class UpdateItem(BaseModel):
    table: str
    id: int
    data: dict

@router.post('')
async def update(items: List[UpdateItem]) -> dict:
    with Dao() as db:
        for item in items:
            update_item(item.table, item.id, item.data, db)
        db.commit()


@router.post('/v2')
async def update_v2(data: dict) -> dict:
    with Dao() as db:
        for table_name, items in data.items():
            if isinstance(items, List):
                for item in items:
                    update_item_v2(table_name, item, db)
            elif isinstance(items, Dict):
                update_item_v2(table_name, items, db)
            else:
                raise Exception('invalid data')
        db.commit()

