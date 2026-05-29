# views/report_view.py

import tkinter as tk
from tkinter import ttk
import os
from views.base_view              import BaseView, FONT_HEADER, FONT_NORMAL, FONT_SMALL
from controllers.report_controller import ReportController
from models.confederacion_model   import ConfederacionModel
from config.constants             import COLOR_PRIMARY, COLOR_BG, COLOR_ACCENT, PAISES_ANFITRIONES


class ReportView(tk.Frame):
    """
    Vista de reportes PDF. Cada reporte tiene su propia pestaña
    con los filtros necesarios y un botón para generar y guardar el PDF.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Reportes PDF", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_BG).pack(anchor="w", padx=12, pady=(10, 4))

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=4)

        tabs = [
            ("B1 · Bitácora",            _ReporteB1),
            ("B2 · Jugadores por medidas", _ReporteB2),
            ("B3 · Valor por confederación", _ReporteB3),
            ("B4 · Equipos por país",    _ReporteB4),
        ]
        for nombre, cls in tabs:
            f = tk.Frame(nb, bg=COLOR_BG)
            nb.add(f, text=nombre)
            cls(f)


# ══════════════════════════════════════════════
# BASE para cada pestaña de reporte
# ══════════════════════════════════════════════
class _ReporteBase(tk.Frame):
    """
    Layout común:
      descripción → filtros → botón Generar PDF → estado
      + área de vista previa (lista de columnas del reporte)
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True, padx=14, pady=10)
        self._build_layout()

    def _build_layout(self):
        # Descripción
        tk.Label(self, text=self._descripcion(), font=FONT_SMALL,
                 fg="#555", bg=COLOR_BG, wraplength=820,
                 justify="left").pack(anchor="w", pady=(0, 10))

        # Panel de filtros
        filtros = tk.Frame(self, bg=COLOR_ACCENT, bd=1,
                            relief="groove", padx=14, pady=10)
        filtros.pack(fill="x", pady=(0, 10))
        self._build_filtros(filtros)

        # Botón generar
        BaseView.make_button(
            filtros, "📄  Generar PDF",
            self._generar, width=20
        ).pack(side="left", padx=(16, 0))

        # Estado
        self._lbl_status = tk.Label(self, text="", font=FONT_SMALL,
                                     bg=COLOR_BG, wraplength=780, justify="left")
        self._lbl_status.pack(anchor="w", pady=(4, 0))

        # Info de columnas del reporte
        tk.Label(self, text=f"Columnas del reporte: {' · '.join(self._columnas_reporte())}",
                 font=FONT_SMALL, fg="#777", bg=COLOR_BG).pack(anchor="w", pady=(8, 0))

    # ── Métodos a implementar ─────────────────
    def _descripcion(self) -> str:
        return ""

    def _columnas_reporte(self) -> list[str]:
        return []

    def _build_filtros(self, frame):
        pass

    def _generar(self):
        raise NotImplementedError

    # ── Helper ────────────────────────────────
    def _pedir_ruta_y_generar(self, nombre_sugerido: str,
                               fn_generar, *args):
        """
        Abre el diálogo de guardar, llama a fn_generar y muestra el resultado.
        fn_generar(*args, ruta) debe retornar (bool, str).
        """
        ruta = BaseView.pedir_ruta_pdf(nombre_sugerido)
        if not ruta:
            return   # usuario canceló

        ok, msg = fn_generar(*args, ruta)

        if ok:
            self._lbl_status.config(
                text=f"✔  PDF generado correctamente: {ruta}",
                fg="#2e7d32"
            )
            # Intentar abrir el PDF automáticamente
            try:
                os.startfile(ruta)          # Windows
            except AttributeError:
                try:
                    import subprocess
                    subprocess.Popen(["xdg-open", ruta])   # Linux (CachyOS)
                except Exception:
                    pass
        else:
            self._lbl_status.config(text=f"⚠  {msg}", fg="#c62828")


# ══════════════════════════════════════════════
# REPORTES CONCRETOS
# ══════════════════════════════════════════════

class _ReporteB1(_ReporteBase):
    """B1: bitácora de accesos en un rango de fechas."""

    def _descripcion(self):
        return (
            "Lista todos los usuarios que ingresaron y salieron del sistema "
            "en el rango de fechas indicado, incluyendo hora exacta de cada evento."
        )

    def _columnas_reporte(self):
        return ["Usuario", "Rol", "Fecha ingreso", "Fecha salida"]

    def _build_filtros(self, f):
        tk.Label(f, text="Desde (YYYY-MM-DD):", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")
        self._e_desde = BaseView.make_entry(f, width=13)
        self._e_desde.pack(side="left", padx=(4, 14))

        tk.Label(f, text="Hasta (YYYY-MM-DD):", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")
        self._e_hasta = BaseView.make_entry(f, width=13)
        self._e_hasta.pack(side="left", padx=(4, 0))

    def _generar(self):
        self._pedir_ruta_y_generar(
            "bitacora_accesos.pdf",
            ReportController.reporte_bitacora,
            self._e_desde.get().strip(),
            self._e_hasta.get().strip(),
        )


class _ReporteB2(_ReporteBase):
    """B2: jugadores dentro de rangos de peso y estatura."""

    def _descripcion(self):
        return (
            "Lista los jugadores cuyo peso y estatura se encuentran dentro "
            "de los rangos que especifiques. Útil para análisis físico del plantel."
        )

    def _columnas_reporte(self):
        return ["Jugador", "Edad", "Peso (kg)", "Estatura (m)", "Valor (€)", "Equipo"]

    def _build_filtros(self, f):
        parametros = [
            ("Peso mín (kg):",    "_e_p_min", 7),
            ("Peso máx (kg):",    "_e_p_max", 7),
            ("Estatura mín (m):", "_e_e_min", 6),
            ("Estatura máx (m):", "_e_e_max", 6),
        ]
        for etq, attr, ancho in parametros:
            tk.Label(f, text=etq, font=FONT_NORMAL, bg=COLOR_ACCENT).pack(side="left")
            e = BaseView.make_entry(f, width=ancho)
            e.pack(side="left", padx=(4, 12))
            setattr(self, attr, e)

    def _generar(self):
        self._pedir_ruta_y_generar(
            "jugadores_por_medidas.pdf",
            ReportController.reporte_jugadores_por_medidas,
            self._e_p_min.get(), self._e_p_max.get(),
            self._e_e_min.get(), self._e_e_max.get(),
        )


class _ReporteB3(_ReporteBase):
    """B3: valor total de jugadores por equipo y confederación."""

    def _descripcion(self):
        return (
            "Muestra el valor total de mercado de los jugadores de cada equipo "
            "perteneciente a la confederación seleccionada, ordenado de mayor a menor."
        )

    def _columnas_reporte(self):
        return ["Equipo", "Valor total jugadores (€)"]

    def _build_filtros(self, f):
        tk.Label(f, text="Confederación:", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")
        confs = ConfederacionModel.get_all()
        self._conf_ids = [c[0] for c in confs]
        self._cb_conf  = BaseView.make_combobox(f, [c[1] for c in confs], width=28)
        self._cb_conf.pack(side="left", padx=(6, 0))

    def _generar(self):
        idx = self._cb_conf.current()
        if idx < 0:
            self._lbl_status.config(
                text="⚠  Selecciona una confederación.", fg="#c62828")
            return
        conf_id = self._conf_ids[idx]
        self._pedir_ruta_y_generar(
            "valor_por_confederacion.pdf",
            ReportController.reporte_valor_total_por_confederacion,
            conf_id,
        )


class _ReporteB4(_ReporteBase):
    """B4: equipos que jugarán en cada país anfitrión."""

    def _descripcion(self):
        return (
            "Lista todos los equipos (países) que disputarán al menos un partido "
            "de fase de grupos en el país anfitrión seleccionado."
        )

    def _columnas_reporte(self):
        return ["Equipo", "Confederación", "Estadio", "Ciudad", "País anfitrión"]

    def _build_filtros(self, f):
        tk.Label(f, text="País anfitrión:", font=FONT_NORMAL,
                 bg=COLOR_ACCENT).pack(side="left")
        self._cb_pais = BaseView.make_combobox(f, PAISES_ANFITRIONES, width=16)
        self._cb_pais.pack(side="left", padx=(6, 0))

    def _generar(self):
        pais = self._cb_pais.get()
        if not pais:
            self._lbl_status.config(
                text="⚠  Selecciona un país anfitrión.", fg="#c62828")
            return
        self._pedir_ruta_y_generar(
            f"equipos_en_{pais.lower().replace(' ', '_')}.pdf",
            ReportController.reporte_paises_por_anfitrion,
            pais,
        )