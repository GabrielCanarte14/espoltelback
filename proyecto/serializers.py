from rest_framework import serializers
from .models import Proyecto, BudgetItem, Solicitud

class BudgetItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetItem
        fields = ['id', 'recurso', 'categoria', 'cantidad', 'valor', 'presupuesto', 'proyecto']

    def create(self, validated_data):
        return BudgetItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.recurso = validated_data.get('recurso', instance.recurso)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.cantidad = validated_data.get('cantidad', instance.cantidad)
        instance.valor = validated_data.get('valor', instance.valor)
        instance.presupuesto = validated_data.get('presupuesto', instance.presupuesto)
        instance.proyecto = validated_data.get('proyecto', instance.proyecto)
        instance.save()
        return instance

class SolicitudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solicitud
        fields = ['id', 'codigo', 'nombre', 'tema', 'tipo', 'estado', 'fecha_creacion', 'proyecto']
        read_only_fields = ['id', 'fecha_creacion', 'codigo']

    def create(self, validated_data):
        return Solicitud.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.tema = validated_data.get('tema', instance.tema)
        instance.tipo = validated_data.get('tipo', instance.tipo)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.proyecto = validated_data.get('proyecto', instance.proyecto)
        instance.save()
        return instance

class ProyectoSerializer(serializers.ModelSerializer):
    budget_items = BudgetItemSerializer(many=True)

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre', 'fecha_creacion', 'project_budget', 'budget_items','user_profile']
        read_only_fields = ['id', 'fecha_creacion']

    def create(self, validated_data):
        budget_items_data = validated_data.pop('budget_items', [])
        proyecto = Proyecto.objects.create(**validated_data)
        for item_data in budget_items_data:
            BudgetItem.objects.create(proyecto=proyecto, **item_data)
        return proyecto

    def update(self, instance, validated_data):
        instance.nombre = validated_data.get('nombre', instance.nombre)
        instance.presupuesto = validated_data.get('presupuesto', instance.presupuesto)

        instance.save()
        return instance
