# controllers/asignaturas_controller.py
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


def save_asignatura(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    NombreAsignaturas = form_fields['NombreAsignaturas']
    CodAsignaturas = form_fields['CodAsignaturas']
    AreaCrecimiento = form_fields['AreaCrecimiento']
    HorasTecnicas = form_fields['HorasTecnicas']
    HorasPracticas = form_fields['HorasPracticas']
    CreditosAcademicos = form_fields['CreditosAcademicos']
    RequisitoPrevios = form_fields['RequisitoPrevios']
    ObjetivosGenerales = form_fields['ObjetivosGenerales']
    ObjetivosEspecificos = form_fields['ObjetivosEspecificos']
    BibliografiaRecomendada = form_fields['BibliografiaRecomendada']
    Periodo = form_fields['Periodo']

    if not validate_required(NombreAsignaturas.get(), "Nombre de Asignatura"):
        return

    cod_valid, cod_value = validate_numeric(CodAsignaturas.get(), "Código Asignatura")
    if not cod_valid:
        return

    horas_tec_valid, horas_tec = validate_numeric(HorasTecnicas.get(), "Horas Técnicas")
    if not horas_tec_valid:
        return

    horas_prac_valid, horas_prac = validate_numeric(HorasPracticas.get(), "Horas Prácticas")
    if not horas_prac_valid:
        return

    creditos_valid, creditos = validate_numeric(CreditosAcademicos.get(), "Créditos Académicos")
    if not creditos_valid:
        return

    parameters = (
        cod_value,
        NombreAsignaturas.get(),
        AreaCrecimiento.get() if AreaCrecimiento.get().strip() else None,
        horas_tec,
        horas_prac,
        creditos,
        RequisitoPrevios.get() if RequisitoPrevios.get().strip() else None,
        ObjetivosGenerales.get() if ObjetivosGenerales.get().strip() else None,
        ObjetivosEspecificos.get() if ObjetivosEspecificos.get().strip() else None,
        BibliografiaRecomendada.get() if BibliografiaRecomendada.get().strip() else None,
        Periodo.get() if Periodo.get().strip() else None,
        1,  # id_cursos por defecto
        1  # id_plan_estudio por defecto
    )

    success, result = model.insert_asignatura(parameters)

    if success:
        messagebox.showinfo("Éxito", "Asignatura guardada correctamente")
        clear_asignatura_form(form_fields)
        load_asignaturas_list(model, treeview)
    else:
        messagebox.showerror("Error", f"Error al guardar asignatura: {result}")


def update_asignatura(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    AsignaturasID = form_fields['AsignaturasID']
    NombreAsignaturas = form_fields['NombreAsignaturas']
    CodAsignaturas = form_fields['CodAsignaturas']
    AreaCrecimiento = form_fields['AreaCrecimiento']
    HorasTecnicas = form_fields['HorasTecnicas']
    HorasPracticas = form_fields['HorasPracticas']
    CreditosAcademicos = form_fields['CreditosAcademicos']
    RequisitoPrevios = form_fields['RequisitoPrevios']
    ObjetivosGenerales = form_fields['ObjetivosGenerales']
    ObjetivosEspecificos = form_fields['ObjetivosEspecificos']
    BibliografiaRecomendada = form_fields['BibliografiaRecomendada']
    Periodo = form_fields['Periodo']

    id_valid, asig_id = validate_numeric(AsignaturasID.get(), "ID Asignatura")
    if not id_valid or not asig_id:
        messagebox.showerror("Error", "Debe ingresar un ID de asignatura válido")
        return

    if not validate_required(NombreAsignaturas.get(), "Nombre de Asignatura"):
        return

    cod_valid, cod_value = validate_numeric(CodAsignaturas.get(), "Código Asignatura")
    if not cod_valid:
        return

    horas_tec_valid, horas_tec = validate_numeric(HorasTecnicas.get(), "Horas Técnicas")
    if not horas_tec_valid:
        return

    horas_prac_valid, horas_prac = validate_numeric(HorasPracticas.get(), "Horas Prácticas")
    if not horas_prac_valid:
        return

    creditos_valid, creditos = validate_numeric(CreditosAcademicos.get(), "Créditos Académicos")
    if not creditos_valid:
        return

    parameters = (
        asig_id,
        cod_value,
        NombreAsignaturas.get(),
        AreaCrecimiento.get() if AreaCrecimiento.get().strip() else None,
        horas_tec,
        horas_prac,
        creditos,
        RequisitoPrevios.get() if RequisitoPrevios.get().strip() else None,
        ObjetivosGenerales.get() if ObjetivosGenerales.get().strip() else None,
        ObjetivosEspecificos.get() if ObjetivosEspecificos.get().strip() else None,
        BibliografiaRecomendada.get() if BibliografiaRecomendada.get().strip() else None,
        Periodo.get() if Periodo.get().strip() else None,
        1,  # id_cursos por defecto
        1  # id_plan_estudio por defecto
    )

    success, result = model.update_asignatura(parameters)

    if success:
        messagebox.showinfo("Éxito", "Asignatura actualizada correctamente")
        load_asignaturas_list(model, treeview)
    else:
        messagebox.showerror("Error", f"Error al actualizar asignatura: {result}")


def delete_asignatura(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    AsignaturasID = form_fields['AsignaturasID']
    id_valid, asig_id = validate_numeric(AsignaturasID.get(), "ID Asignatura")
    if not id_valid or not asig_id:
        messagebox.showerror("Error", "Debe ingresar un ID de asignatura válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta asignatura?"):
        success, result = model.delete_asignatura(asig_id)

        if success:
            messagebox.showinfo("Éxito", "Asignatura eliminada correctamente")
            clear_asignatura_form(form_fields)
            load_asignaturas_list(model, treeview)
        else:
            messagebox.showerror("Error", f"Error al eliminar asignatura: {result}")


def search_asignatura(model, form_fields, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    AsignaturasID = form_fields['AsignaturasID']
    id_valid, asig_id = validate_numeric(AsignaturasID.get(), "ID Asignatura")
    if not id_valid or not asig_id:
        messagebox.showerror("Error", "Debe ingresar un ID de asignatura válido")
        return

    success, result = model.get_asignatura_by_id(asig_id)

    if success and result and len(result) > 0:
        asignatura = result[0]

        # Limpiar el Treeview y agregar solo el resultado encontrado (para "filtrar")
        for item in treeview.get_children():
            treeview.delete(item)
        display_data = asignatura[:12]  # Primeros 12 campos para el Treeview
        treeview.insert('', 'end', values=display_data)

        # Autocompletar campos
        keys = ['CodAsignaturas', 'NombreAsignaturas', 'AreaCrecimiento', 'HorasTecnicas', 'HorasPracticas',
                'CreditosAcademicos',
                'RequisitoPrevios', 'ObjetivosGenerales', 'ObjetivosEspecificos', 'BibliografiaRecomendada', 'Periodo']
        for i, key in enumerate(keys, start=1):
            if key in form_fields:
                form_fields[key].delete(0, tk.END)
                form_fields[key].insert(0, str(asignatura[i]) if asignatura[i] else "")

        messagebox.showinfo("Éxito", f"Asignatura ID {asig_id} encontrada y autocompletada.")
    else:
        messagebox.showinfo("No encontrado", f"No se encontró la asignatura con ID {asig_id}")
        for item in treeview.get_children():
            treeview.delete(item)


def clear_asignatura_form(form_fields):
    for field in form_fields.values():
        field.delete(0, tk.END)


def load_asignaturas_list(model, treeview):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_asignaturas()
    if success:
        for item in treeview.get_children():
            treeview.delete(item)

        for asignatura in results:
            display_data = asignatura[:12]  # Primeros 12 campos
            treeview.insert('', 'end', values=display_data)


def export_asignaturas_to_pdf(model):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_asignaturas()
    if not success:
        messagebox.showerror("Error", "No se pudieron obtener los datos para exportar")
        return

    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, "Reporte de Asignaturas", 0, 1, 'C')
        pdf.ln(5)

        # Fecha de generación
        pdf.set_font("Arial", '', 10)
        pdf.cell(0, 10, f"Generado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 0, 1)
        pdf.ln(10)

        # Encabezados de la tabla
        headers = ['ID', 'Código', 'Nombre', 'Área', 'H. Técnicas', 'H. Prácticas',
                   'Créditos', 'Requisitos', 'Período']

        pdf.set_font("Arial", 'B', 10)
        col_width = pdf.w / 9.5

        for header in headers:
            pdf.cell(col_width, 10, header, 1, 0, 'C')
        pdf.ln()

        # Datos de la tabla
        pdf.set_font("Arial", '', 8)
        for asignatura in results:
            # Tomar solo los primeros 9 campos relevantes para el PDF
            data = asignatura[:9]
            for item in data:
                text = str(item) if item is not None else ""
                if len(text) > 20:
                    text = text[:17] + "..."
                pdf.cell(col_width, 10, text, 1, 0, 'C')
            pdf.ln()

        # Guardar el PDF
        filename = f"asignaturas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        pdf.output(filename)
        messagebox.showinfo("Éxito", f"PDF exportado correctamente como: {filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar PDF: {str(e)}")


def export_asignaturas_to_excel(model):
    if not model.db.connection:
        if not model.db.connect():
            return

    success, results = model.get_all_asignaturas()
    if not success:
        messagebox.showerror("Error", "No se pudieron obtener los datos para exportar")
        return

    try:
        filename = f"asignaturas_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet('Asignaturas')

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
        headers = ['ID', 'Código', 'Nombre', 'Área Crecimiento', 'Horas Técnicas',
                   'Horas Prácticas', 'Créditos Académicos', 'Requisitos Previos',
                   'Objetivos Generales', 'Objetivos Específicos',
                   'Bibliografía Recomendada', 'Período']

        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_format)
            worksheet.set_column(col, col, 15)

        # Datos
        for row, asignatura in enumerate(results, start=1):
            for col, value in enumerate(asignatura[:12]):  # Primeros 12 campos
                text = str(value) if value is not None else ""
                worksheet.write(row, col, text, cell_format)

        # Ajustar anchos de columnas específicas
        worksheet.set_column(2, 2, 25)  # Nombre más ancho
        worksheet.set_column(7, 10, 20)  # Campos de texto más anchos

        workbook.close()
        messagebox.showinfo("Éxito", f"Excel exportado correctamente como: {filename}")

    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar Excel: {str(e)}")