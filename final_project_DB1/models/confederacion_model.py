from models.db_connection import DatabaseConnection


class ConfederacionModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # CRUD
    @staticmethod
    def get_all():
        """Retorna todas las confederaciones."""
        db  = ConfederacionModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, nombre FROM confederaciones ORDER BY nombre")
        rows = cur.fetchall()
        cur.close()
        return rows  # [(id, nombre), ...]

    @staticmethod
    def get_by_id(conf_id: int):
        db  = ConfederacionModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, nombre FROM confederaciones WHERE id = :1", [conf_id])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def insert(nombre: str):
        db  = ConfederacionModel._db()
        cur = db.get_cursor()
        cur.execute(
            "INSERT INTO confederaciones (nombre) VALUES (:1)",
            [nombre]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update(conf_id: int, nombre: str):
        db  = ConfederacionModel._db()
        cur = db.get_cursor()
        cur.execute(
            "UPDATE confederaciones SET nombre = :1 WHERE id = :2",
            [nombre, conf_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(conf_id: int):
        db  = ConfederacionModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM confederaciones WHERE id = :1", [conf_id])
        db.commit()
        cur.close()