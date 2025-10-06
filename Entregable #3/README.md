# Sistema de Gestión Académica

Sistema completo para administrar estudiantes, profesores y asignaturas en instituciones educativas.

## Características Principales
- Gestión completa de Estudiantes, Profesores y Asignaturas
- Exportación de reportes en PDF y Excel
- Interfaz gráfica intuitiva y fácil de usar
- Base de datos MySQL para almacenamiento seguro
- Búsquedas rápidas y filtros avanzados

## Requisitos del Sistema
- Python 3.6 o superior
- MySQL Server 5.7+
- Sistema operativo Windows, Mac o Linux

## Instalación Rápida
1. Descargar el proyecto desde GitHub
2. Renombrar `config_ejemplo.json` a `config.json`
3. Editar `config.json` con tus datos de MySQL
4. Crear la base de datos en MySQL
5. Ejecutar: `python main.py`


## Uso de la Aplicación

1. Ejecutar el comando: `python main.py`
2. La aplicación mostrará una ventana con tres pestañas:
   - **Asignaturas**: Gestionar materias y planes de estudio
   - **Profesores**: Administrar información del personal docente  
   - **Estudiantes**: Gestionar datos de alumnos y matrículas
3. En cada pestaña usar los botones:
   - **Guardar**: Agregar nuevos registros
   - **Buscar**: Encontrar registros existentes
   - **Actualizar**: Modificar información
   - **Eliminar**: Remover registros
   - **Limpiar**: Vaciar formularios
4. Para exportar datos usar:
   - **Exportar PDF**: Generar reporte en formato PDF
   - **Exportar Excel**: Generar reporte en formato Excel

## Estructura del Proyecto

- **`main.py`** - Archivo principal que inicia la aplicación
- **`models/`** - Contiene la conexión a base de datos y modelos de datos
  - `database.py` - Gestión de conexión MySQL
  - `asignaturas_model.py` - Operaciones con asignaturas
  - `profesores_model.py` - Operaciones con profesores
  - `estudiantes_model.py` - Operaciones con estudiantes
- **`controllers/`** - Contiene la lógica de la aplicación
  - `asignaturas_controller.py` - Funciones para gestionar asignaturas
  - `profesores_controller.py` - Funciones para gestionar profesores
  - `estudiantes_controller.py` - Funciones para gestionar estudiantes
- **`views/`** - Contiene las interfaces de usuario
  - `asignaturas_view.py` - Interfaz de asignaturas
  - `profesores_view.py` - Interfaz de profesores
  - `estudiantes_view.py` - Interfaz de estudiantes
- **`config.json`** - Archivo de configuración de la base de datos


## Solución de Problemas

### Error de Conexión a Base de Datos
- Verificar que MySQL esté ejecutándose
- Confirmar que los datos en `config.json` sean correctos
- Asegurar que la base de datos exista en MySQL

### Dependencias Faltantes
  pip install mysql-connector-python

  pip install fpdf

  pip install XlsxWriter