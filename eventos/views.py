from django.shortcuts import render
from rest_framework import status, filters, generics, viewsets, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework.views import APIView 


from .models import Escultores, Eventos, Obras, Votaciones, User
from .serializers import escultoresSerializer, eventosSerializer, obrasSerializer, usuariosSerializer, votacionesSerializer, UserRegisterSerializer, userSerializer, loginSerializer, UserProfileSerializer
from rest_framework.exceptions import PermissionDenied



# Create your views here.

class EscultoresList(viewsets.ModelViewSet):
    queryset = Escultores.objects.all()
    serializer_class = escultoresSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'apellido', 'nacionalidad']

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer.save()
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return []
        return [permissions.IsAdminUser()]


class EventosList(viewsets.ModelViewSet):
    queryset = Eventos.objects.all()
    serializer_class = eventosSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'lugar', 'descripcion']

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer.save()
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return []
        return [permissions.IsAdminUser()]


class ObrasList(viewsets.ModelViewSet):
    queryset = Obras.objects.all()
    serializer_class = obrasSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['titulo', 'material', 'descripcion']

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("You do not have permission to perform this action.")
        serializer.save()
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return []
        return [permissions.IsAdminUser()]


#Registro de usuarios y token
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer= UserRegisterSerializer(data= request.data)

    if serializer.is_valid():
        try:
            user= serializer.save()
            #return Response(status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"error": "Ya existe un usuario con ese nombre de usuario o correo electrónico."}, status=status.HTTP_400_BAD_REQUEST)
        
        token= Token.objects.create(user=user)
        
        
        return Response({"token": token.key }, status= status.HTTP_201_CREATED)
                                            #"user": serializer.data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 


@api_view(['POST'])
@permission_classes([AllowAny])  # No requiere autenticación
def login(request):
    serializer = loginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']

        # Generate token (optional)
        token, _ = Token.objects.get_or_create(user=user)  # Create or retrieve token


        response_data = {
            "token": token.key if token else None,  # Handle case where token already exists
            "user": serializer.data,
        }

        response_data["userinfo"] = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "country": user.usuariosextra.country,
        }
        if user.is_staff:
            response_data["role"] = "STAFF"

        return Response(response_data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_extra = user.usuariosextra  # relación OneToOne entre User y usuarios
        serializer = UserProfileSerializer({
            'user': user,
            'user_extra': user_extra
        })
        return Response(serializer.data)

    def put(self, request):
        user = request.user
        user_extra = user.usuariosextra  # relación OneToOne entre User y usuarios
        serializer = UserProfileSerializer(instance={'user': user, 'user_extra': user_extra}, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([TokenAuthentication])  # Requiere autenticación
@permission_classes([IsAuthenticated])  # Solo usuarios autenticados pueden votar
def votar_obra(request, obra_id):
    # Obtener la obra
    try:
        obra = Obras.objects.get(id=obra_id)
    except Obras.DoesNotExist:
        return Response({'detail': 'Obra no encontrada'}, status=status.HTTP_404_NOT_FOUND)

    #print(obra.id_evento)
    evento = Eventos.objects.get(nombre= obra.id_evento)
    if evento.evento_en_transcurso():
        # Verificar si el usuario ya ha votado en esta obra
        usuario = request.user
        if Votaciones.objects.filter(id_usuario=usuario, id_obra=obra).exists():
            return Response({'detail': 'Ya has votado por esta obra'}, status=status.HTTP_400_BAD_REQUEST)

        # Agregar usuario y obra a los datos del request
        data = request.data.copy()  # Creamos una copia del request.data para modificarla
        data['id_usuario'] = usuario.id  # Añadir el usuario autenticado
        data['id_obra'] = obra.id  # Añadir la obra
        data['id_evento'] = evento.id # Añadir el evento
        

        # Utilizar el serializador para validar y crear la votación
        serializer = votacionesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si hay errores de validación, devolver el error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'detail': 'Votacion finalizada'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
def ver_resultados(request, evento_id):
    # Obtener el evento
    evento = get_object_or_404(Eventos, id=evento_id)

    votaciones= Votaciones()
    resultados = votaciones.resultados_evento(evento_id)

    if not resultados:
        return Response({'detail': 'No hay votaciones para este evento'}, status=status.HTTP_404_NOT_FOUND)

    return Response(resultados, status=status.HTTP_200_OK)


