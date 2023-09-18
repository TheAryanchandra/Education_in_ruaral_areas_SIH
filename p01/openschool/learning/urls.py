
from django.urls import path
from .views import *
from . import views

urlpatterns = [

     path("", views.index, name="index"),
    #path('', views.chat, name='chat'),

   
    path('upload/', views.upload_downloadable_item, name='upload_downloadable_item'),
    path('list/', views.list_downloadable_items, name='list_downloadable_items'),

     path("user_login/", views.user_login, name="user_login"),
    path("signup/", views.signup, name="signup"),
    path("user_homepage/", views.user_homepage, name="user_homepage"),
    path("logout/", views.Logout, name="logout"),


    path("Teacher_signup/", views.Teacher_signup, name="Teacher_signup"),
    path("Teacher_login/", views.Teacher_login, name="Teacher_login"),
    path("Teacher_homepage/", views.Teacher_homepage, name="Teacher_homepage"),
    path("logout/", views.Logout, name="logout"),


     path('chat/',chat,name='chat'),
    path('ajax/',Ajax,name='ajax'),


     path('', views.post_list, name='post-list'),
    path('post/<int:pk>/', views.post_detail, name='post-detail'),


]


