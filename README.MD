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
- **drf-spectacular** (Documentación APi)

## Instalación y Configuración
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/alva-ro/Reporte-SNA-2024
   ```
2. **Configurar las variables de entorno** en `.env`.
   En la raíz del proyecto crear el archivo .env con las configuraciones enviadas vía mail.

3. **Crear y activar un entorno virtual**:
   ```bash
   python -m venv sna_env
   source sna_env/bin/activate  # En Windows: sna_env\Scripts\activate
   ```
4. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt

5. **Levantar el servidor**:
   ```bash
   python manage.py runserver
   ```

## API Endpoints Principales
- **comunas**: `/api/comunas/`
- **ciudades**: `/api/ciudades/`
- **organismos responsales**: `/api/organismo-responsable/`
- **planes ppda**: `/api/planes/`
- **regiones**: `/api/regiones/`


## Información entrega 2
En esta segunda entrega nuestro foco principal fue integrar seguridad a nuestros endpoints a través de token JWT, asignando roles y permisos para controlar los accesos. 

---

### **Próximos pasos**
1. Documentar el proceso de autenticación y autorización para los administradores.
2. Crear nuevos endpoints para mejorar las opciones de filtrados.
3. Integrar rate limiting.
4. Fortacer validaciones en endpoints críticos.


Para más detalles, consulta la documentación en:
```
http://127.0.0.1:8000/api/docs/#/
```

## Búsqueda por Nombre

El sistema permite buscar entidades por nombre utilizando parámetros de consulta (query params). La búsqueda es:
- Parcial (contiene el texto buscado)
- No distingue entre mayúsculas y minúsculas
- Ignora tildes y acentos

### Endpoints con búsqueda por nombre:

1. **Comunas**
   ```
   GET /comunas/?nombre=valor
   GET /comunas/?ciudad_id=valor
   GET /comunas/?ciudad_nombre=valor
   ```
   Ejemplos:
   - `/comunas/?nombre=santiago` encontrará "Santiago", "Sántiago", "SANTIAGO", etc.
   - `/comunas/?ciudad_id=1` encontrará todas las comunas de la ciudad con ID 1
   - `/comunas/?ciudad_nombre=santiago` encontrará todas las comunas de la ciudad Santiago
   - `/comunas/?ciudad_nombre=santiago&nombre=centro` encontrará las comunas de la ciudad Santiago que contengan "centro" en su nombre

2. **Ciudades**
   ```
   GET /ciudades/?nombre=valor
   GET /ciudades/?region_id=valor
   GET /ciudades/?region_nombre=valor
   ```
   Ejemplos:
   - `/ciudades/?nombre=santiago` encontrará "Santiago", "Sántiago", "SANTIAGO", etc.
   - `/ciudades/?region_id=1` encontrará todas las ciudades de la región con ID 1
   - `/ciudades/?region_nombre=metropolitana` encontrará todas las ciudades de la región Metropolitana
   - `/ciudades/?region_nombre=metropolitana&nombre=santiago` encontrará las ciudades de la región Metropolitana que contengan "santiago" en su nombre

3. **Regiones**
   ```
   GET /regiones/?nombre=valor
   ```
   Ejemplo: `/regiones/?nombre=metropolitana` encontrará "Metropolitana", "METROPOLITANA", etc.

4. **Planes PPDA**
   ```
   GET /planes/?nombre=valor
   GET /planes/?mes_reporte=valor
   GET /planes/?anio=valor
   GET /planes/?comuna_id=valor
   ```
   Ejemplos:
   - `/planes/?nombre=descontaminacion` encontrará "Descontaminación", "DESCONTAMINACION", etc.
   - `/planes/?mes_reporte=6` encontrará todos los planes con mes de reporte 6 (junio)
   - `/planes/?anio=2024` encontrará todos los planes del año 2024
   - `/planes/?comuna_id=1` encontrará todos los planes que incluyan la comuna con ID 1
   - `/planes/?anio=2024&mes_reporte=6` encontrará todos los planes del año 2024 con mes de reporte 6
   - `/planes/?comuna_id=1&nombre=santiago` encontrará todos los planes que incluyan la comuna con ID 1 y contengan "santiago" en su nombre

5. **Organismos Responsables**
   ```
   GET /organismo-responsable/?nombre=valor
   ```
   Ejemplo: `/organismo-responsable/?nombre=ministerio` encontrará "Ministerio", "MINISTERIO", etc.

6. **Medidas**
   ```
   GET /medidas/?nombre_corto=valor
   GET /medidas/?referencia_pda=valor
   GET /medidas/?plan_id=valor
   GET /medidas/?organismo_id=valor
   ```
   Ejemplos:
   - `/medidas/?nombre_corto=reduccion` encontrará medidas con "reducción" en su nombre corto
   - `/medidas/?referencia_pda=PPDA-2024` encontrará medidas con referencia PDA que contengan "PPDA-2024"
   - `/medidas/?plan_id=1` encontrará todas las medidas del plan PPDA con ID 1
   - `/medidas/?organismo_id=2` encontrará todas las medidas asignadas al organismo con ID 2
   - `/medidas/?plan_id=1&organismo_id=2` encontrará las medidas del plan con ID 1 que estén asignadas al organismo con ID 2

### Notas:
- Si no se proporciona el parámetro `nombre`, se devuelven todos los registros
- La búsqueda es parcial (encuentra coincidencias en cualquier parte del nombre)