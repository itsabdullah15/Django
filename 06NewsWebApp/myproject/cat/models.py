from django.db import models

# Create your models here.
class Cat(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    count = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    