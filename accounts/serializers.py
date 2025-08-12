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
       # Vérification du statut du compte
            if not user.is_active:
                raise serializers.ValidationError(
                    _("Votre compte est désactivé. Contactez l'administrateur."),
                    code='inactive_account'
                )
                
            if not user.is_verified:
                raise serializers.ValidationError(
                    _("Votre compte est en attente de validation par l'administrateur. "
                      "Vous recevrez un email lorsque votre compte sera activé."),
                    code='pending_approval'
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
        fields = ['email', 'name', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        return User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            role='secretary',
            is_verified=False,  # En attente de validation par admin
            is_active=True
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'role', 'is_verified', 'is_active', 'phone', 'last_login']
        read_only_fields = ['id', 'email', 'role']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['role', 'is_verified', 'is_active', 'phone','name', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'phone': {'required': False}
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        standard_fields = ['name', 'phone', 'role', 'is_verified', 'is_active']
        for field in standard_fields:
            if field in validated_data:
                setattr(instance, field, validated_data[field])
    
    
        instance.save()
        return instance