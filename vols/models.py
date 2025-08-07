from django.db import models

def generate_custom_vol_id():
    last = Vol.objects.order_by('-idVol').first()
    if last and last.idVol.startswith("VOL"):
        number = int(last.idVol[3:]) + 1
    else:
        number = 1
    return f"VOL{number:04d}"

class Vol(models.Model):
    CLASS_CHOICES = [
        ('economy', 'Économie'),
        ('business', 'Affaires'),
        ('first', 'Première'),
    ]

    AVAILABILITY_CHOICES = [
        ('available', 'Disponible'),
        ('limited', 'Limité'),
        ('full', 'Complet'),
    ]

    idVol = models.CharField(
        primary_key=True,
        max_length=10,
        default=generate_custom_vol_id,
        editable=False
    )

    airline = models.CharField(max_length=100)
    flightNumber = models.CharField(max_length=20)

    # Route
    route_from = models.CharField(max_length=100)
    route_to = models.CharField(max_length=100)
    route_fromCode = models.CharField(max_length=10)
    route_toCode = models.CharField(max_length=10)

    # Schedule
    schedule_departure = models.DateTimeField()
    schedule_arrival = models.DateTimeField()
    schedule_duration = models.CharField(max_length=20)

    aircraft = models.CharField(max_length=100)
    flight_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.CharField(max_length=10, choices=AVAILABILITY_CHOICES)

    # Seats
    seats_total = models.IntegerField()
    seats_available = models.IntegerField()

    # Services (liste de chaînes)
    services = models.JSONField(default=list)

    # Baggage
    baggage_carry = models.CharField(max_length=100)
    baggage_checked = models.CharField(max_length=100)

    # Cancellation
    cancellation_flexible = models.BooleanField()
    cancellation_fee = models.DecimalField(max_digits=10, decimal_places=2)

    # Contact
    contact_phone = models.CharField(max_length=20)
    contact_email = models.EmailField()
    contact_website = models.URLField()

    rating = models.FloatField()
    reviews = models.IntegerField()

    lastUsed = models.DateTimeField(null=True, blank=True)
    popularity = models.IntegerField()

    images = models.JSONField(default=list, null=True, blank=True)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.flightNumber} - {self.route_from} → {self.route_to}"

    class Meta:
        db_table = 'vols'
