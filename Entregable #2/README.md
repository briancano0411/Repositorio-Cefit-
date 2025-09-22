# Sistema de Gestión Académica - Horizonte del Saber

## Descripción
Esta es una aplicación de escritorio desarrollada en Python con Tkinter para gestionar un sistema académico. Incluye módulos para manejar asignaturas, aulas, profesores, calificaciones, biblioteca, cursos, estudiantes, planes de estudio y préstamos. La aplicación se conecta a una base de datos MySQL para almacenar y recuperar datos.

## Requisitos
- Python 3.6 o superior
- Tkinter (incluido en Python estándar)
- mysql-connector-python (para conexión a MySQL)
- Servidor MySQL (con la base de datos `horizonte_del_saber_2` creada y las tablas correspondientes)

## Instalación
1. Instala las dependencias:  pip install mysql-connector-python
2. Configura la base de datos:
- Crea la base de datos `horizonte_del_saber_2` en MySQL.
- Asegúrate de que las tablas (asignaturas, aulas, profesores, etc.) existan. Puedes usar scripts SQL para crearlas si no están definidas.
- Actualiza las credenciales en el código (línea ~20): host, database, user, password.

3. Ejecuta el script principal: python nombre_del_archivo.py

## Uso
- La aplicación abre una ventana con pestañas para cada módulo (Asignaturas, Aulas, etc.).
- En cada pestaña, usa el formulario izquierdo para agregar/actualizar datos.
- La lista derecha muestra los registros de la base de datos.
- Botones: Guardar, Actualizar, Eliminar, Buscar, Limpiar.
- Selecciona un ítem en la lista para cargar datos en el formulario.

## Estructura del Proyecto
- **DatabaseConnection**: Clase para manejar la conexión a MySQL.
- **Funciones de validación**: Para números, fechas y campos requeridos.
- **Funciones por módulo**: save_*, update_*, delete_*, search_*, load_*.
- **Interfaz**: Pestañas con formularios y Treeviews para listas.

## Notas
- La aplicación usa procedimientos almacenados (SP) en MySQL para algunas operaciones; asegúrate de que existan (ej. `sp_InsertAsignatura`).
- Para desarrollo, ajusta los valores por defecto (ej. IDs fijos como 1).
- Si hay errores de conexión, verifica las credenciales de MySQL.

## Licencia
Proyecto de código abierto para fines educativos. Modifícalo según necesites.