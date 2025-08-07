from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser # type: ignore
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view # type: ignore

from vols.models import Vol
from .serializers import VolSerializer
from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='post', request_body=VolSerializer, responses={201: VolSerializer})
@api_view(['GET', 'POST', 'DELETE'])
def vol_list(request):
    if request.method == 'GET':
        vols = Vol.objects.all()

        name = request.GET.get('name', None)
        if name is not None:
            vols = vols.filter(name__icontains=name)

        serializer = VolSerializer(vols, many=True)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
       
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = VolSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@swagger_auto_schema(method='put', request_body=VolSerializer, operation_description="Met à jour un vol")
@swagger_auto_schema(method='delete', operation_description="Supprime un vol par ID")
@api_view(['GET', 'PUT', 'DELETE'])
def vol_detail(request, pk):
    try:
        vol = Vol.objects.get(pk=pk)
    except Vol.DoesNotExist:
        return JsonResponse({'message': 'Vol not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VolSerializer(vol)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = VolSerializer(vol, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        vol.delete()
        return JsonResponse({'message': 'Vol deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)