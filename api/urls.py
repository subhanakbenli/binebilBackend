from django.urls import path
from django.urls.conf import include


from . import views

urlpatterns = [
    path('login/', views.login),
    path('logout/', views.logout),
    
    path('save_fares/', views.save_fares),
    path('delete_fare/', views.delete_fare),
    
    path('save_schedule/', views.save_schedules),
    path('delete_schedule/', views.delete_schedule),
    
    path('batch_data/', views.batch_request),
    
    path('all_routes/' , views.routes_with_info ),
    path('save_route/', views.save_route)
]
