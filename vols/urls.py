from django.urls import path
from vols import services


urlpatterns = [
    path('', services.vol_list, name='vol-list'),
    path('<str:pk>/', services.vol_detail, name='vol-detail'),
]
