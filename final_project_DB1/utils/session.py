# Almacena el estado del usuario actualmente
# logueado. Cualquier módulo puede importar
# este objeto y consultar quién está conectado.

from config.constants import PERMISOS


class Session:
    """
    Objeto global que representa la sesión activa.
    Se inicializa vacío y se llena al hacer login.
    """

    _user_id     = None
    _username    = None
    _rol         = None
    _bitacora_id = None   # id de la fila activa en bitácora

    # Login / Logout
    @classmethod
    def login(cls, user_id: int, username: str, rol: str):
        """Guarda los datos del usuario autenticado."""
        cls._user_id  = user_id
        cls._username = username
        cls._rol      = rol
        print(f"[Session] Sesión iniciada: {username} ({rol})")

    @classmethod
    def logout(cls):
        """Limpia la sesión."""
        print(f"[Session] Sesión cerrada: {cls._username}")
        cls._user_id     = None
        cls._username    = None
        cls._rol         = None
        cls._bitacora_id = None

    # Propiedades de solo lectura
    @classmethod
    def get_user_id(cls) -> int | None:
        return cls._user_id

    @classmethod
    def get_username(cls) -> str | None:
        return cls._username

    @classmethod
    def get_rol(cls) -> str | None:
        return cls._rol

    @classmethod
    def is_authenticated(cls) -> bool:
        return cls._user_id is not None

    @classmethod
    def set_bitacora_id(cls, bitacora_id: int):
        cls._bitacora_id = bitacora_id

    @classmethod
    def get_bitacora_id(cls) -> int | None:
        return cls._bitacora_id

    # Permisos
    @classmethod
    def puede(cls, accion: str) -> bool:
        """
        Verifica si el rol actual tiene permiso para una acción.
        Ejemplo: Session.puede("crud")
        """
        if not cls._rol:
            return False
        return PERMISOS.get(cls._rol, {}).get(accion, False)