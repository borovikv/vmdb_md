from django.db import models as m


# Create your models here.
class Words(m.Model):
    word = m.CharField(max_length=50)
    
    def __unicode__(self):
        return self.word