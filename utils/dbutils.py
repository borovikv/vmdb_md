"""
Created on Jul 22, 2013

@author: drifter
"""
from sengine.views import split_text
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
    
    
def get_words(enterprise):
    words = flatten( split_text(word) for word in flatten(enterprise.values()))
    
    return list(set(words))