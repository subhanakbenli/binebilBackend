from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Routes, RouteCoordinates, RouteFares, RouteSchedules
import ast
from .permissions import IsRouteOwner

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)
    if user:
        django_login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'message': 'Login successful'}, status=status.HTTP_200_OK)
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    django_logout(request)
    return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsRouteOwner])  # İzin eklenmiş hali
def save_fares(request):
    data = request.data
    route_url = data.get('route_url')
    
    try:
        related_route = Routes.objects.get(route_url=route_url)
        
        # Kullanıcı bu güzergahı düzenleyebilir mi kontrol et
        if not IsRouteOwner().has_object_permission(request, None, related_route):
            return Response({'error': 'You do not have permission to edit this route'}, status=status.HTTP_403_FORBIDDEN)
        
        for fare_data in data.get('fares', []):
            fare_id = fare_data.get('id')
            fare_title = fare_data.get('fare_title')
            fare = fare_data.get('fare')
            student_fare = fare_data.get('student_fare')

            if fare_id is None or fare_title is None:
                continue

            route_fare, created = RouteFares.objects.get_or_create(
                id=fare_id,
                defaults={'route': related_route, 'fare_title': fare_title, 'fare': fare, 'student_fare': student_fare}
            )

            if not created:
                route_fare.fare_title = fare_title
                route_fare.fare = fare
                route_fare.student_fare = student_fare
                route_fare.save()

        return Response({'message': 'edit_fare'}, status=status.HTTP_200_OK)
    
    except Routes.DoesNotExist:
        return Response({'error': 'Route not found'}, status=status.HTTP_404_NOT_FOUND)



@api_view(['DELETE'])
@permission_classes([IsAuthenticated, IsRouteOwner])  
def delete_fare(request):
    try:
        deleted_id = request.query_params.get('deleted_id')  # DELETE için query parametresinden al
        if not deleted_id:
            return Response({'error': 'deleted_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        related_fare = RouteFares.objects.get(id=deleted_id)

        if not IsRouteOwner().has_object_permission(request, None, related_fare.route):
            return Response({'error': 'You do not have permission to edit this route'}, status=status.HTTP_403_FORBIDDEN)

        related_fare.delete()
        return Response({'message': 'Fare deleted successfully'}, status=status.HTTP_200_OK)

    except RouteFares.DoesNotExist:
        return Response({'error': 'Fare not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated,IsRouteOwner])  # Changed to IsAuthenticated
def save_schedules(request):
    data = request.data
    # {'route_url': '', 'schedule': [{'id': 1741427314012, 'start_time': '14:14', 'plate': '1414'}]}
    route_url = data.get("route_url")
    related_route = Routes.objects.get(route_url=route_url)
    if not IsRouteOwner().has_object_permission(request, None, related_route):
        return Response({'error': 'You do not have permission to edit this route'}, status=status.HTTP_403_FORBIDDEN)
    for schedule_data in data.get("schedule",[]):
        sch_id = schedule_data.get('id')
        start_time = schedule_data.get('start_time')
        schedule , created = RouteSchedules.objects.get_or_create(
            id = sch_id,
            defaults = {"route":related_route,"start_time":start_time}
            )
        if not created:
            schedule.start_time=start_time
            schedule.save()    
    return Response({'message': 'Schedule saved'}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated,IsRouteOwner])  # Changed to IsAuthenticated
def delete_schedule(request):
    try:
        deleted_id = request.query_params.get('deleted_id')  # DELETE için query parametresinden al
        if not deleted_id:
            return Response({'error': 'deleted_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        related_schedule = RouteSchedules.objects.get(id=deleted_id)
        
        if not IsRouteOwner().has_object_permission(request, None, related_schedule.route):
            return Response({'error': 'You do not have permission to edit this route'}, status=status.HTTP_403_FORBIDDEN)
        
        related_schedule.delete()
        return Response({'message': 'Schedule deleted successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])  # Changed to IsAuthenticated
def add_route_coordinates(request,route_url):
    try:
        if request.method == 'GET':
            return Response({'message': 'Send POST request to add coordinates'}, status=status.HTTP_200_OK)
        with open('coordinates.txt', 'r') as f:
            coordinates = f.read()

        coordinates_list = ast.literal_eval(coordinates)

        route = Routes.objects.create(route_url=route_url)
        for i, (latitude, longitude) in enumerate(coordinates_list):
            RouteCoordinates.objects.create(route=route, node_number=i, latitude=latitude, longitude=longitude)

        return Response({'message': 'Coordinates added successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
@permission_classes([AllowAny])  # Reading data can remain public
def batch_request(request):
    try:
        data = request.data
        route_url = data.get('route_url')
        response = {}
        if 'routes' in data:
            print('routes')
            response['routes'] = _get_all_routes()
        if route_url != None and route_url != '':
            route = Routes.objects.get(route_url=route_url)
            
            if 'schedules' in data:
                response['schedules'] = _get_schedule(route = route)
            if 'fares' in data:
                response['fares'] = _get_fare(route = route)

            if 'coordinates' in data:
                response['coordinates'] = _get_coordinates(route = route)
            if 'routeInfo' in data:
                response['routeInfo'] = _get_route_info(route = route)
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny]) 
def routes_with_info(request):
    try:
        response = []
        routes = Routes.objects.all()
        for route in routes:
            route_dict = {
                'route_id' : route.id,
                'route_start': route.route_start,
                'route_end': route.route_end,   
                'route_url': route.route_url,
                'route_distance' : route.route_distance,
                'route_duration' : route.route_duration,
            }
            response.append(route_dict)    
        return Response(response, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # İzin eklenmiş hali
def add_route(request):
    try:
        data = request.data
        route_start = data.get('route_start')
        route_end = data.get('route_end')
        route_distance = data.get('route_distance')
        route_duration = data.get('route_duration')
        
        route = Routes.objects.create(route_start=route_start, route_end=route_end, route_distance=route_distance, route_duration=route_duration)
        return Response({'message': 'Route added successfully', 'route_url': route.route_url}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


def _get_all_routes():
    routes = list(Routes.objects.values('id','route_start','route_end','route_url'))
    print(routes)
    return routes


def _get_schedule(route):
    try:
        return list(RouteSchedules.objects.filter(route=route).values('id','start_time').order_by('start_time'))
    except ObjectDoesNotExist:
        return []


def _get_coordinates(route):
    try:
        return list(RouteCoordinates.objects.filter(route=route).values_list('latitude', 'longitude'))
    except ObjectDoesNotExist:
        return []


def _get_fare(route):
    try:
        return list(RouteFares.objects.filter(route=route).values('id','fare_title','fare','student_fare'))
    except ObjectDoesNotExist:
        return []


def _get_route_info(route):
    try:
        return {'route_start': route.route_start, 'route_end': route.route_end, 'route_distance': route.route_distance, 'route_duration': route.route_duration}
    except ObjectDoesNotExist:
        return {"route_start": "","route_end": "","route_distance": 0,"route_duration": 0}