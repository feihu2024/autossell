#!/usr/bin/env python
# encoding: utf-8
import re

from sqlalchemy.orm.util import AliasedClass

from model.schema import Base


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


def get_table(table_name: str):
    table = table_map[table_name]
    return table


def get_field(field_name: str, main_table=None):
    if '.' in field_name:
        table_name, field_name = field_name.split('.')
        table = get_table(table_name)
        field = getattr(table, field_name)
        return field
    elif main_table:
        table = main_table
        field = getattr(table, field_name)
        return field
    else:
        raise Exception(f'Invalid field name: {field_name}')
