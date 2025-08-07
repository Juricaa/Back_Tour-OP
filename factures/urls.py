from django.urls import path
from . import services

urlpatterns = [
    path('', services.facture_list, name='facture_list'),
    path('<str:pk>/', services.facture_detail, name='facture_detail'),
    path('total-par-client/', services.montant_total_factures_par_client, name='facture_total_par_client'),
]
