from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('roles/', views.RoleListCreate.as_view(), name='roles'),
    path('roles/delete/<int:pk>/', views.RoleDestroy.as_view(), name='delete'),
    path('registro/', views.CreateUserView.as_view(), name='registro'),
    path('rol/',views.UserRoleView.as_view(),name='rol'),

    path('perfil/',views.UserProfileRetrieve.as_view(),name='perfil'),
]
