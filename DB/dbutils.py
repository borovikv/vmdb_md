'''
Created on Jul 22, 2013

@author: drifter
'''
from SearchEngine.views import split_text, flatten

def get_enterprise_fields(enterprise):
    result = {}
    for field, field_value in enterprise.as_list().items():
        
        if field in ('contact_set', 'contactperson_set', 'gproduce_set', ):
            for name, value in get_member_fields(field_value).items():
                result.setdefault(name, []).extend(value)
        
        elif field in  ('dealer',  'titles', 'brand'):
            result[field] = field_value
    return result

def get_member_fields(field_value):
    result = {}
    for member in field_value:
        for name, value in member.items():
            value = value_as_list(name, value)
            if value != None:
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