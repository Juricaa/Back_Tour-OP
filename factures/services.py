from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status
from django.http.response import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from .models import Facture
from .serializers import FactureSerializer, FactureSerializerCreated
# from serializersCopy import FactureSerializerS
from clients.models import Client

@swagger_auto_schema(method='post', request_body=FactureSerializerCreated)
@api_view(['GET', 'POST'])
def facture_list(request):
    if request.method == 'GET':
        factures = Facture.objects.select_related('clientId')
        serializer = FactureSerializer(factures, many=True)
        return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = FactureSerializerCreated(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=FactureSerializerCreated)
@swagger_auto_schema(method='delete')
@api_view(['GET', 'PUT', 'DELETE'])
def facture_detail(request, pk):
    try:
        facture = Facture.objects.get(pk=pk)
    except Facture.DoesNotExist:
        return JsonResponse({'message': 'Facture introuvable'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FactureSerializer(facture)
        return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FactureSerializerCreated(facture, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        facture.delete()
        return JsonResponse({'message': 'Facture supprimée'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def montant_total_factures_par_client(request):
    data = []
    clients = Client.objects.all()
    for client in clients:
        factures = Facture.objects.filter(id_client=client)
        total = sum([float(f.montants) for f in factures])
        data.append({
            'client': f"{client.nom} {client.prenom}",
            'total_factures': len(factures),
            'montant_total': total
        })
    return JsonResponse({'success': True, 'data': data}, status=200)

@api_view(['GET'])
def factures_par_client(request, pk):
    try:
        # 1. Vérifie que le client existe
        client = Client.objects.get(pk=pk)
        
        # 2. Récupère toutes ses factures
        factures = Facture.objects.filter(clientId=pk)
        
        # 3. Sérialise les données
        serializer = FactureSerializerCreated(factures, many=True)
        
        return JsonResponse({
            'success': True,
            'client_id': pk,
            'client_name': f"{client.name}",
            'count': factures.count(),
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Client.DoesNotExist:
        return JsonResponse(
            {'success': False, 'message': f'Client ID {pk} introuvable'},
            status=status.HTTP_404_NOT_FOUND
        )