from models.db_connection import DatabaseConnection


class BitacoraModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    # Registro de eventos
    @staticmethod
    def registrar_ingreso(user_id: int):
        """
        Inserta una fila de ingreso en la bitácora.
        Retorna el id de la fila creada (para actualizarla al salir).
        """
        db  = BitacoraModel._db()
        cur = db.get_cursor()
        # RETURNING id INTO permite obtener el ID generado por la secuencia
        out_id = cur.var(int)
        cur.execute(
            """INSERT INTO bitacora (id_usuario, fecha_ingreso)
               VALUES (:1, SYSDATE)
               RETURNING id INTO :2""",
            [user_id, out_id]
        )
        db.commit()
        bitacora_id = out_id.getvalue()
        cur.close()
        # oracledb puede devolver lista; tomamos el primer elemento
        if isinstance(bitacora_id, list):
            bitacora_id = bitacora_id[0]
        return bitacora_id

    @staticmethod
    def registrar_salida(bitacora_id: int):
        """Actualiza la fecha de salida de la sesión activa."""
        db  = BitacoraModel._db()
        cur = db.get_cursor()
        cur.execute(
            "UPDATE bitacora SET fecha_salida = SYSDATE WHERE id = :1",
            [bitacora_id]
        )
        db.commit()
        cur.close()

    # Consultas
    @staticmethod
    def get_all():
        """
        Reporte B1: todos los registros de bitácora con datos del usuario.
        Retorna lista de (username, rol, fecha_ingreso, fecha_salida).
        """
        db  = BitacoraModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT u.username,
                   u.rol,
                   b.fecha_ingreso,
                   b.fecha_salida
            FROM   bitacora b
            JOIN   usuarios u ON u.id = b.id_usuario
            ORDER  BY b.fecha_ingreso DESC
        """)
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def get_por_fecha(fecha_inicio, fecha_fin):
        """
        Reporte B1 filtrado: usuarios que ingresaron y salieron
        en un rango de fechas específico.
        fecha_inicio / fecha_fin son objetos datetime o strings 'YYYY-MM-DD'.
        """
        db  = BitacoraModel._db()
        cur = db.get_cursor()
        cur.execute("""
            SELECT u.username,
                   u.rol,
                   b.fecha_ingreso,
                   b.fecha_salida
            FROM   bitacora b
            JOIN   usuarios u ON u.id = b.id_usuario
            WHERE  TRUNC(b.fecha_ingreso) BETWEEN TO_DATE(:1,'YYYY-MM-DD')
                                               AND TO_DATE(:2,'YYYY-MM-DD')
            ORDER  BY b.fecha_ingreso DESC
        """, [str(fecha_inicio), str(fecha_fin)])
        rows = cur.fetchall()
        cur.close()
        return rows