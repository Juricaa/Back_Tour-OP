from django.urls import path
from activites import services


urlpatterns = [
    path('', services.activite_list, name='activite-list'),
    path('<str:pk>/', services.activite_detail, name='activite-detail'),
]
