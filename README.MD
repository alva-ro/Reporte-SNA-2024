# Proyecto Reporte SNA 2024

## Descripción
Proyecto Python Backend desarrollado con Django Rest Framework para la disponibilización de indicadores y métodos de verificación en evaluación ambiental.

## Organización de Tareas
Puedes ver el backlog y la organización de tareas en el siguiente enlace:
[Taiga Epics - Reporte SNA 2024](https://tree.taiga.io/project/paulyval-reporte-sna-2024/epics)

## Historias de Usuario
Las historias de usuario y criterios de aceptación puedes verlo en [Taiga Backlog - Reporte SNA 2024](https://tree.taiga.io/project/paulyval-reporte-sna-2024/backlog).

## Tecnologías Utilizadas
- **Python**
- **Django Rest Framework**
- **PostgreSQL**
- **Taiga** (Gestión de tareas)
- **drf-spectacular** (Documentación API JWT)

## Instalación y Configuración
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/alva-ro/Reporte-SNA-2024
   ```

2. **Crear y activar entorno virtual**:
   ```bash
   python -m venv sna_env
   sna_env\Scripts\activate  # En Windows
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno**:
   Crear un archivo `.env` en la raíz con los siguientes campos:
   ```env
   DB_NAME=postgres
   DB_USER=postgres
   DB_PASSWORD=postgres
   DB_HOST=localhost
   DB_PORT=5432
   SECRET_KEY=tu_clave_secreta
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   ```

5. **Aplicar migraciones y levantar el servidor**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

## Autenticación JWT
Para autenticarse y probar endpoints protegidos:

1. Obtener el token:
   ```http
   POST /api/token/
   {
     "username": "tu_usuario",
     "password": "tu_password"
   }
   ```

2. Usar el token en cada petición:
   ```http
   Authorization: Bearer <tu_token>
   ```

## Roles y Permisos

El sistema implementa control de acceso basado en roles, mediante clases personalizadas:

| Rol                        | Permisos                                                                 |
|---------------------------|--------------------------------------------------------------------------|
| `EsRepOrgResOSoloLectura` | Puede listar y crear reportes. No puede modificar ni eliminar.           |
| `EsAdminOSoloLectura`     | Puede modificar el estado de un reporte, eliminar si es necesario.       |
| `EsSuperAdminOSoloLectura`| Tiene acceso total a todos los recursos, incluyendo configuración.       |

Estos roles se validan en cada endpoint mediante `permission_classes` personalizadas.

## Carga de datos de prueba

Para probar la paginación y filtros de reportes, puedes ejecutar el siguiente script que carga reportes demo en la base de datos:

1. Asegúrate de tener al menos:
   - Una medida creada.
   - Dos organismos responsables creados.

2. Activa el entorno virtual:

   - En **Bash**:
     ```bash
     source .venv/Scripts/activate
     ```

   - En **PowerShell**:
     ```powershell
     .venv\Scripts\activate
     ```

3. Ejecuta el shell de Django y corre el script:

   ```bash
   python manage.py shell
   ```

   Dentro del shell:

   ```python
   exec(open('scripts/cargar_reportes_demo.py', encoding='utf-8').read())
   ```

4. Verifica que se hayan cargado correctamente:

   ```python
   from app_reporte.models import Reporte
   print("Reportes creados:", Reporte.objects.count())
   ```

> Este script crea 20 reportes aleatorios con fechas, estados y relaciones reales. Es útil para probar filtros, paginación y trazabilidad de cambios de estado.

> También puedes modificarlo para ajustar la cantidad de datos generados o simular combinaciones específicas de filtros y estados.


## API Endpoints Principales
- **comunas**: `/api/comunas/`
- **ciudades**: `/api/ciudades/`
- **organismos responsales**: `/api/organismo-responsable/`
- **planes ppda**: `/api/planes/`
- **regiones**: `/api/regiones/`

---

## Endpoints desarrollados: Reportes

Los siguientes endpoints permiten gestionar reportes asociados a medidas de los planes PPDA, incluyendo su creación, actualización, validación y trazabilidad de estados.

### 🔹 Listado de Reportes
`GET /api/reportes/`

Este endpoint permite listar los reportes disponibles aplicando filtros opcionales y control de paginación.

#### Parámetros de consulta disponibles:
| Parámetro      | Tipo   | Descripción                                               | Ejemplo                  |
|----------------|--------|-----------------------------------------------------------|--------------------------|
| `organismo`    | int    | ID del organismo responsable                              | `organismo=2`            |
| `estado`       | str    | Estado del reporte (`pendiente`, `aprobado`, `rechazado`) | `estado=pendiente`       |
| `fecha_envio`  | str    | Fecha de envío exacta en formato `YYYY-MM-DD`             | `fecha_envio=2024-04-01` |
| `ordering`     | str    | Campo por el que ordenar (`fecha_envio`, `estado`)        | `ordering=-fecha_envio`  |
| `page`         | int    | Número de página                                          | `page=2`                 |
| `page_size`    | int    | Cantidad de resultados por página                         | `page_size=20`           |

> Los resultados son paginados automáticamente para mejorar el rendimiento.

---

### 🔹 Modificación de Estado
`PUT /api/reportes/{id_reporte}/estado/`

Permite actualizar el estado de un reporte validando las siguientes reglas:
- No se puede aprobar un reporte que ha sido rechazado.
- No se puede modificar un reporte que ya ha sido aprobado.

Cada cambio queda registrado en un historial de trazabilidad (`HistorialEstadoReporte`) con:
- Estado anterior
- Estado nuevo
- Usuario responsable
- Fecha del cambio

---

### 🔹 Operaciones CRUD de un Reporte

| Método | Ruta                          | Descripción                      |
|--------|-------------------------------|----------------------------------|
| POST   | `/api/reporte/`               | Crear un nuevo reporte           |
| GET    | `/api/reporte/{id_reporte}`   | Obtener detalle de un reporte    |
| PUT    | `/api/reporte/{id_reporte}`   | Actualizar un reporte existente  |
| DELETE | `/api/reporte/{id_reporte}`   | Eliminar un reporte existente    |

---

### 🔎 Ejemplo de respuesta con paginación:
```json
{
  "count": 45,
  "next": "http://localhost:8000/api/reportes/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "estado": "pendiente",
      "organismo": 2,
      "fecha_envio": "2024-04-01",
      "descripcion": "Avance preliminar"
    }
  ]
}
```

### Permisos aplicados
- `EsRepOrgResOSoloLectura`: Solo puede listar, ver y crear.
- `EsAdminOSoloLectura`: Puede modificar el estado o eliminar.

---

## Información entrega 2
En esta segunda entrega nuestro foco principal fue integrar seguridad a nuestros endpoints a través de token JWT, asignando roles y permisos para controlar los accesos. 

## Próximos pasos
1. Documentar el proceso de autenticación y autorización para los administradores.
2. Crear nuevos endpoints para mejorar las opciones de filtrados.
3. Integrar rate limiting.
4. Fortalecer validaciones en endpoints críticos.
5. Agregar trazabilidad completa al historial de cambios.
6. Incorporar tests automáticos.

Para más detalles, consulta la documentación en:
```
http://127.0.0.1:8000/api/docs/#/
```
