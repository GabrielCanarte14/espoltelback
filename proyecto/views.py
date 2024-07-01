from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BudgetItem, Proyecto, Solicitud
from .serializers import (BudgetItemSerializer, ProyectoSerializer,
                          SolicitudSerializer)


class ProyectoListCreateAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            proyectos = Proyecto.objects.all()
            if proyectos.exists():
                serializer = ProyectoSerializer(proyectos, many=True)
                response_data = {
                    "status": "success",
                    "message": "Proyectos devueltos con éxito",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "success",
                    "message": "No hay proyectos creados",
                    "data": []
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Fallo en la consulta",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = ProyectoSerializer(data=request.data)
            if serializer.is_valid():
                proyecto = serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Proyecto creado exitosamente",
                    "data": {
                        "id": proyecto.id
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear el proyecto, error del serializer",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear el proyecto, error del servidor",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#GET de todos los proyectos existentes
class ProyectoListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            proyectos = Proyecto.objects.all()
            if proyectos.exists():
                serializer = ProyectoSerializer(proyectos, many=True)
                response_data = {
                    "status": "success",
                    "message": "Proyectos devueltos con éxito",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "success",
                    "message": "No hay proyectos creados",
                    "data": []
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Fallo en la consulta",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class BudgetItemCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, proyecto_id):
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except Proyecto.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el proyecto con id {proyecto_id}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            budget_items_data = request.data.get('budget_items', [])
            errors = []
            for item_data in budget_items_data:
                item_data['proyecto'] = proyecto_id 
                serializer = BudgetItemSerializer(data=item_data)
                if serializer.is_valid():
                    serializer.save()
                else:
                    errors.append(serializer.errors)
            
            if errors:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear uno o más budget_items",
                    "errors": errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            else:
                response_data = {
                    "status": "success",
                    "message": "Budget_items creados exitosamente para el proyecto",
                    "data": {
                        "proyecto_id": proyecto_id
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear los budget_items",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProyectoDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer

#para un futuro detail del item de un proyecto, por ahora muestra todos
class BudgetItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = BudgetItem.objects.all()
    serializer_class = BudgetItemSerializer

#crear una solicitud de un proyecto YA EXISTENTE
class SolicitudCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = SolicitudSerializer
    def post(self, request, proyecto_id):
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except Proyecto.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el proyecto con id {proyecto_id}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            request.data['proyecto'] = proyecto.id
            serializer = SolicitudSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "status": "success",
                    "message": "Solicitud creada exitosamente",
                    "data": {
                        "proyecto_id": proyecto_id,
                        "solicitud_id": serializer.data['id'],
                        "codigo": serializer.data['codigo']
                    }
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "status": "error",
                    "message": "No se pudo crear la solicitud, error del serializer",
                    "errors": serializer.errors
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "No se pudo crear la solicitud",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#GET de todas las solicitudes de todos los proyectos
class SolicitudListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        try:
            solicitudes = Solicitud.objects.all()
            if solicitudes.exists():
                serializer = SolicitudSerializer(solicitudes, many=True)
                response_data = {
                    "status": "success",
                    "message": "Solicitudes devueltas con éxito",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "success",
                    "message": "No hay solicitudes creadas",
                    "data": []
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Fallo en la consulta",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#GET de una solicitud con su id
class SolicitudDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Solicitud.objects.all()
    serializer_class = SolicitudSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        solicitud = self.get_object_or_404(Solicitud, pk=kwargs.get('pk'))
        serializer = SolicitudSerializer(solicitud)
        return Response(serializer.data, status=status.HTTP_200_OK)

#GET de todas las solicitudes por proyecto
class SolicitudByProyectoListAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, proyecto_id):
        try:
            proyecto = Proyecto.objects.get(id=proyecto_id)
        except Proyecto.DoesNotExist:
            response_data = {
                "status": "error",
                "message": f"No se encontró el proyecto con id {proyecto_id}"
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        
        try:
            solicitudes = Solicitud.objects.filter(proyecto=proyecto)
            if solicitudes.exists():
                serializer = SolicitudSerializer(solicitudes, many=True)
                response_data = {
                    "status": "success",
                    "message": "Solicitudes devueltas con éxito",
                    "data": serializer.data
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                response_data = {
                    "status": "success",
                    "message": "No hay solicitudes creadas para este proyecto",
                    "data": []
                }
                return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            response_data = {
                "status": "error",
                "message": "Fallo en la consulta",
                "error": str(e)
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
