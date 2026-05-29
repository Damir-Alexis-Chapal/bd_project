# Maneja autenticación, registro de usuarios
# y el registro automático en bitácora.

from models.user_model     import UserModel
from models.bitacora_model import BitacoraModel
from utils.session         import Session
from config.constants      import ALL_ROLES, ROLE_ADMIN
from config.settings       import MAX_LOGIN_ATTEMPTS


class AuthController:

    # Contador de intentos fallidos por username
    _intentos: dict[str, int] = {}

    # Login
    @classmethod
    def login(cls, username: str, password: str) -> tuple[bool, str]:
        """
        Intenta autenticar al usuario.
        Retorna (éxito: bool, mensaje: str).
        Bloquea el username tras MAX_LOGIN_ATTEMPTS intentos fallidos.
        """
        username = username.strip()

        if not username or not password:
            return False, "Usuario y contraseña son obligatorios."

        # Verificar bloqueo
        if cls._intentos.get(username, 0) >= MAX_LOGIN_ATTEMPTS:
            return False, (
                f"Usuario bloqueado tras {MAX_LOGIN_ATTEMPTS} intentos fallidos. "
                "Contacte al administrador."
            )

        row = UserModel.authenticate(username, password)

        if row is None:
            cls._intentos[username] = cls._intentos.get(username, 0) + 1
            restantes = MAX_LOGIN_ATTEMPTS - cls._intentos[username]
            if restantes > 0:
                return False, f"Credenciales incorrectas. Intentos restantes: {restantes}."
            else:
                return False, (
                    f"Usuario bloqueado tras {MAX_LOGIN_ATTEMPTS} intentos fallidos. "
                    "Contacte al administrador."
                )

        # Login exitoso
        user_id, uname, rol = row
        cls._intentos.pop(username, None)   # resetea contador
        Session.login(user_id, uname, rol)

        # Registrar ingreso en bitácora y guardar id en sesión
        bitacora_id = BitacoraModel.registrar_ingreso(user_id)
        Session.set_bitacora_id(bitacora_id)

        return True, f"Bienvenido, {uname}."

    # Logout 
    @classmethod
    def logout(cls) -> None:
        """Registra la salida en bitácora y limpia la sesión."""
        bitacora_id = Session.get_bitacora_id()
        if bitacora_id:
            BitacoraModel.registrar_salida(bitacora_id)
        Session.logout()

    # Gestión de usuarios (solo Admin)
    @classmethod
    def crear_usuario(cls, username: str, password: str,
                      rol: str) -> tuple[bool, str]:
        """
        Crea un nuevo usuario.
        Solo debe invocarse si Session.puede('crear_usuarios') es True.
        """
        username = username.strip()

        if not username or not password:
            return False, "Usuario y contraseña son obligatorios."

        if rol not in ALL_ROLES:
            return False, f"Rol inválido. Opciones: {', '.join(ALL_ROLES)}."

        if len(password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."

        try:
            UserModel.insert(username, password, rol)
            return True, f"Usuario '{username}' creado exitosamente."
        except ValueError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error al crear usuario: {e}"

    @classmethod
    def listar_usuarios(cls) -> list:
        """Retorna todos los usuarios. Solo Admin."""
        return UserModel.get_all()

    @classmethod
    def eliminar_usuario(cls, user_id: int) -> tuple[bool, str]:
        """Elimina un usuario por id. No permite eliminar al propio Admin activo."""
        if user_id == Session.get_user_id():
            return False, "No puedes eliminar tu propio usuario."
        try:
            UserModel.delete(user_id)
            return True, "Usuario eliminado."
        except Exception as e:
            return False, f"Error al eliminar: {e}"

    @classmethod
    def cambiar_password(cls, user_id: int,
                         new_password: str) -> tuple[bool, str]:
        """Cambia la contraseña de un usuario."""
        if len(new_password) < 6:
            return False, "La contraseña debe tener al menos 6 caracteres."
        try:
            UserModel.update_password(user_id, new_password)
            return True, "Contraseña actualizada."
        except Exception as e:
            return False, f"Error: {e}"

    # Utilidades
    @staticmethod
    def admin_existe() -> bool:
        return UserModel.admin_exists()