from django.db import models

# Create your models here.

class ContactForm(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(max_length=50)
    txt = models.TextField()
    date = models.CharField(max_length=12, default="")
    time = models.CharField(max_length=12, default="")
    
    def __str__(self):
        return self.name
    
