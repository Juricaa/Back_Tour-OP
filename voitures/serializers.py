from rest_framework import serializers 
from voitures.models import Voiture  
 
 
class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = '__all__'


    createdAt = serializers.JSONField(required=False)
    updatedAt = serializers.JSONField(required=False)
    location = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    driverIncluded = serializers.BooleanField(required=False)
    vehicleType = serializers.CharField(required=False)
    brand = serializers.CharField(required=False)
    model = serializers.CharField(required=False)
    capacity = serializers.IntegerField(required=False)
    pricePerDay = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    availability = serializers.ChoiceField(choices=Voiture.AVAILABILITY_CHOICES, required=False)
    image = serializers.ImageField(required=False)

