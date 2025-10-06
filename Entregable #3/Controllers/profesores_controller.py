# controllers/profesores_controller.py
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


def save_profesor(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    Nombre_Prof = form_fields['Nombre_Prof']
    Apellido_Prof = form_fields['Apellido_Prof']
    DNI_Prof = form_fields['DNI_Prof']
    Telefono_Prof = form_fields['Telefono_Prof']
    CorreoInstitucional_Prof = form_fields['CorreoInstitucional_Prof']
    TituloAcademico = form_fields['TituloAcademico']
    Especializacion = form_fields['Especializacion']
    FechaContratacion = form_fields['FechaContratacion']
    Periodo_Prof = form_fields['Periodo_Prof']

    if not validate_required(Nombre_Prof.get(), "Nombre"):
        return

    if not validate_required(Apellido_Prof.get(), "Apellido"):
        return

    if not validate_required(DNI_Prof.get(), "DNI"):
        return

    fecha_contr_valid, fecha_contr = validate_date(FechaContratacion.get())
    if not fecha_contr_valid:
        return

    parameters = (
        Nombre_Prof.get(),
        Apellido_Prof.get(),
        DNI_Prof.get(),
        datetime.now().date(),
        "Dirección por defecto",
        Telefono_Prof.get() if Telefono_Prof.get().strip() else None,
        CorreoInstitucional_Prof.get() if CorreoInstitucional_Prof.get().strip() else None,
        TituloAcademico.get() if TituloAcademico.get().strip() else None,
        Especializacion.get() if Especializacion.get().strip() else None,
        fecha_contr,
        Periodo_Prof.get() if Periodo_Prof.get().strip() else None
    )

    success, result = model.insert_profesor(parameters)

    if success:
        messagebox.showinfo("Éxito", "Profesor guardado correctamente")
        clear_profesor_form(form_fields)
        load_profesores_list(model, treeview)
    else:
        messagebox.showerror("Error", f"Error al guardar profesor: {result}")


def update_profesor(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    ProfesoresID = form_fields['ProfesoresID']
    Nombre_Prof = form_fields['Nombre_Prof']
    Apellido_Prof = form_fields['Apellido_Prof']
    DNI_Prof = form_fields['DNI_Prof']
    Telefono_Prof = form_fields['Telefono_Prof']
    CorreoInstitucional_Prof = form_fields['CorreoInstitucional_Prof']
    TituloAcademico = form_fields['TituloAcademico']
    Especializacion = form_fields['Especializacion']
    FechaContratacion = form_fields['FechaContratacion']
    Periodo_Prof = form_fields['Periodo_Prof']

    id_valid, prof_id = validate_numeric(ProfesoresID.get(), "ID Profesor")
    if not id_valid or not prof_id:
        messagebox.showerror("Error", "Debe ingresar un ID de profesor válido")
        return

    if not validate_required(Nombre_Prof.get(), "Nombre"):
        return

    if not validate_required(Apellido_Prof.get(), "Apellido"):
        return

    if not validate_required(DNI_Prof.get(), "DNI"):
        return

    fecha_contr_valid, fecha_contr = validate_date(FechaContratacion.get())
    if not fecha_contr_valid:
        return

    parameters = (
        prof_id,
        Nombre_Prof.get(),
        Apellido_Prof.get(),
        DNI_Prof.get(),
        datetime.now().date(),
        "Dirección por defecto",
        Telefono_Prof.get() if Telefono_Prof.get().strip() else None,
        CorreoInstitucional_Prof.get() if CorreoInstitucional_Prof.get().strip() else None,
        TituloAcademico.get() if TituloAcademico.get().strip() else None,
        Especializacion.get() if Especializacion.get().strip() else None,
        fecha_contr,
        Periodo_Prof.get() if Periodo_Prof.get().strip() else None
    )

    success, result = model.update_profesor(parameters)

    if success:
        messagebox.showinfo("Éxito", "Profesor actualizado correctamente")
        load_profesores_list(model, treeview)
    else:
        messagebox.showerror("Error", f"Error al actualizar profesor: {result}")


def delete_profesor(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    ProfesoresID = form_fields['ProfesoresID']
    id_valid, prof_id = validate_numeric(ProfesoresID.get(), "ID Profesor")
    if not id_valid or not prof_id:
        messagebox.showerror("Error", "Debe ingresar un ID de profesor válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este profesor?"):
        success, result = model.delete_profesor(prof_id)

        if success:
            messagebox.showinfo("Éxito", "Profesor eliminado correctamente")
            clear_profesor_form(form_fields)
            load_profesores_list(model, treeview)
        else:
            messagebox.showerror("Error", f"Error al eliminar profesor: {result}")


def search_profesor(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    ProfesoresID = form_fields['ProfesoresID']
    id_valid, prof_id = validate_numeric(ProfesoresID.get(), "ID Profesor")
    if id_valid and prof_id:
        success, result = model.get_profesor_by_id(prof_id)
        if success and result:
            profesor = result[0]
            for item in treeview.get_children():
                treeview.delete(item)
            treeview.insert('', 'end', values=profesor)

            keys = ['Nombre_Prof', 'Apellido_Prof', 'DNI_Prof', 'Telefono_Prof', 'CorreoInstitucional_Prof',
                    'TituloAcademico', 'Especializacion', 'FechaContratacion', 'Periodo_Prof']
            for i, key in enumerate(keys, start=1):
                if key in form_fields:
                    form_fields[key].delete(0, tk.END)
                    val = profesor[i]
                    if isinstance(val, (datetime,)):
                        val = val.strftime("%Y-%m-%d")
                    form_fields[key].insert(0, str(val) if val else "")
            return
        else:
            messagebox.showinfo("No encontrado", "Profesor no encontrado por ID")
            return

    search_term = form_fields['Nombre_Prof'].get().strip()
    if not search_term:
        search_term = form_fields['DNI_Prof'].get().strip()

    if not search_term:
        messagebox.showerror("Error", "Debe ingresar un nombre, DNI o ID para buscar")
        return

    success, result = model.search_profesores(search_term)

    if success and result:
        for item in treeview.get_children():
            treeview.delete(item)

        for profesor in result:
            treeview.insert('', 'end', values=profesor)
    else:
        messagebox.showinfo("No encontrado", "No se encontraron profesores")


def clear_profesor_form(form_fields):
    for field in form_fields.values():
        field.delete(0, tk.END)


def load_profesores_list(model, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_profesores()
    if success:
        for item in treeview.get_children():
            treeview.delete(item)

        for profesor in results:
            treeview.insert('', 'end', values=profesor)


def export_profesores_to_pdf(model):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_profesores()
    if not success:
        messagebox.showerror("Error", "No se pudieron obtener los datos para exportar")
        return

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Reporte de Profesores", 0, 1, 'C')
        pdf.ln(5)

        # Fecha de generación
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.ln(10)

        # Encabezados de la tabla
        headers = ['ID', 'Nombre', 'Apellido', 'DNI', 'Teléfono', 'Correo', 'Título', 'Especialización',
                   'Fecha Contratación', 'Período']

        pdf.set_font("Arial", 'B', 10)
        col_width = pdf.w / 10

        for header in headers:
            pdf.cell(col_width, 10, header, 1, 0, 'C')
        pdf.ln()

        # Datos de la tabla
        pdf.set_font("Arial", '', 8)
        for profesor in results:
            # Tomar los campos relevantes para el PDF
            data = profesor[:10]  # Primeros 10 campos
            for item in data:
                text = str(item) if item is not None else ""
                if len(text) > 15:
                    text = text[:12] + "..."
                pdf.cell(col_width, 10, text, 1, 0, 'C')
            pdf.ln()

        # Guardar el PDF
        filename = f"profesores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        messagebox.showinfo("Éxito", f"PDF exportado correctamente como: {filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")


def export_profesores_to_excel(model):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_profesores()
    if not success:
        messagebox.showerror("Error", "No se pudieron obtener los datos para exportar")
        return

    try:
        filename = f"profesores_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Profesores')

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
        headers = ['ID', 'Nombre', 'Apellido', 'DNI', 'Teléfono',
                   'Correo Institucional', 'Título Académico', 'Especialización',
                   'Fecha Contratación', 'Período']

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)

        # Datos
        for row, profesor in enumerate(results, start=1):
            for col, value in enumerate(profesor[:10]):  # Primeros 10 campos
                text = str(value) if value is not None else ""
                worksheet.write(row, col, text, cell_format)

        # Ajustar anchos de columnas específicas
        worksheet.set_column(1, 2, 20)  # Nombre y Apellido más anchos
        worksheet.set_column(6, 7, 18)  # Título y Especialización más anchos

        workbook.close()
        messagebox.showinfo("Éxito", f"Excel exportado correctamente como: {filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar Excel: {str(e)}")