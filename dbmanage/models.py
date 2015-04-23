from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Database(models.Model):
    PERPETUAL = -1
    STANDARD = 3
    EXTENDED = 10
    REG_TYPE_CHOICES = (
        (PERPETUAL, 'perpetual'),
        (STANDARD, 'standard'),
        (EXTENDED, 'extended'),
    )
    UNUSED = 'unused'
    SOLD = 'sold'
    REGISTERED = 'registered'
    STATUS_CHOICES = (
        (UNUSED, UNUSED),
        (SOLD, SOLD),
        (REGISTERED, REGISTERED)
    )
    database_id = models.CharField(max_length=16, unique=True, verbose_name=_('database_id'))
    database_password = models.CharField(max_length=32, verbose_name=_('password'))
    last_update = models.DateField(null=True, blank=True, verbose_name=_('last_update'))
    registration_type = models.PositiveSmallIntegerField(choices=REG_TYPE_CHOICES, default=STANDARD,
                                                         verbose_name=_('registration_type'))
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, verbose_name=_('status'))

    def __unicode__(self):
        return u'%s' % self.database_id

    def max_registrations(self):
        return self.registration_type

    def count_registrations(self):
        return len(self.registrations.all())

    def has_available_registrations(self):
        return self.registration_type == Database.PERPETUAL or self.count_registrations() < self.max_registrations()

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.status:
            self.status = Database.UNUSED
        super(Database, self).save(force_insert, force_update, using, update_fields)


class Registration(models.Model):
    database = models.ForeignKey(Database, related_name='registrations')
    date = models.DateField()

    def __unicode__(self):
        return u'%s' % self.date

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date = timezone.now()
        super(Registration, self).save(force_insert, force_update, using, update_fields)


class Updating(models.Model):
    last_update = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.last_update)