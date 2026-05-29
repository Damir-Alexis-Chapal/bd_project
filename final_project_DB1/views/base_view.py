# views/base_view.py
# ─────────────────────────────────────────────
# Clase base que todas las vistas heredan.
# Centraliza colores, fuentes y widgets
# reutilizables para mantener coherencia visual.
# ─────────────────────────────────────────────

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config.constants import (
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_ACCENT,
    COLOR_SUCCESS, COLOR_DANGER, COLOR_BG,
    COLOR_TEXT, COLOR_TEXT_LIGHT,
)


# ── Fuentes globales ──────────────────────────
FONT_TITLE  = ("Segoe UI", 16, "bold")
FONT_HEADER = ("Segoe UI", 11, "bold")
FONT_NORMAL = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 9)


class BaseView:
    """
    Mixin/base para todas las vistas.
    No hereda de tk.Frame directamente para permitir
    que cada vista defina su propia jerarquía de widgets.
    """

    # ── Widgets de formulario ─────────────────

    @staticmethod
    def make_label(parent, text: str, bold: bool = False, color: str = COLOR_TEXT):
        font = FONT_HEADER if bold else FONT_NORMAL
        return tk.Label(parent, text=text, font=font,
                        fg=color, bg=parent["bg"] if hasattr(parent, "__getitem__") else COLOR_BG)

    @staticmethod
    def make_entry(parent, width: int = 30, show: str = "") -> tk.Entry:
        return tk.Entry(parent, width=width, show=show,
                        font=FONT_NORMAL, relief="solid", bd=1)

    @staticmethod
    def make_combobox(parent, values: list, width: int = 28) -> ttk.Combobox:
        cb = ttk.Combobox(parent, values=values, width=width,
                          font=FONT_NORMAL, state="readonly")
        return cb

    @staticmethod
    def make_button(parent, text: str, command,
                    color: str = COLOR_SECONDARY,
                    text_color: str = COLOR_TEXT_LIGHT,
                    width: int = 14) -> tk.Button:
        return tk.Button(
            parent, text=text, command=command,
            bg=color, fg=text_color,
            font=FONT_NORMAL, relief="flat",
            padx=8, pady=4, width=width,
            cursor="hand2",
            activebackground=COLOR_PRIMARY,
            activeforeground=COLOR_TEXT_LIGHT,
        )

    @staticmethod
    def make_danger_button(parent, text: str, command, width: int = 14) -> tk.Button:
        return BaseView.make_button(parent, text, command,
                                    color=COLOR_DANGER, width=width)

    @staticmethod
    def make_success_button(parent, text: str, command, width: int = 14) -> tk.Button:
        return BaseView.make_button(parent, text, command,
                                    color=COLOR_SUCCESS, width=width)

    # ── Treeview (tabla) ──────────────────────

    @staticmethod
    def make_treeview(parent, columnas: list[str],
                      alto: int = 15) -> tuple[ttk.Treeview, tk.Scrollbar, tk.Scrollbar]:
        """
        Crea un Treeview con scrollbars vertical y horizontal.
        Retorna (tree, scroll_y, scroll_x).
        """
        frame = tk.Frame(parent, bg=COLOR_BG)
        frame.pack(fill="both", expand=True, padx=8, pady=4)

        scroll_y = ttk.Scrollbar(frame, orient="vertical")
        scroll_x = ttk.Scrollbar(frame, orient="horizontal")

        tree = ttk.Treeview(
            frame,
            columns=columnas,
            show="headings",
            height=alto,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
        )

        scroll_y.config(command=tree.yview)
        scroll_x.config(command=tree.xview)

        for col in columnas:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center", minwidth=80)

        # Colores alternados de fila
        tree.tag_configure("par",   background="#ffffff")
        tree.tag_configure("impar", background="#eef3fb")

        scroll_y.pack(side="right",  fill="y")
        scroll_x.pack(side="bottom", fill="x")
        tree.pack(fill="both", expand=True)

        return tree, scroll_y, scroll_x

    @staticmethod
    def poblar_treeview(tree: ttk.Treeview, filas: list):
        """Limpia el treeview y lo rellena con las filas dadas."""
        for item in tree.get_children():
            tree.delete(item)
        for i, fila in enumerate(filas):
            tag = "par" if i % 2 == 0 else "impar"
            tree.insert("", "end", values=fila, tags=(tag,))

    # ── Barra de estado ───────────────────────

    @staticmethod
    def make_status_bar(parent) -> tk.Label:
        """Barra de estado fija en la parte inferior."""
        lbl = tk.Label(
            parent, text="", font=FONT_SMALL,
            fg=COLOR_TEXT_LIGHT, bg=COLOR_PRIMARY,
            anchor="w", padx=10, pady=3,
        )
        lbl.pack(side="bottom", fill="x")
        return lbl

    @staticmethod
    def set_status(label: tk.Label, mensaje: str, ok: bool = True):
        label.config(
            text=mensaje,
            bg=COLOR_SUCCESS if ok else COLOR_DANGER,
        )

    # ── Diálogos ─────────────────────────────

    @staticmethod
    def msg_info(titulo: str, mensaje: str):
        messagebox.showinfo(titulo, mensaje)

    @staticmethod
    def msg_error(titulo: str, mensaje: str):
        messagebox.showerror(titulo, mensaje)

    @staticmethod
    def msg_confirm(titulo: str, mensaje: str) -> bool:
        return messagebox.askyesno(titulo, mensaje)

    @staticmethod
    def pedir_ruta_pdf(nombre_sugerido: str = "reporte.pdf") -> str:
        """Abre un diálogo para elegir dónde guardar el PDF."""
        return filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=nombre_sugerido,
            title="Guardar reporte PDF",
        )

    # ── Panel con título ──────────────────────

    @staticmethod
    def make_section_frame(parent, titulo: str) -> tk.LabelFrame:
        return tk.LabelFrame(
            parent, text=titulo,
            font=FONT_HEADER, fg=COLOR_PRIMARY,
            bg=COLOR_BG, bd=1, relief="groove",
            padx=8, pady=6,
        )

    # ── Estilos ttk globales ──────────────────

    @staticmethod
    def apply_ttk_styles():
        """Aplica estilos globales a los widgets ttk."""
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                         background="white",
                         foreground=COLOR_TEXT,
                         rowheight=24,
                         fieldbackground="white",
                         font=FONT_SMALL)
        style.configure("Treeview.Heading",
                         background=COLOR_PRIMARY,
                         foreground=COLOR_TEXT_LIGHT,
                         font=FONT_HEADER,
                         relief="flat")
        style.map("Treeview.Heading",
                  background=[("active", COLOR_SECONDARY)])
        style.map("Treeview",
                  background=[("selected", COLOR_SECONDARY)],
                  foreground=[("selected", "white")])

        style.configure("TScrollbar", background=COLOR_BG)
        style.configure("TCombobox",  font=FONT_NORMAL)