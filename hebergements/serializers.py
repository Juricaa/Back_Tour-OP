from rest_framework import serializers
from .models import Hebergement

class HebergementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hebergement
        fields = '__all__'

    amenities = serializers.JSONField(required=False)
    rating = serializers.FloatField(required=False)
    popularity= serializers.IntegerField(required=False)
    description = serializers.CharField(required=False, allow_blank=True)