from django.urls import path
from . import views

urlpatterns = [
     path('comment/add/news/<int:pk>/', views.news_cm_add, name='news_cm_add'),
     path('comments/list/', views.comments_list, name='comments_list'),
     path('comments/del/<int:pk>/', views.comments_del, name='comments_del'),
     path('comments/confirmed/<int:pk>/', views.comments_confirmed, name='comments_confirmed'),

]
