# views/profesores_view.py
import tkinter as tk
from tkinter import ttk


def create_profesores_tab(tab, controller, model):
    main_frame = tk.Frame(tab)
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)

    left_frame = tk.Frame(main_frame)
    left_frame.pack(side="left", fill="y", padx=(0, 10))

    titulo = tk.Label(left_frame, text="GESTIÓN DE PROFESORES", font=("Arial", 16, "bold"), fg="blue")
    titulo.pack(pady=20)

    form_frame = tk.Frame(left_frame)
    form_frame.pack(pady=20, anchor="w", padx=20)

    fields = {}
    labels = [
        ("ProfesoresID", 1),
        ("CodigoEmplead", 2),
        ("Nombre", 3),
        ("Apellido", 4),
        ("DNI", 5),
        ("FechaNacimiento", 6),
        ("Direccion", 7),
        ("Telefono", 8),
        ("CorreoInstitucional", 9),
        ("NivelAcademico", 10),
        ("Especialidad", 11),
        ("AñosExperiencia", 12),
        ("FechaContratacion", 13),
        ("TipoContrato", 14),
        ("CursoEspecializado", 15)
    ]

    for label_text, row in labels:
        tk.Label(form_frame, text=label_text + ":", font=("Arial", 12)).grid(row=row, column=0, sticky="w",
                                                                             padx=(0, 10), pady=8)
        entry = tk.Entry(form_frame, width=25, font=("Arial", 12), relief="solid", bd=1)
        entry.grid(row=row, column=1, sticky="w", pady=8)
        fields[label_text] = entry

    button_frame = tk.Frame(left_frame)
    button_frame.pack(pady=20)

    btn_save = tk.Button(button_frame, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
    btn_update = tk.Button(button_frame, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
    btn_delete = tk.Button(button_frame, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
    btn_search = tk.Button(button_frame, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
    btn_clear = tk.Button(button_frame, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)

    btn_save.pack(side=tk.LEFT, padx=3)
    btn_update.pack(side=tk.LEFT, padx=3)
    btn_delete.pack(side=tk.LEFT, padx=3)
    btn_search.pack(side=tk.LEFT, padx=3)
    btn_clear.pack(side=tk.LEFT, padx=3)

    # Botones de exportación agregados
    export_frame = tk.Frame(left_frame)
    export_frame.pack(pady=10)

    btn_export_pdf = tk.Button(export_frame, text="Exportar PDF", font=("Arial", 10), bg="#000000", fg="white",
                               width=12)
    btn_export_excel = tk.Button(export_frame, text="Exportar Excel", font=("Arial", 10), bg="#000000", fg="white",
                                 width=12)

    btn_export_pdf.pack(side=tk.LEFT, padx=3)
    btn_export_excel.pack(side=tk.LEFT, padx=3)

    right_frame = tk.Frame(main_frame)
    right_frame.pack(side="right", fill="both", expand=True)

    tk.Label(right_frame, text="LISTA DE PROFESORES", font=("Arial", 14, "bold")).pack(pady=10)

    tree = ttk.Treeview(right_frame,
                        columns=('ID', 'Codigo', 'Nombre', 'Apellido', 'DNI', 'Nacimiento', 'Direccion', 'Telefono',
                                 'Correo', 'Nivel', 'Especialidad', 'Experiencia', 'Contratacion', 'Contrato'),
                        show='headings', height=20)
    headings = ['ID', 'Código', 'Nombre', 'Apellido', 'DNI', 'Nacimiento', 'Dirección', 'Teléfono', 'Correo',
                'Nivel Acad.', 'Especialidad', 'Experiencia', 'Contratación', 'Contrato']
    widths = [50, 80, 100, 100, 80, 100, 120, 80, 120, 100, 100, 80, 100, 100]

    for col, text, width in zip(tree['columns'], headings, widths):
        tree.heading(col, text=text)
        tree.column(col, width=width)

    tree.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Bind buttons to controller functions
    btn_save.config(command=lambda: controller.save_profesor(model, fields, tree))
    btn_update.config(command=lambda: controller.update_profesor(model, fields, tree))
    btn_delete.config(command=lambda: controller.delete_profesor(model, fields, tree))
    btn_search.config(command=lambda: controller.search_profesor(model, fields, tree))
    btn_clear.config(command=lambda: controller.clear_profesor_form(fields))

    # Bind export buttons to controller functions
    btn_export_pdf.config(command=lambda: controller.export_profesores_to_pdf(model))
    btn_export_excel.config(command=lambda: controller.export_profesores_to_excel(model))

    return fields, tree