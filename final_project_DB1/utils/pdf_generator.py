# Genera PDFs de tabla usando ReportLab.
# Todos los reportes del proyecto pasan por
# PDFGenerator.generar_tabla(...)

from reportlab.lib.pagesizes   import A4, landscape
from reportlab.lib             import colors
from reportlab.lib.styles      import getSampleStyleSheet
from reportlab.lib.units       import cm
from reportlab.platypus        import (
    SimpleDocTemplate, Table, TableStyle,
    Paragraph, Spacer
)
from reportlab.lib.enums       import TA_CENTER
from datetime                  import datetime


# Paleta de colores del proyecto
_AZUL_OSCURO = colors.HexColor("#1a3a5c")
_AZUL_MEDIO  = colors.HexColor("#2e6da4")
_AZUL_CLARO  = colors.HexColor("#dce9f5")
_GRIS_FILA   = colors.HexColor("#f5f5f5")


class PDFGenerator:

    @staticmethod
    def generar_tabla(titulo: str, columnas: list[str],
                      filas: list[tuple], ruta_salida: str,
                      orientacion: str = "auto") -> None:
        """
        Genera un PDF con una tabla de datos.

        Parámetros:
            titulo       – Título que aparece en la cabecera del PDF.
            columnas     – Lista de nombres de columna.
            filas        – Lista de tuplas con los datos.
            ruta_salida  – Ruta completa donde guardar el .pdf.
            orientacion  – 'portrait', 'landscape' o 'auto'
                           (auto elige landscape si hay más de 5 columnas).
        """
        # Elegir orientación
        if orientacion == "auto":
            page_size = landscape(A4) if len(columnas) > 5 else A4
        elif orientacion == "landscape":
            page_size = landscape(A4)
        else:
            page_size = A4

        doc = SimpleDocTemplate(
            ruta_salida,
            pagesize=page_size,
            leftMargin=1.5 * cm,
            rightMargin=1.5 * cm,
            topMargin=2 * cm,
            bottomMargin=1.5 * cm,
        )

        styles  = getSampleStyleSheet()
        story   = []

        # Encabezado
        style_titulo = styles["Heading1"].clone("titulo_pdf")
        style_titulo.textColor  = _AZUL_OSCURO
        style_titulo.alignment  = TA_CENTER
        style_titulo.fontSize   = 14
        style_titulo.spaceAfter = 4

        style_sub = styles["Normal"].clone("subtitulo_pdf")
        style_sub.textColor  = colors.grey
        style_sub.alignment  = TA_CENTER
        style_sub.fontSize   = 9

        story.append(Paragraph(titulo, style_titulo))
        story.append(Paragraph(
            f"Generado: {datetime.now().strftime('%d/%m/%Y  %H:%M:%S')}",
            style_sub
        ))
        story.append(Spacer(1, 0.4 * cm))

        # Datos de la tabla
        # Convertir todos los valores a string para ReportLab
        datos = [columnas]
        for fila in filas:
            datos.append([str(v) if v is not None else "—" for v in fila])

        if len(datos) == 1:
            # Sin filas: mostrar mensaje
            story.append(Paragraph(
                "No se encontraron registros para los filtros aplicados.",
                styles["Normal"]
            ))
        else:
            # Calcular ancho disponible y distribuir columnas
            page_w = page_size[0] - 3 * cm   # margen izq + der
            n_cols = len(columnas)
            col_w  = [page_w / n_cols] * n_cols

            tabla = Table(datos, colWidths=col_w, repeatRows=1)

            # Estilo de la tabla
            estilo = TableStyle([
                # Cabecera
                ("BACKGROUND",    (0, 0), (-1, 0), _AZUL_OSCURO),
                ("TEXTCOLOR",     (0, 0), (-1, 0), colors.white),
                ("FONTNAME",      (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE",      (0, 0), (-1, 0), 9),
                ("ALIGN",         (0, 0), (-1, 0), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
                ("TOPPADDING",    (0, 0), (-1, 0), 6),
                # Filas de datos
                ("FONTNAME",  (0, 1), (-1, -1), "Helvetica"),
                ("FONTSIZE",  (0, 1), (-1, -1), 8),
                ("ALIGN",     (0, 1), (-1, -1), "CENTER"),
                ("VALIGN",    (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING",    (0, 1), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 4),
                # Filas alternadas
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, _GRIS_FILA]),
                # Bordes
                ("GRID",      (0, 0), (-1, -1), 0.4, colors.HexColor("#cccccc")),
                ("LINEBELOW", (0, 0), (-1, 0),  1.0, _AZUL_MEDIO),
            ])
            tabla.setStyle(estilo)
            story.append(tabla)

        # Pie de página (número de registros) ─
        story.append(Spacer(1, 0.3 * cm))
        n_registros = len(filas)
        story.append(Paragraph(
            f"Total de registros: {n_registros}",
            style_sub
        ))

        doc.build(story)