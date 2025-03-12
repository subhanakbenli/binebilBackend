from django.utils.text import slugify
from api.models import Routes, RouteCoordinates, RouteSchedules, RouteFares

# 1. Güzergah Ekle
route = Routes.objects.create(
    route_start="İYTE",
    route_end="Faltay",
    route_distance=12.5,  # Örnek mesafe (km)
    route_duration=30.0   # Örnek süre (dakika)
)

# 2. Koordinatları Ekle
coordinates = [
    (38.3226, 26.6397),  # İYTE Başlangıç
    (38.3235, 26.6408),
    (38.3400, 26.6500),
    (38.3500, 26.6600),
    (38.3610, 26.6700)   # Faltay Bitiş
]

for i, (lat, lon) in enumerate(coordinates, start=1):
    RouteCoordinates.objects.create(
        route=route,
        node_number=i,
        latitude=lat,
        longitude=lon
    )

# 3. Sefer Saatleri Ekle
schedules = ["08:00", "12:00", "16:00", "18:00"]

for time in schedules:
    RouteSchedules.objects.create(
        route=route,
        start_time=time
    )

# 4. Ücret Bilgilerini Ekle
RouteFares.objects.create(
    route=route,
    fare_title="Tam Ücret",
    fare=20.0,
    student_fare=15.0
)

print("İYTE - Faltay güzergahı eklendi!")
