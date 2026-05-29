from models.db_connection import DatabaseConnection


class JugadorModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # CRUD 
    @staticmethod
    def get_all():
        """Retorna todos los jugadores con nombre de equipo."""
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT j.id, j.nombre, j.edad, j.peso, j.estatura, j.valor,
                   j.id_equipo, e.nombre AS equipo
            FROM   jugadores j
            JOIN   equipos e ON e.id = j.id_equipo
            ORDER  BY e.nombre, j.nombre
        """)
        rows = cur.fetchall()
        cur.close()
        return rows  # [(id, nombre, edad, peso, estatura, valor, id_equipo, equipo), ...]

    @staticmethod
    def get_by_id(jugador_id: int):
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT j.id, j.nombre, j.edad, j.peso, j.estatura, j.valor,
                   j.id_equipo, e.nombre AS equipo
            FROM   jugadores j
            JOIN   equipos e ON e.id = j.id_equipo
            WHERE  j.id = :1
        """, [jugador_id])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def insert(nombre: str, edad: int, peso: float,
               estatura: float, valor: float, id_equipo: int):
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute(
            """INSERT INTO jugadores (nombre, edad, peso, estatura, valor, id_equipo)
               VALUES (:1, :2, :3, :4, :5, :6)""",
            [nombre, edad, peso, estatura, valor, id_equipo]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update(jugador_id: int, nombre: str, edad: int, peso: float,
               estatura: float, valor: float, id_equipo: int):
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute(
            """UPDATE jugadores
               SET nombre = :1, edad = :2, peso = :3,
                   estatura = :4, valor = :5, id_equipo = :6
               WHERE id = :7""",
            [nombre, edad, peso, estatura, valor, id_equipo, jugador_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(jugador_id: int):
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM jugadores WHERE id = :1", [jugador_id])
        db.commit()
        cur.close()

    # Consultas especializadas

    @staticmethod
    def get_jugador_mas_costoso_por_confederacion():
        """
        Consulta A1: jugador más costoso por cada confederación.
        Retorna lista de (confederacion, jugador, equipo, valor).
        """
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT conf.nombre   AS confederacion,
                   j.nombre      AS jugador,
                   eq.nombre     AS equipo,
                   j.valor
            FROM   jugadores j
            JOIN   equipos eq      ON eq.id = j.id_equipo
            JOIN   confederaciones conf ON conf.id = eq.id_confederacion
            WHERE  j.valor = (
                       SELECT MAX(j2.valor)
                       FROM   jugadores j2
                       JOIN   equipos eq2 ON eq2.id = j2.id_equipo
                       WHERE  eq2.id_confederacion = eq.id_confederacion
                   )
            ORDER  BY conf.nombre
        """)
        rows = cur.fetchall()
        cur.close()
        return rows  # [(confederacion, jugador, equipo, valor), ...]

    @staticmethod
    def get_cantidad_menores_por_equipo():
        """
        Consulta A4: cantidad de jugadores menores de 21 años por equipo.
        Retorna lista de (equipo, confederacion, cantidad).
        """
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT eq.nombre        AS equipo,
                   conf.nombre      AS confederacion,
                   COUNT(j.id)      AS cantidad_menores
            FROM   jugadores j
            JOIN   equipos eq      ON eq.id = j.id_equipo
            JOIN   confederaciones conf ON conf.id = eq.id_confederacion
            WHERE  j.edad < 21
            GROUP  BY eq.id, eq.nombre, conf.nombre
            ORDER  BY cantidad_menores DESC, eq.nombre
        """)
        rows = cur.fetchall()
        cur.close()
        return rows  # [(equipo, confederacion, cantidad), ...]

    @staticmethod
    def get_jugadores_por_peso_estatura(peso_min: float, peso_max: float,
                                         estatura_min: float, estatura_max: float):
        """
        Reporte B2: jugadores cuyo peso y estatura están dentro del rango indicado.
        Retorna lista de (jugador, edad, peso, estatura, valor, equipo).
        """
        db  = JugadorModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT j.nombre, j.edad, j.peso, j.estatura, j.valor, eq.nombre AS equipo
            FROM   jugadores j
            JOIN   equipos eq ON eq.id = j.id_equipo
            WHERE  j.peso     BETWEEN :1 AND :2
              AND  j.estatura BETWEEN :3 AND :4
            ORDER  BY j.nombre
        """, [peso_min, peso_max, estatura_min, estatura_max])
        rows = cur.fetchall()
        cur.close()
        return rows