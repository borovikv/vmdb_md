"""
Created on Dec 23, 2013

@author: drifter
"""
from django.contrib import admin
from dbmanage.models import Databases, RegisteredDatabases, Updating

admin.site.register(Databases)
admin.site.register(RegisteredDatabases)
admin.site.register(Updating)