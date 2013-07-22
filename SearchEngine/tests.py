#-*- coding: utf-8 -*-
from django.test import TestCase, utils

from django.core.urlresolvers import reverse
from SearchEngine.views import split_text, is_word_suit, to_common_form, flatten,\
    searchEnterprises, get_enterprise_fields, get_words
from DB.models import Enterprise, Language
from SearchEngine import models
from utils.mpprint import mpprint
from SearchEngine.models import Words
utils.setup_test_environment()

class SearchTest(TestCase):
    def test_suit(self):
        words = [',', '', '.', 'abc', u'и', 'and']
        is_suit = [is_word_suit(w) for w in words]
        self.assertEqual(is_suit, [False, False, False, True, False, False])
    
    def test_to_common_form(self):
        words = ['a-b', '123456', '12-34-56', 'ab']
        result = [to_common_form(w) for w in words]
        self.assertEqual(result, [['a', 'b'], ['123456'], ['123456'], ['ab']])
    
    def test_flatten(self):
        self.assertEqual(flatten([[1], [2, 3]]), [1,2,3])
        
    def test_split_words(self):
        text_line = u'Varo-Inform SRL S.R.L., Varo Inform +373-22-444-555 и and si 022-555-999 abc cdesai 903 varo-inform@varo-inform.com'
        words = split_text(text_line)
        test_words = ['varo','inform', '22444555', '22555999', '903', 'abc', 'cdesai', 'varo-inform@varo-inform.com']
        words.sort()
        test_words.sort()
        self.assertEqual(words, test_words)
    
    def test_search_url(self):
        self.assertEqual(reverse('search'), '/search/')
    
    def test_login(self):
        text_line = {'line': u'Varo-Inform SRL реклама и дизайн'}
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 302)
        self.client.login(username='vladimir', password='1')
        response = self.client.post(reverse('search'), text_line)
        
    def test_search(self):
        text_line = {'line': u'Varo-Inform SRL реклама и дизайн'}
        self.client.login(username='vladimir', password='1')
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context != None)
        self.assertIn('enterprises', response.context)
        self.assertTrue(response.context['enterprises'] != None)
        self.assertEqual(response.templates[0].name, 'search/main.html')
    
    def test_empty_search(self):
        text_line = {'line': u''}
        self.client.login(username='vladimir', password='1')
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['enterprises'] == None)
        
    def test_search_enterprises(self):
        text_line = u'Varo-Inform SRL реклама и дизайн'
        varo = self.get_varoinform()
        self.assertEqual(varo.title(Language.RO).lower(), 'varo-inform')
        varo.save()
        print Words.objects.count()
        enterprises = searchEnterprises(text_line)
        self.assertIn(varo, enterprises)
        
    def get_varoinform(self):
        return Enterprise.objects.get(pk=1)
        
    def _test_create_from_enterprise(self):
        varo = self.get_varoinform()
        ew = models.EnterpriseWords.create_from_enterprise(varo)
        test_ew = models.Words.objects.filter(enterprise=varo)
        self.assertEqual(list(ew), list(test_ew))
    
    def test_get_enterpise_fields(self):
        fields = ['sector', 'town', 'good', 'person_name', 'url', 'brand', 
                  'street', 'email', 'phone', 'titles', 'branch', 'top_administrative_unit', 'region']
        fields.sort()
        
        varo = self.get_varoinform()
        varo_fields = get_enterprise_fields(varo)
        mpprint(varo_fields)
        e_fields = varo_fields.keys()
        e_fields.sort()
        self.assertEqual(e_fields, fields)
    
    def test_get_words(self):
        words = list(set([ word.lower() for word in ( 
            'media', 'mediaen', 'vara', 'inf@varo-inform.com', 'varo-inform@varo-inform.com',
            'reclame', 'advertisment', 'Disaine', 'Disine', 'Hasanov', 'Sergei',
            'Serg', 'Al', 'Rozenberg', 'Alex', '22111111', '22111222',
            '22222111', '22222222', '22333', '22333111','22333222', 'Chisinau',
            'Telecentrro', 'Telecentr', 'G.', 'Tudor', 'inform', 'varo', 'informen',
            'Chisinau', 'http://www.freetime.com/', 'http://www.yp.com/', 'http://varo-inform.com/'     
            )]))
        words.sort()
        
        enterprise =  {
             'branch': [ u'media', u'mediaen'],
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
             'region': [ u'Chisinau'],
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
    
        