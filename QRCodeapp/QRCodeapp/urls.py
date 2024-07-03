from django.contrib import admin
from django.urls import path
from app.views import home, decodeimg
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('decode/',decodeimg),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)