"""
Created on Dec 23, 2013

@author: drifter
"""
from django.contrib import admin
from dbregister.models import Databases, RegisteredDatabases

admin.site.register(Databases)
admin.site.register(RegisteredDatabases)