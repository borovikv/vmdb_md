from django.shortcuts import render
from django.http.response import HttpResponseBadRequest
from dbregister.models import Databases, RegisteredDatabases
from dbregister import cypher
from feedparser import binascii

MAX_REGISTRATION = 3


def registry_online(request):
    if request.GET:
        registration_code = request.GET.get('code')

        context = registry(registration_code)
        return render(request, 'db_registry/online.html', context)

    return HttpResponseBadRequest()


def registry_phone(request):
    pass


def registry(registration_code):
    database_id, user_id = parse_code(registration_code)
    db_id = int(database_id, 16)
    us_id = int(user_id, 16)
    if Databases.objects.filter(database_id=db_id).exists():
        db = Databases.objects.filter(database_id=db_id)[0]

        if not registry_db(db, us_id):
            return {'status': 'ERROR', 'value': 'spent'}

        value = encrypt_password(db.database_password, database_id, user_id)
        return {'status': 'SUCCES', 'value': binascii.hexlify(value)}

    return {'status': 'ERROR', 'value': 'wrong'}


def parse_code(registration_code):
    id_db_length = 16

    database_id = registration_code[0:id_db_length]
    user_id = registration_code[id_db_length:]

    return database_id, user_id


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
    return "%s%s" % (database_id, user_id)


def encrypt_password(password, database_id, user_id):
    return cypher.encode(password, cypher.create_key(database_id, user_id))


def decrypt_password(epassword, database_id, user_id):
    return cypher.decode(epassword, cypher.create_key(database_id, user_id))
