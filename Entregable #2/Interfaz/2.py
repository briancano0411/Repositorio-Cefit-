import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from datetime import datetime
import re


# =================== CONFIGURACIÓN DE BASE DE DATOS ===================
class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host='localhost',
                database='horizonte_del_saber_2',
                user='root',
                password='',
                autocommit=False
            )
            self.cursor = self.connection.cursor(buffered=True)
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"Error conectando a la base de datos: {err}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    def call_procedure(self, procedure_name, parameters=None):
        try:
            if parameters:
                self.cursor.callproc(procedure_name, parameters)
            else:
                self.cursor.callproc(procedure_name)


            results = []
            for result in self.cursor.stored_results():
                results.extend(result.fetchall())

            return True, results
        except mysql.connector.Error as err:
            self.connection.rollback()
            return False, str(err)

    def execute_query(self, query, parameters=None):
        try:
            if parameters:
                self.cursor.execute(query, parameters)
            else:
                self.cursor.execute(query)

            if query.strip().upper().startswith('SELECT'):
                return True, self.cursor.fetchall()
            else:
                self.connection.commit()
                return True, "Operación exitosa"
        except mysql.connector.Error as err:
            self.connection.rollback()
            return False, str(err)


# Instancia global de conexión
db = DatabaseConnection()


# =================== FUNCIONES DE VALIDACIÓN ===================
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


# =================== FUNCIONES PARA ASIGNATURAS ===================
def save_asignatura():
    if not db.connection:
        if not db.connect():
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

    success, result = db.call_procedure('sp_InsertAsignatura', parameters)

    if success:
        messagebox.showinfo("Éxito", "Asignatura guardada correctamente")
        clear_asignatura_form()
        load_asignaturas_list()
    else:
        messagebox.showerror("Error", f"Error al guardar asignatura: {result}")


def update_asignatura():
    if not db.connection:
        if not db.connect():
            return

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

    success, result = db.call_procedure('sp_UpdateAsignatura', parameters)

    if success:
        messagebox.showinfo("Éxito", "Asignatura actualizada correctamente")
        load_asignaturas_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar asignatura: {result}")


def delete_asignatura():
    if not db.connection:
        if not db.connect():
            return

    id_valid, asig_id = validate_numeric(AsignaturasID.get(), "ID Asignatura")
    if not id_valid or not asig_id:
        messagebox.showerror("Error", "Debe ingresar un ID de asignatura válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta asignatura?"):
        success, result = db.call_procedure('sp_DeleteAsignatura', (asig_id,))

        if success:
            messagebox.showinfo("Éxito", "Asignatura eliminada correctamente")
            clear_asignatura_form()
            load_asignaturas_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar asignatura: {result}")


def search_asignatura():
    if not db.connection:
        if not db.connect():
            return

    id_valid, asig_id = validate_numeric(AsignaturasID.get(), "ID Asignatura")
    if not id_valid or not asig_id:
        messagebox.showerror("Error", "Debe ingresar un ID de asignatura válido")
        return

    try:
        # Query directo para buscar por ID (ajusta el nombre de tabla/campo si es necesario)
        query = "SELECT * FROM asignaturas WHERE id_asignaturas = %s"
        success, result = db.execute_query(query, (asig_id,))

        if success and result and len(result) > 0:
            asignatura = result[0]

            # Limpiar el Treeview y agregar solo el resultado encontrado (para "filtrar")
            for item in asignaturas_tree.get_children():
                asignaturas_tree.delete(item)
            display_data = asignatura[:12]  # Primeros 12 campos para el Treeview
            asignaturas_tree.insert('', 'end', values=display_data)

            # Autocompletar TODOS los campos del formulario (verifica que haya suficientes datos)
            if len(asignatura) > 1:
                CodAsignaturas.delete(0, tk.END)
                CodAsignaturas.insert(0, str(asignatura[1]) if asignatura[1] else "")
            if len(asignatura) > 2:
                NombreAsignaturas.delete(0, tk.END)
                NombreAsignaturas.insert(0, str(asignatura[2]) if asignatura[2] else "")
            if len(asignatura) > 3:
                AreaCrecimiento.delete(0, tk.END)
                AreaCrecimiento.insert(0, str(asignatura[3]) if asignatura[3] else "")
            if len(asignatura) > 4:
                HorasTecnicas.delete(0, tk.END)
                HorasTecnicas.insert(0, str(asignatura[4]) if asignatura[4] else "")
            if len(asignatura) > 5:
                HorasPracticas.delete(0, tk.END)
                HorasPracticas.insert(0, str(asignatura[5]) if asignatura[5] else "")
            if len(asignatura) > 6:
                CreditosAcademicos.delete(0, tk.END)
                CreditosAcademicos.insert(0, str(asignatura[6]) if asignatura[6] else "")
            if len(asignatura) > 7:
                RequisitoPrevios.delete(0, tk.END)
                RequisitoPrevios.insert(0, str(asignatura[7]) if asignatura[7] else "")
            if len(asignatura) > 8:
                ObjetivosGenerales.delete(0, tk.END)
                ObjetivosGenerales.insert(0, str(asignatura[8]) if asignatura[8] else "")
            if len(asignatura) > 9:
                ObjetivosEspecificos.delete(0, tk.END)
                ObjetivosEspecificos.insert(0, str(asignatura[9]) if asignatura[9] else "")
            if len(asignatura) > 10:
                BibliografiaRecomendada.delete(0, tk.END)
                BibliografiaRecomendada.insert(0, str(asignatura[10]) if asignatura[10] else "")
            if len(asignatura) > 11:
                Periodo.delete(0, tk.END)
                Periodo.insert(0, str(asignatura[11]) if asignatura[11] else "")

            messagebox.showinfo("Éxito", f"Asignatura ID {asig_id} encontrada y autocompletada.")
        else:
            messagebox.showinfo("No encontrado", f"No se encontró la asignatura con ID {asig_id}")
            # Opcional: Limpiar Treeview si no se encuentra
            for item in asignaturas_tree.get_children():
                asignaturas_tree.delete(item)
    except Exception as e:
        messagebox.showerror("Error en Búsqueda", f"Error al buscar asignatura: {str(e)}")
        # Opcional: Imprimir en consola para depurar
        print(f"Error detallado: {e}")


def clear_asignatura_form():
    AsignaturasID.delete(0, tk.END)
    CodAsignaturas.delete(0, tk.END)
    NombreAsignaturas.delete(0, tk.END)
    AreaCrecimiento.delete(0, tk.END)
    HorasTecnicas.delete(0, tk.END)
    HorasPracticas.delete(0, tk.END)
    CreditosAcademicos.delete(0, tk.END)
    RequisitoPrevios.delete(0, tk.END)
    ObjetivosGenerales.delete(0, tk.END)
    ObjetivosEspecificos.delete(0, tk.END)
    BibliografiaRecomendada.delete(0, tk.END)
    Periodo.delete(0, tk.END)


def load_asignaturas_list():
    if not db.connection:
        if not db.connect():
            return

    success, results = db.call_procedure('sp_GetAllAsignaturas')
    if success:
        for item in asignaturas_tree.get_children():
            asignaturas_tree.delete(item)

        for asignatura in results:
            display_data = asignatura[:12]  # Primeros 12 campos
            asignaturas_tree.insert('', 'end', values=display_data)


# =================== FUNCIONES PARA AULAS ===================
def save_aula():
    if not db.connection:
        if not db.connect():
            return

    if not validate_required(NumeroIdentificador.get(), "Número Identificador"):
        return

    piso_valid, piso_value = validate_numeric(NumeroPiso.get(), "Número de Piso")
    if not piso_valid:
        return

    capacidad_valid, capacidad_value = validate_numeric(CapacidadEstudiantes.get(), "Capacidad de Estudiantes")
    if not capacidad_valid:
        return

    query = """INSERT INTO aulas (numero_identificador, edificio, piso, capacidad_estudiantes, 
               tipo, equipamiento_disponible, estado_actual) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    parameters = (
        NumeroIdentificador.get(),
        Edificio.get() if Edificio.get().strip() else None,
        piso_value,
        capacidad_value,
        TipoCurso.get() if TipoCurso.get().strip() else None,
        EquipamientoDisponible.get() if EquipamientoDisponible.get().strip() else None,
        EstadoActual.get() if EstadoActual.get().strip() else None
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Aula guardada correctamente")
        clear_aula_form()
        load_aulas_list()
    else:
        messagebox.showerror("Error", f"Error al guardar aula: {result}")


def update_aula():
    if not db.connection:
        if not db.connect():
            return

    id_valid, aula_id = validate_numeric(AulasID.get(), "ID Aula")
    if not id_valid or not aula_id:
        messagebox.showerror("Error", "Debe ingresar un ID de aula válido")
        return

    piso_valid, piso_value = validate_numeric(NumeroPiso.get(), "Número de Piso")
    if not piso_valid:
        return

    capacidad_valid, capacidad_value = validate_numeric(CapacidadEstudiantes.get(), "Capacidad de Estudiantes")
    if not capacidad_valid:
        return

    query = """UPDATE aulas SET numero_identificador = %s, edificio = %s, piso = %s, 
               capacidad_estudiantes = %s, tipo = %s, equipamiento_disponible = %s, 
               estado_actual = %s WHERE id_aulas = %s"""

    parameters = (
        NumeroIdentificador.get(),
        Edificio.get() if Edificio.get().strip() else None,
        piso_value,
        capacidad_value,
        TipoCurso.get() if TipoCurso.get().strip() else None,
        EquipamientoDisponible.get() if EquipamientoDisponible.get().strip() else None,
        EstadoActual.get() if EstadoActual.get().strip() else None,
        aula_id
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Aula actualizada correctamente")
        load_aulas_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar aula: {result}")


def delete_aula():
    if not db.connection:
        if not db.connect():
            return

    id_valid, aula_id = validate_numeric(AulasID.get(), "ID Aula")
    if not id_valid or not aula_id:
        messagebox.showerror("Error", "Debe ingresar un ID de aula válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta aula?"):
        query = "DELETE FROM aulas WHERE id_aulas = %s"
        success, result = db.execute_query(query, (aula_id,))

        if success:
            messagebox.showinfo("Éxito", "Aula eliminada correctamente")
            clear_aula_form()
            load_aulas_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar aula: {result}")


def search_aula():
    if not db.connection:
        if not db.connect():
            return

    id_valid, aula_id = validate_numeric(AulasID.get(), "ID Aula")
    if not id_valid or not aula_id:
        messagebox.showerror("Error", "Debe ingresar un ID de aula válido")
        return

    query = "SELECT * FROM aulas WHERE id_aulas = %s"
    success, result = db.execute_query(query, (aula_id,))

    if success and result:
        # Limpiar el Treeview y agregar solo el resultado encontrado
        for item in aulas_tree.get_children():
            aulas_tree.delete(item)
        aula = result[0]
        aulas_tree.insert('', 'end', values=aula)

        # Llenar el formulario (como ya lo hacías)
        NumeroIdentificador.delete(0, tk.END)
        NumeroIdentificador.insert(0, aula[1] if aula[1] else "")
        Edificio.delete(0, tk.END)
        Edificio.insert(0, aula[2] if aula[2] else "")
        NumeroPiso.delete(0, tk.END)
        NumeroPiso.insert(0, aula[3] if aula[3] else "")
        CapacidadEstudiantes.delete(0, tk.END)
        CapacidadEstudiantes.insert(0, aula[4] if aula[4] else "")
        TipoCurso.delete(0, tk.END)
        TipoCurso.insert(0, aula[5] if aula[5] else "")
        EquipamientoDisponible.delete(0, tk.END)
        EquipamientoDisponible.insert(0, aula[6] if aula[6] else "")
        EstadoActual.delete(0, tk.END)
        EstadoActual.insert(0, aula[7] if aula[7] else "")
    else:
        messagebox.showinfo("No encontrado", "Aula no encontrada")
        # Opcional: Limpiar Treeview si no se encuentra
        for item in aulas_tree.get_children():
            aulas_tree.delete(item)


def clear_aula_form():
    AulasID.delete(0, tk.END)
    NumeroIdentificador.delete(0, tk.END)
    Edificio.delete(0, tk.END)
    NumeroPiso.delete(0, tk.END)
    CapacidadEstudiantes.delete(0, tk.END)
    TipoCurso.delete(0, tk.END)
    EquipamientoDisponible.delete(0, tk.END)
    EstadoActual.delete(0, tk.END)


def load_aulas_list():
    if not db.connection:
        if not db.connect():
            return

    query = "SELECT * FROM aulas"
    success, results = db.execute_query(query)
    if success:
        for item in aulas_tree.get_children():
            aulas_tree.delete(item)

        for aula in results:
            aulas_tree.insert('', 'end', values=aula)


# =================== FUNCIONES PARA PROFESORES ===================
def save_profesor():
    if not db.connection:
        if not db.connect():
            return

    if not validate_required(Nombre.get(), "Nombre"):
        return

    if not validate_required(Apellido.get(), "Apellido"):
        return

    if not validate_required(DNI.get(), "DNI"):
        return

    cod_emp_valid, cod_emp = validate_numeric(CodigoEmplead.get(), "Código Empleado")
    if not cod_emp_valid:
        return

    fecha_nac_valid, fecha_nac = validate_date(FechaNacimiento.get())
    if not fecha_nac_valid:
        return

    fecha_cont_valid, fecha_cont = validate_date(FechaContratacion.get())
    if not fecha_cont_valid:
        return

    anos_exp_valid, anos_exp = validate_numeric(AñosExperiencia.get(),
                                                "Años de Experiencia") if AñosExperiencia.get().strip() else (True,
                                                                                                              None)
    if not anos_exp_valid:
        return

    parameters = (
        cod_emp,
        Nombre.get(),
        Apellido.get(),
        DNI.get(),
        fecha_nac,
        Direccion.get() if Direccion.get().strip() else None,
        Telefono.get() if Telefono.get().strip() else None,
        CorreoInstitucional.get() if CorreoInstitucional.get().strip() else None,
        NivelAcademico.get() if NivelAcademico.get().strip() else None,
        Especialidad.get() if Especialidad.get().strip() else None,
        anos_exp,
        fecha_cont,
        TipoContrato.get() if TipoContrato.get().strip() else None,
        CursoEspecializado.get() if CursoEspecializado.get().strip() else None
    )

    success, result = db.call_procedure('sp_InsertProfesor', parameters)

    if success:
        messagebox.showinfo("Éxito", "Profesor guardado correctamente")
        clear_profesor_form()
        load_profesores_list()
    else:
        messagebox.showerror("Error", f"Error al guardar profesor: {result}")


def update_profesor():
    if not db.connection:
        if not db.connect():
            return

    id_valid, prof_id = validate_numeric(ProfesoresID.get(), "ID Profesor")
    if not id_valid or not prof_id:
        messagebox.showerror("Error", "Debe ingresar un ID de profesor válido")
        return

    if not validate_required(Nombre.get(), "Nombre"):
        return

    if not validate_required(Apellido.get(), "Apellido"):
        return

    if not validate_required(DNI.get(), "DNI"):
        return

    cod_emp_valid, cod_emp = validate_numeric(CodigoEmplead.get(), "Código Empleado")
    if not cod_emp_valid:
        return

    fecha_nac_valid, fecha_nac = validate_date(FechaNacimiento.get())
    if not fecha_nac_valid:
        return

    fecha_cont_valid, fecha_cont = validate_date(FechaContratacion.get())
    if not fecha_cont_valid:
        return

    anos_exp_valid, anos_exp = validate_numeric(AñosExperiencia.get(),
                                                "Años de Experiencia") if AñosExperiencia.get().strip() else (True,
                                                                                                              None)
    if not anos_exp_valid:
        return

    parameters = (
        prof_id,
        cod_emp,
        Nombre.get(),
        Apellido.get(),
        DNI.get(),
        fecha_nac,
        Direccion.get() if Direccion.get().strip() else None,
        Telefono.get() if Telefono.get().strip() else None,
        CorreoInstitucional.get() if CorreoInstitucional.get().strip() else None,
        NivelAcademico.get() if NivelAcademico.get().strip() else None,
        Especialidad.get() if Especialidad.get().strip() else None,
        anos_exp,
        fecha_cont,
        TipoContrato.get() if TipoContrato.get().strip() else None,
        CursoEspecializado.get() if CursoEspecializado.get().strip() else None
    )

    success, result = db.call_procedure('sp_UpdateProfesor', parameters)

    if success:
        messagebox.showinfo("Éxito", "Profesor actualizado correctamente")
        load_profesores_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar profesor: {result}")


def delete_profesor():
    if not db.connection:
        if not db.connect():
            return

    id_valid, prof_id = validate_numeric(ProfesoresID.get(), "ID Profesor")
    if not id_valid or not prof_id:
        messagebox.showerror("Error", "Debe ingresar un ID de profesor válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este profesor?"):
        success, result = db.call_procedure('sp_DeleteProfesor', (prof_id,))

        if success:
            messagebox.showinfo("Éxito", "Profesor eliminado correctamente")
            clear_profesor_form()
            load_profesores_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar profesor: {result}")


def search_profesor():
    if not db.connection:
        if not db.connect():
            return


    id_valid, prof_id = validate_numeric(ProfesoresID.get(), "ID Profesor")
    if id_valid and prof_id:
        # Búsqueda por ID: Llenar formulario y filtrar Treeview con solo ese resultado
        success, result = db.call_procedure('sp_GetProfesor', (prof_id,))  # Asume que tienes este SP; si no, usa query SELECT
        if success and result:
            profesor = result[0]
            # Limpiar Treeview y agregar solo el resultado
            for item in profesores_tree.get_children():
                profesores_tree.delete(item)
            display_data = profesor[:13]  # Primeros 13 campos
            profesores_tree.insert('', 'end', values=display_data)

            # Llenar TODOS los campos del formulario
            CodigoEmplead.delete(0, tk.END)
            CodigoEmplead.insert(0, profesor[1] if profesor[1] else "")
            Nombre.delete(0, tk.END)
            Nombre.insert(0, profesor[2] if profesor[2] else "")
            Apellido.delete(0, tk.END)
            Apellido.insert(0, profesor[3] if profesor[3] else "")
            DNI.delete(0, tk.END)
            DNI.insert(0, profesor[4] if profesor[4] else "")
            FechaNacimiento.delete(0, tk.END)
            if len(profesor) > 5 and profesor[5]:
                FechaNacimiento.insert(0, profesor[5].strftime("%Y-%m-%d") if hasattr(profesor[5], 'strftime') else str(profesor[5]))
            Direccion.delete(0, tk.END)
            Direccion.insert(0, profesor[6] if len(profesor) > 6 and profesor[6] else "")
            Telefono.delete(0, tk.END)
            Telefono.insert(0, profesor[7] if len(profesor) > 7 and profesor[7] else "")
            CorreoInstitucional.delete(0, tk.END)
            CorreoInstitucional.insert(0, profesor[8] if len(profesor) > 8 and profesor[8] else "")
            NivelAcademico.delete(0, tk.END)
            NivelAcademico.insert(0, profesor[9] if len(profesor) > 9 and profesor[9] else "")
            Especialidad.delete(0, tk.END)
            Especialidad.insert(0, profesor[10] if len(profesor) > 10 and profesor[10] else "")
            AñosExperiencia.delete(0, tk.END)
            AñosExperiencia.insert(0, profesor[11] if len(profesor) > 11 and profesor[11] else "")
            FechaContratacion.delete(0, tk.END)
            if len(profesor) > 12 and profesor[12]:
                FechaContratacion.insert(0, profesor[12].strftime("%Y-%m-%d") if hasattr(profesor[12], 'strftime') else str(profesor[12]))
            TipoContrato.delete(0, tk.END)
            TipoContrato.insert(0, profesor[13] if len(profesor) > 13 and profesor[13] else "")
            CursoEspecializado.delete(0, tk.END)
            CursoEspecializado.insert(0, profesor[14] if len(profesor) > 14 and profesor[14] else "")
            return
        else:
            messagebox.showinfo("No encontrado", "Profesor no encontrado por ID")
            return


    search_term = Nombre.get().strip()
    if not search_term:
        search_term = Apellido.get().strip()
    if not search_term:
        search_term = DNI.get().strip()

    if not search_term:
        messagebox.showerror("Error", "Debe ingresar un nombre, apellido, DNI o ID para buscar")
        return

    success, result = db.call_procedure('sp_SearchProfesores', (search_term,))

    if success and result:
        for item in profesores_tree.get_children():
            profesores_tree.delete(item)

        for profesor in result:
            profesores_tree.insert('', 'end', values=profesor)
    else:
        messagebox.showinfo("No encontrado", "No se encontraron profesores")


def clear_profesor_form():
    ProfesoresID.delete(0, tk.END)
    CodigoEmplead.delete(0, tk.END)
    Nombre.delete(0, tk.END)
    Apellido.delete(0, tk.END)
    DNI.delete(0, tk.END)
    FechaNacimiento.delete(0, tk.END)
    Direccion.delete(0, tk.END)
    Telefono.delete(0, tk.END)
    CorreoInstitucional.delete(0, tk.END)
    NivelAcademico.delete(0, tk.END)
    Especialidad.delete(0, tk.END)
    AñosExperiencia.delete(0, tk.END)
    FechaContratacion.delete(0, tk.END)
    TipoContrato.delete(0, tk.END)
    CursoEspecializado.delete(0, tk.END)


def load_profesores_list():
    if not db.connection:
        if not db.connect():
            return

    success, results = db.call_procedure('sp_GetAllProfesores')
    if success:
        for item in profesores_tree.get_children():
            profesores_tree.delete(item)

        for profesor in results:
            display_data = profesor[:13]  # Primeros 13 campos
            profesores_tree.insert('', 'end', values=display_data)


# =================== FUNCIONES PARA CALIFICACIONES ===================
def save_calificacion():
    if not db.connection:
        if not db.connect():
            return

    if not validate_required(TipoEvaluacion.get(), "Tipo de Evaluación"):
        return

    fecha_valid, fecha_value = validate_date(FechaCalificado.get())
    if not fecha_valid:
        return

    nota_valid, nota_value = validate_numeric(Nota.get(), "Nota")
    if not nota_valid:
        return

    porcentaje_valid, porcentaje_value = validate_numeric(PorcentajeTotal.get(), "Porcentaje Total")
    if not porcentaje_valid:
        return

    parameters = (
        TipoEvaluacion.get(),
        fecha_value,
        nota_value,
        porcentaje_value,
        Observaciones.get() if Observaciones.get().strip() else None,
        "1234567890",  # DNI por defecto
        1,  # id_cursos por defecto
        1  # id_asignaturas por defecto
    )

    success, result = db.call_procedure('sp_InsertCalificacion', parameters)

    if success:
        messagebox.showinfo("Éxito", "Calificación guardada correctamente")
        clear_calificacion_form()
        load_calificaciones_list()
    else:
        messagebox.showerror("Error", f"Error al guardar calificación: {result}")


def update_calificacion():
    if not db.connection:
        if not db.connect():
            return

    id_valid, cal_id = validate_numeric(CalificacionesID.get(), "ID Calificación")
    if not id_valid or not cal_id:
        messagebox.showerror("Error", "Debe ingresar un ID de calificación válido")
        return

    fecha_valid, fecha_value = validate_date(FechaCalificado.get())
    if not fecha_valid:
        return

    nota_valid, nota_value = validate_numeric(Nota.get(), "Nota")
    if not nota_valid:
        return

    porcentaje_valid, porcentaje_value = validate_numeric(PorcentajeTotal.get(), "Porcentaje Total")
    if not porcentaje_valid:
        return

    query = """UPDATE calificaciones SET tipo_evaluacion = %s, fecha = %s, valor_numerico = %s, 
               porcentaje_total = %s, observaciones = %s WHERE id_calificaciones = %s"""

    parameters = (
        TipoEvaluacion.get(),
        fecha_value,
        nota_value,
        porcentaje_value,
        Observaciones.get() if Observaciones.get().strip() else None,
        cal_id
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Calificación actualizada correctamente")
        load_calificaciones_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar calificación: {result}")


def delete_calificacion():
    if not db.connection:
        if not db.connect():
            return

    id_valid, cal_id = validate_numeric(CalificacionesID.get(), "ID Calificación")
    if not id_valid or not cal_id:
        messagebox.showerror("Error", "Debe ingresar un ID de calificación válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar esta calificación?"):
        query = "DELETE FROM calificaciones WHERE id_calificaciones = %s"
        success, result = db.execute_query(query, (cal_id,))

        if success:
            messagebox.showinfo("Éxito", "Calificación eliminada correctamente")
            clear_calificacion_form()
            load_calificaciones_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar calificación: {result}")


def search_calificacion():
    if not db.connection:
        if not db.connect():
            return

    id_valid, cal_id = validate_numeric(CalificacionesID.get(), "ID Calificación")
    if not id_valid or not cal_id:
        messagebox.showerror("Error", "Debe ingresar un ID de calificación válido")
        return

    query = "SELECT * FROM calificaciones WHERE id_calificaciones = %s"
    success, result = db.execute_query(query, (cal_id,))

    if success and result:
        # Limpiar el Treeview y agregar solo el resultado encontrado
        for item in calificaciones_tree.get_children():
            calificaciones_tree.delete(item)
        calificacion = result[0]
        display_data = calificacion[:6]  # Primeros 6 campos para el Treeview
        calificaciones_tree.insert('', 'end', values=display_data)

        # Llenar el formulario
        TipoEvaluacion.delete(0, tk.END)
        TipoEvaluacion.insert(0, calificacion[1] if calificacion[1] else "")
        FechaCalificado.delete(0, tk.END)
        if calificacion[2]:
            FechaCalificado.insert(0, calificacion[2].strftime("%Y-%m-%d"))
        Nota.delete(0, tk.END)
        Nota.insert(0, calificacion[3] if calificacion[3] else "")
        PorcentajeTotal.delete(0, tk.END)
        PorcentajeTotal.insert(0, calificacion[4] if calificacion[4] else "")
        Observaciones.delete(0, tk.END)
        Observaciones.insert(0, calificacion[5] if calificacion[5] else "")
    else:
        messagebox.showinfo("No encontrado", "Calificación no encontrada")
        # Opcional: Limpiar Treeview si no se encuentra
        for item in calificaciones_tree.get_children():
            calificaciones_tree.delete(item)


def clear_calificacion_form():
    CalificacionesID.delete(0, tk.END)
    TipoEvaluacion.delete(0, tk.END)
    FechaCalificado.delete(0, tk.END)
    Nota.delete(0, tk.END)
    PorcentajeTotal.delete(0, tk.END)
    Observaciones.delete(0, tk.END)


def load_calificaciones_list():
    if not db.connection:
        if not db.connect():
            return

    query = "SELECT * FROM calificaciones"
    success, results = db.execute_query(query)
    if success:
        for item in calificaciones_tree.get_children():
            calificaciones_tree.delete(item)

        for calificacion in results:
            display_data = calificacion[:6]  # Primeros 6 campos
            calificaciones_tree.insert('', 'end', values=display_data)


# =================== FUNCIONES PARA BIBLIOTECA ===================
def save_biblioteca():
    if not db.connection:
        if not db.connect():
            return

    if not validate_required(Titulo.get(), "Título"):
        return

    cod_valid, cod_value = validate_numeric(CodigoMaterialBiblioteca.get(), "Código Material")
    if not cod_valid:
        return

    ano_valid, ano_value = validate_numeric(AñoPublicado.get(), "Año Publicado")
    if not ano_valid:
        return

    cantidad_valid, cantidad_value = validate_numeric(CantidadDisponible.get(), "Cantidad Disponible")
    if not cantidad_valid:
        return

    parameters = (
        cod_value,
        Titulo.get(),
        Actores.get() if Actores.get().strip() else None,
        Editorial.get() if Editorial.get().strip() else None,
        ano_value,
        Edicion.get() if Edicion.get().strip() else None,
        ISBN.get() if ISBN.get().strip() else None,
        CategoriaTematica.get() if CategoriaTematica.get().strip() else None,
        Formato.get() if Formato.get().strip() else None,
        UbicacionFisica.get() if UbicacionFisica.get().strip() else None,
        cantidad_value,
        "1234567890"
    )

    success, result = db.call_procedure('sp_InsertMaterialBibliografico', parameters)

    if success:
        messagebox.showinfo("Éxito", "Material bibliográfico guardado correctamente")
        clear_biblioteca_form()
        load_biblioteca_list()
    else:
        messagebox.showerror("Error", f"Error al guardar material: {result}")


def update_biblioteca():
    if not db.connection:
        if not db.connect():
            return

    id_valid, bib_id = validate_numeric(BibliotecaID.get(), "ID Biblioteca")
    if not id_valid or not bib_id:
        messagebox.showerror("Error", "Debe ingresar un ID de biblioteca válido")
        return

    cod_valid, cod_value = validate_numeric(CodigoMaterialBiblioteca.get(), "Código Material")
    if not cod_valid:
        return

    ano_valid, ano_value = validate_numeric(AñoPublicado.get(), "Año Publicado")
    if not ano_valid:
        return

    cantidad_valid, cantidad_value = validate_numeric(CantidadDisponible.get(), "Cantidad Disponible")
    if not cantidad_valid:
        return

    query = """UPDATE biblioteca SET cod_material_bibliografico = %s, titulo = %s, actores = %s, 
               editorial = %s, ano_publicacion = %s, edicion = %s, isbn = %s, 
               categoria_tematica = %s, formato = %s, ubicacion_fisica = %s, 
               cantidad_ejemplares_disponible = %s WHERE id_biblioteca = %s"""

    parameters = (
        cod_value,
        Titulo.get(),
        Actores.get() if Actores.get().strip() else None,
        Editorial.get() if Editorial.get().strip() else None,
        ano_value,
        Edicion.get() if Edicion.get().strip() else None,
        ISBN.get() if ISBN.get().strip() else None,
        CategoriaTematica.get() if CategoriaTematica.get().strip() else None,
        Formato.get() if Formato.get().strip() else None,
        UbicacionFisica.get() if UbicacionFisica.get().strip() else None,
        cantidad_value,
        bib_id
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Material bibliográfico actualizado correctamente")
        load_biblioteca_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar material: {result}")


def delete_biblioteca():
    if not db.connection:
        if not db.connect():
            return

    id_valid, bib_id = validate_numeric(BibliotecaID.get(), "ID Biblioteca")
    if not id_valid or not bib_id:
        messagebox.showerror("Error", "Debe ingresar un ID de biblioteca válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este material?"):
        query = "DELETE FROM biblioteca WHERE id_biblioteca = %s"
        success, result = db.execute_query(query, (bib_id,))

        if success:
            messagebox.showinfo("Éxito", "Material eliminado correctamente")
            clear_biblioteca_form()
            load_biblioteca_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar material: {result}")


def search_biblioteca():
    if not db.connection:
        if not db.connect():
            return

    # Prioridad: Buscar por ID si está presente
    id_valid, bib_id = validate_numeric(BibliotecaID.get(), "ID Biblioteca")
    if id_valid and bib_id:
        # Búsqueda por ID: Llenar formulario y filtrar Treeview con solo ese resultado
        query = "SELECT * FROM biblioteca WHERE id_biblioteca = %s"
        success, result = db.execute_query(query, (bib_id,))
        if success and result:
            material = result[0]
            # Limpiar Treeview y agregar solo el resultado
            for item in biblioteca_tree.get_children():
                biblioteca_tree.delete(item)
            biblioteca_tree.insert('', 'end', values=material)

            # Llenar TODOS los campos del formulario
            CodigoMaterialBiblioteca.delete(0, tk.END)
            CodigoMaterialBiblioteca.insert(0, material[1] if material[1] else "")
            Titulo.delete(0, tk.END)
            Titulo.insert(0, material[2] if material[2] else "")
            Actores.delete(0, tk.END)
            Actores.insert(0, material[3] if material[3] else "")
            Editorial.delete(0, tk.END)
            Editorial.insert(0, material[4] if material[4] else "")
            AñoPublicado.delete(0, tk.END)
            AñoPublicado.insert(0, material[5] if material[5] else "")
            ISBN.delete(0, tk.END)
            ISBN.insert(0, material[6] if material[6] else "")
            CategoriaTematica.delete(0, tk.END)
            CategoriaTematica.insert(0, material[7] if material[7] else "")
            Formato.delete(0, tk.END)
            Formato.insert(0, material[8] if material[8] else "")
            CantidadDisponible.delete(0, tk.END)
            CantidadDisponible.insert(0, material[10] if material[10] else "")  # Ajusta índice si es necesario
            UbicacionFisica.delete(0, tk.END)
            UbicacionFisica.insert(0, material[9] if material[9] else "")
            Edicion.delete(0, tk.END)
            Edicion.insert(0, material[11] if len(material) > 11 and material[11] else "")
            return  # Salir si se encontró por ID
        else:
            messagebox.showinfo("No encontrado", "Material no encontrado por ID")
            return


    search_term = Titulo.get().strip()
    if not search_term:
        search_term = ISBN.get().strip()

    if not search_term:
        messagebox.showerror("Error", "Debe ingresar un título, ISBN o ID para buscar")
        return

    success, result = db.call_procedure('sp_SearchBiblioteca', (search_term,))

    if success and result:
        for item in biblioteca_tree.get_children():
            biblioteca_tree.delete(item)

        for material in result:
            biblioteca_tree.insert('', 'end', values=material)
    else:
        messagebox.showinfo("No encontrado", "No se encontraron materiales")


def clear_biblioteca_form():
    BibliotecaID.delete(0, tk.END)
    CodigoMaterialBiblioteca.delete(0, tk.END)
    Titulo.delete(0, tk.END)
    Actores.delete(0, tk.END)
    Editorial.delete(0, tk.END)
    AñoPublicado.delete(0, tk.END)
    ISBN.delete(0, tk.END)
    CategoriaTematica.delete(0, tk.END)
    Formato.delete(0, tk.END)
    CantidadDisponible.delete(0, tk.END)
    UbicacionFisica.delete(0, tk.END)
    Edicion.delete(0, tk.END)


def load_biblioteca_list():
    if not db.connection:
        if not db.connect():
            return

    query = "SELECT * FROM biblioteca"
    success, results = db.execute_query(query)
    if success:
        for item in biblioteca_tree.get_children():
            biblioteca_tree.delete(item)

        for material in results:
            biblioteca_tree.insert('', 'end', values=material)


# =================== FUNCIONES PARA CURSOS ===================
def save_curso():
    if not db.connection:
        if not db.connect():
            return

    periodo_valid, periodo_value = validate_numeric(PeriodoAcademico.get(), "Período Académico")
    if not periodo_valid:
        return

    cupo_valid, cupo_value = validate_numeric(CupoMaximo.get(), "Cupo Máximo")
    if not cupo_valid:
        return

    query = """INSERT INTO cursos (periodo_academico, horarios, cupo_maximo, metodologia_evaluacion, id_aulas, id_profesores) 
               VALUES (%s, %s, %s, %s, %s, %s)"""

    parameters = (
        periodo_value,
        Horarios.get() if Horarios.get().strip() else None,
        cupo_value,
        MetodologiaEvaluacion.get() if MetodologiaEvaluacion.get().strip() else None,
        1,  # id_aulas por defecto
        1  # id_profesores por defecto
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Curso guardado correctamente")
        clear_curso_form()
        load_cursos_list()
    else:
        messagebox.showerror("Error", f"Error al guardar curso: {result}")


def update_curso():
    if not db.connection:
        if not db.connect():
            return

    id_valid, curso_id = validate_numeric(CursosID.get(), "ID Curso")
    if not id_valid or not curso_id:
        messagebox.showerror("Error", "Debe ingresar un ID de curso válido")
        return

    periodo_valid, periodo_value = validate_numeric(PeriodoAcademico.get(), "Período Académico")
    if not periodo_valid:
        return

    cupo_valid, cupo_value = validate_numeric(CupoMaximo.get(), "Cupo Máximo")
    if not cupo_valid:
        return

    query = """UPDATE cursos SET periodo_academico = %s, horarios = %s, cupo_maximo = %s, 
               metodologia_evaluacion = %s WHERE id_cursos = %s"""

    parameters = (
        periodo_value,
        Horarios.get() if Horarios.get().strip() else None,
        cupo_value,
        MetodologiaEvaluacion.get() if MetodologiaEvaluacion.get().strip() else None,
        curso_id
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Curso actualizado correctamente")
        load_cursos_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar curso: {result}")


def delete_curso():
    if not db.connection:
        if not db.connect():
            return

    id_valid, curso_id = validate_numeric(CursosID.get(), "ID Curso")
    if not id_valid or not curso_id:
        messagebox.showerror("Error", "Debe ingresar un ID de curso válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este curso?"):
        query = "DELETE FROM cursos WHERE id_cursos = %s"
        success, result = db.execute_query(query, (curso_id,))

        if success:
            messagebox.showinfo("Éxito", "Curso eliminado correctamente")
            clear_curso_form()
            load_cursos_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar curso: {result}")


def search_curso():
    if not db.connection:
        if not db.connect():
            return

    id_valid, curso_id = validate_numeric(CursosID.get(), "ID Curso")
    if not id_valid or not curso_id:
        messagebox.showerror("Error", "Debe ingresar un ID de curso válido")
        return

    query = "SELECT * FROM cursos WHERE id_cursos = %s"
    success, result = db.execute_query(query, (curso_id,))

    if success and result:
        # Limpiar el Treeview y agregar solo el resultado encontrado
        for item in cursos_tree.get_children():
            cursos_tree.delete(item)
        curso = result[0]
        display_data = curso[:5]  # Primeros 5 campos para el Treeview
        cursos_tree.insert('', 'end', values=display_data)

        # Llenar el formulario
        PeriodoAcademico.delete(0, tk.END)
        PeriodoAcademico.insert(0, curso[1] if curso[1] else "")
        Horarios.delete(0, tk.END)
        Horarios.insert(0, curso[2] if curso[2] else "")
        CupoMaximo.delete(0, tk.END)
        CupoMaximo.insert(0, curso[3] if curso[3] else "")
        MetodologiaEvaluacion.delete(0, tk.END)
        MetodologiaEvaluacion.insert(0, curso[4] if curso[4] else "")
    else:
        messagebox.showinfo("No encontrado", "Curso no encontrado")
        # Opcional: Limpiar Treeview si no se encuentra
        for item in cursos_tree.get_children():
            cursos_tree.delete(item)

def clear_curso_form():
    CursosID.delete(0, tk.END)
    PeriodoAcademico.delete(0, tk.END)
    Horarios.delete(0, tk.END)
    CupoMaximo.delete(0, tk.END)
    MetodologiaEvaluacion.delete(0, tk.END)


def load_cursos_list():
    if not db.connection:
        if not db.connect():
            return

    query = "SELECT * FROM cursos"
    success, results = db.execute_query(query)
    if success:
        for item in cursos_tree.get_children():
            cursos_tree.delete(item)

        for curso in results:
            display_data = curso[:5]
            cursos_tree.insert('', 'end', values=display_data)


# =================== FUNCIONES PARA ESTUDIANTES ===================
def save_estudiante():
    if not db.connection:
        if not db.connect():
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

    success, result = db.call_procedure('sp_InsertEstudiante', parameters)

    if success:
        messagebox.showinfo("Éxito", "Estudiante guardado correctamente")
        clear_estudiante_form()
        load_estudiantes_list()
    else:
        messagebox.showerror("Error", f"Error al guardar estudiante: {result}")


def update_estudiante():
    if not db.connection:
        if not db.connect():
            return

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
        datetime.now().date(),  # Fecha nacimiento por defecto
        "Dirección por defecto",  # Dirección por defecto
        Telefono_Est.get() if Telefono_Est.get().strip() else None,
        CorreoInstitucional_Est.get() if CorreoInstitucional_Est.get().strip() else None,
        NombreAcudiente.get() if NombreAcudiente.get().strip() else None,
        ContactoEmergencia.get() if ContactoEmergencia.get().strip() else None,
        Periodo_Est.get() if Periodo_Est.get().strip() else None
    )

    success, result = db.call_procedure('sp_UpdateEstudiante', parameters)

    if success:
        messagebox.showinfo("Éxito", "Estudiante actualizado correctamente")
        load_estudiantes_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar estudiante: {result}")


def delete_estudiante():
    if not db.connection:
        if not db.connect():
            return

    id_valid, est_id = validate_numeric(EstudiantesID.get(), "ID Estudiante")
    if not id_valid or not est_id:
        messagebox.showerror("Error", "Debe ingresar un ID de estudiante válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este estudiante?"):
        success, result = db.call_procedure('sp_DeleteEstudiante', (est_id,))

        if success:
            messagebox.showinfo("Éxito", "Estudiante eliminado correctamente")
            clear_estudiante_form()
            load_estudiantes_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar estudiante: {result}")


def search_estudiante():
    if not db.connection:
        if not db.connect():
            return


    id_valid, est_id = validate_numeric(EstudiantesID.get(), "ID Estudiante")
    if id_valid and est_id:

        success, result = db.call_procedure('sp_GetEstudiante', (est_id,))
        if success and result:
            estudiante = result[0]

            for item in estudiantes_tree.get_children():
                estudiantes_tree.delete(item)
            estudiantes_tree.insert('', 'end', values=estudiante)


            Matricula.delete(0, tk.END)
            Matricula.insert(0, estudiante[1] if estudiante[1] else "")
            Nombre_Est.delete(0, tk.END)
            Nombre_Est.insert(0, estudiante[2] if estudiante[2] else "")
            Apellido_Est.delete(0, tk.END)
            Apellido_Est.insert(0, estudiante[3] if estudiante[3] else "")
            DNI_Est.delete(0, tk.END)
            DNI_Est.insert(0, estudiante[4] if estudiante[4] else "")
            Telefono_Est.delete(0, tk.END)
            Telefono_Est.insert(0, estudiante[6] if len(estudiante) > 6 and estudiante[6] else "")
            CorreoInstitucional_Est.delete(0, tk.END)
            CorreoInstitucional_Est.insert(0, estudiante[7] if len(estudiante) > 7 and estudiante[7] else "")
            NombreAcudiente.delete(0, tk.END)
            NombreAcudiente.insert(0, estudiante[9] if len(estudiante) > 9 and estudiante[9] else "")
            ContactoEmergencia.delete(0, tk.END)
            ContactoEmergencia.insert(0, estudiante[10] if len(estudiante) > 10 and estudiante[10] else "")
            FechaIngreso.delete(0, tk.END)
            if len(estudiante) > 11 and estudiante[11]:
                FechaIngreso.insert(0, estudiante[11].strftime("%Y-%m-%d") if hasattr(estudiante[11], 'strftime') else str(estudiante[11]))
            Periodo_Est.delete(0, tk.END)
            Periodo_Est.insert(0, estudiante[12] if len(estudiante) > 12 and estudiante[12] else "")
            return  # Salir si se encontró por ID
        else:
            messagebox.showinfo("No encontrado", "Estudiante no encontrado por ID")
            return

    # Fallback: Búsqueda por texto (como antes)
    search_term = Nombre_Est.get().strip()
    if not search_term:
        search_term = DNI_Est.get().strip()

    if not search_term:
        messagebox.showerror("Error", "Debe ingresar un nombre, DNI o ID para buscar")
        return

    success, result = db.call_procedure('sp_SearchEstudiantes', (search_term,))

    if success and result:
        for item in estudiantes_tree.get_children():
            estudiantes_tree.delete(item)

        for estudiante in result:
            estudiantes_tree.insert('', 'end', values=estudiante)
    else:
        messagebox.showinfo("No encontrado", "No se encontraron estudiantes")


def clear_estudiante_form():
    EstudiantesID.delete(0, tk.END)
    Matricula.delete(0, tk.END)
    Nombre_Est.delete(0, tk.END)
    Apellido_Est.delete(0, tk.END)
    DNI_Est.delete(0, tk.END)
    Telefono_Est.delete(0, tk.END)
    CorreoInstitucional_Est.delete(0, tk.END)
    Fotografia.delete(0, tk.END)
    NombreAcudiente.delete(0, tk.END)
    ContactoEmergencia.delete(0, tk.END)
    FechaIngreso.delete(0, tk.END)
    Periodo_Est.delete(0, tk.END)


def load_estudiantes_list():
    if not db.connection:
        if not db.connect():
            return

    success, results = db.call_procedure('sp_GetAllEstudiantes')
    if success:
        for item in estudiantes_tree.get_children():
            estudiantes_tree.delete(item)

        for estudiante in results:
            estudiantes_tree.insert('', 'end', values=estudiante)


# =================== FUNCIONES PARA PLAN DE ESTUDIO ===================
def save_planestudio():
    if not db.connection:
        if not db.connect():
            return

    if not validate_required(CarreraPerteneciente.get(), "Carrera Perteneciente"):
        return

    cod_valid, cod_value = validate_numeric(CodigoPlanDeEstudio.get(), "Código Plan de Estudio")
    if not cod_valid:
        return

    fecha_valid, fecha_value = validate_date(FechaAprobacion.get())
    if not fecha_valid:
        return

    nivel_valid, nivel_value = validate_numeric(NivelAsignatura.get(), "Nivel Asignatura")
    if not nivel_valid:
        return

    creditos_valid, creditos_value = validate_numeric(CreditosTotales.get(), "Créditos Totales")
    if not creditos_valid:
        return

    query = """INSERT INTO plan_estudio (cod_plan_estudio, carrera_perteneciente, fecha_aprobacion, 
               asignatura_nivel, creditos_totales, requisitos_graduacion, id_cursos) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    parameters = (
        cod_value,
        CarreraPerteneciente.get(),
        fecha_value,
        nivel_value,
        creditos_value,
        RequisitosGraduacion.get() if RequisitosGraduacion.get().strip() else None,
        1
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Plan de estudio guardado correctamente")
        clear_planestudio_form()
        load_planestudio_list()
    else:
        messagebox.showerror("Error", f"Error al guardar plan de estudio: {result}")


def update_planestudio():
    if not db.connection:
        if not db.connect():
            return

    id_valid, plan_id = validate_numeric(PlanEstudioID.get(), "ID Plan de Estudio")
    if not id_valid or not plan_id:
        messagebox.showerror("Error", "Debe ingresar un ID de plan de estudio válido")
        return

    cod_valid, cod_value = validate_numeric(CodigoPlanDeEstudio.get(), "Código Plan de Estudio")
    if not cod_valid:
        return

    fecha_valid, fecha_value = validate_date(FechaAprobacion.get())
    if not fecha_valid:
        return

    nivel_valid, nivel_value = validate_numeric(NivelAsignatura.get(), "Nivel Asignatura")
    if not nivel_valid:
        return

    creditos_valid, creditos_value = validate_numeric(CreditosTotales.get(), "Créditos Totales")
    if not creditos_valid:
        return

    query = """UPDATE plan_estudio SET cod_plan_estudio = %s, carrera_perteneciente = %s, 
               fecha_aprobacion = %s, asignatura_nivel = %s, creditos_totales = %s, 
               requisitos_graduacion = %s WHERE id_plan_estudio = %s"""

    parameters = (
        cod_value,
        CarreraPerteneciente.get(),
        fecha_value,
        nivel_value,
        creditos_value,
        RequisitosGraduacion.get() if RequisitosGraduacion.get().strip() else None,
        plan_id
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Plan de estudio actualizado correctamente")
        load_planestudio_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar plan de estudio: {result}")


def delete_planestudio():
    if not db.connection:
        if not db.connect():
            return

    id_valid, plan_id = validate_numeric(PlanEstudioID.get(), "ID Plan de Estudio")
    if not id_valid or not plan_id:
        messagebox.showerror("Error", "Debe ingresar un ID de plan de estudio válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este plan de estudio?"):
        query = "DELETE FROM plan_estudio WHERE id_plan_estudio = %s"
        success, result = db.execute_query(query, (plan_id,))

        if success:
            messagebox.showinfo("Éxito", "Plan de estudio eliminado correctamente")
            clear_planestudio_form()
            load_planestudio_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar plan de estudio: {result}")


def search_planestudio():
    if not db.connection:
        if not db.connect():
            return

    id_valid, plan_id = validate_numeric(PlanEstudioID.get(), "ID Plan de Estudio")
    if not id_valid or not plan_id:
        messagebox.showerror("Error", "Debe ingresar un ID de plan de estudio válido")
        return

    query = "SELECT * FROM plan_estudio WHERE id_plan_estudio = %s"
    success, result = db.execute_query(query, (plan_id,))

    if success and result:
        # Limpiar el Treeview y agregar solo el resultado encontrado
        for item in planestudio_tree.get_children():
            planestudio_tree.delete(item)
        plan = result[0]
        planestudio_tree.insert('', 'end', values=plan)

        # Llenar el formulario
        CodigoPlanDeEstudio.delete(0, tk.END)
        CodigoPlanDeEstudio.insert(0, plan[1] if plan[1] else "")
        CarreraPerteneciente.delete(0, tk.END)
        CarreraPerteneciente.insert(0, plan[2] if plan[2] else "")
        FechaAprobacion.delete(0, tk.END)
        if plan[3]:
            FechaAprobacion.insert(0, plan[3].strftime("%Y-%m-%d"))
        NivelAsignatura.delete(0, tk.END)
        NivelAsignatura.insert(0, plan[4] if plan[4] else "")
        CreditosTotales.delete(0, tk.END)
        CreditosTotales.insert(0, plan[5] if plan[5] else "")
        RequisitosGraduacion.delete(0, tk.END)
        RequisitosGraduacion.insert(0, plan[6] if plan[6] else "")
    else:
        messagebox.showinfo("No encontrado", "Plan de estudio no encontrado")
        # Opcional: Limpiar Treeview si no se encuentra
        for item in planestudio_tree.get_children():
            planestudio_tree.delete(item)


def clear_planestudio_form():
    PlanEstudioID.delete(0, tk.END)
    CodigoPlanDeEstudio.delete(0, tk.END)
    CarreraPerteneciente.delete(0, tk.END)
    FechaAprobacion.delete(0, tk.END)
    NivelAsignatura.delete(0, tk.END)
    RequisitosGraduacion.delete(0, tk.END)
    CreditosTotales.delete(0, tk.END)


def load_planestudio_list():
    if not db.connection:
        if not db.connect():
            return

    query = "SELECT * FROM plan_estudio"
    success, results = db.execute_query(query)
    if success:
        for item in planestudio_tree.get_children():
            planestudio_tree.delete(item)

        for plan in results:
            planestudio_tree.insert('', 'end', values=plan)


# =================== FUNCIONES PARA PRÉSTAMOS ===================
def save_prestamo():
    if not db.connection:
        if not db.connect():
            return

    cod_valid, cod_value = validate_numeric(CodigoPrestamo.get(), "Código Préstamo")
    if not cod_valid:
        return

    fecha_prest_valid, fecha_prest = validate_date(FechaPrestamo.get())
    if not fecha_prest_valid:
        return

    fecha_dev_valid, fecha_dev = validate_date(FechaDevolucion.get())
    if not fecha_dev_valid:
        return

    multas_valid, multas_value = validate_numeric(MultasAplicadas.get(),
                                                  "Multas Aplicadas") if MultasAplicadas.get().strip() else (True, 0)
    if not multas_valid:
        return

    query = """INSERT INTO prestamos (cod_prestamos, fecha_prestamo, fecha_devolucion, estado, 
               multas_aplicadas, id_profesores, dni_estudiantes, id_biblioteca) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

    parameters = (
        cod_value,
        fecha_prest,
        fecha_dev,
        Estado.get() if Estado.get().strip() else "Activo",
        multas_value,
        1,  # id_profesores por defecto
        "1234567890",  # dni_estudiantes por defecto
        1  # id_biblioteca por defecto
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Préstamo guardado correctamente")
        clear_prestamo_form()
        load_prestamos_list()
    else:
        messagebox.showerror("Error", f"Error al guardar préstamo: {result}")


def update_prestamo():
    if not db.connection:
        if not db.connect():
            return

    id_valid, prest_id = validate_numeric(PrestamosID.get(), "ID Préstamo")
    if not id_valid or not prest_id:
        messagebox.showerror("Error", "Debe ingresar un ID de préstamo válido")
        return

    cod_valid, cod_value = validate_numeric(CodigoPrestamo.get(), "Código Préstamo")
    if not cod_valid:
        return

    fecha_prest_valid, fecha_prest = validate_date(FechaPrestamo.get())
    if not fecha_prest_valid:
        return

    fecha_dev_valid, fecha_dev = validate_date(FechaDevolucion.get())
    if not fecha_dev_valid:
        return

    multas_valid, multas_value = validate_numeric(MultasAplicadas.get(),
                                                  "Multas Aplicadas") if MultasAplicadas.get().strip() else (True, 0)
    if not multas_valid:
        return

    query = """UPDATE prestamos SET cod_prestamos = %s, fecha_prestamo = %s, fecha_devolucion = %s, 
               estado = %s, multas_aplicadas = %s WHERE id_prestamos = %s"""

    parameters = (
        cod_value,
        fecha_prest,
        fecha_dev,
        Estado.get() if Estado.get().strip() else "Activo",
        multas_value,
        prest_id
    )

    success, result = db.execute_query(query, parameters)

    if success:
        messagebox.showinfo("Éxito", "Préstamo actualizado correctamente")
        load_prestamos_list()
    else:
        messagebox.showerror("Error", f"Error al actualizar préstamo: {result}")


def delete_prestamo():
    if not db.connection:
        if not db.connect():
            return

    id_valid, prest_id = validate_numeric(PrestamosID.get(), "ID Préstamo")
    if not id_valid or not prest_id:
        messagebox.showerror("Error", "Debe ingresar un ID de préstamo válido")
        return

    if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este préstamo?"):
        query = "DELETE FROM prestamos WHERE id_prestamos = %s"
        success, result = db.execute_query(query, (prest_id,))

        if success:
            messagebox.showinfo("Éxito", "Préstamo eliminado correctamente")
            clear_prestamo_form()
            load_prestamos_list()
        else:
            messagebox.showerror("Error", f"Error al eliminar préstamo: {result}")


def search_prestamo():
    if not db.connection:
        if not db.connect():
            return

    id_valid, prest_id = validate_numeric(PrestamosID.get(), "ID Préstamo")
    if not id_valid or not prest_id:
        messagebox.showerror("Error", "Debe ingresar un ID de préstamo válido")
        return

    query = "SELECT * FROM prestamos WHERE id_prestamos = %s"
    success, result = db.execute_query(query, (prest_id,))

    if success and result:
        # Limpiar el Treeview y agregar solo el resultado encontrado
        for item in prestamos_tree.get_children():
            prestamos_tree.delete(item)
        prestamo = result[0]
        display_data = prestamo[:6]  # Primeros 6 campos para el Treeview
        prestamos_tree.insert('', 'end', values=display_data)

        # Llenar el formulario (como ya lo hacías)
        CodigoPrestamo.delete(0, tk.END)
        CodigoPrestamo.insert(0, prestamo[1] if prestamo[1] else "")
        FechaPrestamo.delete(0, tk.END)
        if prestamo[2]:
            FechaPrestamo.insert(0, prestamo[2].strftime("%Y-%m-%d"))
        FechaDevolucion.delete(0, tk.END)
        if prestamo[3]:
            FechaDevolucion.insert(0, prestamo[3].strftime("%Y-%m-%d"))
        Estado.delete(0, tk.END)
        Estado.insert(0, prestamo[4] if prestamo[4] else "")
        MultasAplicadas.delete(0, tk.END)
        MultasAplicadas.insert(0, prestamo[5] if prestamo[5] else "")
    else:
        messagebox.showinfo("No encontrado", "Préstamo no encontrado")
        # Opcional: Limpiar Treeview si no se encuentra
        for item in prestamos_tree.get_children():
            prestamos_tree.delete(item)


def clear_prestamo_form():
    PrestamosID.delete(0, tk.END)
    CodigoPrestamo.delete(0, tk.END)
    FechaPrestamo.delete(0, tk.END)
    FechaDevolucion.delete(0, tk.END)
    MultasAplicadas.delete(0, tk.END)
    Estado.delete(0, tk.END)


def load_prestamos_list():
    if not db.connection:
        if not db.connect():
            return

    query = "SELECT * FROM prestamos"
    success, results = db.execute_query(query)
    if success:
        for item in prestamos_tree.get_children():
            prestamos_tree.delete(item)

        for prestamo in results:
            display_data = prestamo[:6]  # Primeros 6 campos
            prestamos_tree.insert('', 'end', values=display_data)


# =================== EVENTOS DE SELECCIÓN EN TREEVIEWS ===================
def on_asignatura_select(event):
    selection = asignaturas_tree.selection()
    if selection:
        item = asignaturas_tree.item(selection[0])
        values = item['values']

        AsignaturasID.delete(0, tk.END)
        AsignaturasID.insert(0, values[0])
        CodAsignaturas.delete(0, tk.END)
        CodAsignaturas.insert(0, values[1])
        NombreAsignaturas.delete(0, tk.END)
        NombreAsignaturas.insert(0, values[2])
        AreaCrecimiento.delete(0, tk.END)
        AreaCrecimiento.insert(0, values[3] if len(values) > 3 else "")
        HorasTecnicas.delete(0, tk.END)
        HorasTecnicas.insert(0, values[4] if len(values) > 4 else "")
        HorasPracticas.delete(0, tk.END)
        HorasPracticas.insert(0, values[5] if len(values) > 5 else "")
        CreditosAcademicos.delete(0, tk.END)
        CreditosAcademicos.insert(0, values[6] if len(values) > 6 else "")
        RequisitoPrevios.delete(0, tk.END)
        RequisitoPrevios.insert(0, values[7] if len(values) > 7 else "")
        ObjetivosGenerales.delete(0, tk.END)
        ObjetivosGenerales.insert(0, values[8] if len(values) > 8 else "")
        ObjetivosEspecificos.delete(0, tk.END)
        ObjetivosEspecificos.insert(0, values[9] if len(values) > 9 else "")
        BibliografiaRecomendada.delete(0, tk.END)
        BibliografiaRecomendada.insert(0, values[10] if len(values) > 10 else "")
        Periodo.delete(0, tk.END)
        Periodo.insert(0, values[11] if len(values) > 11 else "")


def on_profesor_select(event):
    selection = profesores_tree.selection()
    if selection:
        item = profesores_tree.item(selection[0])
        values = item['values']

        ProfesoresID.delete(0, tk.END)
        ProfesoresID.insert(0, values[0])
        CodigoEmplead.delete(0, tk.END)
        CodigoEmplead.insert(0, values[1])
        Nombre.delete(0, tk.END)
        Nombre.insert(0, values[2])
        Apellido.delete(0, tk.END)
        Apellido.insert(0, values[3])
        DNI.delete(0, tk.END)
        DNI.insert(0, values[4])
        FechaNacimiento.delete(0, tk.END)
        if len(values) > 5 and values[5]:
            FechaNacimiento.insert(0, str(values[5]))
        Direccion.delete(0, tk.END)
        Direccion.insert(0, values[6] if len(values) > 6 else "")
        Telefono.delete(0, tk.END)
        Telefono.insert(0, values[7] if len(values) > 7 else "")
        CorreoInstitucional.delete(0, tk.END)
        CorreoInstitucional.insert(0, values[8] if len(values) > 8 else "")
        NivelAcademico.delete(0, tk.END)
        NivelAcademico.insert(0, values[9] if len(values) > 9 else "")
        Especialidad.delete(0, tk.END)
        Especialidad.insert(0, values[10] if len(values) > 10 else "")
        AñosExperiencia.delete(0, tk.END)
        AñosExperiencia.insert(0, values[11] if len(values) > 11 else "")
        FechaContratacion.delete(0, tk.END)
        if len(values) > 12 and values[12]:
            FechaContratacion.insert(0, str(values[12]))
        TipoContrato.delete(0, tk.END)
        TipoContrato.insert(0, values[13] if len(values) > 13 else "")


def on_estudiante_select(event):
    selection = estudiantes_tree.selection()
    if selection:
        item = estudiantes_tree.item(selection[0])
        values = item['values']

        EstudiantesID.delete(0, tk.END)
        EstudiantesID.insert(0, values[0])
        Matricula.delete(0, tk.END)
        Matricula.insert(0, values[1])
        Nombre_Est.delete(0, tk.END)
        Nombre_Est.insert(0, values[2])
        Apellido_Est.delete(0, tk.END)
        Apellido_Est.insert(0, values[3])
        DNI_Est.delete(0, tk.END)
        DNI_Est.insert(0, values[4])
        Telefono_Est.delete(0, tk.END)
        Telefono_Est.insert(0, values[6] if len(values) > 6 else "")
        CorreoInstitucional_Est.delete(0, tk.END)
        CorreoInstitucional_Est.insert(0, values[7] if len(values) > 7 else "")
        NombreAcudiente.delete(0, tk.END)
        NombreAcudiente.insert(0, values[9] if len(values) > 9 else "")
        ContactoEmergencia.delete(0, tk.END)
        ContactoEmergencia.insert(0, values[10] if len(values) > 10 else "")
        FechaIngreso.delete(0, tk.END)
        if len(values) > 11 and values[11]:
            FechaIngreso.insert(0, str(values[11]))
        Periodo_Est.delete(0, tk.END)
        Periodo_Est.insert(0, values[12] if len(values) > 12 else "")


# =================== FUNCIÓN DE CARGA INICIAL ===================
def load_initial_data():
    load_asignaturas_list()
    load_aulas_list()
    load_profesores_list()
    load_calificaciones_list()
    load_biblioteca_list()
    load_cursos_list()
    load_estudiantes_list()
    load_planestudio_list()
    load_prestamos_list()


def on_closing():
    db.disconnect()
    root.destroy()


# =================== CREAR LA INTERFAZ GRÁFICA ===================
# Crear la ventana principal
root = tk.Tk()
root.geometry('1200x700')
root.title("Sistema de Gestión Académica - Horizonte del Saber")

# Conectar a la base de datos al iniciar
if not db.connect():
    root.destroy()
    exit()

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
notebook.add(tab4, text="Calificaciones")
notebook.add(tab5, text="Biblioteca")
notebook.add(tab6, text="Cursos")
notebook.add(tab7, text="Estudiantes")
notebook.add(tab8, text="Plan de Estudio")
notebook.add(tab9, text="Préstamos")

# Empaquetar el Notebook para que se muestre en la ventana
notebook.pack(expand=True, fill="both")


# =================== PESTAÑA 1 (ASIGNATURAS) ===================
# Crear frame principal para asignaturas
main_frame_asignaturas = tk.Frame(tab1)
main_frame_asignaturas.pack(fill="both", expand=True, padx=10, pady=10)

# Frame izquierdo para formulario
left_frame_asignaturas = tk.Frame(main_frame_asignaturas)
left_frame_asignaturas.pack(side="left", fill="y", padx=(0, 10))

# Título
titulo = tk.Label(left_frame_asignaturas, text="GESTIÓN DE ASIGNATURAS", font=("Arial", 16, "bold"), fg="blue")
titulo.pack(pady=20)

# Frame para contener el formulario
form_frame_asignaturas = tk.Frame(left_frame_asignaturas)
form_frame_asignaturas.pack(pady=20, anchor="w", padx=20)

# Campos del formulario
tk.Label(form_frame_asignaturas, text="AsignaturasID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
AsignaturasID = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
AsignaturasID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="CodAsignaturas:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
CodAsignaturas = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
CodAsignaturas.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="NombreAsignaturas:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
NombreAsignaturas = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
NombreAsignaturas.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="AreaCrecimiento:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
AreaCrecimiento = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
AreaCrecimiento.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="HorasTecnicas:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
HorasTecnicas = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
HorasTecnicas.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="HorasPracticas:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
HorasPracticas = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
HorasPracticas.grid(row=6, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="CreditosAcademicos:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=8)
CreditosAcademicos = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
CreditosAcademicos.grid(row=7, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="RequisitoPrevios:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=8)
RequisitoPrevios = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
RequisitoPrevios.grid(row=8, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="ObjetivosGenerales:", font=("Arial", 12)).grid(row=9, column=0, sticky="w", padx=(0, 10), pady=8)
ObjetivosGenerales = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
ObjetivosGenerales.grid(row=9, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="ObjetivosEspecificos:", font=("Arial", 12)).grid(row=10, column=0, sticky="w", padx=(0, 10), pady=8)
ObjetivosEspecificos = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
ObjetivosEspecificos.grid(row=10, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="Bibliografia Recomendada:", font=("Arial", 12)).grid(row=11, column=0, sticky="w", padx=(0, 10), pady=8)
BibliografiaRecomendada = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
BibliografiaRecomendada.grid(row=11, column=1, sticky="w", pady=8)

tk.Label(form_frame_asignaturas, text="Periodo:", font=("Arial", 12)).grid(row=12, column=0, sticky="w", padx=(0, 10), pady=8)
Periodo = tk.Entry(form_frame_asignaturas, width=25, font=("Arial", 12), relief="solid", bd=1)
Periodo.grid(row=12, column=1, sticky="w", pady=8)

# Frame para botones
button_frame_asignaturas = tk.Frame(left_frame_asignaturas)
button_frame_asignaturas.pack(pady=20)

btn_save_asignatura = tk.Button(button_frame_asignaturas, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_asignatura.pack(side=tk.LEFT, padx=3)

btn_update_asignatura = tk.Button(button_frame_asignaturas, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_asignatura.pack(side=tk.LEFT, padx=3)

btn_delete_asignatura = tk.Button(button_frame_asignaturas, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_asignatura.pack(side=tk.LEFT, padx=3)

btn_search_asignatura = tk.Button(button_frame_asignaturas, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_asignatura.pack(side=tk.LEFT, padx=3)

btn_clear_asignatura = tk.Button(button_frame_asignaturas, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_asignatura.pack(side=tk.LEFT, padx=3)
btn_save_asignatura.config(command=save_asignatura)
btn_update_asignatura.config(command=update_asignatura)
btn_delete_asignatura.config(command=delete_asignatura)
btn_search_asignatura.config(command=search_asignatura)
btn_clear_asignatura.config(command=clear_asignatura_form)

# Frame derecho para lista
right_frame_asignaturas = tk.Frame(main_frame_asignaturas)
right_frame_asignaturas.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_asignaturas, text="LISTA DE ASIGNATURAS", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar asignaturas
asignaturas_tree = ttk.Treeview(right_frame_asignaturas, columns=('ID', 'Codigo', 'Nombre', 'Area', 'HTec', 'HPrac', 'Creditos', 'Requisitos', 'ObjGen', 'ObjEsp', 'Bibliografia', 'Periodo'), show='headings', height=20)
asignaturas_tree.heading('ID', text='ID')
asignaturas_tree.heading('Codigo', text='Código')
asignaturas_tree.heading('Nombre', text='Nombre')
asignaturas_tree.heading('Area', text='Área')
asignaturas_tree.heading('HTec', text='H. Téc.')
asignaturas_tree.heading('HPrac', text='H. Prác.')
asignaturas_tree.heading('Creditos', text='Créditos')
asignaturas_tree.heading('Requisitos', text='Requisitos')
asignaturas_tree.heading('ObjGen', text='Obj. Gen.')
asignaturas_tree.heading('ObjEsp', text='Obj. Esp.')
asignaturas_tree.heading('Bibliografia', text='Bibliografía')
asignaturas_tree.heading('Periodo', text='Periodo')

asignaturas_tree.column('ID', width=50)
asignaturas_tree.column('Codigo', width=80)
asignaturas_tree.column('Nombre', width=120)
asignaturas_tree.column('Area', width=80)
asignaturas_tree.column('HTec', width=60)
asignaturas_tree.column('HPrac', width=60)
asignaturas_tree.column('Creditos', width=60)
asignaturas_tree.column('Requisitos', width=80)
asignaturas_tree.column('ObjGen', width=80)
asignaturas_tree.column('ObjEsp', width=80)
asignaturas_tree.column('Bibliografia', width=100)
asignaturas_tree.column('Periodo', width=60)

asignaturas_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para asignaturas
scrollbar_asignaturas = ttk.Scrollbar(right_frame_asignaturas, orient="vertical", command=asignaturas_tree.yview)
asignaturas_tree.configure(yscrollcommand=scrollbar_asignaturas.set)
scrollbar_asignaturas.pack(side="right", fill="y")

# =================== PESTAÑA 2 (AULAS) ===================
main_frame_aulas = tk.Frame(tab2)
main_frame_aulas.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_aulas = tk.Frame(main_frame_aulas)
left_frame_aulas.pack(side="left", fill="y", padx=(0, 10))

titulo2 = tk.Label(left_frame_aulas, text="GESTIÓN DE AULAS", font=("Arial", 16, "bold"), fg="blue")
titulo2.pack(pady=20)

form_frame_aulas = tk.Frame(left_frame_aulas)
form_frame_aulas.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_aulas, text="AulasID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
AulasID = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
AulasID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_aulas, text="NumeroIdentificador:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
NumeroIdentificador = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
NumeroIdentificador.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_aulas, text="Edificio:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
Edificio = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
Edificio.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_aulas, text="NumeroPiso:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
NumeroPiso = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
NumeroPiso.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_aulas, text="CapacidadEstudiantes:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
CapacidadEstudiantes = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
CapacidadEstudiantes.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_aulas, text="TipoCurso:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
TipoCurso = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
TipoCurso.grid(row=6, column=1, sticky="w", pady=8)

tk.Label(form_frame_aulas, text="EquipamientoDisponible:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=8)
EquipamientoDisponible = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
EquipamientoDisponible.grid(row=7, column=1, sticky="w", pady=8)

tk.Label(form_frame_aulas, text="EstadoActual:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=8)
EstadoActual = tk.Entry(form_frame_aulas, width=25, font=("Arial", 12), relief="solid", bd=1)
EstadoActual.grid(row=8, column=1, sticky="w", pady=8)

# Frame para botones de aulas
button_frame_aulas = tk.Frame(left_frame_aulas)
button_frame_aulas.pack(pady=20)

btn_save_aula = tk.Button(button_frame_aulas, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_aula.pack(side=tk.LEFT, padx=3)

btn_update_aula = tk.Button(button_frame_aulas, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_aula.pack(side=tk.LEFT, padx=3)

btn_delete_aula = tk.Button(button_frame_aulas, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_aula.pack(side=tk.LEFT, padx=3)

btn_search_aula = tk.Button(button_frame_aulas, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_aula.pack(side=tk.LEFT, padx=3)

btn_clear_aula = tk.Button(button_frame_aulas, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_aula.pack(side=tk.LEFT, padx=3)
btn_save_aula.config(command=save_aula)
btn_update_aula.config(command=update_aula)
btn_delete_aula.config(command=delete_aula)
btn_search_aula.config(command=search_aula)
btn_clear_aula.config(command=clear_aula_form)

# Frame derecho para lista de aulas
right_frame_aulas = tk.Frame(main_frame_aulas)
right_frame_aulas.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_aulas, text="LISTA DE AULAS", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar aulas
aulas_tree = ttk.Treeview(right_frame_aulas, columns=('ID', 'Numero', 'Edificio', 'Piso', 'Capacidad', 'Tipo', 'Equipamiento', 'Estado'), show='headings', height=20)
aulas_tree.heading('ID', text='ID')
aulas_tree.heading('Numero', text='Número')
aulas_tree.heading('Edificio', text='Edificio')
aulas_tree.heading('Piso', text='Piso')
aulas_tree.heading('Capacidad', text='Capacidad')
aulas_tree.heading('Tipo', text='Tipo Curso')
aulas_tree.heading('Equipamiento', text='Equipamiento')
aulas_tree.heading('Estado', text='Estado')

aulas_tree.column('ID', width=50)
aulas_tree.column('Numero', width=80)
aulas_tree.column('Edificio', width=100)
aulas_tree.column('Piso', width=60)
aulas_tree.column('Capacidad', width=80)
aulas_tree.column('Tipo', width=100)
aulas_tree.column('Equipamiento', width=120)
aulas_tree.column('Estado', width=80)

aulas_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para aulas
scrollbar_aulas = ttk.Scrollbar(right_frame_aulas, orient="vertical", command=aulas_tree.yview)
aulas_tree.configure(yscrollcommand=scrollbar_aulas.set)
scrollbar_aulas.pack(side="right", fill="y")

# =================== PESTAÑA 3 (PROFESORES) ===================
main_frame_profesores = tk.Frame(tab3)
main_frame_profesores.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_profesores = tk.Frame(main_frame_profesores)
left_frame_profesores.pack(side="left", fill="y", padx=(0, 10))

titulo3 = tk.Label(left_frame_profesores, text="GESTIÓN DE PROFESORES", font=("Arial", 16, "bold"), fg="blue")
titulo3.pack(pady=20)

form_frame_profesores = tk.Frame(left_frame_profesores)
form_frame_profesores.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_profesores, text="ProfesoresID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
ProfesoresID = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
ProfesoresID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="CodigoEmpleado:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
CodigoEmplead = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoEmplead.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="Nombre:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
Nombre = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
Nombre.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="Apellido:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
Apellido = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
Apellido.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="DNI:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
DNI = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
DNI.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="FechaNacimiento:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
FechaNacimiento = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaNacimiento.grid(row=6, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="Direccion:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=8)
Direccion = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
Direccion.grid(row=7, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="Telefono:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=8)
Telefono = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
Telefono.grid(row=8, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="CorreoInstitucional:", font=("Arial", 12)).grid(row=9, column=0, sticky="w", padx=(0, 10), pady=8)
CorreoInstitucional = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
CorreoInstitucional.grid(row=9, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="NivelAcademico:", font=("Arial", 12)).grid(row=10, column=0, sticky="w", padx=(0, 10), pady=8)
NivelAcademico = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
NivelAcademico.grid(row=10, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="Especialidad:", font=("Arial", 12)).grid(row=11, column=0, sticky="w", padx=(0, 10), pady=8)
Especialidad = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
Especialidad.grid(row=11, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="AñosExperiencia:", font=("Arial", 12)).grid(row=12, column=0, sticky="w", padx=(0, 10), pady=8)
AñosExperiencia = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
AñosExperiencia.grid(row=12, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="FechaContratacion:", font=("Arial", 12)).grid(row=13, column=0, sticky="w", padx=(0, 10), pady=8)
FechaContratacion = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaContratacion.grid(row=13, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="TipoContrato:", font=("Arial", 12)).grid(row=14, column=0, sticky="w", padx=(0, 10), pady=8)
TipoContrato = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
TipoContrato.grid(row=14, column=1, sticky="w", pady=8)

tk.Label(form_frame_profesores, text="CursoEspecializado:", font=("Arial", 12)).grid(row=15, column=0, sticky="w", padx=(0, 10), pady=8)
CursoEspecializado = tk.Entry(form_frame_profesores, width=25, font=("Arial", 12), relief="solid", bd=1)
CursoEspecializado.grid(row=15, column=1, sticky="w", pady=8)

# Frame para botones de profesores
button_frame_profesores = tk.Frame(left_frame_profesores)
button_frame_profesores.pack(pady=20)

btn_save_profesor = tk.Button(button_frame_profesores, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_profesor.pack(side=tk.LEFT, padx=3)

btn_update_profesor = tk.Button(button_frame_profesores, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_profesor.pack(side=tk.LEFT, padx=3)

btn_delete_profesor = tk.Button(button_frame_profesores, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_profesor.pack(side=tk.LEFT, padx=3)

btn_search_profesor = tk.Button(button_frame_profesores, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_profesor.pack(side=tk.LEFT, padx=3)

btn_clear_profesor = tk.Button(button_frame_profesores, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_profesor.pack(side=tk.LEFT, padx=3)
btn_save_profesor.config(command=save_profesor)
btn_update_profesor.config(command=update_profesor)
btn_delete_profesor.config(command=delete_profesor)
btn_search_profesor.config(command=search_profesor)
btn_clear_profesor.config(command=clear_profesor_form)

# Frame derecho para lista de profesores
right_frame_profesores = tk.Frame(main_frame_profesores)
right_frame_profesores.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_profesores, text="LISTA DE PROFESORES", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar profesores
profesores_tree = ttk.Treeview(right_frame_profesores, columns=('ID', 'Codigo', 'Nombre', 'Apellido', 'DNI', 'Nacimiento', 'Telefono', 'Correo', 'Nivel', 'Especialidad', 'Experiencia', 'Contratacion', 'Contrato'), show='headings', height=20)
profesores_tree.heading('ID', text='ID')
profesores_tree.heading('Codigo', text='Código')
profesores_tree.heading('Nombre', text='Nombre')
profesores_tree.heading('Apellido', text='Apellido')
profesores_tree.heading('DNI', text='DNI')
profesores_tree.heading('Nacimiento', text='Nacimiento')
profesores_tree.heading('Telefono', text='Teléfono')
profesores_tree.heading('Correo', text='Correo')
profesores_tree.heading('Nivel', text='Nivel Acad.')
profesores_tree.heading('Especialidad', text='Especialidad')
profesores_tree.heading('Experiencia', text='Experiencia')
profesores_tree.heading('Contratacion', text='Contratación')
profesores_tree.heading('Contrato', text='Contrato')

profesores_tree.column('ID', width=50)
profesores_tree.column('Codigo', width=80)
profesores_tree.column('Nombre', width=100)
profesores_tree.column('Apellido', width=100)
profesores_tree.column('DNI', width=80)
profesores_tree.column('Nacimiento', width=100)
profesores_tree.column('Telefono', width=80)
profesores_tree.column('Correo', width=120)
profesores_tree.column('Nivel', width=100)
profesores_tree.column('Especialidad', width=100)
profesores_tree.column('Experiencia', width=80)
profesores_tree.column('Contratacion', width=100)
profesores_tree.column('Contrato', width=100)

profesores_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para profesores
scrollbar_profesores = ttk.Scrollbar(right_frame_profesores, orient="vertical", command=profesores_tree.yview)
profesores_tree.configure(yscrollcommand=scrollbar_profesores.set)
scrollbar_profesores.pack(side="right", fill="y")

# =================== PESTAÑA 4 (CALIFICACIONES) ===================
main_frame_calificaciones = tk.Frame(tab4)
main_frame_calificaciones.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_calificaciones = tk.Frame(main_frame_calificaciones)
left_frame_calificaciones.pack(side="left", fill="y", padx=(0, 10))

titulo4 = tk.Label(left_frame_calificaciones, text="GESTIÓN DE CALIFICACIONES", font=("Arial", 16, "bold"), fg="blue")
titulo4.pack(pady=20)

form_frame_calificaciones = tk.Frame(left_frame_calificaciones)
form_frame_calificaciones.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_calificaciones, text="CalificacionesID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
CalificacionesID = tk.Entry(form_frame_calificaciones, width=25, font=("Arial", 12), relief="solid", bd=1)
CalificacionesID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_calificaciones, text="TipoEvaluacion:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
TipoEvaluacion = tk.Entry(form_frame_calificaciones, width=25, font=("Arial", 12), relief="solid", bd=1)
TipoEvaluacion.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_calificaciones, text="FechaCalificado:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
FechaCalificado = tk.Entry(form_frame_calificaciones, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaCalificado.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_calificaciones, text="Nota:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
Nota = tk.Entry(form_frame_calificaciones, width=25, font=("Arial", 12), relief="solid", bd=1)
Nota.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_calificaciones, text="PorcentajeTotal:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
PorcentajeTotal = tk.Entry(form_frame_calificaciones, width=25, font=("Arial", 12), relief="solid", bd=1)
PorcentajeTotal.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_calificaciones, text="Observaciones:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
Observaciones = tk.Entry(form_frame_calificaciones, width=25, font=("Arial", 12), relief="solid", bd=1)
Observaciones.grid(row=6, column=1, sticky="w", pady=8)

# Frame para botones de calificaciones
button_frame_calificaciones = tk.Frame(left_frame_calificaciones)
button_frame_calificaciones.pack(pady=20)

btn_save_calificacion = tk.Button(button_frame_calificaciones, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_calificacion.pack(side=tk.LEFT, padx=3)

btn_update_calificacion = tk.Button(button_frame_calificaciones, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_calificacion.pack(side=tk.LEFT, padx=3)

btn_delete_calificacion = tk.Button(button_frame_calificaciones, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_calificacion.pack(side=tk.LEFT, padx=3)

btn_search_calificacion = tk.Button(button_frame_calificaciones, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_calificacion.pack(side=tk.LEFT, padx=3)

btn_clear_calificacion = tk.Button(button_frame_calificaciones, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_calificacion.pack(side=tk.LEFT, padx=3)
btn_save_calificacion.config(command=save_calificacion)
btn_update_calificacion.config(command=update_calificacion)
btn_delete_calificacion.config(command=delete_calificacion)
btn_search_calificacion.config(command=search_calificacion)
btn_clear_calificacion.config(command=clear_calificacion_form)

# Frame derecho para lista de calificaciones
right_frame_calificaciones = tk.Frame(main_frame_calificaciones)
right_frame_calificaciones.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_calificaciones, text="LISTA DE CALIFICACIONES", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar calificaciones
calificaciones_tree = ttk.Treeview(right_frame_calificaciones, columns=('ID', 'TipoEvaluacion', 'Fecha', 'Nota', 'Porcentaje', 'Observaciones'), show='headings', height=20)
calificaciones_tree.heading('ID', text='ID')
calificaciones_tree.heading('TipoEvaluacion', text='Tipo Evaluación')
calificaciones_tree.heading('Fecha', text='Fecha')
calificaciones_tree.heading('Nota', text='Nota')
calificaciones_tree.heading('Porcentaje', text='Porcentaje')
calificaciones_tree.heading('Observaciones', text='Observaciones')

calificaciones_tree.column('ID', width=50)
calificaciones_tree.column('TipoEvaluacion', width=120)
calificaciones_tree.column('Fecha', width=100)
calificaciones_tree.column('Nota', width=80)
calificaciones_tree.column('Porcentaje', width=100)
calificaciones_tree.column('Observaciones', width=150)

calificaciones_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para calificaciones
scrollbar_calificaciones = ttk.Scrollbar(right_frame_calificaciones, orient="vertical", command=calificaciones_tree.yview)
calificaciones_tree.configure(yscrollcommand=scrollbar_calificaciones.set)
scrollbar_calificaciones.pack(side="right", fill="y")

# =================== PESTAÑA 5 (BIBLIOTECA) ===================
main_frame_biblioteca = tk.Frame(tab5)
main_frame_biblioteca.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_biblioteca = tk.Frame(main_frame_biblioteca)
left_frame_biblioteca.pack(side="left", fill="y", padx=(0, 10))

titulo5 = tk.Label(left_frame_biblioteca, text="GESTIÓN DE BIBLIOTECA", font=("Arial", 16, "bold"), fg="blue")
titulo5.pack(pady=20)

form_frame_biblioteca = tk.Frame(left_frame_biblioteca)
form_frame_biblioteca.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_biblioteca, text="BibliotecaID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
BibliotecaID = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
BibliotecaID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="CodigoMaterialBiblioteca:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
CodigoMaterialBiblioteca = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoMaterialBiblioteca.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="Titulo:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
Titulo = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
Titulo.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="Actores:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
Actores = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
Actores.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="Editorial:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
Editorial = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
Editorial.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="AñoPublicado:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
AñoPublicado = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
AñoPublicado.grid(row=6, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="ISBN:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=8)
ISBN = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
ISBN.grid(row=7, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="CategoriaTematica:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=8)
CategoriaTematica = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
CategoriaTematica.grid(row=8, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="Formato:", font=("Arial", 12)).grid(row=9, column=0, sticky="w", padx=(0, 10), pady=8)
Formato = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
Formato.grid(row=9, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="CantidadDisponible:", font=("Arial", 12)).grid(row=10, column=0, sticky="w", padx=(0, 10), pady=8)
CantidadDisponible = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
CantidadDisponible.grid(row=10, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="UbicacionFisica:", font=("Arial", 12)).grid(row=11, column=0, sticky="w", padx=(0, 10), pady=8)
UbicacionFisica = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
UbicacionFisica.grid(row=11, column=1, sticky="w", pady=8)

tk.Label(form_frame_biblioteca, text="Edicion:", font=("Arial", 12)).grid(row=12, column=0, sticky="w", padx=(0, 10), pady=8)
Edicion = tk.Entry(form_frame_biblioteca, width=25, font=("Arial", 12), relief="solid", bd=1)
Edicion.grid(row=12, column=1, sticky="w", pady=8)

# Frame para botones de biblioteca
button_frame_biblioteca = tk.Frame(left_frame_biblioteca)
button_frame_biblioteca.pack(pady=20)

btn_save_biblioteca = tk.Button(button_frame_biblioteca, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_biblioteca.pack(side=tk.LEFT, padx=3)

btn_update_biblioteca = tk.Button(button_frame_biblioteca, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_biblioteca.pack(side=tk.LEFT, padx=3)

btn_delete_biblioteca = tk.Button(button_frame_biblioteca, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_biblioteca.pack(side=tk.LEFT, padx=3)

btn_search_biblioteca = tk.Button(button_frame_biblioteca, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_biblioteca.pack(side=tk.LEFT, padx=3)

btn_clear_biblioteca = tk.Button(button_frame_biblioteca, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_biblioteca.pack(side=tk.LEFT, padx=3)
btn_save_biblioteca.config(command=save_biblioteca)
btn_update_biblioteca.config(command=update_biblioteca)
btn_delete_biblioteca.config(command=delete_biblioteca)
btn_search_biblioteca.config(command=search_biblioteca)
btn_clear_biblioteca.config(command=clear_biblioteca_form)


# Frame derecho para lista de biblioteca
right_frame_biblioteca = tk.Frame(main_frame_biblioteca)
right_frame_biblioteca.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_biblioteca, text="LISTA DE BIBLIOTECA", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar biblioteca
biblioteca_tree = ttk.Treeview(right_frame_biblioteca, columns=('ID', 'Codigo', 'Titulo', 'Actores', 'Editorial', 'Año', 'ISBN', 'Categoria', 'Formato', 'Cantidad', 'Ubicacion', 'Edicion'), show='headings', height=20)
biblioteca_tree.heading('ID', text='ID')
biblioteca_tree.heading('Codigo', text='Código')
biblioteca_tree.heading('Titulo', text='Título')
biblioteca_tree.heading('Actores', text='Actores')
biblioteca_tree.heading('Editorial', text='Editorial')
biblioteca_tree.heading('Año', text='Año')
biblioteca_tree.heading('ISBN', text='ISBN')
biblioteca_tree.heading('Categoria', text='Categoría')
biblioteca_tree.heading('Formato', text='Formato')
biblioteca_tree.heading('Cantidad', text='Cantidad')
biblioteca_tree.heading('Ubicacion', text='Ubicación')
biblioteca_tree.heading('Edicion', text='Edición')

biblioteca_tree.column('ID', width=50)
biblioteca_tree.column('Codigo', width=80)
biblioteca_tree.column('Titulo', width=100)
biblioteca_tree.column('Actores', width=80)
biblioteca_tree.column('Editorial', width=80)
biblioteca_tree.column('Año', width=60)
biblioteca_tree.column('ISBN', width=80)
biblioteca_tree.column('Categoria', width=80)
biblioteca_tree.column('Formato', width=80)
biblioteca_tree.column('Cantidad', width=70)
biblioteca_tree.column('Ubicacion', width=80)
biblioteca_tree.column('Edicion', width=60)

biblioteca_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para biblioteca
scrollbar_biblioteca = ttk.Scrollbar(right_frame_biblioteca, orient="vertical", command=biblioteca_tree.yview)
biblioteca_tree.configure(yscrollcommand=scrollbar_biblioteca.set)
scrollbar_biblioteca.pack(side="right", fill="y")

# =================== PESTAÑA 6 (CURSOS) ===================
main_frame_cursos = tk.Frame(tab6)
main_frame_cursos.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_cursos = tk.Frame(main_frame_cursos)
left_frame_cursos.pack(side="left", fill="y", padx=(0, 10))

titulo6 = tk.Label(left_frame_cursos, text="GESTIÓN DE CURSOS", font=("Arial", 16, "bold"), fg="blue")
titulo6.pack(pady=20)

form_frame_cursos = tk.Frame(left_frame_cursos)
form_frame_cursos.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_cursos, text="CursosID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
CursosID = tk.Entry(form_frame_cursos, width=25, font=("Arial", 12), relief="solid", bd=1)
CursosID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_cursos, text="PeriodoAcademico:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
PeriodoAcademico = tk.Entry(form_frame_cursos, width=25, font=("Arial", 12), relief="solid", bd=1)
PeriodoAcademico.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_cursos, text="Horarios:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
Horarios = tk.Entry(form_frame_cursos, width=25, font=("Arial", 12), relief="solid", bd=1)
Horarios.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_cursos, text="CupoMaximo:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
CupoMaximo = tk.Entry(form_frame_cursos, width=25, font=("Arial", 12), relief="solid", bd=1)
CupoMaximo.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_cursos, text="MetodologiaEvaluacion:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
MetodologiaEvaluacion = tk.Entry(form_frame_cursos, width=25, font=("Arial", 12), relief="solid", bd=1)
MetodologiaEvaluacion.grid(row=5, column=1, sticky="w", pady=8)

# Frame para botones de cursos
button_frame_cursos = tk.Frame(left_frame_cursos)
button_frame_cursos.pack(pady=20)

btn_save_curso = tk.Button(button_frame_cursos, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_curso.pack(side=tk.LEFT, padx=3)

btn_update_curso = tk.Button(button_frame_cursos, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_curso.pack(side=tk.LEFT, padx=3)

btn_delete_curso = tk.Button(button_frame_cursos, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_curso.pack(side=tk.LEFT, padx=3)

btn_search_curso = tk.Button(button_frame_cursos, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_curso.pack(side=tk.LEFT, padx=3)

btn_clear_curso = tk.Button(button_frame_cursos, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_curso.pack(side=tk.LEFT, padx=3)
btn_save_curso.config(command=save_curso)
btn_update_curso.config(command=update_curso)
btn_delete_curso.config(command=delete_curso)
btn_search_curso.config(command=search_curso)
btn_clear_curso.config(command=clear_curso_form)


# Frame derecho para lista de cursos
right_frame_cursos = tk.Frame(main_frame_cursos)
right_frame_cursos.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_cursos, text="LISTA DE CURSOS", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar cursos
cursos_tree = ttk.Treeview(right_frame_cursos, columns=('ID', 'PeriodoAcademico', 'Horarios', 'CupoMaximo', 'Metodologia'), show='headings', height=20)
cursos_tree.heading('ID', text='ID')
cursos_tree.heading('PeriodoAcademico', text='Periodo Académico')
cursos_tree.heading('Horarios', text='Horarios')
cursos_tree.heading('CupoMaximo', text='Cupo Máximo')
cursos_tree.heading('Metodologia', text='Metodología')

cursos_tree.column('ID', width=50)
cursos_tree.column('PeriodoAcademico', width=120)
cursos_tree.column('Horarios', width=100)
cursos_tree.column('CupoMaximo', width=100)
cursos_tree.column('Metodologia', width=120)

cursos_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para cursos
scrollbar_cursos = ttk.Scrollbar(right_frame_cursos, orient="vertical", command=cursos_tree.yview)
cursos_tree.configure(yscrollcommand=scrollbar_cursos.set)
scrollbar_cursos.pack(side="right", fill="y")

# =================== PESTAÑA 7 (ESTUDIANTES) ===================
main_frame_estudiantes = tk.Frame(tab7)
main_frame_estudiantes.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_estudiantes = tk.Frame(main_frame_estudiantes)
left_frame_estudiantes.pack(side="left", fill="y", padx=(0, 10))

titulo7 = tk.Label(left_frame_estudiantes, text="GESTIÓN DE ESTUDIANTES", font=("Arial", 16, "bold"), fg="blue")
titulo7.pack(pady=20)

form_frame_estudiantes = tk.Frame(left_frame_estudiantes)
form_frame_estudiantes.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_estudiantes, text="EstudiantesID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
EstudiantesID = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
EstudiantesID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="Matricula:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
Matricula = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
Matricula.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="Nombre:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
Nombre_Est = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
Nombre_Est.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="Apellido:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
Apellido_Est = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
Apellido_Est.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="DNI:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
DNI_Est = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
DNI_Est.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="Telefono:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
Telefono_Est = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
Telefono_Est.grid(row=6, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="CorreoInstitucional:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=8)
CorreoInstitucional_Est = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
CorreoInstitucional_Est.grid(row=7, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="Fotografia:", font=("Arial", 12)).grid(row=8, column=0, sticky="w", padx=(0, 10), pady=8)
Fotografia = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
Fotografia.grid(row=8, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="NombreAcudiente:", font=("Arial", 12)).grid(row=9, column=0, sticky="w", padx=(0, 10), pady=8)
NombreAcudiente = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
NombreAcudiente.grid(row=9, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="ContactoEmergencia:", font=("Arial", 12)).grid(row=10, column=0, sticky="w", padx=(0, 10), pady=8)
ContactoEmergencia = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
ContactoEmergencia.grid(row=10, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="FechaIngreso:", font=("Arial", 12)).grid(row=11, column=0, sticky="w", padx=(0, 10), pady=8)
FechaIngreso = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaIngreso.grid(row=11, column=1, sticky="w", pady=8)

tk.Label(form_frame_estudiantes, text="Periodo:", font=("Arial", 12)).grid(row=12, column=0, sticky="w", padx=(0, 10), pady=8)
Periodo_Est = tk.Entry(form_frame_estudiantes, width=25, font=("Arial", 12), relief="solid", bd=1)
Periodo_Est.grid(row=12, column=1, sticky="w", pady=8)

# Frame para botones de estudiantes
button_frame_estudiantes = tk.Frame(left_frame_estudiantes)
button_frame_estudiantes.pack(pady=20)

btn_save_estudiante = tk.Button(button_frame_estudiantes, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_estudiante.pack(side=tk.LEFT, padx=3)

btn_update_estudiante = tk.Button(button_frame_estudiantes, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_estudiante.pack(side=tk.LEFT, padx=3)

btn_delete_estudiante = tk.Button(button_frame_estudiantes, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_estudiante.pack(side=tk.LEFT, padx=3)

btn_search_estudiante = tk.Button(button_frame_estudiantes, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_estudiante.pack(side=tk.LEFT, padx=3)

btn_clear_estudiante = tk.Button(button_frame_estudiantes, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_estudiante.pack(side=tk.LEFT, padx=3)
btn_save_estudiante.config(command=save_estudiante)
btn_update_estudiante.config(command=update_estudiante)
btn_delete_estudiante.config(command=delete_estudiante)
btn_search_estudiante.config(command=search_estudiante)
btn_clear_estudiante.config(command=clear_estudiante_form)


# Frame derecho para lista de estudiantes
right_frame_estudiantes = tk.Frame(main_frame_estudiantes)
right_frame_estudiantes.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_estudiantes, text="LISTA DE ESTUDIANTES", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar estudiantes
estudiantes_tree = ttk.Treeview(right_frame_estudiantes, columns=('ID', 'Matricula', 'Nombre', 'Apellido', 'DNI', 'Telefono', 'Correo', 'Fotografia', 'Acudiente', 'Emergencia', 'FechaIngreso', 'Periodo'), show='headings', height=20)
estudiantes_tree.heading('ID', text='ID')
estudiantes_tree.heading('Matricula', text='Matrícula')
estudiantes_tree.heading('Nombre', text='Nombre')
estudiantes_tree.heading('Apellido', text='Apellido')
estudiantes_tree.heading('DNI', text='DNI')
estudiantes_tree.heading('Telefono', text='Teléfono')
estudiantes_tree.heading('Correo', text='Correo')
estudiantes_tree.heading('Fotografia', text='Fotografía')
estudiantes_tree.heading('Acudiente', text='Acudiente')
estudiantes_tree.heading('Emergencia', text='Emergencia')
estudiantes_tree.heading('FechaIngreso', text='Fecha Ingreso')
estudiantes_tree.heading('Periodo', text='Periodo')

estudiantes_tree.column('ID', width=50)
estudiantes_tree.column('Matricula', width=80)
estudiantes_tree.column('Nombre', width=80)
estudiantes_tree.column('Apellido', width=80)
estudiantes_tree.column('DNI', width=80)
estudiantes_tree.column('Telefono', width=100)
estudiantes_tree.column('Correo', width=120)
estudiantes_tree.column('Fotografia', width=80)
estudiantes_tree.column('Acudiente', width=100)
estudiantes_tree.column('Emergencia', width=100)
estudiantes_tree.column('FechaIngreso', width=100)
estudiantes_tree.column('Periodo', width=80)

estudiantes_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para estudiantes
scrollbar_estudiantes = ttk.Scrollbar(right_frame_estudiantes, orient="vertical", command=estudiantes_tree.yview)
estudiantes_tree.configure(yscrollcommand=scrollbar_estudiantes.set)
scrollbar_estudiantes.pack(side="right", fill="y")

# =================== PESTAÑA 8 (PLAN DE ESTUDIO) ===================
main_frame_planestudio = tk.Frame(tab8)
main_frame_planestudio.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_planestudio = tk.Frame(main_frame_planestudio)
left_frame_planestudio.pack(side="left", fill="y", padx=(0, 10))

titulo8 = tk.Label(left_frame_planestudio, text="GESTIÓN DE PLAN DE ESTUDIO", font=("Arial", 16, "bold"), fg="blue")
titulo8.pack(pady=20)

form_frame_planestudio = tk.Frame(left_frame_planestudio)
form_frame_planestudio.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_planestudio, text="PlanEstudioID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
PlanEstudioID = tk.Entry(form_frame_planestudio, width=25, font=("Arial", 12), relief="solid", bd=1)
PlanEstudioID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_planestudio, text="CodigoPlanDeEstudio:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
CodigoPlanDeEstudio = tk.Entry(form_frame_planestudio, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoPlanDeEstudio.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_planestudio, text="CarreraPerteneciente:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
CarreraPerteneciente = tk.Entry(form_frame_planestudio, width=25, font=("Arial", 12), relief="solid", bd=1)
CarreraPerteneciente.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_planestudio, text="FechaAprobacion:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
FechaAprobacion = tk.Entry(form_frame_planestudio, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaAprobacion.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_planestudio, text="NivelAsignatura:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
NivelAsignatura = tk.Entry(form_frame_planestudio, width=25, font=("Arial", 12), relief="solid", bd=1)
NivelAsignatura.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_planestudio, text="RequisitosGraduacion:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
RequisitosGraduacion = tk.Entry(form_frame_planestudio, width=25, font=("Arial", 12), relief="solid", bd=1)
RequisitosGraduacion.grid(row=6, column=1, sticky="w", pady=8)

tk.Label(form_frame_planestudio, text="CreditosTotales:", font=("Arial", 12)).grid(row=7, column=0, sticky="w", padx=(0, 10), pady=8)
CreditosTotales = tk.Entry(form_frame_planestudio, width=25, font=("Arial", 12), relief="solid", bd=1)
CreditosTotales.grid(row=7, column=1, sticky="w", pady=8)

# Frame para botones de plan de estudio
button_frame_planestudio = tk.Frame(left_frame_planestudio)
button_frame_planestudio.pack(pady=20)

btn_save_planestudio = tk.Button(button_frame_planestudio, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_planestudio.pack(side=tk.LEFT, padx=3)

btn_update_planestudio = tk.Button(button_frame_planestudio, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_planestudio.pack(side=tk.LEFT, padx=3)

btn_delete_planestudio = tk.Button(button_frame_planestudio, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_planestudio.pack(side=tk.LEFT, padx=3)

btn_search_planestudio = tk.Button(button_frame_planestudio, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_planestudio.pack(side=tk.LEFT, padx=3)

btn_clear_planestudio = tk.Button(button_frame_planestudio, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_planestudio.pack(side=tk.LEFT, padx=3)
btn_save_planestudio.config(command=save_planestudio)
btn_update_planestudio.config(command=update_planestudio)
btn_delete_planestudio.config(command=delete_planestudio)
btn_search_planestudio.config(command=search_planestudio)
btn_clear_planestudio.config(command=clear_planestudio_form)


# Frame derecho para lista de plan de estudio
right_frame_planestudio = tk.Frame(main_frame_planestudio)
right_frame_planestudio.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_planestudio, text="LISTA DE PLANES DE ESTUDIO", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar plan de estudio
planestudio_tree = ttk.Treeview(right_frame_planestudio, columns=('ID', 'Codigo', 'Carrera', 'FechaAprobacion', 'Nivel', 'Requisitos', 'Creditos'), show='headings', height=20)
planestudio_tree.heading('ID', text='ID')
planestudio_tree.heading('Codigo', text='Código')
planestudio_tree.heading('Carrera', text='Carrera')
planestudio_tree.heading('FechaAprobacion', text='Fecha Aprobación')
planestudio_tree.heading('Nivel', text='Nivel')
planestudio_tree.heading('Requisitos', text='Requisitos')
planestudio_tree.heading('Creditos', text='Créditos')

planestudio_tree.column('ID', width=50)
planestudio_tree.column('Codigo', width=100)
planestudio_tree.column('Carrera', width=120)
planestudio_tree.column('FechaAprobacion', width=100)
planestudio_tree.column('Nivel', width=80)
planestudio_tree.column('Requisitos', width=100)
planestudio_tree.column('Creditos', width=80)

planestudio_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para plan de estudio
scrollbar_planestudio = ttk.Scrollbar(right_frame_planestudio, orient="vertical", command=planestudio_tree.yview)
planestudio_tree.configure(yscrollcommand=scrollbar_planestudio.set)
scrollbar_planestudio.pack(side="right", fill="y")

# =================== PESTAÑA 9 (PRESTAMOS) ===================
main_frame_prestamos = tk.Frame(tab9)
main_frame_prestamos.pack(fill="both", expand=True, padx=10, pady=10)

left_frame_prestamos = tk.Frame(main_frame_prestamos)
left_frame_prestamos.pack(side="left", fill="y", padx=(0, 10))

titulo9 = tk.Label(left_frame_prestamos, text="GESTIÓN DE PRÉSTAMOS", font=("Arial", 16, "bold"), fg="blue")
titulo9.pack(pady=20)

form_frame_prestamos = tk.Frame(left_frame_prestamos)
form_frame_prestamos.pack(pady=20, anchor="w", padx=20)

tk.Label(form_frame_prestamos, text="PrestamosID:", font=("Arial", 12)).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=8)
PrestamosID = tk.Entry(form_frame_prestamos, width=25, font=("Arial", 12), relief="solid", bd=1)
PrestamosID.grid(row=1, column=1, sticky="w", pady=8)

tk.Label(form_frame_prestamos, text="CodigoPrestamo:", font=("Arial", 12)).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=8)
CodigoPrestamo = tk.Entry(form_frame_prestamos, width=25, font=("Arial", 12), relief="solid", bd=1)
CodigoPrestamo.grid(row=2, column=1, sticky="w", pady=8)

tk.Label(form_frame_prestamos, text="FechaPrestamo:", font=("Arial", 12)).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=8)
FechaPrestamo = tk.Entry(form_frame_prestamos, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaPrestamo.grid(row=3, column=1, sticky="w", pady=8)

tk.Label(form_frame_prestamos, text="FechaDevolucion:", font=("Arial", 12)).grid(row=4, column=0, sticky="w", padx=(0, 10), pady=8)
FechaDevolucion = tk.Entry(form_frame_prestamos, width=25, font=("Arial", 12), relief="solid", bd=1)
FechaDevolucion.grid(row=4, column=1, sticky="w", pady=8)

tk.Label(form_frame_prestamos, text="MultasAplicadas:", font=("Arial", 12)).grid(row=5, column=0, sticky="w", padx=(0, 10), pady=8)
MultasAplicadas = tk.Entry(form_frame_prestamos, width=25, font=("Arial", 12), relief="solid", bd=1)
MultasAplicadas.grid(row=5, column=1, sticky="w", pady=8)

tk.Label(form_frame_prestamos, text="Estado:", font=("Arial", 12)).grid(row=6, column=0, sticky="w", padx=(0, 10), pady=8)
Estado = tk.Entry(form_frame_prestamos, width=25, font=("Arial", 12), relief="solid", bd=1)
Estado.grid(row=6, column=1, sticky="w", pady=8)

# Frame para botones de prestamos
button_frame_prestamos = tk.Frame(left_frame_prestamos)
button_frame_prestamos.pack(pady=20)

btn_save_prestamo = tk.Button(button_frame_prestamos, text="Guardar", font=("Arial", 10), bg="#4CAF50", fg="white", width=10)
btn_save_prestamo.pack(side=tk.LEFT, padx=3)

btn_update_prestamo = tk.Button(button_frame_prestamos, text="Actualizar", font=("Arial", 10), bg="#2196F3", fg="white", width=10)
btn_update_prestamo.pack(side=tk.LEFT, padx=3)

btn_delete_prestamo = tk.Button(button_frame_prestamos, text="Eliminar", font=("Arial", 10), bg="#f44336", fg="white", width=10)
btn_delete_prestamo.pack(side=tk.LEFT, padx=3)

btn_search_prestamo = tk.Button(button_frame_prestamos, text="Buscar", font=("Arial", 10), bg="#FF9800", fg="white", width=10)
btn_search_prestamo.pack(side=tk.LEFT, padx=3)

btn_clear_prestamo = tk.Button(button_frame_prestamos, text="Limpiar", font=("Arial", 10), bg="#9E9E9E", fg="white", width=10)
btn_clear_prestamo.pack(side=tk.LEFT, padx=3)
btn_save_prestamo.config(command=save_prestamo)
btn_update_prestamo.config(command=update_prestamo)
btn_delete_prestamo.config(command=delete_prestamo)
btn_search_prestamo.config(command=search_prestamo)
btn_clear_prestamo.config(command=clear_prestamo_form)


# Frame derecho para lista de prestamos
right_frame_prestamos = tk.Frame(main_frame_prestamos)
right_frame_prestamos.pack(side="right", fill="both", expand=True)

tk.Label(right_frame_prestamos, text="LISTA DE PRÉSTAMOS", font=("Arial", 14, "bold")).pack(pady=10)

# Treeview para mostrar prestamos
prestamos_tree = ttk.Treeview(right_frame_prestamos, columns=('ID', 'Codigo', 'FechaPrestamo', 'FechaDevolucion', 'Multas', 'Estado'), show='headings', height=20)
prestamos_tree.heading('ID', text='ID')
prestamos_tree.heading('Codigo', text='Código')
prestamos_tree.heading('FechaPrestamo', text='Fecha Préstamo')
prestamos_tree.heading('FechaDevolucion', text='Fecha Devolución')
prestamos_tree.heading('Multas', text='Multas')
prestamos_tree.heading('Estado', text='Estado')

prestamos_tree.column('ID', width=50)
prestamos_tree.column('Codigo', width=100)
prestamos_tree.column('FechaPrestamo', width=120)
prestamos_tree.column('FechaDevolucion', width=120)
prestamos_tree.column('Multas', width=100)
prestamos_tree.column('Estado', width=100)

prestamos_tree.pack(fill="both", expand=True, padx=10, pady=10)

# Scrollbar para prestamos
scrollbar_prestamos = ttk.Scrollbar(right_frame_prestamos, orient="vertical", command=prestamos_tree.yview)
prestamos_tree.configure(yscrollcommand=scrollbar_prestamos.set)
scrollbar_prestamos.pack(side="right", fill="y")



# Cargar datos al iniciar
root.after(1000, load_initial_data)  # Cargar después de 1 segundo


# =================== FUNCIÓN DE CIERRE ===================
def on_closing():
    db.disconnect()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)

root.mainloop()