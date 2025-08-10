# accounts/views.py
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegisterSecretaireSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view




class RegisterSecretaireView(APIView):
    @swagger_auto_schema(request_body=RegisterSecretaireSerializer)
    def post(self, request):
        serializer = RegisterSecretaireSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Compte créé. En attente de validation par l’administrateur."}, status=201)
        return Response(serializer.errors, status=400)


class LoginView(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Identifiants invalides"}, status=401)
        if not user.is_verified:
            return Response({"error": "Votre compte n'est pas encore validé par l'administrateur"}, status=403)

        refresh = RefreshToken.for_user(user)
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "name": user.name,
                "role": user.role
            }
        })
