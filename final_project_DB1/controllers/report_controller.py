# Genera los 4 reportes PDF requeridos.
# Usa utils/pdf_generator.py como motor de
# renderizado (ReportLab).
# Cada método retorna (éxito: bool, msg: str).
# msg contiene la ruta del PDF generado o el
# mensaje de error.

from models.bitacora_model import BitacoraModel
from models.jugador_model  import JugadorModel
from models.equipo_model   import EquipoModel
from models.partido_model  import PartidoModel
from models.confederacion_model import ConfederacionModel
from config.constants      import PAISES_ANFITRIONES
from utils.pdf_generator   import PDFGenerator


class ReportController:

    # Reporte B1 
    @staticmethod
    def reporte_bitacora(fecha_inicio: str, fecha_fin: str,
                         ruta_salida: str) -> tuple[bool, str]:
        """
        Lista usuarios que ingresaron y salieron en un rango de fechas.
        fecha_inicio / fecha_fin: strings 'YYYY-MM-DD'.
        """
        if not fecha_inicio or not fecha_fin:
            return False, "Debe especificar fecha de inicio y fin."
        if fecha_inicio > fecha_fin:
            return False, "La fecha de inicio no puede ser posterior a la de fin."
        try:
            filas = BitacoraModel.get_por_fecha(fecha_inicio, fecha_fin)
            columnas = ["Usuario", "Rol", "Fecha ingreso", "Fecha salida"]
            titulo   = f"Bitácora de accesos  {fecha_inicio} → {fecha_fin}"
            PDFGenerator.generar_tabla(titulo, columnas, filas, ruta_salida)
            return True, ruta_salida
        except Exception as e:
            return False, f"Error al generar reporte: {e}"

    # Reporte B2 
    @staticmethod
    def reporte_jugadores_por_medidas(peso_min: float, peso_max: float,
                                      estatura_min: float, estatura_max: float,
                                      ruta_salida: str) -> tuple[bool, str]:
        """
        Lista jugadores cuyo peso y estatura están dentro del rango indicado.
        """
        try:
            pm_in  = float(peso_min)
            pm_ax  = float(peso_max)
            em_in  = float(estatura_min)
            em_ax  = float(estatura_max)
        except (ValueError, TypeError):
            return False, "Los valores de peso y estatura deben ser numéricos."

        if pm_in > pm_ax or em_in > em_ax:
            return False, "El valor mínimo no puede ser mayor al máximo."

        try:
            filas    = JugadorModel.get_jugadores_por_peso_estatura(pm_in, pm_ax, em_in, em_ax)
            columnas = ["Jugador", "Edad", "Peso (kg)", "Estatura (m)", "Valor (€)", "Equipo"]
            titulo   = (
                f"Jugadores  |  Peso: {pm_in}–{pm_ax} kg  "
                f"|  Estatura: {em_in}–{em_ax} m"
            )
            PDFGenerator.generar_tabla(titulo, columnas, filas, ruta_salida)
            return True, ruta_salida
        except Exception as e:
            return False, f"Error al generar reporte: {e}"

    # Reporte B3 
    @staticmethod
    def reporte_valor_total_por_confederacion(id_confederacion: int,
                                              ruta_salida: str) -> tuple[bool, str]:
        """
        Determina el valor total de jugadores por equipo dentro de
        una confederación específica.
        """
        if not id_confederacion:
            return False, "Debe seleccionar una confederación."
        try:
            conf     = ConfederacionModel.get_by_id(id_confederacion)
            nombre_conf = conf[1] if conf else str(id_confederacion)
            filas    = EquipoModel.get_valor_total_por_confederacion(id_confederacion)
            columnas = ["Equipo", "Valor total jugadores (€)"]
            titulo   = f"Valor total de jugadores por equipo  —  {nombre_conf}"
            PDFGenerator.generar_tabla(titulo, columnas, filas, ruta_salida)
            return True, ruta_salida
        except Exception as e:
            return False, f"Error al generar reporte: {e}"

    # Reporte B4 
    @staticmethod
    def reporte_paises_por_anfitrion(pais_anfitrion: str,
                                     ruta_salida: str) -> tuple[bool, str]:
        """
        Lista los equipos (países) que jugarán en el país anfitrión indicado.
        """
        if pais_anfitrion not in PAISES_ANFITRIONES:
            return False, f"País inválido. Opciones: {', '.join(PAISES_ANFITRIONES)}."
        try:
            filas    = PartidoModel.get_paises_por_anfitrion(pais_anfitrion)
            columnas = ["Equipo", "Confederación", "Estadio", "Ciudad", "País anfitrión"]
            titulo   = f"Equipos que juegan en {pais_anfitrion}"
            PDFGenerator.generar_tabla(titulo, columnas, filas, ruta_salida)
            return True, ruta_salida
        except Exception as e:
            return False, f"Error al generar reporte: {e}"