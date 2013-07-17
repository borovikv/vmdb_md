#-*- coding: utf-8 -*-
import re
from SearchEngine.forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it', u'и', u'или', 
                   u'si',])
entyty_type = set(['SRL','S.R.L'])
short_numbers = set(['901', '902', '903', '904'])

def split_text(text):
    text = re.sub('|'.join(entyty_type), '', text, flags=re.U)
    spliter = re.compile('[,\s]*', flags=re.U)
    words = flatten([to_common_form(word) for word in spliter.split(text) if suit(word)])
    print words
    return list(set(words))

def suit(word):
    return bool(word and not word in ignorewords and not re.match('^\W$', word, re.U))

def to_common_form(word):
    word = word.lower()
    
    tel_pattern = re.compile(r'^(\+\d{1,3}|0){0,1}[\d-]{3,16}', re.U)
    if tel_pattern.match(word):
        return [re.sub('^\+373|^0|-', '', word, flags=re.U)]
    
    email_patternt = re.compile(r'^[a-z0-9_.-]+@[a-z0-9_-]+\.[a-z]{3}$', re.U)
    if email_patternt.match(word):
        return [word]
    
    return re.split('-', word, flags=re.U)

def flatten(listOfLists):
    "Flatten one level of nesting"
    #return chain.from_iterable(listOfLists)
    return [item for sublist in listOfLists for item in sublist]



def searchEnterprises(line):
    if not line:
        return
    return ['abc', 'cbc']

@login_required
def search(request):
    form = SearchForm(request.POST or None)
    enterprises = None
    if form.is_valid():
        line = form.cleaned_data['line']
        enterprises = searchEnterprises(line)
    
    return render(request, 'search/main.html', {'form': form, 'enterprises': enterprises})

def get_enterpise_fields(enterprise):
    fields = ['BranchTitle', 'GoodTitle', 'Brand', 'EnterpriseName', 
              'StreetTitle', 'SectorTitle', 'TownTitle', 'RegionTitle', 
              'AdministrativeUnitTitle', 'Phone', 'Email', 'Url', 'PersonName']
    'contact_set', 
    'contactperson_set', 
    'dealer', 
    'gproduce_set', 
    'titles'
    return {}