#-*- coding: utf-8 -*-
from django.test import TestCase, utils

from django.core.urlresolvers import reverse
from SearchEngine.views import split_text, suit, to_common_form, flatten,\
    searchEnterprises, get_enterpise_fields
from DB.models import Enterprise
from SearchEngine import models
utils.setup_test_environment()

class SearchTest(TestCase):
    def test_suit(self):
        words = [',', '', '.', 'abc', u'и', 'and']
        is_suit = [suit(w) for w in words]
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
        enterprises = searchEnterprises(text_line)
        varo = self.get_varoinform()
        self.assertEqual(unicode(varo), 'Varo-Inform')
        self.assertIn(varo, enterprises)
        
    def get_varoinform(self):
        return Enterprise.objects.get(pk=1)
        
    def _test_create_from_enterprise(self):
        varo = self.get_varoinform()
        ew = models.EnterpriseWords.create_from_enterprise(varo)
        test_ew = models.Words.objects.filter(enterprise=varo)
        self.assertEqual(list(ew), list(test_ew))
    
    def test_get_enterpise_fields(self):
        fields = ['BranchTitle', 'GoodTitle', 'Brand', 'EnterpriseName', 
                  'StreetTitle', 'SectorTitle', 'TownTitle', 'RegionTitle', 
                  'AdministrativeUnitTitle', 'Phone', 'Email', 'Url', 'PersonName']
        fields.sort()
        
        varo = self.get_varoinform()
        e_fields = get_enterpise_fields(varo).keys()
        e_fields.sort()
        self.assertEqual(e_fields, fields)
        