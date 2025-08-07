from django.urls import path
from . import services

urlpatterns = [
    path('', services.reservation_list),
    path('<str:pk>/', services.reservation_detail),
    path('total-par-client/', services.reservation_total_par_client),  # optionnel
    path('client/<str:client_id>/', services.reservations_par_client_et_periode),
    path('client/<str:client_id>/reservations/',services.supprimer_reservations_client_periode,
        name='delete-client-reservations'
    ),
]
