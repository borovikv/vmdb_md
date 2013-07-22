#-*- coding: utf-8 -*-
from DB.models import Enterprise, Language, BusinessEntityType,\
    BusinessEntityTitle, Brand, EnterpriseName, Phone, Region, RegionTitle,\
    Street, StreetTitle, Town, TownTitle, Url, Contact, Person, PersonName,\
    ContactPerson, Position, PositionTitle, Good, GoodTitle
import datetime
import re

def createTitle(model, title, language, container):
    obj = model()
    obj.title = title
    obj.language = language
    name = model.__class__.__name__
    name = re.sub('Title$', '', name)
    setattr(obj, 'business_entity', container)
    obj.save()


def createcontact(ent):
    phones = [ u'333', u'333-111', u'333-222']
    urls = [ u'http://www.freetime.com/',
            u'http://www.yp.com/',
            u'http://varo-inform.com/']
    fields = {
             'region': [ u'Chisinau'],
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
    contact = Contact()
    for field, value in fields.items():
        model = models.get(field)
        m, t = None, None
        try:
            m, t = model
        except:
            m = model
        obj = m()
        obj.save()
        setattr(contact, field, obj)
        languages = get_languages()
        for v in value:
            createTitle(t, v, languages[value.index(v)], obj)
    
    for ph in phones:
        p = Phone(phone=ph)
        p.save()
        contact.phone.add(p)
    for url in urls:
        u = Url(url=url)
        u.save()
        contact.url.add(u)

def createcontactPerson(varo, names, phones):
    languages = get_languages()
    person = Person()
    person.save()
    for name in names:
        pn = PersonName(title=name, language=languages[names.index(name)])
        pn.person = person
        pn.save()
    
    position = Position()
    position.save()
    createTitle(PositionTitle, 'директор', languages[0], position)
    contactperson = ContactPerson()
    contactperson.person = person
    contactperson.position = position
    contactperson.enterprise = varo
    for ph in phones:
        p = Phone(phone=ph)
        p.save()
        person.phone.add(p)
        

def creategproduce(varo, titles):
    good = Good()
    good.save()
    languages = get_languages()
    for t in titles:
        createTitle(GoodTitle, t, languages[titles.index(t)], good)


def get_languages():
    ru = Language.objects.get_or_create(title=Language.RU)[0]
    ro = Language.objects.get_or_create(title=Language.RO)[0]
    en = Language.objects.get_or_create(title=Language.EN)[0]
    return ru, ro, en

def create_test_varo():
    ru, ro, en = get_languages()
    varo = Enterprise()
    entity = BusinessEntityType()
    entity.save()
    createTitle(BusinessEntityTitle, 'ООО', ru, entity)
    createTitle(BusinessEntityTitle, 'srl', ro, entity)
    createTitle(BusinessEntityTitle, 'llc', en, entity)
    varo.business_entity = entity
    br = Brand(title='varoinform')
    br.save()
    varo.brand.add(br)
    varo.check_date = datetime.datetime.date()
    varo.yp_url = 'www.yp.md/varo'
    varo.save()
    
    createTitle(EnterpriseName, 'varo-inform', ru, varo)
    createcontact(varo)
    createcontactPerson(varo, ('hasanov serg', u'хасанов сергей'), ['111111', '111222'])
    createcontactPerson(varo, ('rosenberg alex', u'розенберг алекс'), ['222111', '222222'])
    creategproduce(varo, [u'reclame', u'advertisment'])
    creategproduce(varo, [u'Disaine', u'Disine'])

