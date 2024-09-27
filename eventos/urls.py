from rest_framework import routers
from rest_framework.permissions import AllowAny
from django.urls import path, re_path
#from .api import escultoresViewSet, eventosViewSet, obrasViewSet, imagenesViewSet, usuariosViewSet, votacionViewSet
from .views import escultores_list, escultor_info, eventos_list, evento_info, obras_list,obra_info, imagenes_list,imagen_info, register, login , votar_obra, main, ver_resultados, EscultorSearch, EventoSearch, ObraSearch

router = routers.DefaultRouter()

#router.register('api/escultores', escultoresViewSet, 'escultores')
#router.register('api/eventos', eventosViewSet, 'eventos')
#router.register('api/obras', obrasViewSet,'obras')
#router.register('api/imagenes',imagenesViewSet,'imagenes')
#router.register('api/usuarios',usuariosViewSet,'usuarios')
#router.register('api/votaciones',votacionViewSet,'votaciones')

#router.register('api/escultores', escultores_list, basename='escultores')
#urlpatterns= router.urls


from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Bienal API",
        default_version='v1',
        description="API documentation",
    ),
    public=True,
    permission_classes=(AllowAny,),
)


urlpatterns = [
    #DOCUMENTATION
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),


    path('api/escultores/', escultores_list, name='escultores'),
    #path('api/escultoresxd/', escultores_list_post, name='escultores_post'),
    path('api/escultores/<int:pk>/', escultor_info, name='escultor_info'),
    path('api/eventos/', eventos_list, name='eventos'),
    path('api/eventos/<int:pk>', evento_info, name='evento_info'),
    path('api/obras/', obras_list, name='obras'),
    path('api/obras/<int:pk>', obra_info, name='obras_info'),
    path('api/imagenes/', imagenes_list, name='imagenes'),
    path('api/imagenes/<int:pk>', imagen_info, name='imagen_info'),
    re_path('login', login),
    re_path('register', register),
    path('api/votar_obra/<int:obra_id>/', votar_obra, name='votar_obra'),
    #path('', main, name='main'),
    path('api/resultados/<int:evento_id>/', ver_resultados, name='resultados_evento'),
    path('api/escultores/search/', EscultorSearch.as_view(), name='escultor-search'),
    path('api/obras/search/', ObraSearch.as_view(), name='obra-search'),
    path('api/eventos/search/', EventoSearch.as_view(), name='evento-search'),
]