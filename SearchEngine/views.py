#-*- coding: utf-8 -*-
import re
import time
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Q

from SearchEngine.forms import SearchForm
from SearchEngine.models import Words
import DB

class Profiler(object):
    def __enter__(self):
        self._startTime = time.time()
        return self
    
    def __exit__(self, *args):
        self.elapsed = time.time()-self._startTime

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', u'и', u'или', 
                   u'si',])
entyty_type = set(['SRL','S.R.L'])
short_numbers = set(['901', '902', '903', '904'])

def split_text(text):
    text = re.sub('|'.join(entyty_type), '', text, flags=re.U)
    spliter = re.compile('[,\s]*', flags=re.U)
    words = flatten([to_common_form(word) for word in spliter.split(text) if is_word_suit(word)])
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
    return bool(word and not word in ignorewords and not re.match('^\W$', word, re.U))


def is_url(word):
    url_pattern = re.compile(r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'#domain... 
        r'localhost|'#localhost... 
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'# ...or ip 
        r'(?::\d+)?'# optional port
        r'(?:/?|[/?]\S+)$', 
        re.IGNORECASE)
    return bool(url_pattern.match(word))

def is_email(word):
    email_pattern = re.compile(r'^[a-z0-9_.-]+@[a-z0-9_-]+\.[a-z]{3}$', re.U)
    return bool(email_pattern.match(word))

def is_phone(word):
    tel_pattern = re.compile(r'^(\+\d{1,3}\s*|0){0,1}[\d-]{3,16}', re.U)
    return bool(tel_pattern.match(word))

def convert_phone(word):
    rep_pattern = '^\+373[\s-]*0{0,1}|^0|-'
    return re.sub(rep_pattern, '', word, flags=re.U)

def flatten(listOfLists):
    "Flatten one level of nesting"
    #return chain.from_iterable(listOfLists)
    return [item for sublist in listOfLists for item in sublist]

#-------------------------------------------------------------------------------
@login_required
def search(request):
    form = SearchForm(request.POST or None)
    if form.is_valid():
        line = form.cleaned_data['line']
        with Profiler() as p:
            enterprises = searchEnterprises(line, search_and)
        elapsed = p.elapsed
    
    return render(request, 'search/main.html', locals())


def search_and(words):
    result = DB.models.Enterprise.objects.filter(words=words[0])
    for word in words[1:]:
        result = result.filter(words=word)
    
    return result[:]


def search_or(words):
    result = DB.models.Enterprise.objects.filter(words__in=words).distinct()
    return result[:]

def searchEnterprises(line, func):
    words = filter(None, [ get_obj_or_None(Words, word=word) for word in split_text(line) ])
    if not words:
        return
    return func(words)
        
def get_obj_or_None(model, *args, **kwargs):
    obj = model.objects.filter(**kwargs)
    if obj:
        return obj[0]
    return None
#-------------------------------------------------------------------------------


