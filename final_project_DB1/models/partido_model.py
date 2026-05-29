from models.db_connection import DatabaseConnection


class PartidoModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # CRUD 
    @staticmethod
    def get_all():
        """Retorna todos los partidos con datos completos."""
        db  = PartidoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT p.id,
                   e1.nombre  AS equipo1,
                   e2.nombre  AS equipo2,
                   es.nombre  AS estadio,
                   ci.nombre  AS ciudad,
                   ci.pais,
                   g.letra    AS grupo,
                   p.fecha_hora
            FROM   partidos p
            JOIN   equipos  e1 ON e1.id = p.id_equipo1
            JOIN   equipos  e2 ON e2.id = p.id_equipo2
            JOIN   estadios es ON es.id = p.id_estadio
            JOIN   ciudades ci ON ci.id = es.id_ciudad
            JOIN   grupos   g  ON g.id  = p.id_grupo
            ORDER  BY p.fecha_hora
        """)
        rows = cur.fetchall()
        cur.close()
        return rows  # [(id, eq1, eq2, estadio, ciudad, pais, grupo, fecha_hora), ...]

    @staticmethod
    def get_by_id(partido_id: int):
        db  = PartidoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT p.id, p.id_equipo1, p.id_equipo2, p.id_estadio,
                   p.id_grupo, p.fecha_hora
            FROM   partidos p
            WHERE  p.id = :1
        """, [partido_id])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def insert(id_equipo1: int, id_equipo2: int,
               id_estadio: int, id_grupo: int, fecha_hora):
        db  = PartidoModel._db()
        cur = db.get_cursor()
        cur.execute(
            """INSERT INTO partidos (id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora)
               VALUES (:1, :2, :3, :4, :5)""",
            [id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update(partido_id: int, id_equipo1: int, id_equipo2: int,
               id_estadio: int, id_grupo: int, fecha_hora):
        db  = PartidoModel._db()
        cur = db.get_cursor()
        cur.execute(
            """UPDATE partidos
               SET id_equipo1 = :1, id_equipo2 = :2,
                   id_estadio = :3, id_grupo   = :4, fecha_hora = :5
               WHERE id = :6""",
            [id_equipo1, id_equipo2, id_estadio, id_grupo, fecha_hora, partido_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(partido_id: int):
        db  = PartidoModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM partidos WHERE id = :1", [partido_id])
        db.commit()
        cur.close()

    # Consultas especializadas 

    @staticmethod
    def get_partidos_por_estadio(estadio_id: int):
        """
        Consulta A2: partidos que se llevarán a cabo en el estadio indicado.
        Retorna lista de (equipo1, equipo2, estadio, ciudad, pais, grupo, fecha_hora).
        """
        db  = PartidoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT e1.nombre   AS equipo1,
                   e2.nombre   AS equipo2,
                   es.nombre   AS estadio,
                   ci.nombre   AS ciudad,
                   ci.pais,
                   g.letra     AS grupo,
                   p.fecha_hora
            FROM   partidos p
            JOIN   equipos  e1 ON e1.id = p.id_equipo1
            JOIN   equipos  e2 ON e2.id = p.id_equipo2
            JOIN   estadios es ON es.id = p.id_estadio
            JOIN   ciudades ci ON ci.id = es.id_ciudad
            JOIN   grupos   g  ON g.id  = p.id_grupo
            WHERE  p.id_estadio = :1
            ORDER  BY p.fecha_hora
        """, [estadio_id])
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def get_paises_por_anfitrion(pais_anfitrion: str):
        """
        Reporte B4: países (equipos) que jugarán en el país anfitrión indicado.
        Retorna lista de (equipo, confederacion, estadio, ciudad, fecha_hora).
        """
        db  = PartidoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT DISTINCT eq.nombre     AS equipo,
                            conf.nombre   AS confederacion,
                            es.nombre     AS estadio,
                            ci.nombre     AS ciudad,
                            ci.pais
            FROM   partidos p
            JOIN   equipos  eq   ON (eq.id = p.id_equipo1 OR eq.id = p.id_equipo2)
            JOIN   confederaciones conf ON conf.id = eq.id_confederacion
            JOIN   estadios es   ON es.id = p.id_estadio
            JOIN   ciudades ci   ON ci.id = es.id_ciudad
            WHERE  ci.pais = :1
            ORDER  BY eq.nombre
        """, [pais_anfitrion])
        rows = cur.fetchall()
        cur.close()
        return rows