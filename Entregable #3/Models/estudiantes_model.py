# models/estudiantes_model.py
from Models.database import DatabaseConnection

class EstudiantesModel:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def insert_estudiante(self, parameters):
        return self.db.call_procedure('sp_InsertEstudiante', parameters)

    def update_estudiante(self, parameters):
        return self.db.call_procedure('sp_UpdateEstudiante', parameters)

    def delete_estudiante(self, est_id):
        return self.db.call_procedure('sp_DeleteEstudiante', (est_id,))

    def get_all_estudiantes(self):
        return self.db.call_procedure('sp_GetAllEstudiantes')

    def get_estudiante_by_id(self, est_id):
        return self.db.call_procedure('sp_GetEstudiante', (est_id,))

    def search_estudiantes(self, search_term):
        return self.db.call_procedure('sp_SearchEstudiantes', (search_term,))
