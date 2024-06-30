from django.contrib import admin

from .models import UserProfile, Role, UserRole

admin.site.register(UserProfile)
admin.site.register(Role)
admin.site.register(UserRole)
