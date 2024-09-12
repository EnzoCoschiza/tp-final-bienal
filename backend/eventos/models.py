from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Escultores(models.Model):
    nombre= models.CharField(max_length=50, null=False)
    apellido= models.CharField(max_length=100, null=False)
    fecha_nacimiento= models.DateField(null=False)
    nacionalidad= models.CharField(max_length=50, null=False)
    eventos_ganados= models.CharField(max_length=200)

    def __str__(self):
        return self.nombre + self.apellido

class Eventos(models.Model):
    nombre= models.CharField(max_length=100,null=False, default='Evento')
    fecha= models.DateField(null=False)
    lugar= models.CharField(max_length=75, null=False)
    descripcion= models.CharField(max_length= 500, null=False)

    def __str__(self):
        return self.nombre

class Obras(models.Model):
    titulo= models.CharField(max_length=100, null=False) #nombre de la obra
    fecha_creacion= models.DateField(null=False)
    descripcion= models.CharField(max_length=500)
    material= models.CharField(max_length=200) #materiales usados para su construccion
    id_escultor= models.ForeignKey(Escultores, on_delete=models.CASCADE)
    id_evento= models.ForeignKey(Eventos, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo +' de: '+ self.id_escultor.nombre + self.id_escultor.apellido

class Imagenes(models.Model):
    id_obra= models.ForeignKey(Obras, on_delete=models.CASCADE)
    img1= models.ImageField(null=False)
    img2= models.ImageField(null=True)
    img3= models.ImageField(null=True)

'''
class Usuarios(models.Model):
    nombre_usuario= models.CharField(max_length=20, null=False)
    nombre= models.CharField(max_length=50, null=False)
    apellido= models.CharField(max_length=100, null=False)
    email= models.EmailField(null=False)
    nacionalidad= models.CharField(max_length=50)
    fecha_nacimiento= models.DateField(null=False)

    def __str__(self):
        return self.nombre_usuario
'''

class UsuariosExtra(models.Model):
    fecha_nacimiento = models.DateField(null=False)
    pais = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)




class Votaciones(models.Model):
    puntuacion = models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')], default=1)
    id_usuario= models.ForeignKey(User, on_delete=models.DO_NOTHING)
    id_obra=models.ForeignKey(Obras, on_delete=models.DO_NOTHING)
