# Patrón Singleton: una sola conexión activa
# durante toda la sesión de la aplicación.

import oracledb
from config.settings import DB_USER, DB_PASSWORD, DB_DSN


class DatabaseConnection:
    """
    Singleton que mantiene una única conexión a Oracle.
    Uso:
        db  = DatabaseConnection.get_instance()
        con = db.connection
    """

    _instance = None  # única instancia compartida

    def __init__(self):
        self._connection = None
        self._connect()

    # Singleton
    @classmethod
    def get_instance(cls):
        """Devuelve la instancia existente o crea una nueva."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    # Conexión 
    def _connect(self):
        """Abre la conexión en modo Thin (sin Oracle Client instalado)."""
        try:
            self._connection = oracledb.connect(
                user=DB_USER,
                password=DB_PASSWORD,
                dsn=DB_DSN,
            )
            print("[DB] Conexión establecida correctamente.")
        except oracledb.DatabaseError as e:
            print(f"[DB ERROR] No se pudo conectar: {e}")
            self._connection = None
            raise

    def reconnect(self):
        """Cierra y vuelve a abrir la conexión (útil tras un timeout)."""
        self.close()
        self._connect()

    # Propiedades públicas 
    @property
    def connection(self):
        """Devuelve el objeto de conexión activo."""
        return self._connection

    def get_cursor(self):
        """Devuelve un cursor nuevo listo para usar."""
        if self._connection is None:
            raise RuntimeError("No hay conexión activa con la base de datos.")
        return self._connection.cursor()

    def commit(self):
        """Confirma la transacción actual."""
        if self._connection:
            self._connection.commit()

    def rollback(self):
        """Revierte la transacción actual."""
        if self._connection:
            self._connection.rollback()

    # Cierre 
    def close(self):
        """Cierra la conexión y limpia la instancia Singleton."""
        if self._connection:
            try:
                self._connection.close()
                print("[DB] Conexión cerrada.")
            except oracledb.DatabaseError:
                pass
            finally:
                self._connection = None
                DatabaseConnection._instance = None

    # Context Manager
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
        return False   # no suprime excepciones