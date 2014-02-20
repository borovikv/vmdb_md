#-*- coding: utf-8 -*-
"""
sengine
"""
from django.contrib.auth.models import User
from django.test import TestCase, utils

from django.core.urlresolvers import reverse
from django.test.client import Client
from dbe.views import create_test_varo
from sengine.views import split_text, is_word_suit, to_common_form, search_enterprises, search_all, search_max, get_or_create_words
from sengine.models import Words
from dbe.models import Enterprise, Language
from utils.utils import flatten

utils.setup_test_environment()


class SearchTest(TestCase):
    def setUp(self):
        create_test_varo()
        self.get_varoinform().save()
        self.client = Client()
        self.username = 'agconti'
        self.email = 'test@test.com'
        self.password = 'test'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def test_suit(self):
        words = [',', '', '.', 'abc', u'и', 'and']
        is_suit = [is_word_suit(w) for w in words]
        self.assertEqual(is_suit, [False, False, False, True, False, False])

    def test_to_common_form(self):
        words = ['a-b', '123456', '12-34-56', 'ab']
        result = [to_common_form(w) for w in words]
        self.assertEqual(result, [['a', 'b'], ['123456'], ['123456'], ['ab']])

    def test_flatten(self):
        self.assertEqual(flatten([[1], [2, 3]]), [1, 2, 3])

    def test_split_words(self):
        text_line = u'Varo-Inform SRL S.R.L., Varo Inform +373-22-444-555 и and si 022-555-999 abc cdesai 903 varo-inform@varo-inform.com'
        words = split_text(text_line)
        test_words = ['varo', 'inform', '22444555', '22555999', '903', 'abc', 'cdesai', 'varo-inform@varo-inform.com']
        words.sort()
        test_words.sort()
        self.assertEqual(words, test_words)

    def test_search_url(self):
        self.assertEqual(reverse('search'), '/search/')

    def test_redirect(self):
        text_line = {'line': u'Varo-Inform SRL реклама и дизайн'}
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        self.assertTrue(self.client.login(username=self.username, password=self.password))

    def test_search(self):
        text_line = {'line': u'Varo-Inform '}
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context)
        self.assertIn('enterprises', response.context)
        self.assertIsNotNone(response.context['enterprises'])
        self.assertEqual(response.templates[0].name, 'search/main.html')

    def test_empty_search(self):
        text_line = {'line': u''}
        self.assertTrue(self.client.login(username=self.username, password=self.password))
        response = self.client.post(reverse('search'), text_line)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['enterprises'], None)

    def test_search_enterprises(self):
        text_line = u'Varo-Inform SRL реклама и дизайн'
        result = self.search_varo(text_line)
        self.assertIn(self.get_varoinform(), result)

    def test_fail_search(self):
        text_line = u'aabkajsd asdjisdk asdjfimsfo998'
        result = self.search_varo(text_line)
        self.assertTrue(not result)

    def test_fail_and_search(self):
        word = Words(word='xxxyyy')
        word.save()
        text_line = u'Varo-Inform SRL реклама и дизайн xxxyyy'
        result = self.search_varo(text_line)
        self.assertTrue(not result)

    def test_search_single_word(self):
        text_line = u'Varo'
        result = self.search_varo(text_line)
        self.assertIn(self.get_varoinform(), result)

    def test_get_varoinform(self):
        varo = self.get_varoinform()
        self.assertEqual(varo.title(Language.RU).lower(), 'varo-inform')

    def test_max_search(self):
        word = Words(word='xxxyyy')
        word.save()
        text_line = u'Varo-Inform SRL реклама и дизайн xxxyyy'
        result = self.search_varo(text_line, search_max)
        self.assertTrue(result)

    def test_fail_max_search(self):
        get_or_create_words('xxxyyy', 'wwwxxx', 'wsjsdie')
        text_line = 'xxxyyy wwwxxx wsjsdie'
        result = self.search_varo(text_line, search_max)
        self.assertTrue(not result)

    #---------------------------------------------------------------------------
    def search_varo(self, text_line, func=search_all):
        varo = self.get_varoinform()
        varo.save()
        return search_enterprises(text_line, func)

    def get_varoinform(self):
        return Enterprise.objects.get(pk=1)
