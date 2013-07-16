#-*- coding: utf-8 -*-
import re
from itertools import chain


ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', u'и', u'или', u'si'])
entyty_type = set(['SRL','S.R.L'])
short_numbers = set(['901', '902', '903', '904'])

def split_text(text):
    text = re.sub('|'.join(entyty_type), '', text, flags=re.U)
    spliter = re.compile('[,\s\.]*', flags=re.U)
    words = flatten([to_common_form(word) for word in spliter.split(text) if suit(word)])
    return list(set(words))

def suit(word):
    return word and not word in ignorewords

def to_common_form(word):
    tel_pattern = re.compile(r'^(\+\d{1,3}|0){0,1}[\d-]{3,16}', re.U)
    if tel_pattern.match(word):
        return re.sub('^\+373|^0|-', '', word, flags=re.U)
    return re.split('-', word.lower(), flags=re.U)

def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)


def search(request):
    pass

def result(request):
    pass