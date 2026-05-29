# views/bitacora_view.py

import tkinter as tk
from views.base_view        import BaseView, FONT_HEADER, FONT_NORMAL, FONT_SMALL
from models.bitacora_model  import BitacoraModel
from config.constants       import COLOR_PRIMARY, COLOR_BG, COLOR_ACCENT


class BitacoraView(tk.Frame):
    """
    Vista de bitácora. Solo accesible para el Administrador.
    Muestra todos los registros de ingreso/salida con opción
    de filtrar por rango de fechas.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True)
        self._build_ui()
        self._cargar_todos()

    def _build_ui(self):
        tk.Label(self, text="Bitácora de sesiones", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_BG).pack(anchor="w", padx=12, pady=(10, 4))

        # Panel de filtros
        filtros = tk.Frame(self, bg=COLOR_ACCENT, bd=1,
                            relief="groove", padx=12, pady=8)
        filtros.pack(fill="x", padx=8, pady=(0, 6))

        tk.Label(filtros, text="Desde (YYYY-MM-DD):", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")
        self._e_desde = BaseView.make_entry(filtros, width=13)
        self._e_desde.pack(side="left", padx=(4, 14))

        tk.Label(filtros, text="Hasta (YYYY-MM-DD):", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")
        self._e_hasta = BaseView.make_entry(filtros, width=13)
        self._e_hasta.pack(side="left", padx=(4, 14))

        BaseView.make_button(
            filtros, "🔍 Filtrar", self._filtrar, width=12
        ).pack(side="left")
        BaseView.make_button(
            filtros, "🔄 Todos", self._cargar_todos, width=10
        ).pack(side="left", padx=6)

        # Estado / conteo
        self._lbl_status = tk.Label(self, text="", font=FONT_SMALL,
                                     bg=COLOR_BG, fg=COLOR_PRIMARY)
        self._lbl_status.pack(anchor="w", padx=12, pady=(0, 2))

        # Tabla
        columnas = ["Usuario", "Rol", "Fecha ingreso", "Fecha salida"]
        self._tree, _, _ = BaseView.make_treeview(self, columnas, alto=22)

    # ── Carga de datos ────────────────────────
    def _cargar_todos(self):
        try:
            filas = BitacoraModel.get_all()
            self._mostrar(filas)
            self._e_desde.delete(0, "end")
            self._e_hasta.delete(0, "end")
        except Exception as e:
            self._lbl_status.config(
                text=f"⚠  Error al cargar bitácora: {e}", fg="#c62828")

    def _filtrar(self):
        desde = self._e_desde.get().strip()
        hasta = self._e_hasta.get().strip()

        if not desde or not hasta:
            BaseView.msg_error("Filtro", "Ingresa ambas fechas para filtrar.")
            return
        if desde > hasta:
            BaseView.msg_error("Filtro", "La fecha de inicio no puede ser posterior a la de fin.")
            return
        try:
            filas = BitacoraModel.get_por_fecha(desde, hasta)
            self._mostrar(filas)
        except Exception as e:
            self._lbl_status.config(
                text=f"⚠  Error al filtrar: {e}", fg="#c62828")

    def _mostrar(self, filas: list):
        BaseView.poblar_treeview(self._tree, filas)
        n = len(filas)
        self._lbl_status.config(
            text=f"✔  {n} registro{'s' if n != 1 else ''} encontrado{'s' if n != 1 else ''}.",
            fg="#2e7d32"
        )