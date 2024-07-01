from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Role, UserProfile, UserRole

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password']
        extra_kwargs = {'password': {'write_only': True,
                                     'required': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','user', 'email', 'name', 'cedula', 'is_active']
        extra_kwargs = {'id': {'read_only': True},
                        'user': {'required': True},
                        'email': {'required': True},
                        'name': {'required': True},
                        'cedula': {'required': True},
                        'is_active': {'required': True},
                        }

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'description']
        extra_kwargs = {'description': {'required': True}}

class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['user', 'role']
        extra_kwargs = {'role': {'required': True},
                        'user': {'required': True}}
        