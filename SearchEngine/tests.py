#-*- coding: utf-8 -*-
from django.test import TestCase
from django.core.urlresolvers import reverse
from SearchEngine.views import split_text


class SearchTest(TestCase):
    def test_split_words(self):
        text_line = u'Varo-Inform SRL S.R.L., Varo Inform +373-22-444-555 и and si 022-555-999 abc cdesai 903'
        words = split_text(text_line)
        test_words = ['varo','inform', '22444555', '22555999', '903', 'abc', 'cdesai']
        self.assertEqual(words.sort(), test_words.sort())
    
    def test_search_url(self):
        self.assertEqual(reverse('search'), '/search/')
        self.assertEqual(reverse('search-result'), '/search/result/')
    
    def test_search(self):
        text_line = {'line': u'Varo-Inform SRL реклама и дизайн'}
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 301)
        self.client.login(username='vladimir', password='1')
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 200)
        self.assertIn('enterprise', response.context)
        self.assertEqual(response.context['enterprise']['title'], u'Varo-Inform')
        self.assertEqual(response.templates[0].name, 'enterprise_list.html')
    