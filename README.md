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
    "email": "julio@example.com"
  },
  "birthdate": "1990-01-01",
  "country": "Argentina"
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

## Contacto

Para más información o consultas, contacta al equipo de desarrollo.

