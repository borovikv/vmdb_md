from django.shortcuts import render
from django.http.response import HttpResponseBadRequest
from DBAuthentication.models import Databases, RegisteredDatabases

MAX_REGISTRATION = 3


def registry_online(request):
    if request.GET:
        registration_code = request.GET.get('code')
        
        context = registry(registration_code)
        return render(request, 'registry/online.html', context)
    
    return HttpResponseBadRequest()


def registry_phone(request):
    pass


def registry(registration_code):
    database_id, user_id = parse_code(registration_code)
    print database_id, user_id
    print Databases.objects.filter(database_id=database_id)   
    if Databases.objects.filter(database_id=database_id).exists():
        db = Databases.objects.get(database_id=database_id)
        
        if not registry_db(db, user_id):
            return {'status':'ERROR', 'value':'spent'}
        
        value = encrypt_password(db.database_password, database_id, user_id)
        return {'status':'SUCCES', 'value':value}
    
    return {'status':'ERROR', 'value':'wrong'}
    

def parse_code(registration_code):
    id_db_length = 16
    
    database_id = registration_code[0:id_db_length]
    user_id = registration_code[id_db_length:]
    
    return int(database_id, 16), int(user_id, 16)


def registry_db(database, user_id):
    rdobjects = RegisteredDatabases.objects
    user_registered = rdobjects.filter(user_id=user_id, database=database).exists()
    
    if user_registered: return True
     
    if rdobjects.filter(database=database).count() >= MAX_REGISTRATION:
        return False
    
    else:
        rd = RegisteredDatabases()
        rd.database = database
        rd.user_id = user_id
        rd.save()
        return True

def get_registration_code(database_id, user_id):
    return "%s%s"%(database_id, user_id)

def encrypt_password(password, database_id, user_id):
    return password

def decrypt_password(epassword, database_id, user_id):
    return epassword