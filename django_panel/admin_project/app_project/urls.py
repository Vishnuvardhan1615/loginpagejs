from django.urls import path,include
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    path('check_thumbnail_images/', views.check_thumbnail_images, name='check_thumbnail_images'),
    path('register_user/', views.register_user, name='register_user'),
    # path('list_all_folders_view/', views.list_all_folders_view, name='list_all_folders_view'),
]