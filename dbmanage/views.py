import os

from django.db.utils import IntegrityError
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden, \
    HttpResponseNotFound
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from dbmanage.forms import UploadFileForm, RegistrationDbForm, GeneratorForm
from dbmanage.models import Database, Updating
from utils.utils import now


def registry_online(request):
    if request.GET:
        uid = request.GET.get('id')
        print uid
        try:
            password = registry(uid)
            context = {'status': 'OK', 'value': password}

        except ObjectDoesNotExist as e:
            context = {'status': 'NO', 'value': 'wrong id'}

        except Exception as e:
            context = {'status': 'NO', 'value': e}

        return render(request, 'db_registry/online.html', context)

    return HttpResponseBadRequest()


@login_required
def registry_phone(request):
    form = RegistrationDbForm(request.POST)
    context = {}
    if form.is_valid():
        try:
            password = registry(form.cleaned_data['uid'])
            return render(request, 'db_registry/phone.html', {'password': password})

        except ObjectDoesNotExist as e:
            context['message'] = 'Wrong database uid - %s' % form.cleaned_data['uid']

        except Exception as e:
            context['message'] = e

    context['form'] = form
    return render(request, 'db_registry/phone_form.html', context)


def registry(uid):
    if not uid:
        raise Exception("Empty uid")
    db = Database.objects.get(database_id=uid)

    if not db.has_available_registrations():
        raise Exception("Registration exceeding")

    else:
        db.registrations.create()

    return db.database_password


################################################################################

def update(request):
    try:
        db = get_database(request)
    except ValueError as ve:
        return HttpResponseBadRequest(ve)
    except Exception as e:
        print e
        return HttpResponseForbidden(e)

    exist_new_update = lambda date: Updating.objects.filter(last_update__gte=date).exists()
    if db.last_update and not exist_new_update(db.last_update):
        response = HttpResponseNotFound("already updated %s vs %s -" % (db.last_update, Updating.objects.all()[0]))
        return response

    return file_response("./export/DB.h2.db.zip")


def get_database(request):
    uid = request.GET.get('user')
    if not uid:
        raise ValueError("value=null_uid")

    try:
        db = Database.objects.get(database_id=uid)
        if db.status == Database.REGISTERED:
            return db
        else:
            raise Exception("value=unregistered_db")
    except ObjectDoesNotExist:
        raise Exception("value=invalid_uid")


def file_response(f, content_type='application/zip'):
    response = HttpResponse(FileWrapper(open(f)), content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(f)
    return response


def check(request):
    try:
        db = get_database(request)
    except ValueError as ve:
        return HttpResponseBadRequest(ve)
    except Exception as e:
        return HttpResponseForbidden(e)

    last_update = db.last_update

    never_updated = not last_update and Updating.objects.count()
    has_new_updates = last_update and Updating.objects.filter(last_update__gt=last_update).exists()

    exists = never_updated or has_new_updates
    return HttpResponse('Value=%s' % ('Yes' if exists else 'No'))


def confirm(request):
    try:
        db = get_database(request)
    except ValueError as ve:
        return HttpResponseBadRequest(ve)
    except Exception as e:
        return HttpResponseForbidden(e)

    db.last_update = now()
    db.save()
    response = HttpResponse("value=OK")
    return response


# ToDo: create resposes code
# ToDo: test
@method_decorator(csrf_exempt)
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
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

@login_required
def generate(request):
    form = GeneratorForm(request.POST)
    if form.is_valid():
        text = form.cleaned_data['text']
        parts = [[s.strip() for s in line.split('=')] for line in text.split('\n')]
        for uid, db_password in parts:
            d = Database()
            d.database_id = uid
            d.database_password = db_password
            try:
                d.save()
            except IntegrityError:
                pass
        return redirect('/admin')

    return render(request, 'generate.html', {'form': form})


@login_required
def show(request):
    return render(request, 'show.html', {'ids': Database.objects.filter(registered=None)})