from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalogue_list, name='catalogue_list'),
    path('upload/', views.upload_catalogue, name='upload_catalogue'),
    path('home/', views.home, name='home'),  # optional direct home URL
]
