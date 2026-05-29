# views/query_view.py

import tkinter as tk
from tkinter import ttk
from views.base_view             import BaseView, FONT_HEADER, FONT_NORMAL, FONT_SMALL
from controllers.query_controller import QueryController
from controllers.crud_controller  import EstadioController
from config.constants             import COLOR_PRIMARY, COLOR_BG, COLOR_ACCENT, PAISES_ANFITRIONES


class QueryView(tk.Frame):
    """
    Vista de consultas. Muestra las 4 consultas del proyecto
    en pestañas separadas. Todos los roles pueden acceder.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Consultas", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_BG).pack(anchor="w", padx=12, pady=(10, 4))

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=4)

        tabs = [
            ("A1 · Jugador más costoso",    _ConsultaA1),
            ("A2 · Partidos por estadio",   _ConsultaA2),
            ("A3 · Equipo más costoso",     _ConsultaA3),
            ("A4 · Menores de 21",          _ConsultaA4),
        ]
        for nombre, cls in tabs:
            f = tk.Frame(nb, bg=COLOR_BG)
            nb.add(f, text=nombre)
            cls(f)


# ══════════════════════════════════════════════
# BASE para cada pestaña de consulta
# ══════════════════════════════════════════════
class _ConsultaBase(tk.Frame):
    """
    Layout común:
      top  → descripción + filtros + botón Ejecutar
      body → Treeview de resultados
      foot → contador de filas
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True, padx=10, pady=8)
        self._tree = None
        self._build_layout()

    def _build_layout(self):
        # ── Descripción ───────────────────────
        tk.Label(self, text=self._descripcion(), font=FONT_SMALL,
                 fg="#555", bg=COLOR_BG, wraplength=820,
                 justify="left").pack(anchor="w", pady=(0, 6))

        # ── Panel de filtros ──────────────────
        filtros_frame = tk.Frame(self, bg=COLOR_ACCENT, bd=1,
                                  relief="groove", padx=12, pady=8)
        filtros_frame.pack(fill="x", pady=(0, 8))
        self._build_filtros(filtros_frame)

        BaseView.make_button(
            filtros_frame, "▶  Ejecutar consulta",
            self._ejecutar, width=22
        ).pack(side="left", padx=(12, 0))

        # ── Tabla de resultados ───────────────
        self._lbl_status = tk.Label(self, text="", font=FONT_SMALL,
                                     bg=COLOR_BG, fg=COLOR_PRIMARY)
        self._lbl_status.pack(anchor="w", pady=(0, 2))

        # El treeview se construye dinámicamente al ejecutar
        self._tree_frame = tk.Frame(self, bg=COLOR_BG)
        self._tree_frame.pack(fill="both", expand=True)

    # ── Métodos a implementar ─────────────────
    def _descripcion(self) -> str:
        return ""

    def _build_filtros(self, frame):
        pass

    def _ejecutar(self):
        raise NotImplementedError

    # ── Helpers ───────────────────────────────
    def _mostrar_resultado(self, resultado: dict):
        """Recibe el dict {columnas, filas, error} del controller."""
        # Limpiar tree anterior
        for w in self._tree_frame.winfo_children():
            w.destroy()

        if resultado["error"]:
            self._lbl_status.config(text=f"⚠  {resultado['error']}", fg="#c62828")
            return

        columnas = resultado["columnas"]
        filas    = resultado["filas"]

        self._tree, _, _ = BaseView.make_treeview(
            self._tree_frame, columnas, alto=16)
        BaseView.poblar_treeview(self._tree, filas)

        n = len(filas)
        self._lbl_status.config(
            text=f"✔  {n} registro{'s' if n != 1 else ''} encontrado{'s' if n != 1 else ''}.",
            fg="#2e7d32"
        )


# ══════════════════════════════════════════════
# CONSULTAS CONCRETAS
# ══════════════════════════════════════════════

class _ConsultaA1(_ConsultaBase):
    """A1: jugador más costoso por confederación."""

    def _descripcion(self):
        return (
            "Muestra el jugador con mayor valor de mercado dentro de cada "
            "confederación participante en el mundial."
        )

    def _build_filtros(self, frame):
        tk.Label(frame,
                 text="Sin filtros requeridos — presiona Ejecutar.",
                 font=FONT_SMALL, bg=COLOR_ACCENT).pack(side="left")

    def _ejecutar(self):
        resultado = QueryController.jugador_mas_costoso_por_confederacion()
        self._mostrar_resultado(resultado)


class _ConsultaA2(_ConsultaBase):
    """A2: partidos por estadio (el usuario elige el estadio)."""

    def _descripcion(self):
        return (
            "Lista todos los partidos de fase de grupos que se jugarán "
            "en el estadio que selecciones."
        )

    def _build_filtros(self, frame):
        tk.Label(frame, text="Estadio:", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")

        estadios = EstadioController.listar()
        self._estadio_ids   = [e[0] for e in estadios]
        self._estadio_nombres = [e[1] for e in estadios]

        self._cb_estadio = BaseView.make_combobox(
            frame, self._estadio_nombres, width=34)
        self._cb_estadio.pack(side="left", padx=8)

    def _ejecutar(self):
        idx = self._cb_estadio.current()
        if idx < 0:
            self._lbl_status.config(
                text="⚠  Selecciona un estadio.", fg="#c62828")
            return
        estadio_id = self._estadio_ids[idx]
        resultado  = QueryController.partidos_por_estadio(estadio_id)
        self._mostrar_resultado(resultado)


class _ConsultaA3(_ConsultaBase):
    """A3: equipo más costoso que juega en el país anfitrión elegido."""

    def _descripcion(self):
        return (
            "Determina el equipo con mayor valor de mercado entre todos los que "
            "disputan partidos de fase de grupos en el país anfitrión seleccionado."
        )

    def _build_filtros(self, frame):
        tk.Label(frame, text="País anfitrión:", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")
        self._cb_pais = BaseView.make_combobox(frame, PAISES_ANFITRIONES, width=16)
        self._cb_pais.pack(side="left", padx=8)

    def _ejecutar(self):
        pais = self._cb_pais.get()
        if not pais:
            self._lbl_status.config(
                text="⚠  Selecciona un país.", fg="#c62828")
            return
        resultado = QueryController.equipo_mas_costoso_por_pais(pais)
        self._mostrar_resultado(resultado)


class _ConsultaA4(_ConsultaBase):
    """A4: cantidad de jugadores menores de 21 años por equipo."""

    def _descripcion(self):
        return (
            "Muestra cuántos jugadores menores de 21 años tiene cada equipo "
            "participante, ordenado de mayor a menor cantidad."
        )

    def _build_filtros(self, frame):
        tk.Label(frame,
                 text="Sin filtros requeridos — presiona Ejecutar.",
                 font=FONT_SMALL, bg=COLOR_ACCENT).pack(side="left")

    def _ejecutar(self):
        resultado = QueryController.cantidad_menores_por_equipo()
        self._mostrar_resultado(resultado)