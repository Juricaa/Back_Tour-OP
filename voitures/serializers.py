from rest_framework import serializers 
from voitures.models import Voiture  
 
 
class VoitureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voiture
        fields = '__all__'


    createdAt = serializers.JSONField(required=False)