#-*- coding: utf-8 -*-
from django.test import TestCase
from DB.models import BranchTitle, Language, Branch, Enterprise
from SearchEngine.views import get_enterprise_fields, get_words


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
        
    
    def test_enterprise_save(self):
        enterprise = Enterprise.objects.get(pk=1)
        fields = get_enterprise_fields(enterprise)
        words = get_words(fields)
        enterprise.save()
        ewcount = enterprise.enterprisewords_set.count()
        self.assertEqual(len(words), ewcount)
    



            