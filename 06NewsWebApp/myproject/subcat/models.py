from django.db import models

# Create your models here.
class SubCat(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    catname = models.CharField(max_length=50)
    catid = models.IntegerField()
    
    def __str__(self):
        return self.name
    