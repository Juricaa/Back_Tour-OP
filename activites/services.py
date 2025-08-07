from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser # type: ignore
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore

from activites.models import Activite
from .serializers import ActiviteSerializer
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='post', request_body=ActiviteSerializer, responses={201: ActiviteSerializer})
@api_view(['GET', 'POST', 'DELETE'])
def activite_list(request):
    if request.method == 'GET':
        activites = Activite.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            activites = activites.filter(name__icontains=name)

        serializer = ActiviteSerializer(activites, many=True)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
       
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ActiviteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='put', request_body=ActiviteSerializer, operation_description="Met à jour un activite")
@swagger_auto_schema(method='delete', operation_description="Supprime un activite par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def activite_detail(request, pk):
    try:
        activite = Activite.objects.get(pk=pk)
    except activite.DoesNotExist:
        return JsonResponse({'message': 'activite not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ActiviteSerializer(activite)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ActiviteSerializer(activite, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        activite.delete()
        return JsonResponse({'message': 'Activite deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)