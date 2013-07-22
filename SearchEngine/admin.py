'''
Created on Jul 22, 2013

@author: drifter
'''
from django.contrib import admin
from SearchEngine.models import Words, EnterpriseWords

admin.site.register(Words)
admin.site.register(EnterpriseWords)