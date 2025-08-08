from django.urls import path
from voitures import services

urlpatterns = [
    path('', services.voiture_list),
    path('<str:pk>/', services.voiture_detail),


]