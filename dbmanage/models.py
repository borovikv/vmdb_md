from django.db import models


class Databases(models.Model):
    PERPETUAL = -1
    STANDARD = 3
    EXTENDED = 10
    REG_TYPE_CHOICES = (
        (PERPETUAL, 'perpetual'),
        (STANDARD, 'standard'),
        (EXTENDED, 'extended'),
    )
    
    database_id = models.CharField(max_length=25)
    database_password = models.CharField(max_length=32)
    last_update = models.DateField(null=True, blank=True)
    registration_type = models.PositiveSmallIntegerField(choices=REG_TYPE_CHOICES, default=STANDARD)

    def __unicode__(self):
        return u'%s' % self.database_id
    
    def max_regestrations(self):
        return self.registration_type


class RegisteredDatabases(models.Model):
    database = models.ForeignKey(Databases)
    counter = models.PositiveSmallIntegerField(default=0)
    first_date = models.DateField()
    last_date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return u'%s' % (self.database)


class Updating(models.Model):
    last_update = models.DateField(null=True, blank=True)

    def __unicode__(self):
        return unicode(self.last_update)