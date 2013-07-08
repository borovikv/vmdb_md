#-*- coding: utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from DB.models import BranchTitle, Language, Branch


class LanguageTitleTest(TestCase):
    def setUp(self):
        self.bcont = Branch()
        self.bcont.save()
        self.ru = Language(title=Language.RU)
        self.ro = Language(title=Language.RO)
        self.en = Language(title=Language.EN)
        self.ru.save()
        self.ro.save()
        self.en.save()
    
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
        btro = self.get_bt(self.ro, u'romanian')
        self.assertEqual(btru.__unicode__(), self.bcont.__unicode__())
    
    def test_language_ro_container(self):
        btro = self.get_bt(self.ro, u'romanian')
        self.assertEqual(btro.__unicode__(), self.bcont.__unicode__())
    
    
