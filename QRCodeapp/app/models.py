from django.db import models

# Create your models here.


class GeneratedImage(models.Model):
    imag = models.ImageField(upload_to='media')

class DecodeImage(models.Model):
    imag = models.ImageField(upload_to='decodeimg')