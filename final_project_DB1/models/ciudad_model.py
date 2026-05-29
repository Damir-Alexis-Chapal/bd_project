from models.db_connection import DatabaseConnection


class CiudadModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # CRUD
    @staticmethod
    def get_all():
        """Retorna todas las ciudades."""
        db  = CiudadModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, nombre, pais FROM ciudades ORDER BY pais, nombre")
        rows = cur.fetchall()
        cur.close()
        return rows  # [(id, nombre, pais), ...]

    @staticmethod
    def get_by_id(ciudad_id: int):
        db  = CiudadModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, nombre, pais FROM ciudades WHERE id = :1", [ciudad_id])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def get_by_pais(pais: str):
        """Retorna ciudades filtradas por país anfitrión."""
        db  = CiudadModel._db()
        cur = db.get_cursor()
        cur.execute(
            "SELECT id, nombre, pais FROM ciudades WHERE pais = :1 ORDER BY nombre",
            [pais]
        )
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def insert(nombre: str, pais: str):
        db  = CiudadModel._db()
        cur = db.get_cursor()
        cur.execute(
            "INSERT INTO ciudades (nombre, pais) VALUES (:1, :2)",
            [nombre, pais]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update(ciudad_id: int, nombre: str, pais: str):
        db  = CiudadModel._db()
        cur = db.get_cursor()
        cur.execute(
            "UPDATE ciudades SET nombre = :1, pais = :2 WHERE id = :3",
            [nombre, pais, ciudad_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(ciudad_id: int):
        db  = CiudadModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM ciudades WHERE id = :1", [ciudad_id])
        db.commit()
        cur.close()