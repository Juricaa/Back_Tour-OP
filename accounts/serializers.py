# accounts/serializers.py
from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                username=email, password=password)
            if not user:
                raise serializers.ValidationError(
                    _("Email ou mot de passe incorrect."),
                    code='authorization'
                )
        else:
            raise serializers.ValidationError(
                _("Veuillez fournir l'email et le mot de passe."),
                code='authorization'
            )

        attrs['user'] = user
        return attrs


class RegisterSecretaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'name', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            role='secretaire',
            is_verified=False,  # En attente de validation par admin
            is_active=True
        )
