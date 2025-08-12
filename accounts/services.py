# accounts/views.py
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .serializers import LoginSerializer, RegisterSecretaireSerializer, UserSerializer, UserUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes


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
            try:
                user = User.objects.get(email=email)
                if not user.is_active:
                    return Response({"error": "Votre compte est désactivé. Contactez l'administrateur."}, status=403)
                return Response({"error": "Mot de passe incorrect"}, status=401)
            except User.DoesNotExist:
                return Response({"error": "Identifiants invalides"}, status=401)
                              
        if not user.is_verified:
            return Response({"error": "Votre compte n'est pas encore validé par l'administrateur"}, status=403)

        from django.utils import timezone
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])  
        
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
    

class UserListView(APIView):
    permission_classes = []  # Supprime toutes les restrictions d'authentification
    
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)

class UserDetailView(APIView):
    permission_classes = []  # Aucune permission requise

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=UserUpdateSerializer)
    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({"message": "Utilisateur supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
        

@api_view(['PATCH'])
# @permission_classes([IsAdminUser])
def verify_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
        user.is_verified = True
        user.save()
        return Response({"message": "Utilisateur vérifié avec succès"}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({"error": "Utilisateur non trouvé"}, status=status.HTTP_404_NOT_FOUND)
