from django.db import models
from django.utils import timezone
from clients.models import Client

def generate_facture_id():
    last = Facture.objects.order_by('-idFacture').first()
    if last and last.idFacture.startswith("FAC"):
        number = int(last.idFacture[3:]) + 1
    else:
        number = 1
    return f"FAC{number:04d}"

class Facture(models.Model):
    idFacture = models.CharField(
        primary_key=True,
        max_length=10,
        default=generate_facture_id,
        editable=False
    )

    clientId = models.ForeignKey(Client, on_delete=models.CASCADE)
    dateTravel = models.DateField(null=True, blank=True)
    dateReturn = models.DateField(null=True, blank=True)
    # dateReturn = models.DateField()
    dateCreated = models.DateField(default=timezone.now)

    status = models.CharField(
        max_length=50,
        choices=[
            ('confirmé', 'Confirmé'),
            ('payé', 'Payé'),
            ('en_attente', 'En attente'),
            ('annulé', 'Annulé'),
             ('en_cours', 'En cours'),
             ('annule', 'Annulé'),
        ],
        default='en_attente'
    )

    totalPrice = models.DecimalField(max_digits=10, decimal_places=2,null=True, blank=True)

    class Meta:
        db_table = 'factures'

    def __str__(self):
        return f"Facture {self.idFact} - Client {self.id_client_id} - {self.status}"
