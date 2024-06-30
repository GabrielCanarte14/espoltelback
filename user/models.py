from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100, blank=True)
    name = models.CharField(max_length=100, blank=True)
    cedula = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.user.username
    
    def delete_user(self):
        self.user.delete()

class Role(models.Model):
    description = models.TextField(max_length=500, blank=True)

    class Meta:
        permissions = [
            ('can_view_role', 'Can view role'),
            ('can_change_role', 'Can change role'),
            ('can_delete_role', 'Can delete role'),
            ('can_add_role', 'Can add role'),
        ]
    
    def __str__(self):
        return self.description

class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user.username} - {self.role.description}"
    
    
    def __str__(self):
        return self.user.username
    
