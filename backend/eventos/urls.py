from rest_framework import routers
from django.urls import path, re_path
#from .api import escultoresViewSet, eventosViewSet, obrasViewSet, imagenesViewSet, usuariosViewSet, votacionViewSet
from .views import escultores_list, escultor_info, eventos_list, evento_info, obras_list,obra_info, imagenes_list,imagen_info, register, login

router = routers.DefaultRouter()

#router.register('api/escultores', escultoresViewSet, 'escultores')
#router.register('api/eventos', eventosViewSet, 'eventos')
#router.register('api/obras', obrasViewSet,'obras')
#router.register('api/imagenes',imagenesViewSet,'imagenes')
#router.register('api/usuarios',usuariosViewSet,'usuarios')
#router.register('api/votaciones',votacionViewSet,'votaciones')

#router.register('api/escultores', escultores_list, basename='escultores')
#urlpatterns= router.urls

urlpatterns = [
    path('api/escultores/', escultores_list, name='escultores'),
    path('api/escultores/<int:pk>/', escultor_info, name='escultor_info'),
    path('api/eventos/', eventos_list, name='eventos'),
    path('api/eventos/<int:pk>', evento_info, name='evento_info'),
    path('api/obras/', obras_list, name='obras'),
    path('api/obras/<int:pk>', obra_info, name='obras_info'),
    path('api/imagenes/', imagenes_list, name='imagenes'),
    path('api/imagenes/<int:pk>', imagen_info, name='imagen_info'),
    re_path('login', login),
    re_path('register', register)
]