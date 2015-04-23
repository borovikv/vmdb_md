from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class Database(models.Model):
    STANDARD = 3
    UNUSED = 'unused'
    SOLD = 'sold'
    REGISTERED = 'registered'
    STATUS_CHOICES = (
        (UNUSED, _(UNUSED)),
        (SOLD, _(SOLD)),
        (REGISTERED, _(REGISTERED))
    )
    database_id = models.CharField(max_length=16, unique=True, verbose_name=_('database_id'))
    database_password = models.CharField(max_length=32, verbose_name=_('password'))
    last_update = models.DateField(null=True, blank=True, verbose_name=_('last_update'))
    max_registrations = models.PositiveSmallIntegerField(default=STANDARD, verbose_name=_('max_registrations'))
    is_perpetual = models.BooleanField(default=False, verbose_name=_('is_perpetual'))
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, verbose_name=_('status'))

    def __unicode__(self):
        return u'%s' % self.database_id

    def count_registrations(self):
        return len(self.registrations.all())

    def has_available_registrations(self):
        return self.is_perpetual or self.count_registrations() < self.max_registrations

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.status:
            self.status = Database.UNUSED
        super(Database, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _('database')
        verbose_name_plural = _('databases')


class Registration(models.Model):
    database = models.ForeignKey(Database, related_name='registrations')
    date = models.DateField(verbose_name=_('date'))

    def __unicode__(self):
        return u'%s' % self.date

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.date = timezone.now()
        super(Registration, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')


class Updating(models.Model):
    last_update = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.last_update)