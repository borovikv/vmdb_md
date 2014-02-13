from DBAuthentication.models import Databases
from DBAuthentication.cypher import encode, decode, create_key
from DBAuthentication.views import registry, decrypt_password,\
    get_registration_code
from django.test import TestCase, utils
from django.test.client import Client
import binascii

utils.setup_test_environment()

class Test(TestCase):
    def setUp(self):
        self.database_id = "1111111111111111"
        print int(self.database_id, 16)
        self.user_id = "000C299B664E"
        db = Databases()
        db.database_id = int(self.database_id, 16)
        db.database_password = "secret"
        db.save()
        
    def test_create_key(self):
        database_id = "1111111111111111"
        user_id = "000C299B664E"
        key = create_key(database_id, user_id)
        
        java_data = "AB89EB4D35BFE274DE77B8318E426089".decode('hex')
        
        self.assertEquals(key, bytearray(java_data))    
    
    
    def test_encode(self):
        word = "the word"
        key = create_key(self.database_id, self.user_id)
        encode_word = encode(word, key)
        self.assertEqual(word, decode(encode_word, key)) 
        
    
    def test_registration(self):
        epassword = registry(self.get_registry_data())["value"]
        self.assertTrue(epassword)
        
        db = Databases.objects.get(database_id = self.database_id)
        password = db.database_password
        print password
        self.assertEquals(password, decrypt_password(epassword.decode("hex"), self.database_id, self.user_id))

    
    def get_registry_data(self):
        return get_registration_code(self.database_id, self.user_id)

    
    def test_registry_succes(self):
        c = Client()
        response = c.get("/registry/online/", {"code": self.get_registry_data()})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context)
        
        status = response.context.get('status')
        self.assertEqual(status, 'SUCCES')
        
        value = response.context['value']
        self.assertTrue(value)
        
    
    def test_regisrty_error_not_exist(self):
        c = Client()
        response = c.get("/registry/online/", {"code": get_registration_code("2"*16, self.user_id)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context)
        
        status = response.context['status']
        self.assertEqual(status, 'ERROR')
        
        value = response.context['value']
        self.assertEquals(value, 'wrong')

    
    def test_regisrty_error_end(self):
        c = Client()
        c.get("/registry/online/", {"code": get_registration_code('1111111111111111', '000C299B664E')})
        c.get("/registry/online/", {"code": get_registration_code('1111111111111111', '100C299B664E')})
        c.get("/registry/online/", {"code": get_registration_code('1111111111111111', '200C299B664E')})
        response = c.get("/registry/online/", {"code": get_registration_code('1111111111111111', '300C299B664E')})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context)
        
        status = response.context.get('status')
        self.assertEqual(status, 'ERROR')
        
        value = response.context.get('value')
        self.assertEquals(value, 'spent')
        
    def test_bad_request(self):
        c = Client()
        response = c.get("/registry/online/")
        print response.status_code
        self.assertEqual(response.status_code, 400)
        
    def test_password(self):
        password = "secret"
        key = create_key(self.database_id, self.user_id)
        print "encrypt"
        encode_word = encode(password, key)
    
        print "decrypt", binascii.hexlify(encode_word)
        result = decode(encode_word, key)
        self.assertEquals(password, result)
        
        
        
            
        
    
        