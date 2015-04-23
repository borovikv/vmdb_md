from django.core.urlresolvers import reverse
from dbmanage.models import Database
from dbmanage.cypher import encode, decode, create_key
from dbmanage.views import registry
from django.test import TestCase, utils
from django.test.client import Client
import binascii

utils.setup_test_environment()


class Test(TestCase):
    def setUp(self):
        self.str_db_id = "1111111111111111"
        self.user_id = "000C299B664E"
        db = Database()
        db.database_id = self.str_db_id
        db.database_password = "secret"
        db.save()


    def test_registration(self):
        print(Database.objects.all())
        epassword = registry(self.str_db_id)
        self.assertTrue(epassword)
        print Database.objects.all()
        db = Database.objects.get(database_id=self.str_db_id)
        password = db.database_password
        print password

    def test_registry_success(self):
        print("-"*100)
        c = Client()
        response = c.get(reverse('db_registry-online'), {"id": self.str_db_id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context)

        status = response.context.get('status')
        self.assertEqual('OK', status)

        value = response.context['value']
        self.assertTrue(value)
        print(Database.objects.get(database_id=self.str_db_id).registrations.all())
        print("-"*100)

    def test_registry_error_not_exist(self):
        c = Client()
        response = c.get(reverse('db_registry-online'), {"id": '22222222222'})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context)

        status = response.context['status']
        self.assertEqual('NO', status)

        value = response.context['value']
        self.assertEquals('wrong id', value)

    def test_registrations_exceeding(self):
        c = Client()
        for _ in range(4):
            response = c.get(reverse('db_registry-online'), {"id": self.str_db_id})
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context)

        # noinspection PyUnboundLocalVariable
        status = response.context.get('status')
        self.assertEqual('NO', status)

        value = response.context['value']
        self.assertEqual('Registration exceeding', str(value))

    def test_bad_request(self):
        c = Client()
        response = c.get(reverse('db_registry-online'))
        print response.status_code
        self.assertEqual(response.status_code, 400)

    def test_password(self):
        password = "secret"
        key = create_key(self.str_db_id, self.user_id)
        print "encrypt"
        encode_word = encode(password, key)

        print "decrypt", binascii.hexlify(encode_word)
        result = decode(encode_word, key)
        self.assertEquals(password, result)