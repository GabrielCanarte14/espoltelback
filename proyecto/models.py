from django.db import models
from datetime import datetime
from user.models import UserProfile

class BudgetItem(models.Model):
    recurso = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    valor = models.FloatField(default=float(0))
    presupuesto = models.FloatField(default=float(0))
    proyecto = models.ForeignKey('Proyecto', related_name='budget_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} - {self.categoria}"

class Solicitud(models.Model):
    codigo = models.CharField(max_length=15)  #este se hace automatico
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    tema = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    fecha_creacion = models.DateField(auto_now_add=True)
    proyecto = models.ForeignKey('Proyecto', related_name='solicitudes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.codigo} - creado el {self.fecha_creacion}"

    def save(self, *args, **kwargs):
        if not self.codigo:
            self.codigo = self.generate_codigo(self.tema, self.fecha_creacion, self.proyecto)
        super().save(*args, **kwargs)

    def create_codigo(self):
        self.codigo = f"{self.proyecto.nombre}-{self.id}"
        self.save()
    class Meta:
        ordering = ['-fecha_creacion']

    def generate_codigo(self, nombre, fecha_creacion, proyecto):
        # Formato: "TEM-AAAAMM-000"
        tema_str = nombre[:3].upper() # usa las primeras tres letras del tema
        fecha_str = datetime.now().strftime('%Y-%m') # formato de la fecha: AAAAMM
        secuencia = self.get_secuencia(proyecto)
        codigo = f"{tema_str}-{fecha_str}-{secuencia:03d}"
        return codigo

    def get_secuencia(self, proyecto):
        return Solicitud.objects.filter(proyecto=proyecto).count() + 1

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, default="Nuevo Proyecto")
    fecha_creacion = models.DateField(auto_now_add=True)
    project_budget = models.IntegerField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='proyectos')

    def __str__(self):
        return f"{self.nombre} - creado el {self.fecha_creacion}"

    class Meta:
        ordering = ['-fecha_creacion']
