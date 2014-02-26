"""
Created on Jul 22, 2013

@author: drifter
"""
from django.db.models import ManyToManyField
from django.db.models.related import RelatedObject


def obj_as_dict(obj):
    result = {}
    for field in get_all_fields(obj):
        field_name = field if isinstance(field, basestring) else field.name
        if hasattr(obj, 'exclude') and field_name in obj.exclude:
            continue
        obj_field = obj._meta.get_field_by_name(field_name)[0]
        if not isinstance(obj_field, RelatedObject):
            field_value = get_field_value(obj, obj_field)
            result[field_name] = field_value

    return result


def get_all_fields(obj):
        return obj.__class__._meta.get_all_field_names()


def get_field_value(obj, field):
    if isinstance(field, ManyToManyField):
        return [v.pk for v in field.value_from_object(obj).all()]
    else:
        value = field.value_from_object(obj)
        if isinstance(value, basestring):
            value = unicode(value).encode('utf-8')
        return value