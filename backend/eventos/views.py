from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db import IntegrityError

from .models import Escultores, Eventos, Obras, Imagenes, Votaciones, User
from .serializers import escultoresSerializer, eventosSerializer, obrasSerializer, imagenesSerializer, usuariosSerializer, votacionesSerializer, UserRegisterSerializer

# Create your views here.

@api_view(['GET', 'POST'])
def escultores_list(request):
    if request.method == 'GET':
        escultores = Escultores.objects.all()
        serializer= escultoresSerializer(escultores, many=True)
        return Response(serializer.data)
    
    elif request.method== 'POST' and request.user.is_authenticated and request.user.is_staff:
        serializer= escultoresSerializer(data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        print('No log...')
        return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'DELETE', 'PUT'])
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
            serializer.save()
        except IntegrityError as e:
            return Response({"error": "Ya existe un usuario con ese nombre de usuario o correo electrónico."}, status=status.HTTP_400_BAD_REQUEST)


        user= User.objects.get(username= serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()


        token= Token.objects.create(user=user)
        return Response({"token": token.key, "user": serializer.data}, status= status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



'''
#Login de usuario y token
@api_view(['POST'])
def login(request):
    user= get_object_or_404(Usuarios, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({"error": "invalid password"}, status=status.HTTP_400_BAD_REQUEST)
    
    token, created = Token.objects.get_or_create(user=user)

    serializer= usuariosSerializer(instance=user)

    return Response({"token": token.key, "user": serializer.data}, status=status.HTTP_200_OK)
'''