from rest_framework import serializers 
from activites.models import Activite 
 
 
class ActiviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activite
        fields = '__all__'



    description = serializers.JSONField(required=False)
    includes = serializers.JSONField(required=False)     # Éléments inclus (guide, repas, etc.)
    requirements = serializers.JSONField(required=False)
    reviews = serializers.JSONField(required=False)
    seasons = serializers.JSONField(required=False)        # Périodes ou saisons disponibles
    favorite = serializers.JSONField(required=False)
    popularity = serializers.JSONField(required=False)
   