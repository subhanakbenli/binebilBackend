from django.urls import path
from django.urls.conf import include


from . import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),

    
    # path('get_routes/', views.get_routes),
    
    # path('get_schedule/<str:route>/', views.get_schedule),
    # path('edit_schedule/<str:route>', views.edit_time),
    
    path('add_coordinates/<str:route>/', views.add_route_coordinates),
    # path('get_coordinates/<str:route>/', views.get_coordinates),    
    
    path('save_fare/', views.edit_fare),
    # path('get_fare/<str:route>', views.get_fare),
    path('batch_data/', views.batch_request),
    path('batch_data/<str:route_url>/', views.batch_request, name='home_page'),
    # path('<str:route>/', views.get_schedules),
]
# Compare this snippet from api/views.py:
# from django.http import JsonResponse