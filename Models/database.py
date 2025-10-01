# models/database.py
import mysql.connector
from tkinter import messagebox

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
