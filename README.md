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
