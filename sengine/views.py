#-*- coding: utf-8 -*-
import re

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from sengine.forms import SearchForm
from sengine.models import Words
import dbe
from utils.utils import Profiler, flatten, is_url, is_email, get_obj_or_none


ignore_words = {'the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', u'и', u'или', u'si'}
entity_type = {'SRL', 'S.R.L'}
short_numbers = {'901', '902', '903', '904'}


def split_text(text):
    text = re.sub('|'.join(entity_type), '', text, flags=re.U)
    splitter = re.compile('[,\s]*', flags=re.U)
    words = flatten([to_common_form(word) for word in splitter.split(text) if is_word_suit(word)])
    return list(set(words))


def to_common_form(word):
    word = word.lower()

    if is_phone(word):
        return [convert_phone(word)]

    elif is_email(word):
        return [word]

    elif is_url(word):
        return [word]

    return re.split('-', word, flags=re.U)


def is_word_suit(word):
    return bool(word and not word in ignore_words and not re.match('^\W$', word, re.U))


def is_phone(word):
    tel_pattern = re.compile(r'^(\+\d{1,3}\s*|0){0,1}[\d-]{3,16}', re.U)
    return bool(tel_pattern.match(word))


def convert_phone(word):
    rep_pattern = '^\+373[\s-]*0{0,1}|^0|-'
    return re.sub(rep_pattern, '', word, flags=re.U)

#-------------------------------------------------------------------------------
@login_required
def search(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        line = form.cleaned_data['line']
        with Profiler() as p:
            enterprises = search_enterprises(line, search_all)
        elapsed = p.elapsed

    return render(request, 'search/main.html', locals())


def search_all(words):
    result = dbe.models.Enterprise.objects.filter(words=words[0])
    for word in words[1:]:
        result = result.filter(words=word)

    return result[:]


def search_at_least_one(words):
    result = dbe.models.Enterprise.objects.filter(words__in=words).distinct()
    return result[:]


def search_max(words):
    result = dbe.models.Enterprise.objects
    fails = []
    for word in words:
        temp = result.filter(words=word)
        if temp:
            result = temp
        else:
            fails.append(word)
    if len(words) == len(fails):
        return []
    return result[:]


def search_enterprises(line, func):
    words = get_words_from_line(line)
    if not words:
        return
    return func(words)


def get_words_from_line(line):
    return filter(None, [get_obj_or_none(Words, word=word) for word in split_text(line)])


def get_or_create_words(*words):
    get_or_create = lambda word: Words.objects.get_or_create(word=word)
    return [get_or_create(word) for word in words]



