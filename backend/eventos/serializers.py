from rest_framework import serializers
from .models import *

class escultoresSerializer(serializers.ModelSerializer):
    class Meta:
        model= Escultores
        fields= ('id','nombre','apellido','fecha_nacimiento','nacionalidad','eventos_ganados')
        read_only_fields= ('id',)

class eventosSerializer(serializers.ModelSerializer):
    class Meta:
        model= Eventos
        fields= ('id','nombre','fecha','lugar','descripcion')
        read_only_fields= ('id',)

class obrasSerializer(serializers.ModelSerializer):
    class Meta:
        model= Obras
        fields= ('id','titulo','fecha_creacion','descripcion','material','id_escultor','id_evento')
        #read_only_fields= ('id', 'id_escultor', 'id_evento')

class imagenesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Imagenes
        fields= ('id', 'id_obra', 'img1','img2','img3')
        read_only_fields= ('id','id_obra')

class userSerializer(serializers.ModelSerializer):
    class Meta:
        model= User 
        fields= ('id','username','first_name','last_name','email','password')
        read_only_fields=('id',)

class usuariosSerializer(serializers.ModelSerializer):
    class Meta:
        model= UsuariosExtra
        fields=('id','username','first_name','last_name','email','password','fecha_nacimiento','pais')
        read_only_fields=('id',)

class UserRegisterSerializer(serializers.Serializer):
    user = userSerializer()
    user_extra = usuariosSerializer()

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_extra_data = validated_data.pop('user_extra')

        user = User.objects.create_user(**user_data)
        user_extra = UsuariosExtra.objects.create(user=user, **user_extra_data)
        return user
    

class votacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Votaciones
        fields= ('id','puntuacion','id_usuario','id_obra')
        #read_only_fields=('id','id_usuario','id_obra')

