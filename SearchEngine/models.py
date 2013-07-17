from django.db import models
from DB.models import Enterprise

# Create your models here.
class Words(models.Model):
    word = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.word

class EnterpriseWords(models.Model):
    word = models.ForeignKey(Words)
    enterprise = models.ForeignKey(Enterprise)
    
    def __unicode__(self):
        return "%s, %s"%(self.word, self.enterprise)
    
    @staticmethod
    def create_from_enterprise(enterprise):
        pass
    
    
    
