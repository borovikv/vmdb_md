#-*- coding: utf-8 -*-
from django.test import TestCase

from dbe.models import BranchTitle, Language, Branch, Enterprise
from utils.mpprint import mpprint
from dbe.views import create_test_varo


class Test(TestCase):
    def setUp(self):
        self.bcont = Branch()
        self.bcont.save()
        self.ru = Language.objects.get_or_create(title=Language.RU)[0]
        self.ro = Language.objects.get_or_create(title=Language.RO)[0]
        self.en = Language.objects.get_or_create(title=Language.EN)[0]
        create_test_varo()

    def test_language_empty_container(self):
        bcont = Branch()
        bcont.save()
        self.assertEqual(bcont.pk, bcont.__unicode__())

    def get_bt(self, lang, text):
        bt = BranchTitle()
        bt.language = lang
        bt.title = text
        bt.container = self.bcont
        bt.save()
        return bt

    def test_language_ru_container(self):
        btru = self.get_bt(self.ru, u'русский')
        self.get_bt(self.ro, u'romanian')
        print btru, self.bcont
        self.assertEqual(btru.__unicode__(), self.bcont.__unicode__())

    def test_language_ro_container(self):
        btro = self.get_bt(self.ro, u'romanian')
        self.assertEqual(btro.__unicode__(), self.bcont.__unicode__())

    def test_get_energise_fields(self):
        fields = ['sector', 'town', 'good', 'person_name', 'url', 'brand',
                  'street', 'email', 'phone', 'titles', 'branch', 'top_administrative_unit', 'region']
        fields.sort()

        varo = Enterprise.objects.get(pk=1)
        varo_fields = varo.get_fields()
        mpprint(varo_fields)
        e_fields = varo_fields.keys()
        e_fields.sort()
        self.assertEqual(e_fields, fields)