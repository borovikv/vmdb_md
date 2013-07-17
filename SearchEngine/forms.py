#-*- coding: utf-8 -*-
from django import forms

class SearchForm(forms.Form):
    line = forms.CharField(widget=forms.TextInput(attrs={'class':'search'}), required=False)
    