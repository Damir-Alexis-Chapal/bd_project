# main.py
# ─────────────────────────────────────────────
# Punto de entrada de la aplicación.
# Abre la ventana raíz oculta, lanza el login
# y al autenticarse muestra la ventana principal.
# ─────────────────────────────────────────────

import tkinter as tk
import hashlib
from models.db_connection import DatabaseConnection


def iniciar():
    # Ventana raíz invisible (requerida por Tkinter)
    root = tk.Tk()
    root.withdraw()

    # Verificar conexión a BD antes de mostrar cualquier ventana
    try:
        DatabaseConnection.get_instance()
    except Exception as e:
        import tkinter.messagebox as mb
        mb.showerror(
            "Error de conexión",
            f"No se pudo conectar a Oracle:\n{e}\n\n"
            "Verifica la configuración en config/settings.py."
        )
        root.destroy()
        return

    def on_login_exitoso():
        from views.main_view import MainView
        app = MainView()
        app.mainloop()

    from views.login_view import LoginView
    LoginView(root, on_login_exitoso)
    root.mainloop()


if __name__ == "__main__":
    iniciar()