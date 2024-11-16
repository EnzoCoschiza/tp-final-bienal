import hashlib
import time
from django.conf import settings

def generate_token():
    current_time = int(time.time() // 60)  # Cambia cada 1 minutos, cambiar el 60 para modificar el tiempo de expiración
    secret = settings.SECRET_KEY
    token = hashlib.sha256(f'{current_time}{secret}'.encode()).hexdigest()
    return token