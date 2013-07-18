#-*- coding: utf-8 -*-
from django.db import models
import datetime
import inspect
from SearchEngine.views import flatten

class Field(object):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def __str__(self):
        return self.name
    
    

def get_names(obj):
    if obj:
        return obj.all_titles()
    return []

def get_call_results(obj, start):
    result = []
    for name, method in inspect.getmembers(obj, predicate=inspect.ismethod):
        if name.startswith(start):
            field = method()
            try:
                result.extend(field)
            except:
                result.append(field)
    return result
               
               
class Language(models.Model):
    RU = 'RU'
    EN = 'EN'
    RO = 'RO'
    LANGUAGE_CHOICES = (
        (RU, RU,),
        (RO, RO,),
        (EN, EN,),
    )
    LANGUAGE_PRIORITY = (RU, RO, EN, )
    title = models.CharField(max_length=4, choices=LANGUAGE_CHOICES, default=RU)
    
    def __unicode__(self):
        return self.title

class LanguageTitle(models.Model):
    language = models.ForeignKey(Language)
    title = models.CharField(max_length=100)
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        abstract = True

class LanguageTitleContainer:
    
    def title(self, lang):
        if not self.titles.count():
            return
        try:
            language = Language.objects.get(title=lang)
            return self.titles.get(language=language).title
        except:
            pass
    def all_titles(self):
        return [title.title for title in self.titles.all()]
    
    def __unicode__(self):
        for lang in Language.LANGUAGE_PRIORITY:
            title = self.title(lang)
            if title:
                return title
        return self.id
################################################################################
#
################################################################################

class Branch(models.Model, LanguageTitleContainer):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
        
    def childrens(self):
        self.objects.filter(parent=self)

class BranchTitle(LanguageTitle):
    branch = models.ForeignKey(Branch, related_name='titles')

# properties
class BusinessEntityType(models.Model, LanguageTitleContainer):
    pass

class BusinessEntityTitle(LanguageTitle):
    business_entity = models.ForeignKey(BusinessEntityType, related_name='titles')
    

class Brand(models.Model):
    title = models.CharField(max_length=100)
   
 
class Enterprise(models.Model, LanguageTitleContainer):
    business_entity = models.ForeignKey(BusinessEntityType)
    dealer = models.ManyToManyField(Brand, null=True, blank=True)
    
    creation = models.DateField(null=True, blank=True)
    foreing_capital = models.NullBooleanField(null=True, blank=True)
    workplaces = models.PositiveIntegerField(null=True, blank=True)
    check_date = models.DateField()
    last_change = models.DateTimeField()
    logo = models.ImageField(upload_to='enterprise/logo', null=True, blank=True)
    yp_url = models.URLField()
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.last_change = datetime.datetime.now()
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
    
    def enterprise_products(self):
        return Field('GoodTitle', 
                      flatten( [ product.good.all_titles() 
                                 for product in self.gproduce_set.all() 
                                 if product.good ] ) )
     
    def enterprise_branches(self):
        return Field('BranchTitle', 
                      flatten( [ product.good.branch.all_titles() 
                                 for product in self.gproduce_set.all() 
                                 if product.good.branch ] ) )
     
    def enterprise_brands(self):
        return Field('Brand', 
                        [ brand.title for brand in self.dealer.all()
                                 if brand ])
    
    def enterprise_titles(self):
        return Field('EnterpriseName', LanguageTitleContainer.all_titles(self))   
    
    def enterprise_contacts(self):
        return flatten([ x.all() for x in self.contact_set.all() if x])
     
    def enterprise_persons(self):
        return flatten([ x.all() for x in self.contactperson_set.all() if x])
    
    def get_enterprise_fields(self):
        result = {}
        fields = get_call_results(self, 'enterprise') 
        for field in fields:
            result.setdefault(field.name, []).extend(field.value)
        return result
     
    

class EnterpriseName(LanguageTitle):
    enterprise = models.ForeignKey(Enterprise, related_name='titles')   

class Contact(models.Model):
    enterpise = models.ForeignKey(Enterprise)
    postal_code = models.CharField(max_length=10)
    house_number = models.CharField(max_length=10)
    office_number = models.CharField(max_length=10, null=True, blank=True)
    street = models.ForeignKey("Street")
    sector = models.ForeignKey("Sector", null=True, blank=True)
    town = models.ForeignKey("Town")
    region = models.ForeignKey("Region") 
    top_administrative_unit = models.ForeignKey('TopAdministrativeUnit', null=True, blank=True)
    phone = models.ManyToManyField("Phone")
    url = models.ManyToManyField("Url")
    email = models.ManyToManyField("Email")
    
    def contact_phones(self):
        return Field('Phone', [phone.phone for phone in self.phone.all() if phone])
    
    def contact_urls(self):
        return Field('Url', [url.url for url in self.url.all() if url])
    
    def contact_emails(self):
        return Field('Email', [email.email for email in self.email.all() if email])
    
    def contact_street_names(self):
        return Field('StreetTitle', get_names(self.street))
    
    def contact_sector_names(self):
        return Field('SectorTitle', get_names(self.sector))
    
    def contact_town_names(self):
        return Field('TownTitle', get_names(self.town))
    
    def contact_region_names(self):
        return Field('RegionTitle', get_names(self.region))
    
    def contact_tau_names(self):
        return Field('AdministrativeUnitTitle', get_names(self.top_administrative_unit))
    
    def all(self):
        return get_call_results(self, 'contact')
    
class Street(models.Model, LanguageTitleContainer):
    pass
class StreetTitle(LanguageTitle):
    street = models.ForeignKey(Street, related_name='titles')

class Sector(models.Model, LanguageTitleContainer):
    pass
class SectorTitle(LanguageTitle):
    sector = models.ForeignKey(Sector, related_name='titles')
    
class Town(models.Model, LanguageTitleContainer):
    pass
class TownTitle(LanguageTitle):
    town = models.ForeignKey(Town, related_name='titles')

class Region(models.Model, LanguageTitleContainer):
    pass
class RegionTitle(LanguageTitle):
    region = models.ForeignKey(Region, related_name='titles')

class TopAdministrativeUnit(models.Model, LanguageTitleContainer):
    pass
class AdministrativeUnitTitle(LanguageTitle):
    region = models.ForeignKey(TopAdministrativeUnit, related_name='titles')

class Phone(models.Model):
    phone = models.CharField(max_length=12)
    
    def get_phone(self):
        return u'+373 022 %s'%self.phone
        
    def __unicode__(self):
        #return '(+%(country_code)s) %(town_code)s %(telephone)s'%self.__dict__
        return self.get_phone()

class Email(models.Model):
    email = models.EmailField()

class Url(models.Model):
    url = models.URLField()

################################################################################
#
################################################################################
class Good(models.Model, LanguageTitleContainer):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    branch = models.ForeignKey(Branch, blank=True, null=True,)
    
class GoodTitle(LanguageTitle):
    good = models.ForeignKey(Good, related_name='titles')

class Gproduce(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    good = models.ForeignKey(Good)
    gproduce  = models.BooleanField()

################################################################################
#
################################################################################
class Position(models.Model, LanguageTitleContainer):
    pass

class PositionTitle(LanguageTitle):
    position = models.ForeignKey(Position, related_name='titles')

class Person(models.Model, LanguageTitleContainer):
    pass

class PersonName(LanguageTitle):
    person = models.ForeignKey(Person, related_name='titles')

class ContactPerson(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    person = models.ForeignKey(Person)
    position = models.ForeignKey(Position)
    phone = models.ManyToManyField(Phone)
    
    def person_names(self):
        return Field('PersonName', get_names(self.person))
    
    def person_phone(self):
        return Field('Phone', [phone.phone for phone in self.phone.all() if phone])
    
    def all(self):
        return get_call_results(self, 'person')
        
################################################################################
#
################################################################################
class Advertisment(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    image = models.ImageField(upload_to='enterprise/advertisment')

class AdvertismentText(models.Model):
    advertisment = models.ForeignKey(Advertisment)
    language = models.ForeignKey(Language)
    text = models.TextField(null=True, blank=True)
    