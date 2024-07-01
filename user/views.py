from django.db.utils import OperationalError
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import UserSerializer, RoleSerializer, UserProfileSerializer
from .models import UserProfile, Role, UserRole

# Create your views here.


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    permissions = [('can_add_user', 'Can add user'),
                   ('can_change_user', 'Can change user'),
                   ('can_delete_user', 'Can delete user'),
                   ('can_view_user', 'Can view user')]


class UserProfileRetrieve(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, pk=request.user.id)
            user_profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OperationalError as e:
            response_data = {
                "status": "error",
                "message": "Fallo al obtener el perfil del usuario",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateUserProfile(generics.CreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


class RoleListCreate(generics.ListCreateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Role.objects.all()

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(description=self.request.data.get('description'))
        else:
            return Response({'error': 'You do not have permission to create a role'},
                            status=status.HTTP_403_FORBIDDEN)


class UserRoleView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the role of the authenticated user.
        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: The serialized role data of the user.
        """
        user_role = get_object_or_404(UserRole, user=request.user)
        serializer = RoleSerializer(user_role.role)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RoleDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Role.objects.all()

    def perform_destroy(self, instance):
        instance.delete()

    def delete(self, request, *args, **kwargs):
        role_id = kwargs.get('pk')
        role = get_object_or_404(Role, pk=role_id)
        print(f"Deleting role: {role} with id: {role_id}")
        self.perform_destroy(role)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleUpdate(generics.UpdateAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Role.objects.all()
        else:
            return Role.objects.none()

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(description=self.request.data.get('description'))
        else:
            return Response({'error': 'You do not have permission to update a role'},
                            status=status.HTTP_403_FORBIDDEN)


class RoleRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RoleSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Role.objects.all()
        else:
            return Role.objects.none()

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(description=self.request.data.get('description'))
        else:
            return Response({'error': 'You do not have permission to update a role'},
                            status=status.HTTP_403_FORBIDDEN)

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            instance.delete()
        else:
            return Response({'error': 'You do not have permission to delete a role'},
                            status=status.HTTP_403_FORBIDDEN)
