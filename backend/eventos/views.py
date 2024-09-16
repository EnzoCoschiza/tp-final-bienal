from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate

from .models import Escultores, Eventos, Obras, Imagenes, Votaciones, User
from .serializers import escultoresSerializer, eventosSerializer, obrasSerializer, imagenesSerializer, usuariosSerializer, votacionesSerializer, UserRegisterSerializer, userSerializer, loginSerializer

# Create your views here.

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
def escultores_list(request):
    if request.method == 'GET':
        escultores = Escultores.objects.all()
        serializer = escultoresSerializer(escultores, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if not request.user.is_staff:  # Verificar que el usuario es admin para POST
            return Response({'detail': 'No tienes permiso para realizar esta acción.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = escultoresSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([TokenAuthentication])
def escultor_info(request,pk):
    try:
        escultor = Escultores.objects.get(pk=pk)      
    except Escultores.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer= escultoresSerializer(escultor)
        return Response (serializer.data)
        
    elif request.user.is_authenticated and request.user.is_staff:
        if request.method== 'DELETE':
            escultor.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'PUT':
            serializer= escultoresSerializer(escultor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)            
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
def eventos_list(request):
    if request.method=='GET':
        eventos= Eventos.objects.all()
        serializer = eventosSerializer(eventos, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST' and request.user.is_authenticated and request.user.is_staff:
        serializer= eventosSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return Response(status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([TokenAuthentication])
def evento_info(request, pk):
    try:
        evento= Eventos.objects.get(pk=pk)
    except Eventos.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method== 'GET':
        serializer= eventosSerializer(evento)
        return Response(serializer.data)
    
    elif request.user.is_authenticated and request.user.is_staff:
        if request.method=='DELETE':
            evento.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method=='PUT':
            serializer= eventosSerializer(evento,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
def obras_list(request):
    if request.method=='GET':
        obras= Obras.objects.all()
        serializer = obrasSerializer(obras, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST' and request.user.is_authenticated and request.user.is_staff:
        serializer= obrasSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return Response(status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([TokenAuthentication])
def obra_info(request, pk):
    try:
        obra= Obras.objects.get(pk=pk)
    except Obras.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method== 'GET':
        serializer= obrasSerializer(obra)
        return Response(serializer.data)
    
    elif request.user.is_authenticated and request.user.is_staff:
        if request.method=='DELETE':
            obra.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method=='PUT':
            serializer= obrasSerializer(obra,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
def imagenes_list(request):
    if request.method=='GET':
        imagenes= Imagenes.objects.all()
        serializer = imagenesSerializer(imagenes, many=True)
        return Response(serializer.data)
    
    elif request.method=='POST' and request.user.is_authenticated and request.user.is_staff:
        serializer= imagenesSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return Response(status= status.HTTP_400_BAD_REQUEST)
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([TokenAuthentication])
def imagen_info(request, pk):
    try:
        imagen= Imagenes.objects.get(pk=pk)
    except Imagenes.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method== 'GET':
        serializer= imagenesSerializer(imagen)
        return Response(serializer.data)
    
    elif request.user.is_authenticated and request.user.is_staff:
        if request.method=='DELETE':
            imagen.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        elif request.method=='PUT':
            serializer= imagenesSerializer(imagen,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(status=status.HTTP_401_UNAUTHORIZED)


#Registro de usuarios y token
@api_view(['POST'])
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
def login(request):
    serializer = loginSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.validated_data['user']

        # Generate token (optional)
        token, _ = Token.objects.get_or_create(user=user)  # Create or retrieve token

        return Response({
            "token": token.key if token else None,  # Handle case where token already exists
            "user": serializer.data
        }, status=status.HTTP_200_OK)

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

        # Utilizar el serializador para validar y crear la votación
        serializer = votacionesSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si hay errores de validación, devolver el error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'detail': 'Votacion finalizada'}, status=status.HTTP_400_BAD_REQUEST)