from django.urls import path
from . import services
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'', services, basename='client')

urlpatterns = [
    path('', services.hebergement_list),
    path('<str:pk>/', services.hebergement_detail),


]