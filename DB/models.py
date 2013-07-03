from django.db import models
# Create your models here.

class Language(models.Model):
    RU = 'RU'
    EN = 'EN'
    RO = 'RO'
    title = models.CharField(max_length=4)

class LanguageTitle(models.Model):
    language = models.ForeignKey(Language)
    title = models.CharField(max_length=100)#, related_name='titles')
    
    class Meta:
        abstract = True

class LanguageTitleContainer:
    
    def title(self, language):
        title = self.titles.filter(language=language)
        if title.count():
            return title[0]
        else:
            return 'The title for %s not exist'%language
    

class Branch(models.Model, LanguageTitleContainer):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
        
    def childrens(self):
        self.objects.filter(parent=self)

class BranchTitle(LanguageTitle):
    branch = models.ForeignKey(Branch)

# properties
class BusinessEntityType(models.Model, LanguageTitleContainer):
    pass

class BusinessEntityTitle(LanguageTitle):
    business_entity = models.ForeignKey(BusinessEntityType)
    

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

class EnterpriseName(LanguageTitle):
    enterprise = models.ForeignKey(Enterprise)   

class Contact(models.Model):
    enterpise = models.ForeignKey(Enterprise)
    mail_code = models.CharField(max_length=10)
    house_number = models.CharField(max_length=10)
    office_number = models.CharField(max_length=10, null=True, blank=True)
    street = models.ForeignKey("Street")
    sector = models.ForeignKey("Sector", null=True, blank=True)
    town = models.ForeignKey("Town")
    region = models.ForeignKey("Region") 
    top_administrative_unit = models.ForeignKey('TopAdministrativeUnit', null=True, blank=True)
    phones = models.ManyToManyField("Phone")

class Street(models.Model, LanguageTitleContainer):
    pass
class StreetL(LanguageTitle):
    street = models.ForeignKey(Street)

class Sector(models.Model, LanguageTitleContainer):
    pass
class SectorTitle(LanguageTitle):
    sector = models.ForeignKey(Sector)
    
class Town(models.Model, LanguageTitleContainer):
    pass
class TownTitle(LanguageTitle):
    town = models.ForeignKey(Town)

class Region(models.Model, LanguageTitleContainer):
    pass
class RegionTitle(LanguageTitle):
    region = models.ForeignKey(Region)

class TopAdministrativeUnit(models.Model, LanguageTitleContainer):
    pass
class AdministrativeUnitTitle(LanguageTitle):
    region = models.ForeignKey(TopAdministrativeUnit)

class Url(models.Model):
    contact = models.ManyToManyField(Contact)
    url = models.URLField()
    
class Email(models.Model):
    contact = models.ManyToManyField(Contact)
    email = models.EmailField()

class Phone(models.Model):
    phone = models.CharField(max_length=12)
    
    def get_phone(self):
        return u'+373 022 %s'%self.phone
        
    def __unicode__(self):
        return self.get_phone()
        #return '(+%(country_code)s) %(town_code)s %(telephone)s'%self.__dict__
    
################################################################################
#
################################################################################
class Good(models.Model, LanguageTitleContainer):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    branch = models.ForeignKey(Branch, blank=True, null=True,)
    
class GoodTitlte(LanguageTitle):
    good = models.ForeignKey(Good)

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
    position = models.ForeignKey(Position)

class Person(models.Model, LanguageTitleContainer):
    pass

class PersonName(LanguageTitle):
    person = models.ForeignKey(Person)

class ContactPerson(models.Model):
    enterprise = models.ManyToManyField(Enterprise)
    person = models.ForeignKey(Person)
    position = models.ForeignKey(Position)
    phones = models.ManyToManyField(Phone)

        
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
    