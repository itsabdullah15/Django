from django.db import models

# Create your models here.

class Main(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=900,null=True, blank=True)
    about_text = models.TextField(null=True, blank=True)
    youtube = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    tell = models.CharField(max_length=15, null=True, blank=True)
    link = models.URLField(max_length=200, null=True, blank=True)
    set_name = models.TextField(default='-', null=True)
    picurl = models.TextField(default=" ", null=True)
    picname = models.TextField(default=" ", null=True)
    picurl2 = models.TextField(default=" ", null=True)
    picname2 = models.TextField(default=" ", null=True)
    
    
    
    def __str__(self):
        return self.set_name + " | " + str(self.pk)
    
    
