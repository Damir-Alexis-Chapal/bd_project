from models.db_connection import DatabaseConnection


class GrupoModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # CRUD 
    @staticmethod
    def get_all():
        """Retorna todos los grupos."""
        db  = GrupoModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, letra FROM grupos ORDER BY letra")
        rows = cur.fetchall()
        cur.close()
        return rows  # [(id, letra), ...]

    @staticmethod
    def get_by_id(grupo_id: int):
        db  = GrupoModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, letra FROM grupos WHERE id = :1", [grupo_id])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def insert(letra: str):
        db  = GrupoModel._db()
        cur = db.get_cursor()
        cur.execute("INSERT INTO grupos (letra) VALUES (:1)", [letra])
        db.commit()
        cur.close()

    @staticmethod
    def update(grupo_id: int, letra: str):
        db  = GrupoModel._db()
        cur = db.get_cursor()
        cur.execute("UPDATE grupos SET letra = :1 WHERE id = :2", [letra, grupo_id])
        db.commit()
        cur.close()

    @staticmethod
    def delete(grupo_id: int):
        db  = GrupoModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM grupos WHERE id = :1", [grupo_id])
        db.commit()
        cur.close()

    @staticmethod
    def get_nombres_para_combo():
        """Retorna (id, letra) para poblar un combobox."""
        db  = GrupoModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, letra FROM grupos ORDER BY letra")
        rows = cur.fetchall()
        cur.close()
        return rows