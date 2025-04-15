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

## API Endpoints

### 🔹 Regiones

#### Listado de Regiones
`GET /api/regiones/`

Lista todas las regiones disponibles con filtrado opcional por nombre.

##### Parámetros de consulta disponibles:
| Parámetro | Tipo   | Descripción                                    | Ejemplo                  |
|-----------|--------|------------------------------------------------|--------------------------|
| `nombre`  | str    | Filtrar por nombre (búsqueda parcial)          | `nombre=metropolitana`   |

##### Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "nombre": "Región Metropolitana"
  }
]
```

#### Operaciones CRUD de Regiones

| Método | Ruta                    | Descripción                      |
|--------|-------------------------|----------------------------------|
| POST   | `/api/regiones/`        | Crear una nueva región           |
| GET    | `/api/regiones/{id}/`   | Obtener detalle de una región    |
| PUT    | `/api/regiones/{id}/`   | Actualizar una región existente  |
| DELETE | `/api/regiones/{id}/`   | Eliminar una región existente    |

### 🔹 Ciudades

#### Listado de Ciudades
`GET /api/ciudades/`

Lista todas las ciudades con filtrado por nombre, región ID o nombre de región.

##### Parámetros de consulta disponibles:
| Parámetro      | Tipo   | Descripción                                    | Ejemplo                       |
|----------------|--------|------------------------------------------------|-------------------------------|
| `nombre`       | str    | Filtrar por nombre (búsqueda parcial)          | `nombre=santiago`             |
| `region_id`    | int    | Filtrar por ID de región                       | `region_id=1`                 |
| `region_nombre`| str    | Filtrar por nombre de región                   | `region_nombre=metropolitana` |

##### Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "nombre": "Santiago",
    "region": 1
  }
]
```

#### Operaciones CRUD de Ciudades

| Método | Ruta                    | Descripción                      |
|--------|-------------------------|----------------------------------|
| POST   | `/api/ciudades/`        | Crear una nueva ciudad           |
| GET    | `/api/ciudades/{id}/`   | Obtener detalle de una ciudad    |
| PUT    | `/api/ciudades/{id}/`   | Actualizar una ciudad existente  |
| DELETE | `/api/ciudades/{id}/`   | Eliminar una ciudad existente    |

### 🔹 Comunas

#### Listado de Comunas
`GET /api/comunas/`

Lista todas las comunas con filtrado por nombre, ciudad ID o nombre de ciudad.

##### Parámetros de consulta disponibles:
| Parámetro      | Tipo   | Descripción                                    | Ejemplo                  |
|----------------|--------|------------------------------------------------|--------------------------|
| `nombre`       | str    | Filtrar por nombre (búsqueda parcial)          | `nombre=santiago`        |
| `ciudad_id`    | int    | Filtrar por ID de ciudad                       | `ciudad_id=1`            |
| `ciudad_nombre`| str    | Filtrar por nombre de ciudad                   | `ciudad_nombre=santiago` |

##### Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "nombre": "Santiago Centro",
    "ciudad": 1
  }
]
```

#### Operaciones CRUD de Comunas

| Método | Ruta                    | Descripción                      |
|--------|-------------------------|----------------------------------|
| POST   | `/api/comunas/`         | Crear una nueva comuna           |
| GET    | `/api/comunas/{id}/`    | Obtener detalle de una comuna    |
| PUT    | `/api/comunas/{id}/`    | Actualizar una comuna existente  |
| DELETE | `/api/comunas/{id}/`    | Eliminar una comuna existente    |

### 🔹 Planes PPDA

#### Listado de Planes PPDA
`GET /api/planes/`

Lista todos los planes PPDA con filtrado por nombre, mes, año y comuna.

##### Parámetros de consulta disponibles:
| Parámetro      | Tipo   | Descripción                                    | Ejemplo                  |
|----------------|--------|------------------------------------------------|--------------------------|
| `nombre`       | str    | Filtrar por nombre (búsqueda parcial)          | `nombre=descontaminacion`|
| `mes_reporte`  | int    | Filtrar por mes de reporte (1-12)              | `mes_reporte=6`          |
| `anio`         | int    | Filtrar por año                                | `anio=2024`              |
| `comuna_id`    | int    | Filtrar por ID de comuna                       | `comuna_id=1`            |

##### Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "nombre": "Plan de Descontaminación",
    "anio": 2024,
    "mes_reporte": 6,
    "comunas": [1, 2, 3]
  }
]
```

#### Operaciones CRUD de Planes PPDA

| Método | Ruta                    | Descripción                      |
|--------|-------------------------|----------------------------------|
| POST   | `/api/planes/`          | Crear un nuevo plan PPDA         |
| GET    | `/api/planes/{id}/`     | Obtener detalle de un plan PPDA  |
| PUT    | `/api/planes/{id}/`     | Actualizar un plan PPDA existente|
| DELETE | `/api/planes/{id}/`     | Eliminar un plan PPDA existente  |

### 🔹 Organismos Responsables

#### Listado de Organismos Responsables
`GET /api/organismo-responsable/`

Lista todos los organismos responsables con filtrado por nombre.

##### Parámetros de consulta disponibles:
| Parámetro | Tipo   | Descripción                                    | Ejemplo                  |
|-----------|--------|------------------------------------------------|--------------------------|
| `nombre`  | str    | Filtrar por nombre (búsqueda parcial)          | `nombre=ministerio`      |

##### Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "nombre": "Ministerio del Medio Ambiente"
  }
]
```

#### Operaciones CRUD de Organismos Responsables

| Método | Ruta                               | Descripción                      |
|--------|------------------------------------|----------------------------------|
| POST   | `/api/organismo-responsable/`      | Crear un nuevo organismo         |
| GET    | `/api/organismo-responsable/{id}/` | Obtener detalle de un organismo  |
| PUT    | `/api/organismo-responsable/{id}/` | Actualizar un organismo existente|
| DELETE | `/api/organismo-responsable/{id}/` | Eliminar un organismo existente  |

### 🔹 Medidas

#### Listado de Medidas
`GET /api/medidas/`

Lista todas las medidas con filtrado por nombre corto, referencia PDA, plan y organismo.

##### Parámetros de consulta disponibles:
| Parámetro       | Tipo   | Descripción                                    | Ejemplo                   |
|-----------------|--------|------------------------------------------------|---------------------------|
| `nombre_corto`  | str    | Filtrar por nombre corto                       | `nombre_corto=reduccion`  |
| `referencia_pda`| str    | Filtrar por referencia PDA                     | `referencia_pda=PPDA-2024`|
| `plan_id`       | int    | Filtrar por ID de plan                         | `plan_id=1`               |
| `organismo_id`  | int    | Filtrar por ID de organismo                    | `organismo_id=2`          |

##### Ejemplo de respuesta:
```json
[
  {
    "id": 1,
    "nombre_corto": "Reducción de emisiones",
    "referencia_pda": "PPDA-2024-001",
    "plan": 1,
    "organismos": [1, 2]
  }
]
```

#### Operaciones CRUD de Medidas

| Método | Ruta                    | Descripción                      |
|--------|-------------------------|----------------------------------|
| POST   | `/api/medidas/`         | Crear una nueva medida           |
| GET    | `/api/medidas/{id}/`    | Obtener detalle de una medida    |
| PUT    | `/api/medidas/{id}/`    | Actualizar una medida existente  |
| DELETE | `/api/medidas/{id}/`    | Eliminar una medida existente    |

### Notas Generales
- Las búsquedas por nombre son:
  - Parciales (contienen el texto buscado)
  - No distinguen entre mayúsculas y minúsculas
  - Ignoran tildes y acentos

## Reportes

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
  "next": "http://localhost:8000/api/reportes/?page=1",
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

