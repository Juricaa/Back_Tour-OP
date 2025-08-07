from django.utils import timezone
from django.db import models

def generate_custom_client_id():
    last = Client.objects.order_by('-idClient').first()
    if last and last.idClient.startswith("C"):
        number = int(last.idClient[3:]) + 1
    else:
        number = 1
    return f"C{number:04d}"
class Client(models.Model):
    idClient = models.CharField(primary_key=True,
        max_length=10,
        default=generate_custom_client_id,
        editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=50)
    nationality = models.CharField(max_length=100)
    address = models.TextField()
    lastVisit = models.DateField(auto_now=True)
    notes = models.TextField(blank=True, null=True)
    nbpersonnes = models.PositiveIntegerField()
    destinations = models.JSONField(default=list)
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clients'  

    