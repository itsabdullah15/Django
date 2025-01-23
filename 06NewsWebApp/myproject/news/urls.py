from django.urls import path
from . import views

urlpatterns = [
    path('news/<slug:slug>/', views.news_details, name='news_detail'),
    path('panel/news/list/', views.news_list, name='news_list'),
    path('panel/news/add/', views.news_add, name='news_add'),
    path('panel/news/delete/<int:pk>/', views.news_delete, name='news_delete'),
    path('panel/news/edit/<int:pk>/', views.news_edit, name='news_edit'),
    path('panel/news/publish/<int:pk>/', views.news_publish, name='news_publish'),
    path('all/news/<slug:slug>/', views.news_all_show, name='news_all_show'),
    

    
]