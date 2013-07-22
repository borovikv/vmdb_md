from django.db import models

# Create your models here.
class Words(models.Model):
    word = models.CharField(max_length=50)
    
    def __unicode__(self):
        return self.word

    
    
    
