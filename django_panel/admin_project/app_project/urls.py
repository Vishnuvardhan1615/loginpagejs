from django.urls import path,include
from . import views

urlpatterns = [
    path('members/', views.members, name='members'),
    # path('list_all_folders_view/', views.list_all_folders_view, name='list_all_folders_view'),
]