from datetime import datetime

from django.db import models

from user.models import UserProfile


class BudgetItem(models.Model):
    recurso = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    valor = models.FloatField(default=float(0))
    presupuesto = models.FloatField(default=float(0))
    proyecto = models.ForeignKey('Proyecto', related_name='budget_items', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.recurso} - {self.categoria}"

class Solicitud(models.Model):
    codigo = models.CharField(max_length=15)
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
            self.codigo = self.generate_codigo(self.tema, self.proyecto)
        super().save(*args, **kwargs)

    def create_codigo(self):
        """
        Creates a unique codigo for the instance by combining the nombre
          of the proyecto and the id of the instance.
        """
        self.codigo = f"{self.proyecto.nombre}-{self.id}"
        self.save()
    class Meta:
        ordering = ['-fecha_creacion']

    def generate_codigo(self, nombre, proyecto):
        """
        Generates a unique code based on the given parameters.

        Parameters:
        - nombre (str): The name of the code.
        - fecha_creacion (datetime): The creation date of the code.
        - proyecto (str): The project associated with the code.

        Returns:
        - str: The generated code in the format "TEM-AAAAMM-000".
        """
        tema_str = nombre[:3].upper()
        fecha_str = datetime.now().strftime('%Y-%m')
        secuencia = self.get_secuencia(proyecto)
        codigo = f"{tema_str}-{fecha_str}-{secuencia:03d}"
        return codigo

    def get_secuencia(self, proyecto):
        """
        Returns the sequence number for a given project.

        Parameters:
        - proyecto: The project for which the sequence number is requested.

        Returns:
        - The sequence number for the project.
        """
        return Solicitud.objects.filter(proyecto=proyecto).count() + 1

class Proyecto(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, default="Nuevo Proyecto")
    fecha_creacion = models.DateField(auto_now_add=True)
    project_budget = models.IntegerField()
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,
                                      related_name='proyectos')

    def __str__(self):
        return f"{self.nombre} - creado el {self.fecha_creacion}"

    class Meta:
        ordering = ['-fecha_creacion']
