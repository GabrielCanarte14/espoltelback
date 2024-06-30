from django.contrib import admin
from django.urls import path, include
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('saludo/', views.saludo, name='saludo'),
    
    path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
    path('api/', include('api.urls')),
    path('api/', include('proyecto.urls')),
    
    path('user/', include('user.urls')),
    
    #ruta con parámetros
    path('numero/<int:num>/', views.numero, name='numero'),
    path('vista/', views.vista, name='vista'),
    path('dinamico/<str:username>', views.dinamico, name='dinamico'),
    path('estaticos/', views.estaticos, name='estaticos'),

    path('herencia/', views.herencia, name='herencia'),
    path('hijo1/', views.hijo1, name='hijo1'),
    path('hijo2/', views.hijo2, name='hijo2'),

    
]
