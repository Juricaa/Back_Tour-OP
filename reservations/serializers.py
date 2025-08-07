from rest_framework import serializers 
from reservations.models import Reservation 
 
 
class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'



    # lieu_depart= serializers.JSONField(required=False)
    # lieu_arrivee = serializers.JSONField(required=False)    
   