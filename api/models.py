from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
    
from django.db import models
from django.utils.text import slugify


class Routes(models.Model):
    route_start = models.CharField(max_length=255, verbose_name="route_start")
    route_end = models.CharField(max_length=255, verbose_name="route_end")
    route_url = models.CharField(max_length=255, verbose_name="route_url", unique=True)
    kml_file = models.FileField(upload_to='routes/', null=True, blank=True)
    route_distance = models.FloatField(verbose_name="distance", null=True, blank=True)
    route_duration = models.FloatField(verbose_name="duration", null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")

    owners = models.ManyToManyField(User, related_name="routes")


    def save(self, *args, **kwargs):
        if not self.route_url:
            base_slug = slugify(f"{self.route_start}-{self.route_end}", allow_unicode=True)
            unique_slug = base_slug
            counter = 1
            while Routes.objects.filter(route_url=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.route_url = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.route_start} - {self.route_end}"


     
class RouteSchedules(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, verbose_name="route")
    start_time = models.TimeField(verbose_name="start_time", null=True, blank=True)

class RouteFares(models.Model):
    route = models.ForeignKey(Routes, on_delete=models.CASCADE, verbose_name="route")
    fare_title = models.CharField(max_length=255, verbose_name="fare_title", null=True, blank=True)
    fare = models.FloatField(verbose_name="fare", null=True, blank=True)
    student_fare = models.FloatField(verbose_name="student_fare", null=True, blank=True)