"""
Created on Jul 22, 2013

@author: drifter
"""
from django.db.models import ManyToManyField
from django.db.models.related import RelatedObject


# noinspection PyProtectedMember
def obj_as_dict(obj):
    result = {}
    for field_name in get_all_field_names(obj.__class__):
        if hasattr(obj, 'exclude') and field_name in obj.exclude:
            continue
        obj_field = obj._meta.get_field_by_name(field_name)[0]
        if not isinstance(obj_field, RelatedObject):
            field_value = get_field_value(obj, obj_field)
            result[field_name] = field_value

    return result


# noinspection PyProtectedMember
def get_all_fields(model):
    return model._meta.get_all_field_names()


def get_all_field_names(model):
    return [fn if isinstance(fn, basestring) else fn.name for fn in get_all_fields(model)]


def get_field_value(obj, field):
    if isinstance(field, ManyToManyField):
        return [v.pk for v in field.value_from_object(obj).all()]
    else:
        value = field.value_from_object(obj)
        if isinstance(value, basestring):
            value = unicode(value).encode('utf-8')
        return value