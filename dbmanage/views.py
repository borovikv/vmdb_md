import csv
from zipfile import ZipFile
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
import os
from django.shortcuts import render
from django.http.response import HttpResponseBadRequest
from django.utils.timezone import utc
import datetime
import shutil
from dbmanage.models import Databases, RegisteredDatabases, Updating
from dbmanage import cypher
from feedparser import binascii
from utils.dbutils import obj_as_dict
from django.db import models
from django.core.servers.basehttp import FileWrapper

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


def update(request):
    user_id = request.GET.get('user')
    if not user_id:
        return HttpResponseBadRequest("haven't user id")

    try:
        db = RegisteredDatabases.objects.get(user_id=user_id).database
    except ObjectDoesNotExist:
        return HttpResponseBadRequest("user not exist")

    if not Updating.objects.filter(last_update__gte=db.last_update).exists():
        return HttpResponse("already updated %s vs %s -" % (db.last_update, Updating.objects.all()[0]))

    upd_query = Updating.objects.order_by('-last_update')
    
    zip_with_highest_datetime = last_update_zip()
    zip_suit = lambda: zip_with_highest_datetime and creation_datetime(zip_with_highest_datetime).date() >= upd_query[0].last_update > db.last_update
    is_user_preview_updated = lambda: upd_query.count() >= 2 and db.last_update >= upd_query[1].last_update
    if upd_query.exists() and zip_suit() and is_user_preview_updated():
        return ZipResponse(zip_with_highest_datetime)

    zipfile = export(db.last_update)
    if not zipfile:
        return HttpResponse("zip is null %s" % now())

    db.last_update = now()
    db.save()
    return ZipResponse(zipfile)


def last_update_zip():
    dirname = "./export/"
    is_file = lambda f: os.path.isfile(os.path.join(dirname, f))
    fs = [f for f in os.listdir(dirname) if is_file(f)]
    if len(fs):
        fs.sort()
        return os.path.join("./export", fs[-1])


def creation_datetime(path):
    name = os.path.splitext(os.path.basename(path))[0]
    return datetime.datetime.strptime(name, get_time_format())


def ZipResponse(zipfile):
    response = HttpResponse(FileWrapper(open(zipfile)), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(zipfile)
    return response


def export(last_update):
    app = models.get_app('dbe')
    ms = models.get_models(app, include_auto_created=False)

    dirname = get_dirname()

    for m in ms:
        if last_update:
            model_to_csv(m, dirname, last_change__gte=last_update)
        else:
            model_to_csv(m, dirname)

    zip_file = zip_csv_model(dirname)

    shutil.rmtree(dirname)

    return zip_file


def now():
    return datetime.datetime.utcnow().replace(tzinfo=utc)


def get_time_format():
    return '%Y-%m-%d-%H-%M-%S'


def get_dirname():
    dirname = os.path.abspath("./export/%s" % now().strftime(get_time_format()))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    return dirname


def model_to_csv(model, dirname, **kwargs):
    if kwargs:
        objects = model.objects.filter(**kwargs)
    else:
        objects = model.objects.all()

    if not objects.count():
        return

    model_name = model.__name__
    file_name = os.path.join(dirname, model_name) + '.csv'

    with open(file_name, 'w+') as f:
        writer = csv.writer(f)
        for o in objects:
            row = obj_as_dict(o)

            writer.writerow([row[key] for key in row.keys()])


def zip_csv_model(path):
    zip_fn = path + ".zip"
    with ZipFile(zip_fn, 'w') as zip_file:
        is_file = lambda f: os.path.isfile(os.path.join(path, f))
        files = [f for f in os.listdir(path) if is_file(f)]
        if not files:
            os.remove(zip_file.filename)
            return
        for filename in files:
            zip_file.write(os.path.join(path, filename), filename)

    return zip_fn