from django.contrib import admin
from app.models import GeneratedImage, DecodeImage
# Register your models here.

@admin.register(GeneratedImage)
class GeneratedImageAdmin(admin.ModelAdmin):
    list_display = ('id','imag')

@admin.register(DecodeImage)
class DecodeImageImageAdmin(admin.ModelAdmin):
    list_display = ('id','imag')
