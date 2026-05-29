# Las 4 consultas requeridas por el proyecto.
# Todos los roles pueden ejecutarlas.
#
# Cada método retorna:
#   {
#     "columnas": [...],   # nombres de columna para la tabla
#     "filas":    [...],   # lista de tuplas con los datos
#     "error":    str|None
#   }

from models.jugador_model import JugadorModel
from models.partido_model import PartidoModel
from models.equipo_model  import EquipoModel
from config.constants     import PAISES_ANFITRIONES


def _resultado(columnas: list, filas: list) -> dict:
    return {"columnas": columnas, "filas": filas, "error": None}

def _error(mensaje: str) -> dict:
    return {"columnas": [], "filas": [], "error": mensaje}


class QueryController:

    # Consulta A1
    @staticmethod
    def jugador_mas_costoso_por_confederacion() -> dict:
        """
        Determina el jugador más costoso por confederación.
        Columnas: Confederación | Jugador | Equipo | Valor (€)
        """
        try:
            filas = JugadorModel.get_jugador_mas_costoso_por_confederacion()
            return _resultado(
                ["Confederación", "Jugador", "Equipo", "Valor (€)"],
                filas
            )
        except Exception as e:
            return _error(f"Error al ejecutar consulta: {e}")

    # Consulta A2
    @staticmethod
    def partidos_por_estadio(estadio_id: int) -> dict:
        """
        Lista los partidos que se llevarán a cabo en el estadio indicado.
        Columnas: Equipo 1 | Equipo 2 | Estadio | Ciudad | País | Grupo | Fecha y Hora
        """
        if not estadio_id:
            return _error("Debe seleccionar un estadio.")
        try:
            filas = PartidoModel.get_partidos_por_estadio(estadio_id)
            if not filas:
                return _resultado(
                    ["Equipo 1", "Equipo 2", "Estadio", "Ciudad", "País", "Grupo", "Fecha y Hora"],
                    []
                )
            return _resultado(
                ["Equipo 1", "Equipo 2", "Estadio", "Ciudad", "País", "Grupo", "Fecha y Hora"],
                filas
            )
        except Exception as e:
            return _error(f"Error al ejecutar consulta: {e}")

    # Consulta A3
    @staticmethod
    def equipo_mas_costoso_por_pais(pais: str) -> dict:
        """
        Determina el equipo más costoso que juega en la fase de grupos
        del país anfitrión indicado (México, USA, Canadá).
        Columnas: Equipo | Confederación | Valor de Mercado (€) | País
        """
        if pais not in PAISES_ANFITRIONES:
            return _error(
                f"País inválido. Opciones: {', '.join(PAISES_ANFITRIONES)}."
            )
        try:
            fila = EquipoModel.get_equipo_mas_costoso_por_pais(pais)
            filas = [fila] if fila else []
            return _resultado(
                ["Equipo", "Confederación", "Valor de Mercado (€)", "País"],
                filas
            )
        except Exception as e:
            return _error(f"Error al ejecutar consulta: {e}")

    # Consulta A4 
    @staticmethod
    def cantidad_menores_por_equipo() -> dict:
        """
        Determina la cantidad de jugadores menores de 21 años por equipo.
        Columnas: Equipo | Confederación | Jugadores < 21 años
        """
        try:
            filas = JugadorModel.get_cantidad_menores_por_equipo()
            return _resultado(
                ["Equipo", "Confederación", "Jugadores < 21 años"],
                filas
            )
        except Exception as e:
            return _error(f"Error al ejecutar consulta: {e}")