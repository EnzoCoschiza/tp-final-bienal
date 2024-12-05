from django.shortcuts import render
from rest_framework import status, filters, generics, viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework.views import APIView 
from rest_framework.exceptions import NotFound
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string



from .models import Escultores, Eventos, Obras, Votaciones, User, UsuariosExtra, Profile
from .serializers import escultoresSerializer, eventosSerializer, obrasSerializer, usuariosSerializer, votacionesSerializer, UserRegisterSerializer, userSerializer, loginSerializer, UserProfileSerializer, VotosUserSerializer, UsuariosCompleteSerializer, PasswordResetRequestSerializer, PasswordResetSerializer
from rest_framework.exceptions import PermissionDenied

from telnet import send_email

# Create your views here.

class EscultoresList(viewsets.ModelViewSet):
    queryset = Escultores.objects.all()
    serializer_class = escultoresSerializer
    authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'apellido', 'nacionalidad']
    filterset_fields = ['id', 'eventos_ganados', 'nacionalidad', 'nombre','apellido']

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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nombre', 'lugar', 'descripcion']
    filterset_fields = ['id', 'lugar', 'nombre','fecha_inicio', 'fecha_final']

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
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['titulo', 'material', 'descripcion']
    filterset_fields = ['id', 'titulo', 'id_escultor', 'id_evento']

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
            user.is_active= False
            user.save()
        except IntegrityError as e:
            return Response({"error": "Ya existe un usuario con ese nombre de usuario o correo electrónico."}, status=status.HTTP_400_BAD_REQUEST)
        
        token= Token.objects.create(user=user)

        token_email_verif = get_random_string(length=32)
        user.profile.activation_token = token_email_verif
        user.profile.save()

        activation_url = f"http://localhost:3000/activate/{token_email_verif}"
        subject = "Activa tu cuenta de Bienal"
        #body = f"Click en el link para comenzar a usar Bienal App: {activation_url}"
        body=  f"""<h2>Activa tu cuenta desde el siguiente enlace.</h2>
                <a href="{activation_url}" class="button">Ir al Sitio</a>
                <p>Gracias por unirte a nosotros. Esperamos que disfrutes de tu experiencia.</p>"""           
        send_email(subject, body, user.email)
        

        
        return Response({"token": token.key }, status= status.HTTP_201_CREATED)
                                            #"user": serializer.data
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



@api_view(['POST'])
@permission_classes([AllowAny])
def activate_account(request, token):
    try:
        user = User.objects.get(profile__activation_token=token)
        user.is_active = True
        user.profile.activation_token = None
        user.save()
        email= user.email
        subject = "Cuenta activada"
        body = f"""<h2>Cuenta activada de forma exitosa!</h2>
                <a href="{settings.FRONTEND_URL}" class="button">Ir al Sitio</a>
                <p>Ya podes empezar a participar en nuestras votaciones...</p>
                <p>Gracias por unirte a nosotros. Esperamos que disfrutes de tu experiencia.</p>"""
        
        send_email(subject, body, email)
        return Response({"detail": "Account activated successfully."}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({"detail": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny]) 
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

        response_data["user_info"] = {
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "country": user.usuariosextra.country,
        }
        
        response_data["staff"] = user.is_staff
        

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
    estado_evento= evento.evento_en_transcurso()
    if estado_evento == 'En curso':
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

            # Enviar email con votacion realizada
            subject = "Votación realizada"
            body = f"""<h2>Realizaste una votación de forma exitosa.</h2>
                <p>Has votado por la obra {obra.titulo} en el evento {evento.nombre}</p>
                <a href="{settings.FRONTEND_URL}" class="button">Ir al Sitio</a>
                <p>Gracias por participar.</p>"""
            send_email(subject, body, usuario.email)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        # Si hay errores de validación, devolver el error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'detail': 'Votacion finalizada'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([AllowAny])
def ver_resultados(request, evento_id):
    # Obtener el evento
    evento = get_object_or_404(Eventos, id=evento_id)

    votaciones= Votaciones()
    resultados = votaciones.resultados_evento(evento_id)

    if not resultados:
        return Response({'detail': 'No hay votaciones para este evento'}, status=status.HTTP_404_NOT_FOUND)

    return Response(resultados, status=status.HTTP_200_OK)



class UserVotacionesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        votaciones = Votaciones.objects.filter(id_usuario=user)
        data = []
        for votacion in votaciones:
            obra= Obras.objects.get(id= votacion.id_obra.id)
            evento= Eventos.objects.get(id= obra.id_evento.id)

            votacion_data = {
                'id_voto': votacion.id,
                'id_obra': obra.id,
                'titulo_obra': obra.titulo,
                'puntuacion': votacion.puntuacion,
                'id_evento': evento.id,
                'nombre_evento': evento.nombre,
                'id_usuario': votacion.id_usuario.id,
                'nombre_escultor': obra.id_escultor.nombre,
                'apellido_escultor': obra.id_escultor.apellido
            }
            data.append(votacion_data)


        serializer = VotosUserSerializer(data, many=True)
        return Response(serializer.data)

    
class UsuariosCompleteViewSet(viewsets.ModelViewSet):
    queryset = UsuariosExtra.objects.all()
    serializer_class = UsuariosCompleteSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ['user__username', 'user__email', 'country']

    def get_queryset(self):
        queryset = super().get_queryset()
        user_id = self.request.query_params.get('user_id', None)
        if user_id is not None:
            queryset = queryset.filter(user__id=user_id)
        return queryset

    def get_object(self):
        queryset = self.get_queryset()
        user_id = self.kwargs.get('pk')
        try:
            return queryset.get(user__id=user_id)
        except UsuariosExtra.DoesNotExist:
            raise NotFound('Usuario no encontrado')



@permission_classes([AllowAny])
class PasswordResetRequestView(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"detail": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            token = get_random_string(length=32)
            user.profile.password_reset_token = token
            user.profile.save()

            reset_url = f"http://localhost:3000/reset-password/{token}"
            subject = "Solicitud de restablecimiento de contraseña"
            body = f"""<h2>Realiza el cambio de contraseña desde el siguiente enlace.</h2>
                <a href="{reset_url}" class="button">Ir al Sitio</a>
                <p>En caso de no poder acceder mediante el botón, link: {reset_url}.</p>"""
            try:
                send_email(subject, body, user.email)
            except Exception as e:
                return Response({"detail": "Error al enviar el correo electrónico."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"detail": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([AllowAny])
class PasswordResetView(APIView):
    permission_classes= [AllowAny]
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            user = User.objects.get(profile__password_reset_token=token)
            user.set_password(new_password)
            user.profile.password_reset_token = None
            user.profile.save()
            user.save()
            body= f"""<h2>Contraseña restablecida de forma exitosa.</h2>
            <a href="{settings.FRONTEND_URL}" class="button">Ir al Sitio</a>"""
            send_email("Contraseña restablecida", body, user.email)
            return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from .utils import generate_token
@permission_classes([AllowAny])
class GenerateTokenView(APIView):
    def get(self, request):
        token = generate_token()
        return Response({"token": token}, status=status.HTTP_200_OK)
    
@permission_classes([AllowAny])   
class VoteView(APIView):
    def post(self, request, obra_id, token):
        # Validar el token
        expected_token = generate_token()
        if token != expected_token:
            return Response({"detail": "Token inválido o expirado."}, status=status.HTTP_400_BAD_REQUEST)

        # Obtener la obra
        try:
            obra = Obras.objects.get(id=obra_id)
        except Obras.DoesNotExist:
            return Response({"detail": "Obra no encontrada."}, status=status.HTTP_404_NOT_FOUND)

        evento = Eventos.objects.get(nombre= obra.id_evento)
        if evento.evento_en_transcurso() == 'En curso':
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

                # Enviar email con votacion realizada
                subject = "Votación realizada"
                body = f"""<h2>Hola, {usuario.first_name}! <br> Realizaste una votación de forma exitosa.</h2>
                <p>Has votado por la obra {obra.titulo} en el evento {evento.nombre}</p>
                <a href="{settings.FRONTEND_URL}" class="button">Ir al Sitio</a>
                <p>Gracias por participar.</p>"""
                send_email(subject, body, usuario.email)

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            # Si hay errores de validación, devolver el error
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        return Response({'detail': 'Votacion finalizada'}, status=status.HTTP_400_BAD_REQUEST)



@permission_classes([AllowAny])
class EscultoresConSusObras(APIView):
    def get(self, request):
        id_escultor = request.query_params.get('id_escultor', None)
        
        if id_escultor:
            escultores = Escultores.objects.filter(id=id_escultor).order_by('id')
        else:
            escultores = Escultores.objects.all().order_by('id')

        data = []
        for escultor in escultores:
            obras = Obras.objects.filter(id_escultor=escultor).order_by('id')
            obras_data = []
            for obra in obras:
                obra_data = {
                    'id': obra.id,
                    'titulo': obra.titulo,
                    'material': obra.material,
                    'descripcion': obra.descripcion
                }
                obras_data.append(obra_data)

            escultor_data = {
                'id': escultor.id,
                'nombre': escultor.nombre,
                'apellido': escultor.apellido,
                'nacionalidad': escultor.nacionalidad,
                'obras': obras_data
            }
            data.append(escultor_data)

        return Response(data, status=status.HTTP_200_OK)