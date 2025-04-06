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
3. Integrar rate limiting


Para más detalles, consulta la documentación en:
```
http://127.0.0.1:8000/api/docs/#/
```
