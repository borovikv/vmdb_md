#-*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from DB.models import BranchTitle, Language, Branch, Enterprise
from pprint import pprint
#from DB.dbparse import get_fields, get_scheme, create_objects


class Test(TestCase):
    def setUp(self):
        self.bcont = Branch()
        self.bcont.save()
        self.ru = Language.objects.get(title=Language.RU)
        self.ro = Language.objects.get(title=Language.RO)
        self.en = Language.objects.get(title=Language.EN)
    
    def test_language_empty_container(self):
        bcont = Branch()
        self.assertEqual(bcont.pk, bcont.__unicode__())
    
    def get_bt(self, lang, text):
        bt = BranchTitle()
        bt.language = lang
        bt.title = text
        bt.branch = self.bcont
        bt.save()
        return bt
            
    def test_language_ru_container(self):
        btru = self.get_bt(self.ru, u'русский')
        self.get_bt(self.ro, u'romanian')
        self.assertEqual(btru.__unicode__(), self.bcont.__unicode__())
    
    def test_language_ro_container(self):
        btro = self.get_bt(self.ro, u'romanian')
        self.assertEqual(btro.__unicode__(), self.bcont.__unicode__())
        
    def test_get_enterpise_fields(self):
        fields = ['BranchTitle', 'GoodTitle', 'Brand', 'EnterpriseName', 
                  'StreetTitle', 'SectorTitle', 'TownTitle', 'RegionTitle', 
                  'AdministrativeUnitTitle', 'Phone', 'Email', 'Url', 'PersonName']
        fields.sort()
        
        varo = Enterprise.objects.get(pk=1)
        varo_fields = varo.get_enterprise_fields()
        pprint(varo_fields)
        e_fields = varo_fields.keys()
        e_fields.sort()
        self.assertEqual(e_fields, fields)
    
# class DbParserTest(TestCase):
#     def test_get_model_fields(self):
#         obj = None
#         fields = get_fields(obj)
#         def_fiels = {}
#         self.assertEqual(fields, def_fiels)
#         
#     def test_parse_xml(self):
#         xml_scheme = 'path_to_xml'
#         scheme = get_scheme(xml_scheme)
#         def_scheme = {}
#         self.assertEqual(scheme, def_scheme)    
#     
#     def test_create_scheme_obj(self):
#         scheme_model_map = {'path1': ('Model1', 'Model2'), 'path2':('Model3')}
#         objs = create_objects(scheme_model_map)
#         def_objs = {}
#         field_objs = get_fields(**objs)
#         field_def = get_fields(**def_objs)
#         self.assertEqual(field_def, field_objs)



            