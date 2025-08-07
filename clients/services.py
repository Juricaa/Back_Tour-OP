from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser # type: ignore
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore

from clients.models import Client
from .serializers import ClientSerializer


from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='post', request_body=ClientSerializer, responses={201: ClientSerializer})
@api_view(['GET', 'POST', 'DELETE'])
def client_list(request):
    if request.method == 'GET':
        clients = Client.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            clients = clients.filter(name__icontains=name)

        serializer = ClientSerializer(clients, many=True)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
       

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@swagger_auto_schema(method='put', request_body=ClientSerializer, operation_description="Met à jour un client")
@swagger_auto_schema(method='delete', operation_description="Supprime un client par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def client_detail(request, pk):
    try:
        client = Client.objects.get(pk=pk)
    except Client.DoesNotExist:
        return JsonResponse({'message': 'Client not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ClientSerializer(client)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ClientSerializer(client, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        client.delete()
        return  JsonResponse(
                {
                    'success': True,
                    'message': 'Vol deleted successfully!'
                 
                 },status=status.HTTP_200_OK)

