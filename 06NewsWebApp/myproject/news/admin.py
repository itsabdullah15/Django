from django.contrib import admin
from .models import News

class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}  # Auto-fill slug from title
    list_display = ("title", "publication_date", "slug")  # Show slug in the list view

admin.site.register(News, NewsAdmin)

