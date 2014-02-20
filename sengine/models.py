from django.db import models as m


class Words(m.Model):
    word = m.CharField(max_length=50)
    
    def __unicode__(self):
        return self.word if self.word else ""