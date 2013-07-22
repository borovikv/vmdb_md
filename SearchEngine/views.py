#-*- coding: utf-8 -*-
import re
from SearchEngine.forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import time
from SearchEngine.models import Words, EnterpriseWords

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

def is_word_suit(word):
    return bool(word and not word in ignorewords and not re.match('^\W$', word, re.U))

def to_common_form(word):
    word = word.lower()
    
    tel_pattern = re.compile(r'^(\+\d{1,3}\s*|0){0,1}[\d-]{3,16}', re.U)
    if tel_pattern.match(word):
        rep_pattern = '^\+373[\s-]*0{0,1}|^0|-'
        return [re.sub(rep_pattern, '', word, flags=re.U)]
    
    email_pattern = re.compile(r'^[a-z0-9_.-]+@[a-z0-9_-]+\.[a-z]{3}$', re.U)
    if email_pattern.match(word):
        return [word]
    
    url_pattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if url_pattern.match(word):
        return [word]
    return re.split('-', word, flags=re.U)

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
            enterprises = searchEnterprises(line)
        elapsed = p.elapsed
        print elapsed
    
    return render(request, 'search/main.html', locals())

def searchEnterprises(line):
    if not line:
        return
    words = split_text(line)
    result = set()
    for word in words:
        word = Words.objects.filter(word=word)
        if word:
            epks = EnterpriseWords.objects.filter(word=word[0]).values_list('enterprise', flat=True)
            result.update(epks)
    es = list()
    for epk in result:
        es.append(epk)
    return es

#-------------------------------------------------------------------------------
def update_enterprisewords(enterprise):
    enterprise.enterprisewords_set.all().delete()
    fields = get_enterprise_fields(enterprise)
    for word in get_words(fields):
        word = Words.objects.get_or_create(word=word)[0]
        ew = EnterpriseWords(word=word, enterprise=enterprise)
        ew.save()

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
