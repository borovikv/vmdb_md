from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import os
from django.shortcuts import render
from django.http.response import HttpResponseBadRequest
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from dbmanage.forms import UploadFileForm
from dbmanage.models import Databases, RegisteredDatabases, Updating
from dbmanage import cypher
from feedparser import binascii
from django.core.servers.basehttp import FileWrapper
from utils.utils import now

MAX_REGISTRATION = 3


def registry_online(request):
    if request.GET:
        registration_code = request.GET.get('code')

        context = registry(registration_code)
        return render(request, 'db_registry/online.html', context)

    return HttpResponseBadRequest()


# noinspection PyUnusedLocal
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
    rd_objs = RegisteredDatabases.objects
    user_registered = rd_objs.filter(user_id=user_id, database=database).exists()

    if user_registered:
        return True

    if rd_objs.filter(database=database).count() >= MAX_REGISTRATION:
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


########################################################################################################################


def update(request):
    user_id = request.GET.get('user')
    if not user_id:
        return HttpResponseBadRequest("haven't user id")

    try:
        db = RegisteredDatabases.objects.get(user_id=user_id).database
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("user not exist")

    if db.last_update and not Updating.objects.filter(last_update__gte=db.last_update).exists():
        return HttpResponse("already updated %s vs %s -" % (db.last_update, Updating.objects.all()[0]))

    return file_response("./export/DB.h2.db")


def file_response(f, content_type='application/zip'):
    response = HttpResponse(FileWrapper(open(f)), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(f)
    return response


#ToDo: create resposes code
#ToDo: test
@method_decorator(csrf_exempt)
def upload(request):
    if request.method == 'POST':
        print request.POST
        print request.FILES
        form = UploadFileForm(request.POST, request.FILES)
        print form
        if form.is_valid():
            handle_uploaded_file(form.cleaned_data.get('title'), request.FILES['db'])
            upd = Updating()
            upd.last_update = now()
            upd.save()
            response = "file uploaded successfully"
        else:
            response = "form invalid"
    else:
        response = "request is not post"
    return HttpResponse(response)


def handle_uploaded_file(name, f):
    with open('./export/%s' % name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
