from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser # type: ignore
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore

from voitures.models import Voiture
from .serializers import VoitureSerializer
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='post', request_body=VoitureSerializer, responses={201: VoitureSerializer})
@api_view(['GET', 'POST', 'DELETE'])
def voiture_list(request):
    if request.method == 'GET':
        voitures = Voiture.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            voitures = voitures.filter(name__icontains=name)

        serializer = VoitureSerializer(voitures, many=True)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
       
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VoitureSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='put', request_body=VoitureSerializer, operation_description="Met à jour un vehicule")
@swagger_auto_schema(method='delete', operation_description="Supprime un vehicule par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def voiture_detail(request, pk):
    try:
        voiture = Voiture.objects.get(pk=pk)
    except Voiture.DoesNotExist:
        return JsonResponse({'message': 'vehicule not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VoitureSerializer(voiture)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
    
    elif request.method == 'PATCH':  # 👈 nouveau
        data = JSONParser().parse(request)
        serializer = VoitureSerializer(voiture, data=data, partial=True)  # 👈 clé ici
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VoitureSerializer(voiture, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        voiture.delete()
        return JsonResponse({'message': 'Vehicule deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)