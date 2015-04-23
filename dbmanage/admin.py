"""
Created on Dec 23, 2013

@author: drifter
"""
from django.contrib import admin
from dbmanage.models import *

class RegisteredInline(admin.StackedInline):
    model = Registration
    extra = 0
    readonly_fields = ['date']

class DatabaseAdmin(admin.ModelAdmin):
    list_filter = ('status', 'is_perpetual', 'max_registrations', )
    search_fields = ['^database_id']
    inlines = [RegisteredInline]


admin.site.register(Database, DatabaseAdmin)
admin.site.register(Updating)
admin.site.register(Registration)