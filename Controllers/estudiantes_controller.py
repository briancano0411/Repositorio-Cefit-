# controllers/estudiantes_controller.py
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import xlsxwriter
from fpdf import FPDF


def validate_numeric(value, field_name):
    if not value.strip():
        return True, None
    try:
        return True, float(value) if '.' in value else int(value)
    except ValueError:
        messagebox.showerror("Error de Validación", f"{field_name} debe ser un número válido")
        return False, None


def validate_required(value, field_name):
    if not value.strip():
        messagebox.showerror("Error de Validación", f"{field_name} es requerido")
        return False
    return True


def validate_date(date_string):
    if not date_string.strip():
        return True, None
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
        return True, date_obj
    except ValueError:
        messagebox.showerror("Error de Validación", "Fecha debe estar en formato YYYY-MM-DD")
        return False, None


def save_estudiante(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    Nombre_Est = form_fields['Nombre_Est']
    Apellido_Est = form_fields['Apellido_Est']
    DNI_Est = form_fields['DNI_Est']
    Matricula = form_fields['Matricula']
    Telefono_Est = form_fields['Telefono_Est']
    CorreoInstitucional_Est = form_fields['CorreoInstitucional_Est']
    NombreAcudiente = form_fields['NombreAcudiente']
    ContactoEmergencia = form_fields['ContactoEmergencia']
    FechaIngreso = form_fields['FechaIngreso']
    Periodo_Est = form_fields['Periodo_Est']

    if not validate_required(Nombre_Est.get(), "Nombre"):
        return

    if not validate_required(Apellido_Est.get(), "Apellido"):
        return

    if not validate_required(DNI_Est.get(), "DNI"):
        return

    matricula_valid, matricula_value = validate_numeric(Matricula.get(), "Matrícula")
    if not matricula_valid:
        return

    fecha_ing_valid, fecha_ing = validate_date(FechaIngreso.get())
    if not fecha_ing_valid:
        return

    parameters = (
        matricula_value,
        Nombre_Est.get(),
        Apellido_Est.get(),
        DNI_Est.get(),
        datetime.now().date(),
        "Dirección por defecto",
        Telefono_Est.get() if Telefono_Est.get().strip() else None,
        CorreoInstitucional_Est.get() if CorreoInstitucional_Est.get().strip() else None,
        NombreAcudiente.get() if NombreAcudiente.get().strip() else None,
        ContactoEmergencia.get() if ContactoEmergencia.get().strip() else None,
        fecha_ing,
        Periodo_Est.get() if Periodo_Est.get().strip() else None
    )

    success, result = model.insert_estudiante(parameters)

    if success:
        messagebox.showinfo("Éxito", "Estudiante guardado correctamente")
        clear_estudiante_form(form_fields)
        load_estudiantes_list(model, treeview)
    else:
        messagebox.showerror("Error", f"Error al guardar estudiante: {result}")


def update_estudiante(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    EstudiantesID = form_fields['EstudiantesID']
    Nombre_Est = form_fields['Nombre_Est']
    Apellido_Est = form_fields['Apellido_Est']
    DNI_Est = form_fields['DNI_Est']
    Matricula = form_fields['Matricula']
    Telefono_Est = form_fields['Telefono_Est']
    CorreoInstitucional_Est = form_fields['CorreoInstitucional_Est']
    NombreAcudiente = form_fields['NombreAcudiente']
    ContactoEmergencia = form_fields['ContactoEmergencia']
    Periodo_Est = form_fields['Periodo_Est']

    id_valid, est_id = validate_numeric(EstudiantesID.get(), "ID Estudiante")
    if not id_valid or not est_id:
        messagebox.showerror("Error", "Debe ingresar un ID de estudiante válido")
        return

    if not validate_required(Nombre_Est.get(), "Nombre"):
        return

    if not validate_required(Apellido_Est.get(), "Apellido"):
        return

    if not validate_required(DNI_Est.get(), "DNI"):
        return

    matricula_valid, matricula_value = validate_numeric(Matricula.get(), "Matrícula")
    if not matricula_valid:
        return

    parameters = (
        est_id,
        matricula_value,
        Nombre_Est.get(),
        Apellido_Est.get(),
        DNI_Est.get(),
        datetime.now().date(),
        "Dirección por defecto",
        Telefono_Est.get() if Telefono_Est.get().strip() else None,
        CorreoInstitucional_Est.get() if CorreoInstitucional_Est.get().strip() else None,
        NombreAcudiente.get() if NombreAcudiente.get().strip() else None,
        ContactoEmergencia.get() if ContactoEmergencia.get().strip() else None,
        Periodo_Est.get() if Periodo_Est.get().strip() else None
    )

    success, result = model.update_estudiante(parameters)

    if success:
        messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
        load_estudiantes_list(model, treeview)
    else:
        messagebox.showerror("Error", f"Error al actualizar estudiante: {result}")


def delete_estudiante(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    EstudiantesID = form_fields['EstudiantesID']
    id_valid, est_id = validate_numeric(EstudiantesID.get(), "ID Estudiante")
    if not id_valid or not est_id:
        messagebox.showerror("Error", "Debe ingresar un ID de estudiante válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este estudiante?"):
        success, result = model.delete_estudiante(est_id)

        if success:
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
            clear_estudiante_form(form_fields)
            load_estudiantes_list(model, treeview)
        else:
            messagebox.showerror("Error", f"Error al eliminar estudiante: {result}")


def search_estudiante(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    EstudiantesID = form_fields['EstudiantesID']
    id_valid, est_id = validate_numeric(EstudiantesID.get(), "ID Estudiante")
    if id_valid and est_id:
        success, result = model.get_estudiante_by_id(est_id)
        if success and result:
            estudiante = result[0]
            for item in treeview.get_children():
                treeview.delete(item)
            treeview.insert('', 'end', values=estudiante)

            keys = ['Matricula', 'Nombre_Est', 'Apellido_Est', 'DNI_Est', 'Telefono_Est', 'CorreoInstitucional_Est',
                    'Fotografia', 'NombreAcudiente', 'ContactoEmergencia', 'FechaIngreso', 'Periodo_Est']
            for i, key in enumerate(keys, start=1):
                if key in form_fields:
                    form_fields[key].delete(0, tk.END)
                    val = estudiante[i]
                    if isinstance(val, (datetime,)):
                        val = val.strftime("%Y-%m-%d")
                    form_fields[key].insert(0, str(val) if val else "")
            return
        else:
            messagebox.showinfo("No encontrado", "Estudiante no encontrado por ID")
            return

    search_term = form_fields['Nombre_Est'].get().strip()
    if not search_term:
        search_term = form_fields['DNI_Est'].get().strip()

    if not search_term:
        messagebox.showerror("Error", "Debe ingresar un nombre, DNI o ID para buscar")
        return

    success, result = model.search_estudiantes(search_term)

    if success and result:
        for item in treeview.get_children():
            treeview.delete(item)

        for estudiante in result:
            treeview.insert('', 'end', values=estudiante)
    else:
        messagebox.showinfo("No encontrado", "No se encontraron estudiantes")


def clear_estudiante_form(form_fields):
    for field in form_fields.values():
        field.delete(0, tk.END)


def load_estudiantes_list(model, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_estudiantes()
    if success:
        for item in treeview.get_children():
            treeview.delete(item)

        for estudiante in results:
            treeview.insert('', 'end', values=estudiante)


def export_estudiantes_to_pdf(model):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_estudiantes()
    if not success:
        messagebox.showerror("Error", "No se pudieron obtener los datos para exportar")
        return

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Reporte de Estudiantes", 0, 1, 'C')
        pdf.ln(5)

        # Fecha de generación
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.ln(10)

        # Encabezados de la tabla
        headers = ['ID', 'Matrícula', 'Nombre', 'Apellido', 'DNI', 'Teléfono', 'Correo', 'Acudiente', 'Contacto Emerg.',
                   'Fecha Ingreso', 'Período']

        pdf.set_font("Arial", 'B', 10)
        col_width = pdf.w / 11

        for header in headers:
            pdf.cell(col_width, 10, header, 1, 0, 'C')
        pdf.ln()

        # Datos de la tabla
        pdf.set_font("Arial", '', 8)
        for estudiante in results:
            # Tomar los campos relevantes para el PDF
            data = estudiante[:11]  # Primeros 11 campos
            for item in data:
                text = str(item) if item is not None else ""
                if len(text) > 15:
                    text = text[:12] + "..."
                pdf.cell(col_width, 10, text, 1, 0, 'C')
            pdf.ln()

        # Guardar el PDF
        filename = f"estudiantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        messagebox.showinfo("Éxito", f"PDF exportado correctamente como: {filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")


def export_estudiantes_to_excel(model):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_estudiantes()
    if not success:
        messagebox.showerror("Error", "No se pudieron obtener los datos para exportar")
        return

    try:
        filename = f"estudiantes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Estudiantes')

        # Formatos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#366092',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter'
        })

        cell_format = workbook.add_format({
            'border': 1,
            'align': 'left',
            'valign': 'vcenter'
        })

        # Encabezados
        headers = ['ID', 'Matrícula', 'Nombre', 'Apellido', 'DNI', 'Teléfono',
                   'Correo Institucional', 'Nombre Acudiente', 'Contacto Emergencia',
                   'Fecha Ingreso', 'Período']

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)

        # Datos
        for row, estudiante in enumerate(results, start=1):
            for col, value in enumerate(estudiante[:11]):  # Primeros 11 campos
                text = str(value) if value is not None else ""
                worksheet.write(row, col, text, cell_format)

        # Ajustar anchos de columnas específicas
        worksheet.set_column(2, 3, 20)  # Nombre y Apellido más anchos
        worksheet.set_column(6, 8, 18)  # Campos de contacto más anchos

        workbook.close()
        messagebox.showinfo("Éxito", f"Excel exportado correctamente como: {filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar Excel: {str(e)}")