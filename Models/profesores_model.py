# models/profesores_model.py
from Models.database import DatabaseConnection

class ProfesoresModel:
    def __init__(self, db: DatabaseConnection):
        self.db = db

    def insert_profesor(self, parameters):
        return self.db.call_procedure('sp_InsertProfesor', parameters)

    def update_profesor(self, parameters):
        return self.db.call_procedure('sp_UpdateProfesor', parameters)

    def delete_profesor(self, prof_id):
        return self.db.call_procedure('sp_DeleteProfesor', (prof_id,))

    def get_all_profesores(self):
        return self.db.call_procedure('sp_GetAllProfesores')

    def get_profesor_by_id(self, prof_id):
        return self.db.call_procedure('sp_GetProfesor', (prof_id,))

    def search_profesores(self, search_term):
        return self.db.call_procedure('sp_SearchProfesores', (search_term,))
