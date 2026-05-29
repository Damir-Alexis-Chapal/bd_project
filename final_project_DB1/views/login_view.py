# views/login_view.py

import tkinter as tk
from tkinter import ttk
from views.base_view          import BaseView, FONT_TITLE, FONT_NORMAL, FONT_SMALL
from controllers.auth_controller import AuthController
from config.constants         import COLOR_PRIMARY, COLOR_SECONDARY, COLOR_BG, COLOR_TEXT_LIGHT
from config.settings          import APP_TITLE


class LoginView(tk.Toplevel):
    """
    Ventana modal de login.
    Al autenticarse exitosamente llama a on_success_callback()
    para que main.py abra la ventana principal.
    """

    def __init__(self, master, on_success_callback):
        super().__init__(master)
        self._callback = on_success_callback

        self.title("Iniciar sesión")
        self.resizable(False, False)
        self.configure(bg=COLOR_BG)
        self.grab_set()        # modal
        self.focus_set()

        BaseView.apply_ttk_styles()
        self._build_ui()
        self._center()

    # ── UI ────────────────────────────────────
    def _build_ui(self):
        # Barra superior
        header = tk.Frame(self, bg=COLOR_PRIMARY, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="⚽  " + APP_TITLE,
                 font=FONT_TITLE, fg=COLOR_TEXT_LIGHT,
                 bg=COLOR_PRIMARY).pack(expand=True)

        # Formulario
        form = tk.Frame(self, bg=COLOR_BG, padx=40, pady=30)
        form.pack()

        tk.Label(form, text="Usuario", font=FONT_NORMAL,
                 bg=COLOR_BG).grid(row=0, column=0, sticky="w", pady=(0, 2))
        self._entry_user = BaseView.make_entry(form, width=28)
        self._entry_user.grid(row=1, column=0, pady=(0, 12))

        tk.Label(form, text="Contraseña", font=FONT_NORMAL,
                 bg=COLOR_BG).grid(row=2, column=0, sticky="w", pady=(0, 2))
        self._entry_pass = BaseView.make_entry(form, width=28, show="•")
        self._entry_pass.grid(row=3, column=0, pady=(0, 18))

        BaseView.make_button(
            form, "Ingresar", self._intentar_login,
            width=28
        ).grid(row=4, column=0, pady=(0, 6))

        # Mensaje de error
        self._lbl_error = tk.Label(form, text="", font=FONT_SMALL,
                                   fg="#c62828", bg=COLOR_BG, wraplength=240)
        self._lbl_error.grid(row=5, column=0, pady=(4, 0))

        # Bind Enter
        self.bind("<Return>", lambda e: self._intentar_login())
        self._entry_user.focus_set()

    # ── Lógica ────────────────────────────────
    def _intentar_login(self):
        usuario = self._entry_user.get().strip()
        clave   = self._entry_pass.get()

        self._lbl_error.config(text="")

        exito, mensaje = AuthController.login(usuario, clave)

        if exito:
            self.destroy()
            self._callback()
        else:
            self._lbl_error.config(text=mensaje)
            self._entry_pass.delete(0, "end")
            self._entry_pass.focus_set()

    # ── Centrar ventana ───────────────────────
    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")