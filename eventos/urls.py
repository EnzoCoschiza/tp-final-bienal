from rest_framework import routers
from rest_framework.permissions import AllowAny
from django.urls import path, re_path, include
from .views import register, login , votar_obra, ver_resultados, EscultoresList, EventosList, ObrasList, UserProfileView, UserVotacionesView
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'api/escultores', EscultoresList, basename='escultores')
router.register(r'api/eventos', EventosList, basename='eventos')
router.register(r'api/obras', ObrasList, basename='obras')


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

    path('', include(router.urls)),

    path('api/resultados/<int:evento_id>/', ver_resultados, name='resultados_evento'),
    re_path('login', login),
    re_path('register', register),
    path('api/votar_obra/<int:obra_id>/', votar_obra, name='votar_obra'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/votaciones/', UserVotacionesView.as_view(), name='user-votaciones'),

    #path('api/escultores/', EscultoresList.as_view(), name='escultores'),
    #path('api/escultores/<int:pk>/', escultor_info, name='escultor_info'),
    #path('api/eventos/', eventos_list, name='eventos'),
    #path('api/eventos/<int:pk>', evento_info, name='evento_info'),
    #path('api/obras/', obras_list, name='obras'),
    #path('api/obras/<int:pk>', obra_info, name='obras_info'),
    #path('api/imagenes/', imagenes_list, name='imagenes'),
    #path('api/imagenes/<int:pk>', imagen_info, name='imagen_info'),
    #path('', main, name='main'),
    #path('api/escultores/search/', EscultorSearch.as_view(), name='escultor-search'),
    #path('api/obras/search/', ObraSearch.as_view(), name='obra-search'),
    #path('api/eventos/search/', EventoSearch.as_view(), name='evento-search'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)