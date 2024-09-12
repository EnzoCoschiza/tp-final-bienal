from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Escultores)
admin.site.register(Obras)
admin.site.register(Imagenes)
admin.site.register(Eventos)
#admin.site.register(User)
admin.site.register(UsuariosExtra)
admin.site.register(Votaciones)