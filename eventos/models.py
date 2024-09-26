from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import Avg, Count
# Create your models here.

class Escultores(models.Model):
    nombre= models.CharField(max_length=50, null=False)
    apellido= models.CharField(max_length=100, null=False)
    fecha_nacimiento= models.DateField(null=False)
    nacionalidad= models.CharField(max_length=50, null=False)
    eventos_ganados= models.CharField(max_length=200)
    #foto_perfil= models.ImageField(null=True)

    def __str__(self):
        return self.nombre + self.apellido

class Eventos(models.Model):
    nombre= models.CharField(max_length=100,null=False, default='Evento')
    fecha_inicio= models.DateField(null=False)
    fecha_final= models.DateField(null=False, default= '2030-01-01')
    lugar= models.CharField(max_length=75, null=False)
    descripcion= models.CharField(max_length= 500, null=False)

    def __str__(self):
        return self.nombre
    
    def evento_en_transcurso(self):
        fecha_actual = timezone.now().date()
        if self.fecha_final >= fecha_actual:
            return True
        else:
            return False

class Obras(models.Model):
    titulo= models.CharField(max_length=100, null=False) #nombre de la obra
    fecha_creacion= models.DateField(null=False)
    descripcion= models.CharField(max_length=500)
    codigo_qr= models.CharField(max_length=200, null=True, blank=True)
    qr_expiracion = models.DateTimeField(null=True, blank=True)
    material= models.CharField(max_length=200) #materiales usados para su construccion
    id_escultor= models.ForeignKey(Escultores, on_delete=models.CASCADE)
    id_evento= models.ForeignKey(Eventos, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo +' de: '+ self.id_escultor.nombre + self.id_escultor.apellido
    
    def es_qr_valido(self):
        return self.qr_expiracion and self.qr_expiracion > timezone.now().date()

class Imagenes(models.Model):
    id_obra= models.ForeignKey(Obras, on_delete=models.CASCADE)
    img1= models.ImageField(null=False)
    img2= models.ImageField(null=True)
    img3= models.ImageField(null=True)


class UsuariosExtra(models.Model):
    fecha_nacimiento = models.DateField(null=False)
    pais = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)




class Votaciones(models.Model):
    puntuacion = models.IntegerField(choices=[(1, '1 estrella'), (2, '2 estrellas'), (3, '3 estrellas'), (4, '4 estrellas'), (5, '5 estrellas')], default=1)
    id_usuario= models.ForeignKey(User, on_delete=models.DO_NOTHING)
    id_obra=models.ForeignKey(Obras, on_delete=models.DO_NOTHING)
    id_evento=models.ForeignKey(Eventos, on_delete=models.DO_NOTHING)

    class Meta:
        unique_together = ('id_usuario', 'id_obra')  # Evita que un usuario vote más de una vez por obra
    
    def __str__(self):
        r= str(self.puntuacion)+'-'+ str(self.id_obra)+'-'+str(self.id_usuario)
        return r

    def resultados_evento(self, id_evento): 
        # Filtramos las votaciones del evento específico y agrupamos por obra
        resultados = Votaciones.objects.filter(id_evento=id_evento)\
            .values('id_obra__titulo')\
            .annotate(promedio_puntuacion=Avg('puntuacion'), total_votos=Count('puntuacion'))
        # Creamos un diccionario con los resultados
        resultados_dict = {
            resultado['id_obra__titulo']: {
                "promedio_puntuacion": round(resultado['promedio_puntuacion'], 2),  # Redondeamos a 2 decimales
                "total_votos": resultado['total_votos']
            }
            for resultado in resultados
        }

        return resultados_dict
    