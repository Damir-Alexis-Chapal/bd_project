from models.db_connection import DatabaseConnection


class EquipoModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # CRUD
    @staticmethod
    def get_all():
        """Retorna todos los equipos con nombre de confederación."""
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT e.id, e.nombre, e.id_confederacion, c.nombre AS confederacion,
                   e.id_dt, e.valor_mercado
            FROM   equipos e
            JOIN   confederaciones c ON c.id = e.id_confederacion
            ORDER  BY e.nombre
        """)
        rows = cur.fetchall()
        cur.close()
        return rows  # [(id, nombre, id_conf, conf, id_dt, valor_mercado), ...]

    @staticmethod
    def get_by_id(equipo_id: int):
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT e.id, e.nombre, e.id_confederacion, c.nombre AS confederacion,
                   e.id_dt, e.valor_mercado
            FROM   equipos e
            JOIN   confederaciones c ON c.id = e.id_confederacion
            WHERE  e.id = :1
        """, [equipo_id])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def insert(nombre: str, id_confederacion: int, id_dt: int, valor_mercado: float):
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute(
            """INSERT INTO equipos (nombre, id_confederacion, id_dt, valor_mercado)
               VALUES (:1, :2, :3, :4)""",
            [nombre, id_confederacion, id_dt, valor_mercado]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update(equipo_id: int, nombre: str, id_confederacion: int,
               id_dt: int, valor_mercado: float):
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute(
            """UPDATE equipos
               SET nombre = :1, id_confederacion = :2, id_dt = :3, valor_mercado = :4
               WHERE id = :5""",
            [nombre, id_confederacion, id_dt, valor_mercado, equipo_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(equipo_id: int):
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM equipos WHERE id = :1", [equipo_id])
        db.commit()
        cur.close()

    @staticmethod
    def get_nombres_para_combo():
        """Retorna (id, nombre) para poblar un combobox."""
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, nombre FROM equipos ORDER BY nombre")
        rows = cur.fetchall()
        cur.close()
        return rows

    # Consultas especializadas

    @staticmethod
    def get_equipo_mas_costoso_por_pais(pais: str):
        """
        Consulta: equipo más costoso de los que juegan en
        la fase de grupos en el país indicado (México, USA, Canadá).
        Retorna una sola fila: (equipo, confederacion, valor_mercado, pais).
        """
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT eq.nombre        AS equipo,
                   conf.nombre      AS confederacion,
                   eq.valor_mercado,
                   ci.pais
            FROM   equipos eq
            JOIN   confederaciones conf ON conf.id = eq.id_confederacion
            JOIN   (
                       -- equipos que participan en partidos jugados en el país
                       SELECT DISTINCT e2.id
                       FROM   equipos e2
                       JOIN   partidos p  ON (p.id_equipo1 = e2.id OR p.id_equipo2 = e2.id)
                       JOIN   estadios es ON es.id = p.id_estadio
                       JOIN   ciudades ci2 ON ci2.id = es.id_ciudad
                       WHERE  ci2.pais = :1
                   ) sub ON sub.id = eq.id
            JOIN   partidos p2  ON (p2.id_equipo1 = eq.id OR p2.id_equipo2 = eq.id)
            JOIN   estadios es2 ON es2.id = p2.id_estadio
            JOIN   ciudades ci  ON ci.id = es2.id_ciudad AND ci.pais = :2
            WHERE  ROWNUM = 1
            ORDER  BY eq.valor_mercado DESC
        """, [pais, pais])
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def get_valor_total_por_confederacion(id_confederacion: int):
        """
        Reporte: valor total de jugadores de todos los equipos
        de una confederación específica.
        Retorna lista de (equipo, suma_valor_jugadores).
        """
        db  = EquipoModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT eq.nombre      AS equipo,
                   SUM(j.valor)   AS valor_total_jugadores
            FROM   equipos eq
            JOIN   jugadores j ON j.id_equipo = eq.id
            WHERE  eq.id_confederacion = :1
            GROUP  BY eq.id, eq.nombre
            ORDER  BY valor_total_jugadores DESC
        """, [id_confederacion])
        rows = cur.fetchall()
        cur.close()
        return rows