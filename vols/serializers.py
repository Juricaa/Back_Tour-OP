from rest_framework import serializers 
from vols.models import Vol
class VolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vol
        fields = '__all__'

images = serializers.JSONField(required=False)  
lastUsed = serializers.DateTimeField(required=False)
schedule_departure = serializers.JSONField(required=False)
schedule_arrival = serializers.JSONField(required=False)
schedule_duration = serializers.JSONField(required=False)

seats_total = serializers.IntegerField(required=False)
seats_available = serializers.IntegerField(required=False)
cancellation_flexible = serializers.BooleanField(required=False)
cancellation_fee = serializers.DecimalField(
    max_digits=10, decimal_places=2, required=False
)

availability = serializers.JSONField(required=False)
