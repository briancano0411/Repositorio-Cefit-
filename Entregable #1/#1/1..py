
import tkinter as tk
from tkinter import ttk

# Crear la ventana principal
root = tk.Tk()
root.geometry('1000x600')
root.title("Horizonte Del Saber")

# Crear el widget Notebook (pestañas)
notebook = ttk.Notebook(root)

# Crear los frames que irán dentro de las pestañas
tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)
tab5 = ttk.Frame(notebook)
tab6 = ttk.Frame(notebook)
tab7 = ttk.Frame(notebook)
tab8 = ttk.Frame(notebook)
tab9 = ttk.Frame(notebook)

# Añadir las pestañas al Notebook
notebook.add(tab1, text="Asignaturas")
notebook.add(tab2, text="Aulas")
notebook.add(tab3, text="Profesores")
notebook.add(tab4, text="Calificaciones" )
notebook.add(tab5, text="Bibioteca" )
notebook.add(tab6, text="Cursos" )
notebook.add(tab7, text="Estudiantes")
notebook.add(tab8, text="PlanDeEstudio")
notebook.add(tab9, text="Prestamos")



# Empaquetar el Notebook para que se muestre en la ventana
notebook.pack(expand=True, fill="both")

# CONTENIDO DE LA PESTAÑA 1 (ASIGNATURAS)
# Título
titulo = tk.Label(tab1,
                  text="FORMULARIO DE ASIGNATURAS",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab1)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: AsignaturasID (Izquierda)
tk.Label(left_frame, text="AsignaturasID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
AsignaturasID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
AsignaturasID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Cod_Asignaturas (Izquierda)
tk.Label(left_frame, text="CodAsignaturas:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CodAsignaturas = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CodAsignaturas.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Nombre_Asignaturas (Izquierda)
tk.Label(left_frame, text="NombreAsignaturas:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
NombreAsignaturas = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
NombreAsignaturas.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Area_Crecimiento (Izquierda)
tk.Label(left_frame, text="AreaCrecimiento:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
AreaCrecimiento = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
AreaCrecimiento.grid(row=4, column=1, sticky="w", pady=10)

# Fila 5: Horas_Tecnicas (Izquierda)
tk.Label(left_frame, text="HorasTecnicas:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
HorasTecnicas = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
HorasTecnicas.grid(row=5, column=1, sticky="w", pady=10)

# Fila 6: Horas_Practicas (Izquierda)
tk.Label(left_frame, text="HorasPracticas:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
HorasPracticas = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
HorasPracticas.grid(row=6, column=1, sticky="w", pady=10)

# Fila 7: Creditos_Academicos (Derecha)
tk.Label(right_frame, text="CreditosAcademicos:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
CreditosAcademicos = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CreditosAcademicos.grid(row=1, column=1, sticky="w", pady=10)

# Fila 8: Requisitos_Previos (Derecha)
tk.Label(right_frame, text="RequisitoPrevios:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
RequisitoPrevios = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
RequisitoPrevios.grid(row=2, column=1, sticky="w", pady=10)

# Fila 9: Objetivos_Generales (Derecha)
tk.Label(right_frame, text="ObjetivosGenerales:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
ObjetivosGenerales = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
ObjetivosGenerales.grid(row=3, column=1, sticky="w", pady=10)

# Fila 10: Objetivos_Especifico (Derecha)
tk.Label(right_frame, text="ObjetivosEspecificos:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
ObjetivosEspecificos = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
ObjetivosEspecificos.grid(row=4, column=1, sticky="w", pady=10)

# Fila 11: Bibliografia_Recomendada (Derecha)
tk.Label(right_frame, text="Bibliografia Recomendada:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
BibliografiaRecomendada = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
BibliografiaRecomendada.grid(row=5, column=1, sticky="w", pady=10)

# Fila 12: Periodo (Derecha)
tk.Label(right_frame, text="Periodo:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
Periodo = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Periodo.grid(row=6, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)



# CONTENIDO DE LA PESTAÑA 2 (AULAS)
# Título
titulo = tk.Label(tab2,
                  text="FORMULARIO DE AULAS",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab2)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: AulasID (Izquierda)
tk.Label(left_frame, text="AulasID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
AulasID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
AulasID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Numero_Identificador (Izquierda)
tk.Label(left_frame, text="NumeroIdentificador:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
NumeroIdentificador = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
NumeroIdentificador.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Nombre del Edificio (Izquierda)
tk.Label(left_frame, text="Edificio:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
Edificio = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Edificio.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Numero de piso (Izquierda)
tk.Label(left_frame, text="NumeroPiso:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
NumeroPiso = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
NumeroPiso.grid(row=4, column=1, sticky="w", pady=10)

# Fila 5: Capacidad_Estudiantes (Derecha)
tk.Label(right_frame, text="CapacidadEstudiantes:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
CapacidadEstudiantes = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CapacidadEstudiantes.grid(row=1, column=1, sticky="w", pady=10)

# Fila 6: Tipo de curso (Derecha)
tk.Label(right_frame, text="TipoCurso:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
TipoCurso = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
TipoCurso.grid(row=2, column=1, sticky="w", pady=10)

# Fila 7: Equipamiento_Disponible (Derecha)
tk.Label(right_frame, text="EquipamientoDisponible:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
EquipamientoDisponible = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
EquipamientoDisponible.grid(row=3, column=1, sticky="w", pady=10)

# Fila 8: Estado_Actual (Derecha)
tk.Label(right_frame, text="EstadoActual:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
EstadoActual = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
EstadoActual.grid(row=4, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(tab2)
button_frame.pack(pady=20)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)


# CONTENIDO DE LA PESTAÑA 3 (Profesores)
# Título
titulo = tk.Label(tab3,
                  text="FORMULARIO DE PROFESORES",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab3)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: ProfesoresID (Izquierda)
tk.Label(left_frame, text="ProfesoresID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
ProfesoresID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
ProfesoresID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Codigo del empleado (Izquierda)
tk.Label(left_frame, text="CodigoEmpleado:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CodigoEmplead = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoEmplead.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: nombre del profesor (Izquierda)
tk.Label(left_frame, text="Nombre:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
Nombre = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Nombre.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: apellido del profesor (Izquierda)
tk.Label(left_frame, text="Apellido:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
Apellido = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Apellido.grid(row=4, column=1, sticky="w", pady=10)

# Fila 5: dni (Izquierda)
tk.Label(left_frame, text="DNI:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
DNI = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
DNI.grid(row=5, column=1, sticky="w", pady=10)

# Fila 6: Fecha nacimiento (Izquierda)
tk.Label(left_frame, text="FechaNacimiento:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
FechaNacimiento = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaNacimiento.grid(row=6, column=1, sticky="w", pady=10)

# Fila 7: Direccion (Izquierda)
tk.Label(left_frame, text="Direccion:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=10)
Direccion = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Direccion.grid(row=7, column=1, sticky="w", pady=10)

# Fila 8: Telefono (Derecha)
tk.Label(right_frame, text="Telefono:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
Telefono = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Telefono.grid(row=1, column=1, sticky="w", pady=10)

# Fila 9: Correo Institucional (Derecha)
tk.Label(right_frame, text="CorreoInstitucional:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CorreoInstitucional = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CorreoInstitucional.grid(row=2, column=1, sticky="w", pady=10)

# Fila 10: Nivel de formacion academica (Derecha)
tk.Label(right_frame, text="NivelAcademico:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
NivelAcademico = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
NivelAcademico.grid(row=3, column=1, sticky="w", pady=10)

# Fila 11: Especialidad (Derecha)
tk.Label(right_frame, text="Especialidad:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
Especialidad = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Especialidad.grid(row=4, column=1, sticky="w", pady=10)

# Fila 12: Años de experiencia (Derecha)
tk.Label(right_frame, text="AñosExperiencia:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
AñosExperiencia = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
AñosExperiencia.grid(row=5, column=1, sticky="w", pady=10)

# Fila 13: Fecha de contratacion (Derecha)
tk.Label(right_frame, text="FechaContratacion:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
FechaContratacion = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaContratacion.grid(row=6, column=1, sticky="w", pady=10)

# Fila 14: Tipo de contrato (Derecha)
tk.Label(right_frame, text="TipoContrato:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=10)
TipoContrato = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
TipoContrato.grid(row=7, column=1, sticky="w", pady=10)

# Fila 15: Curso especializado (Derecha)
tk.Label(right_frame, text="CursoEspecializado:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=10)
CursoEspecializado = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CursoEspecializado.grid(row=8, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(tab3)
button_frame.pack(pady=20)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)

# CONTENIDO DE LA PESTAÑA 4 (Calificaciones)
# Título
titulo = tk.Label(tab4,
                  text="FORMULARIO DE CALIFICACIONES",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab4)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: CalificacionesID (Izquierda)
tk.Label(left_frame, text="CalificacionesID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
CalificacionesID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CalificacionesID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Tipo de evaluacion (Izquierda)
tk.Label(left_frame, text="TipoEvaluacion:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
TipoEvaluacion = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
TipoEvaluacion.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Fecha Calificado (Izquierda)
tk.Label(left_frame, text="FechaCalificado:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
FechaCalificado = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaCalificado.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Nota (Derecha)
tk.Label(right_frame, text="Nota:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
Nota = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Nota.grid(row=1, column=1, sticky="w", pady=10)

# Fila 5: Porcentaje Total (Derecha)
tk.Label(right_frame, text="CursoEspecializado:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CursoEspecializado = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CursoEspecializado.grid(row=2, column=1, sticky="w", pady=10)

# Fila 6: Observaciones (Derecha)
tk.Label(right_frame, text="FechaNacimiento:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
FechaNacimiento = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaNacimiento.grid(row=3, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)

# CONTENIDO DE LA PESTAÑA 5 (Biblioteca)
# Título
titulo = tk.Label(tab5,
                  text="FORMULARIO DE BIBLIOTECA",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab5)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: CalificacionesID (Izquierda)
tk.Label(left_frame, text="BibliotecaID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
BibliotecaID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
BibliotecaID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Codigo Material Bibliografico (Izquierda)
tk.Label(left_frame, text="CodigoMaterialBiblioteca:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CodigoMaterialBiblioteca = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoMaterialBiblioteca.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Titulo (Izquierda)
tk.Label(left_frame, text="Titulo:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
Titulo = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Titulo.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Actores (Izquierda)
tk.Label(left_frame, text="Actores:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
Actores = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Actores.grid(row=4, column=1, sticky="w", pady=10)

# Fila 5: Editorial (Izquierda)
tk.Label(left_frame, text="Editorial:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
Editorial = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Editorial.grid(row=5, column=1, sticky="w", pady=10)

# Fila 6: Año Publicado (Izquierda)
tk.Label(left_frame, text="AñoPublicado:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
AñoPublicado = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
AñoPublicado.grid(row=6, column=1, sticky="w", pady=10)

# Fila 7: ISBN (Derecha)
tk.Label(right_frame, text="ISBN:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
ISBN = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
ISBN.grid(row=1, column=1, sticky="w", pady=10)

# Fila 8: Categoria Tematica (Derecha)
tk.Label(right_frame, text="CategoriaTematica:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CategoriaTematica = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CategoriaTematica.grid(row=2, column=1, sticky="w", pady=10)

# Fila 9: Formato (Derecha)
tk.Label(right_frame, text="Formato:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
Formato = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Formato.grid(row=3, column=1, sticky="w", pady=10)

# Fila 10: Cantidad Disponible (Derecha)
tk.Label(right_frame, text="CantidadDisponible:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
CantidadDisponible = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CantidadDisponible.grid(row=4, column=1, sticky="w", pady=10)

# Fila 11: Ubicacion Fisica (Derecha)
tk.Label(right_frame, text="UbicacionFisica:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
UbicacionFisica = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
UbicacionFisica.grid(row=5, column=1, sticky="w", pady=10)

# Fila 12: Edicion (Derecha)
tk.Label(right_frame, text="Edicion:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
Edicion = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Edicion.grid(row=6, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)

# CONTENIDO DE LA PESTAÑA 6 (Cursos)
# Título
titulo = tk.Label(tab6,
                  text="FORMULARIO DE CURSOS",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab6)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: CursosID (Izquierda)
tk.Label(left_frame, text="CursosID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
CursosID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CursosID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Periodo Academico (Izquierda)
tk.Label(left_frame, text="PeriodoAcademico:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
PeriodoAcademico = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
PeriodoAcademico.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Horarios (Izquierda)
tk.Label(left_frame, text="Horarios:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
Horarios = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Horarios.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Cupo Maximo (Derecha)
tk.Label(right_frame, text="CupoMaximo:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
CupoMaximo = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CupoMaximo.grid(row=1, column=1, sticky="w", pady=10)

# Fila 5: Metodologia Evaluacion (Derecha)
tk.Label(right_frame, text="MetodologiaEvaluacion :", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
MetodologiaEvaluacion  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
MetodologiaEvaluacion .grid(row=2, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)

# CONTENIDO DE LA PESTAÑA 7 (Estudiantes)
# Título
titulo = tk.Label(tab7,
                  text="FORMULARIO DE ESTUDIANTES ",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab7)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: EstudiantesID (Izquierda)
tk.Label(left_frame, text="EstudiantesID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
EstudiantesID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
EstudiantesID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Matricula (Izquierda)
tk.Label(left_frame, text="Matricula:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
Matricula = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Matricula.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Nombre (Izquierda)
tk.Label(left_frame, text="Nombre:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
Nombre = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Nombre.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Apellido (Izquierda)
tk.Label(left_frame, text="Apellido:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
Apellido = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Apellido.grid(row=4, column=1, sticky="w", pady=10)

# Fila 5: DNI (Izquierda)
tk.Label(left_frame, text="DNI :", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
DNI  = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
DNI .grid(row=5, column=1, sticky="w", pady=10)

# Fila 6: Telefono (Izquierda)
tk.Label(left_frame, text="Telefono :", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
Telefono = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Telefono .grid(row=6, column=1, sticky="w", pady=10)

# Fila 7: CorreoInstitucional (Derecha)
tk.Label(right_frame, text="CorreoInstitucional:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
CorreoInstitucional  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CorreoInstitucional.grid(row=1, column=1, sticky="w", pady=10)

# Fila 8: Fotografia (Derecha)
tk.Label(right_frame, text="Fotografia :", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
Fotografia = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Fotografia .grid(row=2, column=1, sticky="w", pady=10)

# Fila 9: Nombre Acudiente (Derecha)
tk.Label(right_frame, text="NombreAcudiente :", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
NombreAcudiente  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
NombreAcudiente .grid(row=3, column=1, sticky="w", pady=10)

# Fila 10: Contacto Emergencia (Derecha)
tk.Label(right_frame, text="ContactoEmergencia:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
ContactoEmergencia  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
ContactoEmergencia .grid(row=4, column=1, sticky="w", pady=10)

# Fila 11: Fecha Ingreso (Derecha)
tk.Label(right_frame, text="FechaIngreso :", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=10)
FechaIngreso  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaIngreso .grid(row=5, column=1, sticky="w", pady=10)

# Fila 12: Periodo (Derecha)
tk.Label(right_frame, text="Periodo :", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=10)
Periodo  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Periodo .grid(row=6, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)

# CONTENIDO DE LA PESTAÑA 8 (Plan De Estudio)
# Título
titulo = tk.Label(tab8,
                  text="FORMULARIO PLAN DE ESTUDIO ",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab8)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: Plan EstudioID (Izquierda)
tk.Label(left_frame, text="PlanEstudioID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
PlanEstudioID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
PlanEstudioID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Codigo PlanDe Estudio (Izquierda)
tk.Label(left_frame, text="CodigoPlanDeEstudio:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CodigoPlanDeEstudio = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoPlanDeEstudio.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Carrera Perteneciente (Izquierda)
tk.Label(left_frame, text="CarreraPerteneciente:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
CarreraPerteneciente = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CarreraPerteneciente.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Fecha Aprobacion (Derecha)
tk.Label(right_frame, text="FechaAprobacion:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
FechaAprobacion = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaAprobacion.grid(row=1, column=1, sticky="w", pady=10)

# Fila 5: Nivel Asignatura (Derecha)
tk.Label(right_frame, text="NivelAsignatura :", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
NivelAsignatura  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
NivelAsignatura .grid(row=2, column=1, sticky="w", pady=10)

# Fila 6: Requisitos Graduacion (Derecha)
tk.Label(right_frame, text="RequisitosGraduacion :", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
RequisitosGraduacion  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
RequisitosGraduacion .grid(row=3, column=1, sticky="w", pady=10)

# Fila 7: Creditos Totales (Derecha)
tk.Label(right_frame, text="CreditosTotales :", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=10)
CreditosTotales  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CreditosTotales .grid(row=4, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)

# CONTENIDO DE LA PESTAÑA 9 (Prestamo
# Título
titulo = tk.Label(tab9,
                  text="FORMULARIO PLAN DE PRESTAMO ",
                  font=("Arial", 16, "bold"),
                  fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame = tk.Frame(tab9)
form_frame.pack(pady=20, anchor="w", padx=50)

# Columna izquierda
left_frame = tk.Frame(form_frame)
left_frame.grid(row=0, column=0, padx=(0, 20))

# Columna derecha
right_frame = tk.Frame(form_frame)
right_frame.grid(row=0, column=1)

# Fila 1: PrestamosID (Izquierda)
tk.Label(left_frame, text="PrestamosID", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(1, 10), pady=10)
PrestamosID = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
PrestamosID.grid(row=1, column=1, sticky="w", pady=10)

# Fila 2: Codigo De Prestamo (Izquierda)
tk.Label(left_frame, text="CodigoPrestamo:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
CodigoPrestamo = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoPrestamo.grid(row=2, column=1, sticky="w", pady=10)

# Fila 3: Fecha Prestamo (Izquierda)
tk.Label(left_frame, text="FechaPrestamo:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
FechaPrestamo = tk.Entry(left_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaPrestamo.grid(row=3, column=1, sticky="w", pady=10)

# Fila 4: Fecha Devolucion (Derecha)
tk.Label(right_frame, text="FechaDevolucion:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=10)
FechaDevolucion= tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaDevolucion.grid(row=1, column=1, sticky="w", pady=10)

# Fila 5: Multas Aplicadas (Derecha)
tk.Label(right_frame, text="MultasAplicadas :", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=10)
MultasAplicadas = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
MultasAplicadas .grid(row=2, column=1, sticky="w", pady=10)

# Fila 6: Estado (Derecha)
tk.Label(right_frame, text="Estado :", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=10)
Estado  = tk.Entry(right_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
Estado .grid(row=3, column=1, sticky="w", pady=10)

# Frame para botones
button_frame = tk.Frame(form_frame)
button_frame.grid(row=1, column=0, columnspan=2, pady=20)

# Botones de acción - CENTRADOS
btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 12), bg="#4CAF50", fg="white", width=10)
btn_save.pack(side=tk.LEFT, padx=5)

btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 12), bg="#2196F3", fg="white", width=10)
btn_update.pack(side=tk.LEFT, padx=5)

btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 12), bg="#f44336", fg="white", width=10)
btn_delete.pack(side=tk.LEFT, padx=5)

btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 12), bg="#FF9800", fg="white", width=10)
btn_clear.pack(side=tk.LEFT, padx=5)


root.mainloop()