from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Hebergement
from .serializers import HebergementSerializer

from drf_yasg.utils import swagger_auto_schema

@swagger_auto_schema(method='post', request_body=HebergementSerializer) # type: ignore
@api_view(['GET', 'POST', 'DELETE'])
def hebergement_list(request):
    # GET ALL
    if request.method == 'GET':
        hebergements = Hebergement.objects.all()
        lookup_field = 'idHebergement' 
        
        name = request.GET.get('name', None)
        if name is not None:
            hebergements = hebergements.filter(name__icontains=name)
            
        location = request.GET.get('location', None)
        if location is not None:
            hebergements = hebergements.filter(location__icontains=location)
            
        type_heb = request.GET.get('type', None)
        if type_heb is not None:
            hebergements = hebergements.filter(type__iexact=type_heb)

        serializer = HebergementSerializer(hebergements, many=True)
        return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)

    # CREATE
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = HebergementSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(
                {
                    'success': True,
                    'data': serializer.data
                 
                 },status=status.HTTP_200_OK)
        print(serializer.errors) 
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE ALL
    elif request.method == 'DELETE':
        count = Hebergement.objects.all().delete()
        return JsonResponse(
            {'message': f'{count[0]} hebergements deleted successfully!'},
            status=status.HTTP_204_NO_CONTENT
        )
@swagger_auto_schema(method='put', request_body=HebergementSerializer, operation_description="Met à jour un client") # type: ignore
@swagger_auto_schema(method='delete', operation_description="Supprime un hebergment par ID") # type: ignore
@api_view(['GET', 'PUT', 'DELETE'])
def hebergement_detail(request, pk):
    try:
        hebergement = Hebergement.objects.get(pk=pk)
    except Hebergement.DoesNotExist:
        return JsonResponse(
            {'message': 'Hebergement not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

    # GET ONE
    if request.method == 'GET':
        serializer = HebergementSerializer(hebergement)
        return JsonResponse(serializer.data)

    # UPDATE
    elif request.method == 'PUT':
        serializer = HebergementSerializer(hebergement, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
            {
                'success': True,
                'message': 'Hebergement deleted successfully!'
            }, 
            status=status.HTTP_200_OK
        )
            
        return Response(
            {
                'success': True,
                'errors': serializer.errors
            }, 
            status=status.HTTP_400_BAD_REQUEST
        )
    # DELETE
    
    elif request.method == 'DELETE':
        hebergement.delete()
        return JsonResponse(
            {'message': 'Hebergement deleted successfully!'}, 
            status=status.HTTP_204_NO_CONTENT
        )