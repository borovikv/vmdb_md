from django.db import models


class Databases(models.Model):
    database_id = models.PositiveIntegerField()
    database_password = models.CharField(max_length=25)
    last_update = models.DateField(null=True, blank=True)
    
    def __unicode__(self):
        return u'%s'%self.database_id


class RegisteredDatabases(models.Model):
    database = models.ForeignKey(Databases)
    user_id = models.PositiveIntegerField()
    
    def __unicode__(self):
        return "%s, %s"%(self.user_id , self.database) 


