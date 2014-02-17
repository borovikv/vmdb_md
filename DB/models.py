#-*- coding: utf-8 -*-
from django.db import models
import datetime
from DB.dbutils import get_enterprise_fields, get_words
from SearchEngine.models import Words


def obj_as_list(obj):
    result = {}
    for field in obj.get_all_fields():
        name = field if isinstance(field, basestring) else field.name
        field_value = obj.get_field_value(name, getattr(obj, name))
        result[name] = field_value
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
        return self.pk


################################################################################
#
################################################################################


class Branch(models.Model, LanguageTitleContainer):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')

    def children(self):
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
    brand = models.ManyToManyField(Brand, null=True, blank=True)

    creation = models.DateField(null=True, blank=True)
    foreing_capital = models.NullBooleanField(null=True, blank=True)
    workplaces = models.PositiveIntegerField(null=True, blank=True)
    check_date = models.DateField()
    last_change = models.DateTimeField()
    logo = models.ImageField(upload_to='enterprise/logo', null=True, blank=True)
    yp_url = models.URLField()

    words = models.ManyToManyField(Words)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.last_change = datetime.datetime.now()
        self.add_words()
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using,
                                 update_fields=update_fields)

    def add_words(self):
        fields = get_enterprise_fields(self)
        words = get_words(fields)
        words = [Words.objects.get_or_create(word=word)[0] for word in words if word]
        for word in words:
            self.words.add(word)

    def get_all_fields(self):
        links = [rel.get_accessor_name() for rel in self._meta.get_all_related_objects()]
        return self._meta.fields + self._meta.local_many_to_many + links

    def get_field_value(self, name, value):
        if name in ['brand', ]:
            return [brand.title for brand in value.all()]

        if name in ['contact_set', 'contactperson_set', 'gproduce_set']:
            return [obj.as_list() for obj in value.all() if obj]

        elif name == 'titles':
            return self.all_titles()

        elif name in ('advertisment_set', ):
            return

        elif name == 'business_entity':
            return value.all_titles()
        else:
            return value

    def as_list(self):
        return obj_as_list(self)


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

    def get_all_fields(self):
        return self._meta.fields + self._meta.local_many_to_many

    @staticmethod
    def get_field_value(name, value):
        if name in ['street', 'sector', 'town', 'region', 'top_administrative_unit']:
            return value.all_titles() if value else []
        elif name in ['phone', 'url', 'email']:
            return value.all()
        return value

    def as_list(self):
        return obj_as_list(self)


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
        return u'+373-%s' % self.phone

    def __unicode__(self):
        #return '(+%(country_code)s) %(town_code)s %(telephone)s'%self.__dict__
        return self.get_phone()


class Email(models.Model):
    email = models.EmailField()

    def __unicode__(self):
        return self.email


class Url(models.Model):
    url = models.URLField()

    def __unicode__(self):
        return self.url


################################################################################
#
################################################################################


class Good(models.Model, LanguageTitleContainer):
    branch = models.ForeignKey(Branch, blank=True, null=True, )


class GoodTitle(LanguageTitle):
    good = models.ForeignKey(Good, related_name='titles')


class Gproduce(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    good = models.ForeignKey(Good)
    gproduce = models.BooleanField()

    def as_list(self):
        return {'good': self.good.all_titles(),
                'branch': self.good.branch.all_titles() if self.good.branch else []}


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

    def as_list(self):
        return {'person_name': self.person.all_titles(), 'phone': self.phone.all()}


################################################################################
#
################################################################################


class Advertisement(models.Model):
    enterprise = models.ForeignKey(Enterprise)
    image = models.ImageField(upload_to='enterprise/advertisment')


class AdvertisementText(models.Model):
    advertisement = models.ForeignKey(Advertisement)
    language = models.ForeignKey(Language)
    text = models.TextField(null=True, blank=True)