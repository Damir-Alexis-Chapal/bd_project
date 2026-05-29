# views/crud_view.py

import tkinter as tk
from tkinter import ttk
from views.base_view import (
    BaseView, FONT_HEADER, FONT_NORMAL, FONT_SMALL,
)
from config.constants import (
    COLOR_PRIMARY, COLOR_BG, COLOR_ACCENT,
    COLOR_TEXT, PAISES_ANFITRIONES,
)
from controllers.crud_controller import (
    ConfederacionController, CiudadController,
    EstadioController, GrupoController,
    EquipoController, JugadorController, PartidoController,
)


class CrudView(tk.Frame):
    """
    Vista de gestión de datos con una pestaña por entidad.
    Cada pestaña tiene: tabla de datos + formulario lateral.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True)
        self._build_ui()

    def _build_ui(self):
        tk.Label(self, text="Gestión de datos", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_BG).pack(anchor="w", padx=12, pady=(10, 4))

        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=8, pady=4)

        # Una pestaña por entidad
        tabs = [
            ("Confederaciones", ConfederacionTab),
            ("Ciudades",        CiudadTab),
            ("Estadios",        EstadioTab),
            ("Grupos",          GrupoTab),
            ("Equipos",         EquipoTab),
            ("Jugadores",       JugadorTab),
            ("Partidos",        PartidoTab),
        ]
        for nombre, cls in tabs:
            frame = tk.Frame(nb, bg=COLOR_BG)
            nb.add(frame, text=nombre)
            cls(frame)


# ══════════════════════════════════════════════
# BASE para cada pestaña CRUD
# ══════════════════════════════════════════════
class _CrudTab(tk.Frame):
    """
    Plantilla reutilizable:
      izquierda → Treeview con los registros
      derecha   → Formulario (campos + botones)
    Las subclases implementan:
      _columnas()  → list[str]
      _cargar()    → list[tuple]
      _campos_form(frame) → construye los campos del formulario
      _on_guardar()
      _on_eliminar()
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLOR_BG)
        self.pack(fill="both", expand=True)
        self._id_seleccionado = None
        self._build_layout()
        self.refrescar()

    def _build_layout(self):
        # Panel izquierdo (tabla)
        left = tk.Frame(self, bg=COLOR_BG)
        left.pack(side="left", fill="both", expand=True, padx=(8, 4), pady=8)

        self._tree, _, _ = BaseView.make_treeview(left, self._columnas(), alto=18)
        self._tree.bind("<<TreeviewSelect>>", self._on_seleccionar)

        btn_row = tk.Frame(left, bg=COLOR_BG)
        btn_row.pack(fill="x", padx=8, pady=4)
        BaseView.make_button(btn_row, "🔄 Actualizar", self.refrescar, width=16).pack(side="left")
        BaseView.make_danger_button(btn_row, "🗑 Eliminar", self._on_eliminar, width=16).pack(side="left", padx=6)

        # Panel derecho (formulario)
        right = tk.Frame(self, bg=COLOR_ACCENT, bd=1, relief="groove")
        right.pack(side="right", fill="y", padx=(4, 8), pady=8, ipadx=10, ipady=10)

        tk.Label(right, text="Formulario", font=FONT_HEADER,
                 fg=COLOR_PRIMARY, bg=COLOR_ACCENT).pack(anchor="w", pady=(0, 8))

        self._campos_form(right)

        btn_form = tk.Frame(right, bg=COLOR_ACCENT)
        btn_form.pack(pady=10)
        BaseView.make_success_button(btn_form, "💾 Guardar", self._on_guardar, width=14).pack(side="left")
        BaseView.make_button(btn_form, "✖ Limpiar", self._limpiar_form, width=10).pack(side="left", padx=4)

        self._lbl_status = tk.Label(right, text="", font=FONT_SMALL,
                                     bg=COLOR_ACCENT, wraplength=230)
        self._lbl_status.pack()

    # ── Helpers internos ──────────────────────
    def refrescar(self):
        filas = self._cargar()
        BaseView.poblar_treeview(self._tree, filas)
        self._limpiar_form()

    def _on_seleccionar(self, event=None):
        sel = self._tree.selection()
        if not sel:
            return
        valores = self._tree.item(sel[0], "values")
        self._id_seleccionado = valores[0]
        self._rellenar_form(valores)

    def _mostrar_status(self, ok: bool, msg: str):
        self._lbl_status.config(
            text=msg,
            fg="#2e7d32" if ok else "#c62828",
        )

    # ── Métodos a implementar ─────────────────
    def _columnas(self) -> list:
        raise NotImplementedError

    def _cargar(self) -> list:
        raise NotImplementedError

    def _campos_form(self, frame):
        raise NotImplementedError

    def _rellenar_form(self, valores: tuple):
        raise NotImplementedError

    def _limpiar_form(self):
        self._id_seleccionado = None
        raise NotImplementedError

    def _on_guardar(self):
        raise NotImplementedError

    def _on_eliminar(self):
        raise NotImplementedError


# ══════════════════════════════════════════════
# PESTAÑAS concretas
# ══════════════════════════════════════════════

class ConfederacionTab(_CrudTab):

    def _columnas(self):
        return ["ID", "Nombre"]

    def _cargar(self):
        return ConfederacionController.listar()

    def _campos_form(self, f):
        tk.Label(f, text="Nombre", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_nombre = BaseView.make_entry(f, width=26)
        self._e_nombre.pack(pady=(0, 8))

    def _rellenar_form(self, v):
        self._e_nombre.delete(0, "end")
        self._e_nombre.insert(0, v[1])

    def _limpiar_form(self):
        self._id_seleccionado = None
        if hasattr(self, "_e_nombre"):
            self._e_nombre.delete(0, "end")

    def _on_guardar(self):
        nombre = self._e_nombre.get()
        if self._id_seleccionado:
            ok, msg = ConfederacionController.actualizar(self._id_seleccionado, nombre)
        else:
            ok, msg = ConfederacionController.crear(nombre)
        self._mostrar_status(ok, msg)
        if ok:
            self.refrescar()

    def _on_eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un registro primero.")
            return
        if BaseView.msg_confirm("Eliminar", "¿Eliminar esta confederación?"):
            ok, msg = ConfederacionController.eliminar(self._id_seleccionado)
            self._mostrar_status(ok, msg)
            if ok:
                self.refrescar()


class CiudadTab(_CrudTab):

    def _columnas(self):
        return ["ID", "Nombre", "País"]

    def _cargar(self):
        return CiudadController.listar()

    def _campos_form(self, f):
        tk.Label(f, text="Nombre", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_nombre = BaseView.make_entry(f, width=26)
        self._e_nombre.pack(pady=(0, 8))

        tk.Label(f, text="País", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._cb_pais = BaseView.make_combobox(f, PAISES_ANFITRIONES)
        self._cb_pais.pack(pady=(0, 8))

    def _rellenar_form(self, v):
        self._e_nombre.delete(0, "end")
        self._e_nombre.insert(0, v[1])
        self._cb_pais.set(v[2])

    def _limpiar_form(self):
        self._id_seleccionado = None
        if hasattr(self, "_e_nombre"):
            self._e_nombre.delete(0, "end")
            self._cb_pais.set("")

    def _on_guardar(self):
        nombre = self._e_nombre.get()
        pais   = self._cb_pais.get()
        if self._id_seleccionado:
            ok, msg = CiudadController.actualizar(self._id_seleccionado, nombre, pais)
        else:
            ok, msg = CiudadController.crear(nombre, pais)
        self._mostrar_status(ok, msg)
        if ok:
            self.refrescar()

    def _on_eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un registro primero.")
            return
        if BaseView.msg_confirm("Eliminar", "¿Eliminar esta ciudad?"):
            ok, msg = CiudadController.eliminar(self._id_seleccionado)
            self._mostrar_status(ok, msg)
            if ok:
                self.refrescar()


class EstadioTab(_CrudTab):

    def _columnas(self):
        return ["ID", "Nombre", "Capacidad", "ID Ciudad", "Ciudad", "País"]

    def _cargar(self):
        return EstadioController.listar()

    def _campos_form(self, f):
        tk.Label(f, text="Nombre", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_nombre = BaseView.make_entry(f, width=26)
        self._e_nombre.pack(pady=(0, 8))

        tk.Label(f, text="Capacidad", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_cap = BaseView.make_entry(f, width=26)
        self._e_cap.pack(pady=(0, 8))

        tk.Label(f, text="Ciudad", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        ciudades = CiudadController.listar()
        self._ciudad_ids  = [c[0] for c in ciudades]
        self._cb_ciudad   = BaseView.make_combobox(f, [c[1] for c in ciudades])
        self._cb_ciudad.pack(pady=(0, 8))

    def _rellenar_form(self, v):
        self._e_nombre.delete(0, "end")
        self._e_nombre.insert(0, v[1])
        self._e_cap.delete(0, "end")
        self._e_cap.insert(0, v[2])
        try:
            idx = self._ciudad_ids.index(int(v[3]))
            self._cb_ciudad.current(idx)
        except (ValueError, IndexError):
            pass

    def _limpiar_form(self):
        self._id_seleccionado = None
        if hasattr(self, "_e_nombre"):
            self._e_nombre.delete(0, "end")
            self._e_cap.delete(0, "end")
            self._cb_ciudad.set("")

    def _on_guardar(self):
        nombre = self._e_nombre.get()
        cap    = self._e_cap.get()
        idx    = self._cb_ciudad.current()
        ciudad_id = self._ciudad_ids[idx] if idx >= 0 else None
        if self._id_seleccionado:
            ok, msg = EstadioController.actualizar(self._id_seleccionado, nombre, cap, ciudad_id)
        else:
            ok, msg = EstadioController.crear(nombre, cap, ciudad_id)
        self._mostrar_status(ok, msg)
        if ok:
            self.refrescar()

    def _on_eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un registro primero.")
            return
        if BaseView.msg_confirm("Eliminar", "¿Eliminar este estadio?"):
            ok, msg = EstadioController.eliminar(self._id_seleccionado)
            self._mostrar_status(ok, msg)
            if ok:
                self.refrescar()


class GrupoTab(_CrudTab):

    def _columnas(self):
        return ["ID", "Letra"]

    def _cargar(self):
        return GrupoController.listar()

    def _campos_form(self, f):
        tk.Label(f, text="Letra / Nombre", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_letra = BaseView.make_entry(f, width=10)
        self._e_letra.pack(pady=(0, 8))

    def _rellenar_form(self, v):
        self._e_letra.delete(0, "end")
        self._e_letra.insert(0, v[1])

    def _limpiar_form(self):
        self._id_seleccionado = None
        if hasattr(self, "_e_letra"):
            self._e_letra.delete(0, "end")

    def _on_guardar(self):
        letra = self._e_letra.get()
        if self._id_seleccionado:
            ok, msg = GrupoController.actualizar(self._id_seleccionado, letra)
        else:
            ok, msg = GrupoController.crear(letra)
        self._mostrar_status(ok, msg)
        if ok:
            self.refrescar()

    def _on_eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un registro primero.")
            return
        if BaseView.msg_confirm("Eliminar", "¿Eliminar este grupo?"):
            ok, msg = GrupoController.eliminar(self._id_seleccionado)
            self._mostrar_status(ok, msg)
            if ok:
                self.refrescar()


class EquipoTab(_CrudTab):

    def _columnas(self):
        return ["ID", "Nombre", "ID Conf.", "Confederación", "ID DT", "Valor mercado"]

    def _cargar(self):
        return EquipoController.listar()

    def _campos_form(self, f):
        from models.confederacion_model import ConfederacionModel
        from models.jugador_model       import JugadorModel

        tk.Label(f, text="Nombre", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_nombre = BaseView.make_entry(f, width=26)
        self._e_nombre.pack(pady=(0, 6))

        tk.Label(f, text="Confederación", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        confs = ConfederacionModel.get_all()
        self._conf_ids = [c[0] for c in confs]
        self._cb_conf  = BaseView.make_combobox(f, [c[1] for c in confs])
        self._cb_conf.pack(pady=(0, 6))

        tk.Label(f, text="ID Director Técnico (jugador)", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_dt = BaseView.make_entry(f, width=10)
        self._e_dt.pack(pady=(0, 6))

        tk.Label(f, text="Valor de mercado (€)", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_valor = BaseView.make_entry(f, width=26)
        self._e_valor.pack(pady=(0, 6))

    def _rellenar_form(self, v):
        self._e_nombre.delete(0, "end");  self._e_nombre.insert(0, v[1])
        try:
            idx = self._conf_ids.index(int(v[2]))
            self._cb_conf.current(idx)
        except (ValueError, IndexError):
            pass
        self._e_dt.delete(0, "end");    self._e_dt.insert(0, v[4])
        self._e_valor.delete(0, "end"); self._e_valor.insert(0, v[5])

    def _limpiar_form(self):
        self._id_seleccionado = None
        if hasattr(self, "_e_nombre"):
            self._e_nombre.delete(0, "end")
            self._cb_conf.set("")
            self._e_dt.delete(0, "end")
            self._e_valor.delete(0, "end")

    def _on_guardar(self):
        nombre = self._e_nombre.get()
        idx    = self._cb_conf.current()
        conf_id = self._conf_ids[idx] if idx >= 0 else None
        dt_id   = self._e_dt.get()
        valor   = self._e_valor.get()
        if self._id_seleccionado:
            ok, msg = EquipoController.actualizar(self._id_seleccionado, nombre, conf_id, dt_id, valor)
        else:
            ok, msg = EquipoController.crear(nombre, conf_id, dt_id, valor)
        self._mostrar_status(ok, msg)
        if ok:
            self.refrescar()

    def _on_eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un registro primero.")
            return
        if BaseView.msg_confirm("Eliminar", "¿Eliminar este equipo?"):
            ok, msg = EquipoController.eliminar(self._id_seleccionado)
            self._mostrar_status(ok, msg)
            if ok:
                self.refrescar()


class JugadorTab(_CrudTab):

    def _columnas(self):
        return ["ID", "Nombre", "Edad", "Peso", "Estatura", "Valor (€)", "ID Equipo", "Equipo"]

    def _cargar(self):
        return JugadorController.listar()

    def _campos_form(self, f):
        campos_simples = [
            ("Nombre",        "_e_nombre",   26),
            ("Edad",          "_e_edad",     8),
            ("Peso (kg)",     "_e_peso",     10),
            ("Estatura (m)",  "_e_estatura", 10),
            ("Valor (€)",     "_e_valor",    16),
        ]
        for etiqueta, attr, ancho in campos_simples:
            tk.Label(f, text=etiqueta, font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
            entry = BaseView.make_entry(f, width=ancho)
            entry.pack(pady=(0, 6))
            setattr(self, attr, entry)

        tk.Label(f, text="Equipo", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        equipos = EquipoController.listar()
        self._eq_ids  = [e[0] for e in equipos]
        self._cb_equipo = BaseView.make_combobox(f, [e[1] for e in equipos])
        self._cb_equipo.pack(pady=(0, 6))

    def _rellenar_form(self, v):
        for attr, idx in [("_e_nombre", 1), ("_e_edad", 2), ("_e_peso", 3),
                           ("_e_estatura", 4), ("_e_valor", 5)]:
            e = getattr(self, attr)
            e.delete(0, "end")
            e.insert(0, v[idx])
        try:
            eq_idx = self._eq_ids.index(int(v[6]))
            self._cb_equipo.current(eq_idx)
        except (ValueError, IndexError):
            pass

    def _limpiar_form(self):
        self._id_seleccionado = None
        for attr in ("_e_nombre", "_e_edad", "_e_peso", "_e_estatura", "_e_valor"):
            if hasattr(self, attr):
                getattr(self, attr).delete(0, "end")
        if hasattr(self, "_cb_equipo"):
            self._cb_equipo.set("")

    def _on_guardar(self):
        idx = self._cb_equipo.current()
        eq_id = self._eq_ids[idx] if idx >= 0 else None
        args = (
            self._e_nombre.get(), self._e_edad.get(),
            self._e_peso.get(), self._e_estatura.get(),
            self._e_valor.get(), eq_id,
        )
        if self._id_seleccionado:
            ok, msg = JugadorController.actualizar(self._id_seleccionado, *args)
        else:
            ok, msg = JugadorController.crear(*args)
        self._mostrar_status(ok, msg)
        if ok:
            self.refrescar()

    def _on_eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un registro primero.")
            return
        if BaseView.msg_confirm("Eliminar", "¿Eliminar este jugador?"):
            ok, msg = JugadorController.eliminar(self._id_seleccionado)
            self._mostrar_status(ok, msg)
            if ok:
                self.refrescar()


class PartidoTab(_CrudTab):

    def _columnas(self):
        return ["ID", "Equipo 1", "Equipo 2", "Estadio", "Ciudad", "País", "Grupo", "Fecha y Hora"]

    def _cargar(self):
        return PartidoController.listar()

    def _campos_form(self, f):
        equipos  = EquipoController.listar()
        estadios = EstadioController.listar()
        grupos   = GrupoController.listar()

        self._eq_ids  = [e[0] for e in equipos]
        self._es_ids  = [e[0] for e in estadios]
        self._gr_ids  = [g[0] for g in grupos]

        tk.Label(f, text="Equipo 1", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._cb_eq1 = BaseView.make_combobox(f, [e[1] for e in equipos])
        self._cb_eq1.pack(pady=(0, 6))

        tk.Label(f, text="Equipo 2", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._cb_eq2 = BaseView.make_combobox(f, [e[1] for e in equipos])
        self._cb_eq2.pack(pady=(0, 6))

        tk.Label(f, text="Estadio", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._cb_es = BaseView.make_combobox(f, [e[1] for e in estadios])
        self._cb_es.pack(pady=(0, 6))

        tk.Label(f, text="Grupo", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._cb_gr = BaseView.make_combobox(f, [g[1] for g in grupos])
        self._cb_gr.pack(pady=(0, 6))

        tk.Label(f, text="Fecha y hora (YYYY-MM-DD HH:MM)", font=FONT_SMALL, bg=COLOR_ACCENT).pack(anchor="w")
        self._e_fecha = BaseView.make_entry(f, width=22)
        self._e_fecha.pack(pady=(0, 6))

    def _rellenar_form(self, v):
        # v = (id, eq1, eq2, estadio, ciudad, pais, grupo, fecha_hora)
        # Buscamos por nombre en los combos no tenemos id directo en el tree
        # Usamos el controlador para obtener el registro completo por id
        row = PartidoController.obtener(v[0])
        if not row:
            return
        # row = (id, id_eq1, id_eq2, id_estadio, id_grupo, fecha_hora)
        try:
            self._cb_eq1.current(self._eq_ids.index(row[1]))
            self._cb_eq2.current(self._eq_ids.index(row[2]))
            self._cb_es.current(self._es_ids.index(row[3]))
            self._cb_gr.current(self._gr_ids.index(row[4]))
        except (ValueError, IndexError):
            pass
        self._e_fecha.delete(0, "end")
        self._e_fecha.insert(0, str(row[5]) if row[5] else "")

    def _limpiar_form(self):
        self._id_seleccionado = None
        if hasattr(self, "_cb_eq1"):
            for cb in (self._cb_eq1, self._cb_eq2, self._cb_es, self._cb_gr):
                cb.set("")
            self._e_fecha.delete(0, "end")

    def _on_guardar(self):
        i1 = self._cb_eq1.current()
        i2 = self._cb_eq2.current()
        ie = self._cb_es.current()
        ig = self._cb_gr.current()
        eq1_id = self._eq_ids[i1] if i1 >= 0 else None
        eq2_id = self._eq_ids[i2] if i2 >= 0 else None
        es_id  = self._es_ids[ie] if ie >= 0 else None
        gr_id  = self._gr_ids[ig] if ig >= 0 else None
        fecha  = self._e_fecha.get()

        if self._id_seleccionado:
            ok, msg = PartidoController.actualizar(
                self._id_seleccionado, eq1_id, eq2_id, es_id, gr_id, fecha)
        else:
            ok, msg = PartidoController.crear(eq1_id, eq2_id, es_id, gr_id, fecha)
        self._mostrar_status(ok, msg)
        if ok:
            self.refrescar()

    def _on_eliminar(self):
        if not self._id_seleccionado:
            BaseView.msg_error("Error", "Selecciona un registro primero.")
            return
        if BaseView.msg_confirm("Eliminar", "¿Eliminar este partido?"):
            ok, msg = PartidoController.eliminar(self._id_seleccionado)
            self._mostrar_status(ok, msg)
            if ok:
                self.refrescar()