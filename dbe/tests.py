#-*- coding: utf-8 -*-
from django.test import TestCase

from dbe.models import BranchTitle, Language, Branch, Enterprise
from utils.dbutils import get_words
from utils.mpprint import mpprint
from dbe.views import create_test_varo


class Test(TestCase):
    def setUp(self):
        self.bcont = Branch()
        self.bcont.save()
        self.ru = Language.objects.get_or_create(title=Language.RU)[0]
        self.ro = Language.objects.get_or_create(title=Language.RO)[0]
        self.en = Language.objects.get_or_create(title=Language.EN)[0]

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

    def skip_test_get_energise_fields(self):
        fields = ['sector', 'town', 'good', 'person_name', 'url', 'brand',
                  'street', 'email', 'phone', 'titles', 'branch', 'top_administrative_unit', 'region']
        fields.sort()

        varo = Enterprise.objects.get(pk=1)
        varo_fields = varo.get_fields()
        mpprint(varo_fields)
        e_fields = varo_fields.keys()
        e_fields.sort()
        self.assertEqual(e_fields, fields)

    def test_get_words(self):
        words = list(set([word.lower() for word in (
            'media', 'mediaen', 'vara', 'inf@varo-inform.com', 'varo-inform@varo-inform.com',
            'reclame', 'advertisment', 'Disaine', 'Disine', 'Hasanov', 'Sergei',
            'Serg', 'Al', 'Rozenberg', 'Alex', '22111111', '22111222',
            '22222111', '22222222', '22333', '22333111', '22333222', 'Chisinau',
            'Telecentrro', 'Telecentr', 'G.', 'Tudor', 'inform', 'varo', 'informen',
            'Chisinau', 'http://www.freetime.com/', 'http://www.yp.com/', 'http://varo-inform.com/'
        )]))
        words.sort()

        enterprise = {
            'branch': [u'media', u'mediaen'],
            'brand': [u'varo-inform', u'vara'],
            'email': [u'inf@varo-inform.com', u'varo-inform@varo-inform.com'],
            'good': [u'reclame',
                     u'advertisment',
                     u'Disaine',
                     u'Disine'],
            'person_name': [u'Hasanov Sergei',
                            u'Hasanov Serg',
                            u'Rozenberg Al',
                            u'Rozenberg Alex'],
            'phone': [u'+373-022-111-111',
                      u'+373-022-111-222',
                      u'+373-022-222-111',
                      u'+373-022-222-222',
                      u'+373-022-333',
                      u'+373-022-333-111',
                      u'+373-022-333-222'],
            'region': [u'Chisinau'],
            'sector': [u'Telecentrro',
                       u'Telecentr'],
            'street': [u'G. Tudor',
                       u'Tudor G.'],
            'titles': [u'varo-inform',
                       u'varo-informen'],
            'top_administrative_unit': [],
            'town': [u'Chisinau'],
            'url': [u'http://www.freetime.com/',
                    u'http://www.yp.com/',
                    u'http://varo-inform.com/']}
        result = get_words(enterprise)
        result.sort()
        self.assertEqual(words, result)

    def skip_test_enterprise_save(self):
        enterprise = Enterprise.objects.get(pk=1)
        fields = enterprise.get_fields()
        words = get_words(fields)
        enterprise.save()
        ewcount = enterprise.words.count()
        print ewcount, len(words)
        self.assertEqual(len(words), ewcount)

    def skip_test_create_test(self):
        create_test_varo()