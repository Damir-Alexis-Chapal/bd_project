from models.db_connection import DatabaseConnection


class EstadioModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # CRUD
    @staticmethod
    def get_all():
        """Retorna todos los estadios con nombre de ciudad."""
        db  = EstadioModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT e.id, e.nombre, e.capacidad, e.id_ciudad, c.nombre AS ciudad, c.pais
            FROM   estadios e
            JOIN   ciudades c ON c.id = e.id_ciudad
            ORDER  BY c.pais, e.nombre
        """)
        rows = cur.fetchall()
        cur.close()
        return rows  # [(id, nombre, capacidad, id_ciudad, ciudad, pais), ...]

    @staticmethod
    def get_by_id(estadio_id: int):
        db  = EstadioModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT e.id, e.nombre, e.capacidad, e.id_ciudad, c.nombre AS ciudad, c.pais
            FROM   estadios e
            JOIN   ciudades c ON c.id = e.id_ciudad
            WHERE  e.id = :1
        """, [estadio_id])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def insert(nombre: str, capacidad: int, id_ciudad: int):
        db  = EstadioModel._db()
        cur = db.get_cursor()
        cur.execute(
            "INSERT INTO estadios (nombre, capacidad, id_ciudad) VALUES (:1, :2, :3)",
            [nombre, capacidad, id_ciudad]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update(estadio_id: int, nombre: str, capacidad: int, id_ciudad: int):
        db  = EstadioModel._db()
        cur = db.get_cursor()
        cur.execute(
            "UPDATE estadios SET nombre = :1, capacidad = :2, id_ciudad = :3 WHERE id = :4",
            [nombre, capacidad, id_ciudad, estadio_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(estadio_id: int):
        db  = EstadioModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM estadios WHERE id = :1", [estadio_id])
        db.commit()
        cur.close()

    # Consulta especializada
    @staticmethod
    def get_nombres_para_combo():
        """Retorna (id, nombre) para poblar un combobox."""
        db  = EstadioModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, nombre FROM estadios ORDER BY nombre")
        rows = cur.fetchall()
        cur.close()
        return rows