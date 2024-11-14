from rest_framework import routers
from rest_framework.permissions import AllowAny
from django.urls import path, re_path, include
from .views import register, login , votar_obra, ver_resultados, EscultoresList, EventosList, ObrasList, UserProfileView, UserVotacionesView, UsuariosCompleteViewSet, PasswordResetRequestView, PasswordResetView, activate_account
from django.conf import settings
from django.conf.urls.static import static


router = routers.DefaultRouter()
router.register(r'api/escultores', EscultoresList, basename='escultores')
router.register(r'api/eventos', EventosList, basename='eventos')
router.register(r'api/obras', ObrasList, basename='obras')
router.register(r'api/usuarios', UsuariosCompleteViewSet, basename='usuarios')


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
    
    #GOOGLE AUTHENTICATION
    #path('accounts/', include('allauth.urls')),

    #Restablecer password
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('password-reset-confirm/', PasswordResetView.as_view(), name='password_reset_confirm'),

    path('', include(router.urls)),

    path('api/resultados/<int:evento_id>/', ver_resultados, name='resultados_evento'),
    #Login, register, verificación de email
    re_path('login', login),
    re_path('register', register),
    path('verify-email/<str:token>/', activate_account, name='activate_account'),

    path('api/votar_obra/<int:obra_id>/', votar_obra, name='votar_obra'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('api/votaciones/', UserVotacionesView.as_view(), name='user-votaciones'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)