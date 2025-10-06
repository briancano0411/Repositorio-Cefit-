# models/asignaturas_model.py
from Models.database import DatabaseConnection

class AsignaturasModel:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def insert_asignatura(self, parameters):
        return self.db.call_procedure('sp_InsertAsignatura', parameters)

    def update_asignatura(self, parameters):
        return self.db.call_procedure('sp_UpdateAsignatura', parameters)

    def delete_asignatura(self, asig_id):
        return self.db.call_procedure('sp_DeleteAsignatura', (asig_id,))

    def get_all_asignaturas(self):
        return self.db.call_procedure('sp_GetAllAsignaturas')

    def get_asignatura_by_id(self, asig_id):
        query = "SELECT * FROM asignaturas WHERE id_asignaturas = %s"
        return self.db.execute_query(query, (asig_id,))