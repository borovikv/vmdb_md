#-*- coding: utf-8 -*-
from django.http.response import HttpResponse
from dbe.models import Enterprise, Language, BusinessEntityType, \
    BusinessEntityTitle, Brand, EnterpriseTitle, Phone, Region, RegionTitle, \
    Street, StreetTitle, Town, TownTitle, Url, Contact, Person, PersonTitle, \
    ContactPerson, Position, PositionTitle, Good, GoodTitle, Gproduce
import datetime
from utils.utils import Profiler, now


def create_varo(request):
    amount = int(request.GET.get('amount', 0))

    with Profiler() as p:
        for _ in xrange(amount):
            create_test_varo()

    return HttpResponse('created %s enterprises at - %s sec' % (amount, p.elapsed))


def create_test_varo():
    ru, ro, en = get_languages()
    varo = Enterprise()
    varo.check_date = datetime.date.today()
    varo.yp_url = 'www.yp.md/varo'

    entity = BusinessEntityType()
    entity.save()
    create_title(BusinessEntityTitle, 'ООО', ru, entity)
    create_title(BusinessEntityTitle, 'srl', ro, entity)
    create_title(BusinessEntityTitle, 'llc', en, entity)
    varo.business_entity = entity

    br = Brand(title='varoinform')
    br.save()
    varo.save()
    varo.brands.add(br)
    varo.save()

    create_title(EnterpriseTitle, 'varo-inform', ru, varo)
    create_contact(varo)
    create_contact_person(varo, ('hasanov serg', u'хасанов сергей'), ['111111', '111222'])
    create_contact_person(varo, ('rosenberg alex', u'розенберг алекс'), ['222111', '222222'])
    create_gproduce(varo, [u'reclame', u'advertisment'])
    create_gproduce(varo, [u'Disaine', u'Disine'])


def get_languages():
    ru = Language.objects.get_or_create(title=Language.RU)[0]
    ro = Language.objects.get_or_create(title=Language.RO)[0]
    en = Language.objects.get_or_create(title=Language.EN)[0]
    return ru, ro, en


def create_title(model, title, language, container):
    obj = model()
    obj.title = '%s - %s' % (title, now())
    obj.language = language
    obj.container = container
    obj.save()


def create_contact(ent):
    phones = [u'333', u'333-111', u'333-222']
    urls = [u'http://www.freetime.com/',
            u'http://www.yp.com/',
            u'http://varo-inform.com/']
    fields = {
        'region': [u'Chisinau'],
        'sector': [u'Telecentrro',
                   u'Telecentr'],
        'street': [u'G. Tudor',
                   u'Tudor G.'],
        'top_administrative_unit': [],
        'town': [u'Chisinau'],
    }
    models = {
        'region': [Region, RegionTitle],
        'street': [Street, StreetTitle],
        'town': [Town, TownTitle],
    }
    #     postal_code  
    #     house_number
    #     office_number 
    contact = Contact(enterprise=ent)
    for field, value in fields.items():
        model = models.get(field)
        if not model: continue

        m, t = model

        obj = m()
        obj.save()
        setattr(contact, field, obj)
        languages = get_languages()
        for v in value:
            create_title(t, v, languages[value.index(v)], obj)

    contact.save()
    for ph in phones:
        p = Phone(phone=ph)
        p.type = 1
        p.save()
        contact.phones.add(p)
    for url in urls:
        u = Url(url=url)
        u.save()
        contact.urls.add(u)
    contact.save()


def create_contact_person(varo, names, phones):
    languages = get_languages()
    person = Person()
    person.save()
    for name in names:
        pn = PersonTitle(title=name, language=languages[names.index(name)])
        pn.container = person
        pn.save()

    position = Position()
    position.save()
    create_title(PositionTitle, 'директор', languages[0], position)
    contactperson = ContactPerson()
    contactperson.position = position
    contactperson.person = person
    contactperson.enterprise = varo
    contactperson.save()

    for ph in phones:
        p = Phone(phone=ph)
        p.type = 1
        p.save()
        contactperson.phones.add(p)


def create_gproduce(varo, titles):
    good = Good()
    good.save()
    languages = get_languages()
    for t in titles:
        create_title(GoodTitle, t, languages[titles.index(t)], good)

    gp = Gproduce()
    gp.enterprise = varo
    gp.good = good
    gp.is_produce = True
    gp.save()
