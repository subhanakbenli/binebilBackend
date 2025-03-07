from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Routes, RouteCoordinates, RouteFares, RouteSchedules
import ast


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
@permission_classes([AllowAny])
def edit_fare(request):
    # {'fares': [{'fare_title': 'bamboo', 'fare': '5', 'student_fare': 30}, {'fare_title': 'iyte', 'fare': 75, 'student_fare': 50}]}
    
    data = request.data
    print(data)
    route = Routes.objects.get(route_url=data['route_url'])
    for title, fare, student_fare in data['fares']:
        route_fare =RouteFares.objects.get_or_create(route=route, fare_title=title)
        burada kladım buraya eklemem gerekn şey fareyi id ile sçemek 
        route_fare.fare_title=title 
        route_fare.fare=title 
        route_fare.student_fare=title 
        route_fare.save()
    return Response({'message': 'edit_fare'}, status=status.HTTP_200_OK)



@api_view(['GET'])
@permission_classes([AllowAny])
def get_schedules(request, route):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def edit_schedule(request):
    return Response({'message': 'edit_time'}, status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
@permission_classes([AllowAny])
def add_route_coordinates(request,route):
    try:
        if request.method == 'GET':
            return Response({'message': 'Send POST request to add coordinates'}, status=status.HTTP_200_OK)
        with open('coordinates.txt', 'r') as f:
            coordinates = f.read()

        coordinates_list = ast.literal_eval(coordinates)

        route = Routes.objects.create(route=route)
        for i, (latitude, longitude) in enumerate(coordinates_list):
            RouteCoordinates.objects.create(route=route, node_number=i, latitude=latitude, longitude=longitude)

        return Response({'message': 'Coordinates added successfully'}, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
def batch_request(request, route_url="route-deneme"):
    try:
        data = request.data
        response = {}
        route = Routes.objects.get(route_url=route_url)
        if 'routes' in data:
            response['routes'] = _get_all_routes()
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


def _get_all_routes():
    routes = list(Routes.objects.values('route','route_url'))
    print(routes)
    return routes
def _get_schedule(route):
    try:
        route_obj = Routes.objects.get(route=route)
        
        return RouteSchedules.objects.filter(route=route_obj).values_list('start_time',flat=True)

    except ObjectDoesNotExist:
        return []

def _get_coordinates(route):
    try:
        route_id = Routes.objects.values_list('id', flat=True).get(route=route)
        return list(RouteCoordinates.objects.filter(route_id=route_id).values_list('latitude', 'longitude'))
    except ObjectDoesNotExist:
        return []


def _get_fare(route):
    try:
        route_obj = Routes.objects.get(route=route)
        return list(RouteFares.objects.filter(route=route_obj).values('fare_title','fare','student_fare'))
    except ObjectDoesNotExist:
        return []

def _get_route_info(route):
    try:
        route_obj = Routes.objects.get(route=route)
        route_distance = route_obj.route_distance
        route_duration = route_obj.route_duration
        return {'route_distance': route_distance, 'route_duration': route_duration}
    except ObjectDoesNotExist:
        return {'route_distance': None, 'route_duration': None}

