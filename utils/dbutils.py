"""
Created on Jul 22, 2013

@author: drifter
"""
from utils.utils import flatten


def get_member_fields(field_value):
    result = {}
    for member in field_value:
        for name, value in member.items():
            value = value_as_list(name, value)
            if value:
                result.setdefault(name, []).extend(value)
    return result


def value_as_list(name, value):
    if name in ('sector', 'town', 'street', 'region', 'good', 'branch', 'person_name', 'top_administrative_unit'):
        return value
    if name in ('email', 'phone', 'url'):
        return [unicode(obj) for obj in value]


def obj_as_dict(obj):
    result = {}
    for field in obj.get_all_fields():
        field_name = field if isinstance(field, basestring) else field.name
        obj_field = getattr(obj, field_name)
        field_value = obj.get_field_value(field_name, obj_field)
        result[field_name] = field_value

    return result