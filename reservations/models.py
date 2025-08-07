from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from clients.models import Client  

def generate_reservation_id():
    last = Reservation.objects.order_by('-idReservation').first()
    if last and last.idReservation.startswith("RES"):
        number = int(last.idReservation[3:]) + 1
    else:
        number = 1
    return f"RES{number:04d}"

class Reservation(models.Model):
    idReservation = models.CharField(
        primary_key=True,
        max_length=10,
        default=generate_reservation_id,
        editable=False
    )

    # id_client = models.CharField(max_length=10)  # ou ForeignKey si tu as une table Client
    id_client = models.ForeignKey(Client, on_delete=models.CASCADE)

    # Lien générique vers vol, voiture, activité ou hébergement
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=20)
    objet = GenericForeignKey('content_type', 'object_id')

    type = models.CharField(
        max_length=20,
        choices=[
            ('vol', 'Vol'),
            ('voiture', 'Voiture'),
            ('hebergement', 'Hébergement'),
            ('activité', 'Activité'),
        ]
    )

    date_debut = models.DateField()
    date_fin = models.DateField(null=True, blank=True)  # optionnel si un seul jour
    quantite = models.PositiveIntegerField(default=1)
    montant = models.DecimalField(max_digits=20, decimal_places=2)

    lieu_depart = models.CharField(max_length=100, blank=True, null=True)
    lieu_arrivee = models.CharField(max_length=100, blank=True, null=True)

   

    class Meta:
        db_table = 'reservations'

    def __str__(self):
        return f"{self.idReservation} - {self.type} ({self.id_client})"
