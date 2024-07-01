from django.urls import path
from . import views

urlpatterns = [
    path('proyectos/', views.ProyectoListCreateAPIView.as_view(), name='proyecto-list-create'),
    path('proyectos/<int:pk>/', views.ProyectoDetailAPIView.as_view(), name='proyecto-detail'),
    path('proyectos/<int:proyecto_id>/items/', views.BudgetItemCreateAPIView.as_view(),
          name='crear-budget-items'),
    path('solicitudes/', views.SolicitudListAPIView.as_view(), name='lista-solicitudes'),
    path('solicitudes/<int:pk>/', views.SolicitudDetailAPIView.as_view(), name='detalle-solicitud'),
    path('proyectos/<int:proyecto_id>/solicitud/', views.SolicitudCreateAPIView.as_view(),
          name='crear-solicitud'),
]
