from django.db import models

def generate_custom_activite_id():
    last = Activite.objects.order_by('-idActivite').first()
    if last and last.idActivite.startswith("ACT"):
        number = int(last.idActivite[3:]) + 1
    else:
        number = 1
    return f"ACT{number:04d}"


class Activite(models.Model):
    DIFFICULTY_CHOICES = [
        ('facile', 'Facile'),
        ('moyenne', 'Moyenne'),
        ('difficile', 'Difficile'),
    ]

    idActivite = models.CharField(
        primary_key=True,
        max_length=10,
        default=generate_custom_activite_id,
        editable=False
    )
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    priceAdult = models.DecimalField(max_digits=10, decimal_places=2)
    priceGuide = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Groupe taille minimale et maximale
    groupSizeMin = models.PositiveIntegerField()
    groupSizeMax = models.PositiveIntegerField()
    
    description = models.TextField()
    includes = models.JSONField(default=list)       # Éléments inclus (guide, repas, etc.)
    requirements = models.JSONField(default=list)   # Pré-requis pour participer
    guideRequired = models.BooleanField()
    guideName = models.CharField(max_length=100, blank=True, null=True)
    guidePhone = models.CharField(max_length=50, blank=True, null=True)
    
    rating = models.FloatField()
    reviews = models.PositiveIntegerField()
    seasons = models.JSONField(default=list)        # Périodes ou saisons disponibles
    favorite = models.BooleanField(default=False)
    popularity = models.PositiveIntegerField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activites'
