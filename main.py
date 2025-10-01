import tkinter as tk
from tkinter import ttk

# Importa los módulos completos para evitar problemas de importación
import Models.database as database
import Models.asignatura_model as asignaturas_model
import Models.profesores_model as profesores_model
import Models.estudiantes_model as estudiantes_model

import Controllers.asignaturas_controller as asignaturas_controller
import Controllers.profesores_controller as profesores_controller
import Controllers.estudiantes_controller as estudiantes_controller

import View.asignaturas_view as asignaturas_view
import View.profesores_view as profesores_view
import View.estudiantes_view as estudiantes_view


def main():
    root = tk.Tk()
    root.geometry('1200x700')
    root.title("Sistema de Gestión Académica - Horizonte del Saber")

    db = database.DatabaseConnection()
    if not db.connect():
        root.destroy()
        return

    notebook = ttk.Notebook(root)

    tab_asignaturas = ttk.Frame(notebook)
    tab_profesores = ttk.Frame(notebook)
    tab_estudiantes = ttk.Frame(notebook)

    notebook.add(tab_asignaturas, text="Asignaturas")
    notebook.add(tab_profesores, text="Profesores")
    notebook.add(tab_estudiantes, text="Estudiantes")

    notebook.pack(expand=True, fill="both")

    # Crear modelos
    asignaturas_m = asignaturas_model.AsignaturasModel(db)
    profesores_m = profesores_model.ProfesoresModel(db)
    estudiantes_m = estudiantes_model.EstudiantesModel(db)

    # Crear vistas y obtener referencias a campos y treeviews
    asignaturas_fields, asignaturas_tree = asignaturas_view.create_asignaturas_tab(tab_asignaturas, asignaturas_controller, asignaturas_m)
    profesores_fields, profesores_tree = profesores_view.create_profesores_tab(tab_profesores, profesores_controller, profesores_m)
    estudiantes_fields, estudiantes_tree = estudiantes_view.create_estudiantes_tab(tab_estudiantes, estudiantes_controller, estudiantes_m)

    def on_closing():
        db.disconnect()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()
