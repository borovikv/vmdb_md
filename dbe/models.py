#-*- coding: utf-8 -*-
import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import utc


class ChangeAbstract(models.Model):
    last_change = models.DateTimeField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.last_change = datetime.datetime.utcnow().replace(tzinfo=utc)
        return models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using,
                                 update_fields=update_fields)

    class Meta:
        abstract = True


class Title(ChangeAbstract):
    language = models.ForeignKey('Language')
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title

    class Meta:
        abstract = True


class LanguageTitleContainer(ChangeAbstract):
    def title(self, lang):
        if not self.titles.count():
            return
        try:
            language = Language.objects.get(title=lang)
            title = self.titles.get(language=language)
            return title.title
        except ObjectDoesNotExist:
            return None

    def all_titles(self):
        return [title.title for title in self.titles.all()]

    def __unicode__(self):
        for lang in Language.LANGUAGE_PRIORITY:
            title = self.title(lang)
            if title:
                return title
        return self.pk or self.__class__.__name__

    class Meta:
        abstract = True


class Language(ChangeAbstract):
    RU = 'RU'
    EN = 'EN'
    RO = 'RO'
    LANGUAGE_CHOICES = (
        (RU, RU,),
        (RO, RO,),
        (EN, EN,),
    )
    LANGUAGE_PRIORITY = (RU, RO, EN, )
    title = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=RU)

    def __unicode__(self):
        return self.title


class Branch(LanguageTitleContainer):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')


class BranchTitle(Title):
    container = models.ForeignKey(Branch, related_name='titles')


# properties
class BusinessEntityType(LanguageTitleContainer):
    pass


class BusinessEntityTitle(Title):
    container = models.ForeignKey(BusinessEntityType, related_name='titles')


class Brand(ChangeAbstract):
    title = models.CharField(max_length=100)

    def __unicode__(self):
        return self.title or u''


class Enterprise(LanguageTitleContainer):
    brand = models.ManyToManyField(Brand, null=True, blank=True)

    business_entity = models.ForeignKey(BusinessEntityType)
    creation = models.DateField(null=True, blank=True)
    foreign_capital = models.NullBooleanField(null=True, blank=True)
    workplaces = models.PositiveIntegerField(null=True, blank=True)
    check_date = models.DateField()
    logo = models.ImageField(upload_to='enterprise/logo', null=True, blank=True)
    yp_url = models.URLField()


class EnterpriseTitle(Title):
    container = models.ForeignKey(Enterprise, related_name='titles')


class Contact(ChangeAbstract):
    enterprise = models.ForeignKey(Enterprise)
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


class Street(LanguageTitleContainer):
    pass


class StreetTitle(Title):
    container = models.ForeignKey(Street, related_name='titles')


class Sector(LanguageTitleContainer):
    pass


class SectorTitle(Title):
    container = models.ForeignKey(Sector, related_name='titles')


class Town(LanguageTitleContainer):
    pass


class TownTitle(Title):
    container = models.ForeignKey(Town, related_name='titles')


class Region(LanguageTitleContainer):
    pass


class RegionTitle(Title):
    container = models.ForeignKey(Region, related_name='titles')


class TopAdministrativeUnit(LanguageTitleContainer):
    pass


class AdministrativeUnitTitle(Title):
    container = models.ForeignKey(TopAdministrativeUnit, related_name='titles')


class Phone(ChangeAbstract):
    phone = models.CharField(max_length=12)
    type = models.PositiveSmallIntegerField()

    def get_phone(self):
        return u'+373-%s' % self.phone

    def __unicode__(self):
        return self.get_phone()


class Email(ChangeAbstract):
    email = models.EmailField()

    def __unicode__(self):
        return self.email


class Url(ChangeAbstract):
    url = models.URLField()

    def __unicode__(self):
        return self.url


################################################################################
#
################################################################################


class Good(LanguageTitleContainer):
    branch = models.ForeignKey(Branch, blank=True, null=True, )


class GoodTitle(Title):
    container = models.ForeignKey(Good, related_name='titles')


class Gproduce(ChangeAbstract):
    enterprise = models.ForeignKey(Enterprise)
    good = models.ForeignKey(Good)
    is_produce = models.BooleanField()

################################################################################
#
################################################################################


class Position(LanguageTitleContainer):
    pass


class PositionTitle(Title):
    container = models.ForeignKey(Position, related_name='titles')


class Person(LanguageTitleContainer):
    pass


class PersonTitle(Title):
    container = models.ForeignKey(Person, related_name='titles')


class ContactPerson(ChangeAbstract):
    enterprise = models.ForeignKey(Enterprise)
    person = models.ForeignKey(Person)
    position = models.ForeignKey(Position)
    phone = models.ManyToManyField(Phone)

################################################################################
#
################################################################################


class Advertisement(ChangeAbstract):
    enterprise = models.ForeignKey(Enterprise)
    image = models.ImageField(upload_to='enterprise/advertisment')


class AdvertisementText(ChangeAbstract):
    advertisement = models.ForeignKey(Advertisement)
    language = models.ForeignKey(Language)
    text = models.TextField(null=True, blank=True)
