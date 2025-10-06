# models/database.py
import mysql.connector
import json
import os
from tkinter import messagebox


class DatabaseConnection:
    def __init__(self):
        self.connection = None
        self.cursor = None
        self.config = self._load_config()

    def _load_config(self):
        """Carga la configuración desde config.json"""
        try:
            # Busca el archivo config.json en la misma carpeta que database.py
            current_dir = os.path.dirname(__file__)
            config_path = os.path.join(current_dir, 'config.json')

            with open(config_path, 'r') as f:
                config_data = json.load(f)
                return config_data['database']
        except FileNotFoundError:
            messagebox.showerror("Error",
                                 "Archivo config.json no encontrado. Crea el archivo con la configuración de la base de datos.")
            return None
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Error leyendo config.json. Verifica que el formato sea correcto.")
            return None
        except KeyError:
            messagebox.showerror("Error", "Configuración de base de datos no encontrada en config.json")
            return None
        except Exception as e:
            messagebox.showerror("Error", f"Error cargando configuración: {e}")
            return None

    def connect(self):
        if not self.config:
            return False

        try:
            self.connection = mysql.connector.connect(
                host=self.config['host'],
                database=self.config['database'],
                user=self.config['user'],
                password=self.config['password'],
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