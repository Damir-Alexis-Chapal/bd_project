# views/user_view.py

import tkinter as tk
from views.base_view              import BaseView, FONT_HEADER, FONT_NORMAL, FONT_SMALL
from controllers.auth_controller  import AuthController
from config.constants             import (
    COLOR_PRIMARY, COLOR_BG, COLOR_ACCENT,
    COLOR_DANGER, ALL_ROLES,
)


class UserView(tk.Frame):
    """
    Gestión de usuarios. Solo accesible para el Administrador.
    Permite crear, ver y eliminar usuarios, y cambiar contraseñas.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True)
        self._id_seleccionado = None
        self._build_ui()
        self.refrescar()

    def _build_ui(self):
        tk.Label(self, text="Gestión de usuarios", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_BG).pack(anchor="w", padx=12, pady=(10, 4))

        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill="both", expand=True, padx=8)

        # ── Tabla (izquierda) ─────────────────
        left = tk.Frame(body, bg=COLOR_BG)
        left.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self._tree, _, _ = BaseView.make_treeview(
            left, ["ID", "Usuario", "Rol"], alto=20)
        self._tree.bind("<<TreeviewSelect>>", self._on_seleccionar)

        btn_row = tk.Frame(left, bg=COLOR_BG)
        btn_row.pack(fill="x", padx=8, pady=4)
        BaseView.make_button(btn_row, "🔄 Actualizar", self.refrescar, width=16).pack(side="left")
        BaseView.make_danger_button(
            btn_row, "🗑 Eliminar", self._eliminar, width=16
        ).pack(side="left", padx=6)

        # ── Formulario (derecha) ──────────────
        right = tk.Frame(body, bg=COLOR_ACCENT, bd=1,
                          relief="groove", padx=14, pady=14)
        right.pack(side="right", fill="y")

        # — Crear usuario —
        tk.Label(right, text="Crear usuario", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_ACCENT).pack(anchor="w", pady=(0, 8))

        tk.Label(right, text="Nombre de usuario", font=FONT_SMALL,
                 bg=COLOR_ACCENT).pack(anchor="w")
        self._e_user = BaseView.make_entry(right, width=24)
        self._e_user.pack(pady=(0, 6))

        tk.Label(right, text="Contraseña", font=FONT_SMALL,
                 bg=COLOR_ACCENT).pack(anchor="w")
        self._e_pass = BaseView.make_entry(right, width=24, show="•")
        self._e_pass.pack(pady=(0, 6))

        tk.Label(right, text="Rol", font=FONT_SMALL,
                 bg=COLOR_ACCENT).pack(anchor="w")
        self._cb_rol = BaseView.make_combobox(right, ALL_ROLES, width=22)
        self._cb_rol.pack(pady=(0, 10))

        BaseView.make_success_button(
            right, "➕ Crear", self._crear, width=22
        ).pack(pady=(0, 14))

        tk.ttk.Separator(right, orient="horizontal").pack(fill="x", pady=6)

        # — Cambiar contraseña —
        tk.Label(right, text="Cambiar contraseña", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_ACCENT).pack(anchor="w", pady=(6, 8))
        tk.Label(right,
                 text="Selecciona un usuario en la tabla\nluego escribe la nueva contraseña.",
                 font=FONT_SMALL, bg=COLOR_ACCENT, fg="#555",
                 justify="left").pack(anchor="w", pady=(0, 6))

        self._e_newpass = BaseView.make_entry(right, width=24, show="•")
        self._e_newpass.pack(pady=(0, 8))

        BaseView.make_button(
            right, "🔑 Cambiar contraseña",
            self._cambiar_pass, width=22
        ).pack()

        # Estado
        self._lbl_status = tk.Label(right, text="", font=FONT_SMALL,
                                     bg=COLOR_ACCENT, wraplength=220)
        self._lbl_status.pack(pady=(10, 0))

    # ── Datos ─────────────────────────────────
    def refrescar(self):
        filas = AuthController.listar_usuarios()
        BaseView.poblar_treeview(self._tree, filas)
        self._id_seleccionado = None
        self._lbl_status.config(text="")

    def _on_seleccionar(self, event=None):
        sel = self._tree.selection()
        if sel:
            self._id_seleccionado = self._tree.item(sel[0], "values")[0]

    # ── Acciones ──────────────────────────────
    def _crear(self):
        username = self._e_user.get().strip()
        password = self._e_pass.get()
        rol      = self._cb_rol.get()

        ok, msg = AuthController.crear_usuario(username, password, rol)
        self._lbl_status.config(
            text=msg,
            fg="#2e7d32" if ok else "#c62828",
        )
        if ok:
            self._e_user.delete(0, "end")
            self._e_pass.delete(0, "end")
            self._cb_rol.set("")
            self.refrescar()

    def _eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un usuario primero.")
            return
        if BaseView.msg_confirm("Eliminar usuario",
                                "¿Estás seguro de eliminar este usuario? Esta acción no se puede deshacer."):
            ok, msg = AuthController.eliminar_usuario(int(self._id_seleccionado))
            self._lbl_status.config(
                text=msg,
                fg="#2e7d32" if ok else "#c62828",
            )
            if ok:
                self.refrescar()

    def _cambiar_pass(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un usuario de la tabla primero.")
            return
        nueva = self._e_newpass.get()
        ok, msg = AuthController.cambiar_password(int(self._id_seleccionado), nueva)
        self._lbl_status.config(
            text=msg,
            fg="#2e7d32" if ok else "#c62828",
        )
        if ok:
            self._e_newpass.delete(0, "end")