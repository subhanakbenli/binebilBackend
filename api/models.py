from django.db import models
from django.contrib.auth.models import User

    
class Routes(models.Model):
    route = models.CharField(max_length=255, verbose_name="route", unique=True)
    route_url = models.CharField(max_length=255, verbose_name="route_url", unique=True)
    coordinates = models.TextField(verbose_name="coordinates", blank=True, null=True) 
    
    route_distance = models.FloatField(verbose_name="distance", null=True, blank=True)
    route_duration = models.FloatField(verbose_name="duration", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")
    
    def __str__(self):
        return self.route

class RouteCoordinates(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, verbose_name="route")
    node_number = models.IntegerField(verbose_name="node_number", unique=True)
    latitude = models.FloatField(verbose_name="latitude", null=True, blank=True)
    longitude = models.FloatField(verbose_name="longitude", null=True, blank=True)
     
class RouteSchedules(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, verbose_name="route")
    start_time = models.DateTimeField(verbose_name="start_time", null=True, blank=True)

class RouteFares(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, verbose_name="route")
    fare_title = models.CharField(max_length=255, verbose_name="fare_title", null=True, blank=True)
    fare = models.FloatField(verbose_name="fare", null=True, blank=True)
    student_fare = models.FloatField(verbose_name="student_fare", null=True, blank=True)