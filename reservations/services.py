import datetime
from django.db import connection
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.contenttypes.models import ContentType
from drf_yasg.utils import swagger_auto_schema
from .models import Reservation
from .serializers import ReservationSerializer
from clients.models import Client
from django.db.models import Q
from factures.models import Facture
from vols.models import Vol
from hebergements.models import Hebergement
from voitures.models import Voiture
from activites.models import Activite
from rest_framework.response import Response

from django.http import JsonResponse
from datetime import datetime

@swagger_auto_schema(method='post', request_body=ReservationSerializer)
@api_view(['GET', 'POST'])
def reservation_list(request):
    if request.method == 'GET':
        reservations = Reservation.objects.select_related('id_client')
        serializer = ReservationSerializer(reservations, many=True)
        return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ReservationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='put', request_body=ReservationSerializer)
@swagger_auto_schema(method='delete')
@api_view(['GET', 'PUT', 'DELETE'])
def reservation_detail(request, pk):
    try:
        reservation = Reservation.objects.get(pk=pk)
    except Reservation.DoesNotExist:
        return JsonResponse({'message': 'Réservation introuvable'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ReservationSerializer(reservation)
        return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)

        # Calcul du montant
        from datetime import datetime
        date_debut = datetime.strptime(data['date_debut'], '%Y-%m-%d').date()
        date_fin = datetime.strptime(data['date_fin'], '%Y-%m-%d').date()
        quantite = int(data.get('quantite', 1))
        nb_jours = (date_fin - date_debut).days
        montant = nb_jours * quantite
        data['montant'] = montant

        serializer = ReservationSerializer(reservation, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        reservation.delete()
        return JsonResponse({'message': 'Réservation supprimée'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['DELETE'])
def supprimer_reservations_client_periode(request, client_id):
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    # Validation des paramètres
    if not date_debut or not date_fin:
        return Response(
            {'error': 'Les paramètres date_debut et date_fin sont requis'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        datetime.strptime(date_debut, '%Y-%m-%d')
        datetime.strptime(date_fin, '%Y-%m-%d')
    except ValueError:
        return Response(
            {'error': 'Format de date invalide. Utilisez YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Récupération et suppression
    reservations = Reservation.objects.filter(
        id_client_id=client_id,
        date_debut__gte=date_debut,
        date_fin__lte=date_fin
    )
    
    count = reservations.count()
    reservations.delete()
    
    return Response({
        'success': True,
        'message': f'{count} réservation(s) supprimée(s)',
        'client_id': client_id,
        'periode': f'{date_debut} à {date_fin}'
    }, status=status.HTTP_200_OK)

@api_view(['GET'])
def reservation_total_par_client(request):
    data = []
    clients = Client.objects.all()
    for client in clients:
        reservations = Reservation.objects.filter(client=client)
        total = sum([res.montant for res in reservations])
        data.append({
            'client': f"{client.nom} {client.prenom}",
            'total_reservations': len(reservations),
            'montant_total': total
        })
    return JsonResponse({'success': True, 'data': data}, status=200)




@api_view(['GET'])

# def reservations_par_client_et_periode(request, client_id):
#     try:
#         factures = Facture.objects.filter(clientId_id=client_id)
#         reservations = Reservation.objects.filter(id_client_id=client_id)

#         results = []

#         for res in reservations:
#             for facture in factures:
#                 if res.date_debut >= facture.dateTravel and res.date_fin <= facture.dateReturn:
#                     # Récupérer l'objet lié dynamiquement
#                     try:
#                         model_class = res.content_type.model_class()
#                         related_object = model_class.objects.get(pk=res.object_id)
#                         related_data = related_object.__dict__
#                         related_data.pop("_state", None)
#                     except Exception:
#                         related_data = {}

#                     results.append({
#                         'reservation': ReservationSerializer(res).data,
#                         'objet_reserve': related_data
#                     })

#         return JsonResponse({'success': True, 'data': results}, status=200)

#     except Exception as e:
#         return JsonResponse({'success': False, 'error': str(e)}, status=500)




def reservations_par_client_et_periode(request, client_id):
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    
    
    if not date_debut or not date_fin:
        return JsonResponse({'error': 'Les paramètres date_debut et date_fin sont requis'}, status=400)
    
    try:
        datetime.strptime(date_debut, '%Y-%m-%d')
        datetime.strptime(date_fin, '%Y-%m-%d')
    except ValueError:
        return JsonResponse({'error': 'Format de date invalide. Utilisez YYYY-MM-DD'}, status=400)
    
    # Récupérer les réservations
    reservations = Reservation.objects.filter(
        id_client_id=client_id,
        date_debut__gte=date_debut,
        date_fin__lte=date_fin
    )
    
    # Préparer les données
    results = []
    
    # Récupérer tous les IDs par type
    hebergement_ids = [r.object_id for r in reservations if r.type == 'hebergement']
    voiture_ids = [r.object_id for r in reservations if r.type == 'voiture']
    activite_ids = [r.object_id for r in reservations if r.type == 'activité']
    vol_ids = [r.object_id for r in reservations if r.type == 'vol']
    
    # Charger tous les objets en une seule requête par type
    hebergements = {h.idHebergement: h for h in Hebergement.objects.filter(idHebergement__in=hebergement_ids)}
    voitures = {v.idVoiture: v for v in Voiture.objects.filter(idVoiture__in=voiture_ids)}
    activites = {a.idActivite: a for a in Activite.objects.filter(idActivite__in=activite_ids)}
    vols = {v.idVol: v for v in Vol.objects.filter(idVol__in=vol_ids)}
    
    for reservation in reservations:
        item_data = None
        
        if reservation.type == 'hebergement' and reservation.object_id in hebergements:
            h = hebergements[reservation.object_id]
            item_data = {
                'type': 'hebergement',
                'id': h.idHebergement,
                'name': h.name,
                'location': h.location,
                'priceRange': h.priceRange,
                'capacity': h.capacity,
                'phone': h.phone,
                'form': h.type
            }
        
        elif reservation.type == 'voiture' and reservation.object_id in voitures:
            v = voitures[reservation.object_id]
            item_data = {
                'type': 'voiture',
                'id': v.idVoiture,
                'brand': v.brand,
                'model': v.model,
                'pricePerDay': v.pricePerDay,
                'vehicleType': v.vehicleType,
                'description': v.description,
                'driverIncluded': v.driverIncluded,
                'driverName': v.driverName,
                'driverPhone': v.driverPhone,

            }
        
        elif reservation.type == 'activité' and reservation.object_id in activites:
            a = activites[reservation.object_id]
            item_data = {
                'type': 'activite',
                'id': a.idActivite,
                'name': a.name,
                'category': a.category,
                'priceAdult': a.priceAdult,
                'priceGuide': a.priceGuide,
                'duration': a.duration,
                'guideRequired': a.guideRequired,
                'guideName': a.guideName,
                'guidePhone': a.guidePhone,
            }
        
        elif reservation.type == 'vol' and reservation.object_id in vols:
            v = vols[reservation.object_id]
            item_data = {
                'type': 'vol',
                'id': v.idVol,
                'airline': v.airline,
                'flightNumber': v.flightNumber,
                'route_from': v.route_from,
                'route_to': v.route_to,
                'price': v.price,
                'classType': v.flight_class,
            }
        
        results.append({
            'idReservation': reservation.idReservation,
            'date_debut': reservation.date_debut.strftime('%Y-%m-%d'),
            'date_fin': reservation.date_fin.strftime('%Y-%m-%d'),
            'lieu_depart': reservation.lieu_depart,
            'lieu_arrivee': reservation.lieu_arrivee,   
            'quantite': reservation.quantite,
            'montant': str(reservation.montant),
            'item': item_data
        })
    
    return JsonResponse({'success': True, 'data': results}, safe=False)
