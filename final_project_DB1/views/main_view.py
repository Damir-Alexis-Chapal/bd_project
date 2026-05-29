# views/main_view.py

import tkinter as tk
from tkinter import ttk
from views.base_view       import BaseView, FONT_TITLE, FONT_HEADER, FONT_NORMAL, FONT_SMALL
from utils.session         import Session
from controllers.auth_controller import AuthController
from config.constants      import (
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_BG,
    COLOR_TEXT_LIGHT, COLOR_TEXT, COLOR_ACCENT,
)
from config.settings       import APP_TITLE, APP_WIDTH, APP_HEIGHT


class MainView(tk.Tk):
    """
    Ventana principal de la aplicación.
    Contiene:
      - Barra superior con info de sesión y botón de logout
      - Panel lateral con menú dinámico según rol
      - Área de contenido central (frame intercambiable)
      - Barra de estado inferior
    """

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.minsize(900, 600)
        self.configure(bg=COLOR_BG)
        BaseView.apply_ttk_styles()

        self._frame_actual = None   # frame de contenido activo
        self._build_ui()
        self._center()
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    # ── Construcción de UI ────────────────────
    def _build_ui(self):
        self._build_topbar()
        self._build_body()
        self._status_bar = BaseView.make_status_bar(self)

    def _build_topbar(self):
        bar = tk.Frame(self, bg=COLOR_PRIMARY, height=52)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        tk.Label(bar, text="⚽  " + APP_TITLE,
                 font=FONT_TITLE, fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_PRIMARY).pack(side="left", padx=16)

        # Info de usuario (derecha)
        info_frame = tk.Frame(bar, bg=COLOR_PRIMARY)
        info_frame.pack(side="right", padx=10)

        tk.Label(info_frame,
                 text=f"👤  {Session.get_username()}  |  {Session.get_rol()}",
                 font=FONT_SMALL, fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_PRIMARY).pack(side="left", padx=(0, 12))

        tk.Button(info_frame, text="Cerrar sesión",
                  command=self._logout,
                  bg=COLOR_SECONDARY, fg=COLOR_TEXT_LIGHT,
                  font=FONT_SMALL, relief="flat", padx=8, pady=2,
                  cursor="hand2").pack(side="left")

    def _build_body(self):
        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill="both", expand=True)

        self._build_sidebar(body)

        # Área de contenido
        self._content_area = tk.Frame(body, bg=COLOR_BG)
        self._content_area.pack(side="left", fill="both", expand=True)

        # Bienvenida inicial
        self._mostrar_bienvenida()

    def _build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=COLOR_PRIMARY, width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="MENÚ",
                 font=FONT_SMALL, fg="#90caf9",
                 bg=COLOR_PRIMARY).pack(pady=(16, 4))

        ttk.Separator(sidebar, orient="horizontal").pack(fill="x", padx=12, pady=4)

        # Botones según permiso
        opciones = [
            ("📋  Gestión de datos", "crud",           self._abrir_crud),
            ("🔍  Consultas",        "consultas",       self._abrir_consultas),
            ("📄  Reportes PDF",     "reportes",        self._abrir_reportes),
            ("📒  Bitácora",         "bitacora",        self._abrir_bitacora),
            ("👥  Usuarios",         "crear_usuarios",  self._abrir_usuarios),
        ]

        for texto, permiso, comando in opciones:
            if Session.puede(permiso):
                self._sidebar_btn(sidebar, texto, comando)

    def _sidebar_btn(self, parent, texto: str, comando):
        btn = tk.Button(
            parent, text=texto, command=comando,
            bg=COLOR_PRIMARY, fg=COLOR_TEXT_LIGHT,
            font=FONT_NORMAL, relief="flat",
            anchor="w", padx=16, pady=8,
            cursor="hand2", width=22,
            activebackground=COLOR_SECONDARY,
            activeforeground=COLOR_TEXT_LIGHT,
        )
        btn.pack(fill="x")

        # Hover
        btn.bind("<Enter>", lambda e: btn.config(bg=COLOR_SECONDARY))
        btn.bind("<Leave>", lambda e: btn.config(bg=COLOR_PRIMARY))

    # ── Área de contenido ─────────────────────
    def _limpiar_contenido(self):
        """Destruye el frame de contenido actual."""
        if self._frame_actual:
            self._frame_actual.destroy()
        self._frame_actual = tk.Frame(self._content_area, bg=COLOR_BG)
        self._frame_actual.pack(fill="both", expand=True)
        return self._frame_actual

    def _mostrar_bienvenida(self):
        f = self._limpiar_contenido()
        tk.Label(f,
                 text=f"Bienvenido, {Session.get_username()} 👋",
                 font=FONT_TITLE, fg=COLOR_PRIMARY, bg=COLOR_BG
                 ).pack(expand=True)
        tk.Label(f,
                 text=f"Rol: {Session.get_rol()}  |  Selecciona una opción del menú.",
                 font=FONT_NORMAL, fg=COLOR_TEXT, bg=COLOR_BG
                 ).pack()

    # ── Navegación ────────────────────────────
    def _abrir_crud(self):
        from views.crud_view import CrudView
        f = self._limpiar_contenido()
        CrudView(f)

    def _abrir_consultas(self):
        from views.query_view import QueryView
        f = self._limpiar_contenido()
        QueryView(f)

    def _abrir_reportes(self):
        from views.report_view import ReportView
        f = self._limpiar_contenido()
        ReportView(f)

    def _abrir_bitacora(self):
        from views.bitacora_view import BitacoraView
        f = self._limpiar_contenido()
        BitacoraView(f)

    def _abrir_usuarios(self):
        from views.user_view import UserView
        f = self._limpiar_contenido()
        UserView(f)

    # ── Logout / cierre ───────────────────────
    def _logout(self):
        if BaseView.msg_confirm("Cerrar sesión", "¿Deseas cerrar la sesión?"):
            AuthController.logout()
            self.destroy()
            # Reinicia la app desde main.py
            import main
            main.iniciar()

    def _on_close(self):
        if BaseView.msg_confirm("Salir", "¿Deseas salir de la aplicación?"):
            AuthController.logout()
            self.destroy()

    # ── Utilitarios ───────────────────────────
    def set_status(self, mensaje: str, ok: bool = True):
        BaseView.set_status(self._status_bar, mensaje, ok)

    def _center(self):
        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        w, h = APP_WIDTH, APP_HEIGHT
        self.geometry(f"{w}x{h}+{(sw - w) // 2}+{(sh - h) // 2}")