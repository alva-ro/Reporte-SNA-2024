# Proyecto Reporte SNA 2024

## Descripción
Proyecto Python Backend desarrollado con Django Rest Framework para la disponibilización de indicadores y métodos de verificación en evaluación ambiental.

## Organización de Tareas
Puedes ver el backlog y la organización de tareas en el siguiente enlace:
[Taiga - Reporte SNA 2024](https://tree.taiga.io/project/paulyval-reporte-sna-2024/epics)

## Historias de Usuario
Nuestro proyecto se define a partir de la siguiente historia de usuario, la cual ayudó a definir y priorizar nuestras tareas.

### Disponibilización de Indicadores y Métodos de Verificación

**Descripción:**  
Como miembro de la SEREMI del Medio Ambiente, quiero disponibilizar información sobre indicadores de evaluación ambiental **ordenada y filtrada** para que los organismos responsables puedan usarla y entender los criterios e indicadores que deben reportar a la superintendencia.

**Criterios de Aceptación:**
- La información sobre indicadores y criterios está organizada y disponible en un formato accesible.
- Los filtros permiten obtener datos específicos según la región o tipo de medida.

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
- **Obtener comunas**: `GET /api/comunas/`
- **Insertar comuna**: `POST /api/comunas/`

- **Obtener ciudades**: `GET /api/ciudades/`
- **Insertar ciudad**: `POST /api/ciudades/`

- **Obtener regiones**: `GET /api/regiones/`
- **Insertar región**: `POST /api/regiones/`

- **Obtener planes PPDA**: `GET /api/planes/`
- **Insertar plan PPDA**: `POST /api/planes/`

## Disclaimer
Estos primeros endpoints de esta API están diseñados para ser utilizados **únicamente de manera interna por los administradores**. Como siguiente paso, se planea implementar un sistema de **autenticación y autorización** basado en usuarios para garantizar la seguridad y el control de acceso a los recursos. Los endpoint ciudades y regiones fueron integrados para mantener la coherencia de datos.

---

### **Próximos pasos**
1. Implementar autenticación basada en tokens.
2. Añadir roles y permisos para controlar el acceso a los endpoints.
3. Documentar el proceso de autenticación y autorización para los administradores.
4. Crear nuevos endpoints para filtrar planes por región, comuna y organismos responsables.


Para más detalles, consulta la documentación en:
```
http://127.0.0.1:8000/api/docs/#/
```
