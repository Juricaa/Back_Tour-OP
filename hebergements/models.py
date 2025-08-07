
from django.db import models

from django.utils import timezone

def generate_custom_id():
    last = Hebergement.objects.order_by('-idHebergement').first()
    if last and last.idHebergement.startswith("HEB"):
        number = int(last.idHebergement[3:]) + 1
    else:
        number = 1
    return f"HEB{number:04d}"


class Hebergement(models.Model):
    idHebergement = models.CharField(
        primary_key=True,
        max_length=10,
        default=generate_custom_id,
        editable=False
    )
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50)  # ex: Bungalow, Hôtel
    location = models.CharField(max_length=100)
    address = models.TextField()
    priceRange = models.DecimalField(max_digits=20, decimal_places=2)
    rating = models.FloatField()
    amenities = models.JSONField()  # Liste des équipements (wifi, spa, etc.)
    capacity = models.PositiveIntegerField()
    description = models.TextField()
    phone = models.CharField(max_length=50)
    email = models.EmailField()
    favorite = models.BooleanField(default=False)
    createdAt = models.DateTimeField(default=timezone.now)
    lastUsed = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)
    popularity = models.PositiveIntegerField(default=0)
   
    

    class Meta:
        db_table = 'hebergements'