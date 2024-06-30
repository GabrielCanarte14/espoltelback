from django.contrib import admin

from .models import BudgetItem, Solicitud, Proyecto

admin.site.register(BudgetItem)
admin.site.register(Solicitud)
admin.site.register(Proyecto)
