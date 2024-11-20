# API Bienal - Documentación

Esta API es parte del sistema de votaciones de la Bienal de escultores. A continuación, se describen los distintos endpoints y sus funcionalidades.

## Endpoints

### Escultores

#### Listar Escultores
- **Método**: `GET`
- **Ruta**: `/api/escultores/`
- **Descripción**: Devuelve todos los escultores registrados en la base de datos.
- **Autenticación**: No requerida.

#### Crear Escultor
- **Método**: `POST`
- **Ruta**: `/api/escultores/`
- **Descripción**: Crea un nuevo escultor (solo staff).
- **Autenticación**: Requerida (staff).

**Ejemplo de JSON**:
```json
{
  "nombre": "Leonardo",
  "apellido": "Da Vinci",
  "fecha_nacimiento": "1452-04-15",
  "nacionalidad": "Italia",
  "eventos_ganados": 1,
  "foto_perfil": null
}
```

### Eventos

#### Listar Eventos
- **Método**: `GET`
- **Ruta**: `/api/eventos/`
- **Descripción**: Devuelve todos los eventos registrados.
- **Autenticación**: No requerida.

#### Crear Evento
- **Método**: `POST`
- **Ruta**: `/api/eventos/`
- **Descripción**: Crea un nuevo evento (solo staff).
- **Autenticación**: Requerida (staff).

**Ejemplo de JSON**:
```json
{
  "nombre": "Bienal 2024",
  "fecha_inicio": "2024-09-16",
  "fecha_final": "2024-09-26",
  "lugar": "Resistencia",
  "descripcion": "Una locura"
}
```

### Obras

#### Listar Obras
- **Método**: `GET`
- **Ruta**: `/api/obras/`
- **Descripción**: Devuelve todas las obras registradas.
- **Autenticación**: No requerida.

#### Crear Obra
- **Método**: `POST`
- **Ruta**: `/api/obras/`
- **Descripción**: Crea una nueva obra (solo staff).
- **Autenticación**: Requerida (staff).

**Ejemplo de JSON**:
```json
{
  "titulo": "El perro",
  "fecha_creacion": "2024-07-02",
  "descripcion": "Escultura en madera",
  "material": "Madera",
  "id_escultor": 2,
  "id_evento": 1
}
```

### Usuarios

#### Listar Usuarios
- **Método**: `GET`
- **Ruta**: `/api/usuarios/`
- **Descripción**: Devuelve todos los usuarios (solo staff).
- **Autenticación**: Requerida (staff).

#### Crear Usuario
- **Método**: `POST`
- **Ruta**: `/api/usuarios/`
- **Descripción**: Crea un nuevo usuario (solo staff).
- **Autenticación**: Requerida (staff).

**Ejemplo de JSON**:
```json
{
  "user": {
    "username": "julito",
    "first_name": "Julio",
    "last_name": "César",
    "email": "julio@example.com",
    "password": "pass123"
  },
  "user_extra":{
    "birthdate": "1990-01-01",
    "country": "Argentina"
  }
}
```

### Votaciones

#### Listar Votaciones
- **Método**: `GET`
- **Ruta**: `/api/votaciones/`
- **Descripción**: Devuelve todos los votos realizados por el usuario logueado.
- **Autenticación**: Requerida.

#### Votar Obra
- **Método**: `POST`
- **Ruta**: `/api/votar_obra/{id_obra}/`
- **Descripción**: Permite votar una obra.
- **Autenticación**: Requerida (usuario logueado).

**Ejemplo de JSON**:
```json
{
  "puntuacion": 5
}
```

### Resultados

#### Ver Resultados de Evento
- **Método**: `GET`
- **Ruta**: `/api/resultados/{id_evento}/`
- **Descripción**: Devuelve el promedio de puntaje y la cantidad de votos por obra de un evento específico.
- **Autenticación**: No requerida.

**Ejemplo de JSON**:
```json
{
  "El perro": {
    "promedio_puntuacion": 4.5,
    "total_votos": 10
  }
}
```

## Autenticación

Para acceder a los endpoints restringidos es necesario autenticarse usando el token devuelto en `/login/` o `/register/`.

**Ejemplo de login**:
```json
{
  "username": "jesusito",
  "password": "password123"
}
```

La respuesta contiene un token que se utilizará en las siguientes peticiones:
```json
{
  "token": "c3cfbd3e5579ab14c65ffa2f7621b8844ae35550"
}
```

---
## Password Reset
Para el reseteo de password debemos hacer una petición POST a /password-reset/ con los siguientes datos:
```json
{
  "email": "email_usuario_que_desea_cambiar_pass@mail.com"
}
```
Este chequeará que haya un usuario asociado a este email, de ser así, enviará un email con un token de reinicio de password a dicho email.

Luego con dicho token debemos hacer una petición POST a /password-reset-confirm/ con la siguiente estructura: 
```json
{
  "token": "UHCl2k7kW7FLMJuhHGwhLk1iZ4L7oAdm",
  "new_password" : "tunuevapass"
}
```
En caso del token ser correcto, esto efecturá el cambio de contraseña en dicha cuenta asociada...

---
## Confirmar correo electronico al crear cuenta
Cuando utilizamos el POST en el endpoint "Register", nos enviarán un correo de confirmación al email que especificamos en el register. 
La cuenta se creará, pero se pondrá en inactiva hasta que completemos la confirmación. 

- **Método**: `POST`
- **Ruta**: `/verify-email/{TOKEN}`

Para activar la cuenta, debemos copiar el token que nos viene al correo. 

Ejemplo : "http://your-frontend-url.com/activate/vjuFuO6yPyzxBqByMJNvACN0xBr1lUSl"

TOKEN: vjuFuO6yPyzxBqByMJNvACN0xBr1lUSl

Con este token, realizamos un POST a "/verify-email/{TOKEN}"

Una vez realizada la accion previa, esto pondra la cuenta como activa y ya podremos accionar con dicho usuario. 

---
## Votacion con endpoint dinamico para la creación de QR

- **Método**: `GET`
- **Ruta**: `/generate-token/`

Cuando realizamos un GET a este enpoint, recibimos un token-hash, que se regenera cada 1 minuto, este hash, sirve para que cada usuario logueado(con su respectivo Auth Token), pueda realizar un voto en el siguiente enpoint:

- **Método**: `POST`
- **Ruta**: `/vote/{obra_id}/{hash-token}/`

**Ejemplo de JSON**:
```json
{
  "puntuacion": 5
}
```
En el header debe ir el token auth del usuario.

En caso de que el token haya vencido, no permitirá realizar la accion de voto.

---
## GET Escultores con sus respectivas obras
- **Método**: `GET`
- **Ruta**: `/api/escultores-obras/`

Este endpoint, trae todos los escultores con sus respectivas obras.
Es decir devuelve un JSON con datos de un escultor y le añade un array con todos los datos de cada una de sus obras.

**Ejemplo de JSON**:
```json
[
    {
        "id": 2,
        "nombre": "Leonardo",
        "apellido": "Da Vinci",
        "nacionalidad": "Italia",
        "obras": [
            {
                "id": 1,
                "titulo": "El perro",
                "material": "Madera",
                "descripcion": "adasdasd"
            },
            {
                "id": 5,
                "titulo": "El truco del dedo magico",
                "material": "Ni idea",
                "descripcion": "Una locura"
            }
        ]
    },
    {
        "id": 3,
        "nombre": "Enzo",
        "apellido": "Palo",
        "nacionalidad": "Italia",
        "obras": [
            {
                "id": 6,
                "titulo": "La Gioconda",
                "material": "Ni idea",
                "descripcion": "Lalalala"
            }
        ]
    }]
```

Ademas, este endpoint, acepta query params para filtrar por algún escultor que deseemos.
- **Ruta**: `/api/escultores-obras/?id_escultor=idQueDeseemos`

---
## Contacto

Para más información o consultas, contacta al equipo de desarrollo.

