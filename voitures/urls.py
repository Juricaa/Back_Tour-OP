from django.urls import path
from django.conf.urls import url
from voitures import services

urlpatterns = [
    path('', services.voiture_list),
    path('<str:pk>/', services.voiture_detail),


]