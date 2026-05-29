# Las contraseñas se almacenan como hash SHA-256.
# Nunca se guarda la contraseña en texto plano.

import hashlib
from models.db_connection import DatabaseConnection
from config.constants import ROLE_ADMIN


class UserModel:

    @staticmethod
    def _db():
        return DatabaseConnection.get_instance()

    @staticmethod
    def _hash_password(password: str) -> str:
        """Genera SHA-256 del password."""
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Autenticación 
    @staticmethod
    def authenticate(username: str, password: str):
        """
        Verifica credenciales.
        Retorna (id, username, rol) si son correctas, None si no.
        """
        db   = UserModel._db()
        cur  = db.get_cursor()
        hashed = UserModel._hash_password(password)
        cur.execute(
            """SELECT id, username, rol
               FROM   usuarios
               WHERE  username = :1 AND password = :2""",
            [username, hashed]
        )
        row = cur.fetchone()
        cur.close()
        return row  # (id, username, rol) | None

    # CRUD 
    @staticmethod
    def get_all():
        """Solo el Administrador debe llamar este método."""
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute("SELECT id, username, rol FROM usuarios ORDER BY rol, username")
        rows = cur.fetchall()
        cur.close()
        return rows

    @staticmethod
    def get_by_id(user_id: int):
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute(
            "SELECT id, username, rol FROM usuarios WHERE id = :1",
            [user_id]
        )
        row = cur.fetchone()
        cur.close()
        return row

    @staticmethod
    def username_exists(username: str) -> bool:
        """Verifica si el username ya está tomado."""
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute(
            "SELECT COUNT(*) FROM usuarios WHERE username = :1",
            [username]
        )
        count = cur.fetchone()[0]
        cur.close()
        return count > 0

    @staticmethod
    def insert(username: str, password: str, rol: str):
        """
        Crea un nuevo usuario. Solo el Admin puede invocar esto.
        Lanza ValueError si el username ya existe.
        """
        if UserModel.username_exists(username):
            raise ValueError(f"El usuario '{username}' ya existe.")
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute(
            "INSERT INTO usuarios (username, password, rol) VALUES (:1, :2, :3)",
            [username, UserModel._hash_password(password), rol]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update_password(user_id: int, new_password: str):
        """Actualiza la contraseña de un usuario."""
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute(
            "UPDATE usuarios SET password = :1 WHERE id = :2",
            [UserModel._hash_password(new_password), user_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def update_rol(user_id: int, nuevo_rol: str):
        """Cambia el rol de un usuario. Solo el Admin puede hacerlo."""
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute(
            "UPDATE usuarios SET rol = :1 WHERE id = :2",
            [nuevo_rol, user_id]
        )
        db.commit()
        cur.close()

    @staticmethod
    def delete(user_id: int):
        """
        Elimina un usuario.
        No permite eliminar al Admin (id protegido por constraint en BD).
        """
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute("DELETE FROM usuarios WHERE id = :1", [user_id])
        db.commit()
        cur.close()

    @staticmethod
    def admin_exists() -> bool:
        """Verifica si ya existe al menos un usuario Admin en el sistema."""
        db  = UserModel._db()
        cur = db.get_cursor()
        cur.execute(
            "SELECT COUNT(*) FROM usuarios WHERE rol = :1",
            [ROLE_ADMIN]
        )
        count = cur.fetchone()[0]
        cur.close()
        return count > 0