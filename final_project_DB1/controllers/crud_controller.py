# Coordina las operaciones CRUD de todas las
# entidades. Valida datos antes de pasarlos
# al model correspondiente.
# Solo Admin y Tradicional pueden usarlo.

from models.confederacion_model import ConfederacionModel
from models.ciudad_model        import CiudadModel
from models.estadio_model       import EstadioModel
from models.grupo_model         import GrupoModel
from models.equipo_model        import EquipoModel
from models.jugador_model       import JugadorModel
from models.partido_model       import PartidoModel
from config.constants           import PAISES_ANFITRIONES


# Helpers internos
def _requerir(*campos) -> str | None:
    """Retorna mensaje de error si algún campo está vacío, None si todo OK."""
    for nombre, valor in campos:
        if valor is None or str(valor).strip() == "":
            return f"El campo '{nombre}' es obligatorio."
    return None

def _try(fn, *args) -> tuple[bool, str]:
    """Ejecuta fn(*args) y captura excepciones. Retorna (éxito, mensaje)."""
    try:
        fn(*args)
        return True, "Operación realizada exitosamente."
    except Exception as e:
        return False, f"Error: {e}"


# CONFEDERACIONES
class ConfederacionController:

    @staticmethod
    def listar():
        return ConfederacionModel.get_all()

    @staticmethod
    def obtener(conf_id: int):
        return ConfederacionModel.get_by_id(conf_id)

    @staticmethod
    def crear(nombre: str) -> tuple[bool, str]:
        err = _requerir(("Nombre", nombre))
        if err:
            return False, err
        return _try(ConfederacionModel.insert, nombre.strip())

    @staticmethod
    def actualizar(conf_id: int, nombre: str) -> tuple[bool, str]:
        err = _requerir(("Nombre", nombre))
        if err:
            return False, err
        return _try(ConfederacionModel.update, conf_id, nombre.strip())

    @staticmethod
    def eliminar(conf_id: int) -> tuple[bool, str]:
        return _try(ConfederacionModel.delete, conf_id)


# CIUDADES
class CiudadController:

    @staticmethod
    def listar():
        return CiudadModel.get_all()

    @staticmethod
    def obtener(ciudad_id: int):
        return CiudadModel.get_by_id(ciudad_id)

    @staticmethod
    def crear(nombre: str, pais: str) -> tuple[bool, str]:
        err = _requerir(("Nombre", nombre), ("País", pais))
        if err:
            return False, err
        if pais not in PAISES_ANFITRIONES:
            return False, f"País inválido. Opciones: {', '.join(PAISES_ANFITRIONES)}."
        return _try(CiudadModel.insert, nombre.strip(), pais)

    @staticmethod
    def actualizar(ciudad_id: int, nombre: str, pais: str) -> tuple[bool, str]:
        err = _requerir(("Nombre", nombre), ("País", pais))
        if err:
            return False, err
        if pais not in PAISES_ANFITRIONES:
            return False, f"País inválido. Opciones: {', '.join(PAISES_ANFITRIONES)}."
        return _try(CiudadModel.update, ciudad_id, nombre.strip(), pais)

    @staticmethod
    def eliminar(ciudad_id: int) -> tuple[bool, str]:
        return _try(CiudadModel.delete, ciudad_id)


# ESTADIOS
class EstadioController:

    @staticmethod
    def listar():
        return EstadioModel.get_all()

    @staticmethod
    def obtener(estadio_id: int):
        return EstadioModel.get_by_id(estadio_id)

    @staticmethod
    def listar_para_combo():
        return EstadioModel.get_nombres_para_combo()

    @staticmethod
    def crear(nombre: str, capacidad, id_ciudad) -> tuple[bool, str]:
        err = _requerir(("Nombre", nombre), ("Capacidad", capacidad), ("Ciudad", id_ciudad))
        if err:
            return False, err
        try:
            cap = int(capacidad)
            if cap <= 0:
                return False, "La capacidad debe ser un número positivo."
        except ValueError:
            return False, "La capacidad debe ser un número entero."
        return _try(EstadioModel.insert, nombre.strip(), cap, int(id_ciudad))

    @staticmethod
    def actualizar(estadio_id: int, nombre: str,
                   capacidad, id_ciudad) -> tuple[bool, str]:
        err = _requerir(("Nombre", nombre), ("Capacidad", capacidad), ("Ciudad", id_ciudad))
        if err:
            return False, err
        try:
            cap = int(capacidad)
        except ValueError:
            return False, "La capacidad debe ser un número entero."
        return _try(EstadioModel.update, estadio_id, nombre.strip(), cap, int(id_ciudad))

    @staticmethod
    def eliminar(estadio_id: int) -> tuple[bool, str]:
        return _try(EstadioModel.delete, estadio_id)


# GRUPOS
class GrupoController:

    @staticmethod
    def listar():
        return GrupoModel.get_all()

    @staticmethod
    def listar_para_combo():
        return GrupoModel.get_nombres_para_combo()

    @staticmethod
    def crear(letra: str) -> tuple[bool, str]:
        err = _requerir(("Letra/Nombre", letra))
        if err:
            return False, err
        return _try(GrupoModel.insert, letra.strip().upper())

    @staticmethod
    def actualizar(grupo_id: int, letra: str) -> tuple[bool, str]:
        err = _requerir(("Letra/Nombre", letra))
        if err:
            return False, err
        return _try(GrupoModel.update, grupo_id, letra.strip().upper())

    @staticmethod
    def eliminar(grupo_id: int) -> tuple[bool, str]:
        return _try(GrupoModel.delete, grupo_id)


# EQUIPOS
class EquipoController:

    @staticmethod
    def listar():
        return EquipoModel.get_all()

    @staticmethod
    def obtener(equipo_id: int):
        return EquipoModel.get_by_id(equipo_id)

    @staticmethod
    def listar_para_combo():
        return EquipoModel.get_nombres_para_combo()

    @staticmethod
    def crear(nombre: str, id_confederacion,
              id_dt, valor_mercado) -> tuple[bool, str]:
        err = _requerir(
            ("Nombre", nombre),
            ("Confederación", id_confederacion),
            ("DT", id_dt),
            ("Valor de mercado", valor_mercado),
        )
        if err:
            return False, err
        try:
            valor = float(valor_mercado)
            if valor < 0:
                return False, "El valor de mercado no puede ser negativo."
        except ValueError:
            return False, "El valor de mercado debe ser un número."
        return _try(
            EquipoModel.insert,
            nombre.strip(), int(id_confederacion), int(id_dt), valor
        )

    @staticmethod
    def actualizar(equipo_id: int, nombre: str, id_confederacion,
                   id_dt, valor_mercado) -> tuple[bool, str]:
        err = _requerir(
            ("Nombre", nombre),
            ("Confederación", id_confederacion),
            ("DT", id_dt),
            ("Valor de mercado", valor_mercado),
        )
        if err:
            return False, err
        try:
            valor = float(valor_mercado)
        except ValueError:
            return False, "El valor de mercado debe ser un número."
        return _try(
            EquipoModel.update,
            equipo_id, nombre.strip(), int(id_confederacion), int(id_dt), valor
        )

    @staticmethod
    def eliminar(equipo_id: int) -> tuple[bool, str]:
        return _try(EquipoModel.delete, equipo_id)


# JUGADORES
class JugadorController:

    @staticmethod
    def listar():
        return JugadorModel.get_all()

    @staticmethod
    def obtener(jugador_id: int):
        return JugadorModel.get_by_id(jugador_id)

    @staticmethod
    def _validar_campos(nombre, edad, peso, estatura, valor, id_equipo):
        err = _requerir(
            ("Nombre", nombre), ("Edad", edad), ("Peso", peso),
            ("Estatura", estatura), ("Valor", valor), ("Equipo", id_equipo),
        )
        if err:
            return None, None, None, None, None, err
        try:
            e = int(edad)
            p = float(peso)
            s = float(estatura)
            v = float(valor)
            if e <= 0 or p <= 0 or s <= 0 or v < 0:
                return None, None, None, None, None, "Edad, peso y estatura deben ser positivos."
        except ValueError:
            return None, None, None, None, None, "Edad, peso, estatura y valor deben ser numéricos."
        return e, p, s, v, None, None

    @staticmethod
    def crear(nombre: str, edad, peso, estatura,
              valor, id_equipo) -> tuple[bool, str]:
        e, p, s, v, _, err = JugadorController._validar_campos(
            nombre, edad, peso, estatura, valor, id_equipo)
        if err:
            return False, err
        return _try(JugadorModel.insert, nombre.strip(), e, p, s, v, int(id_equipo))

    @staticmethod
    def actualizar(jugador_id: int, nombre: str, edad, peso,
                   estatura, valor, id_equipo) -> tuple[bool, str]:
        e, p, s, v, _, err = JugadorController._validar_campos(
            nombre, edad, peso, estatura, valor, id_equipo)
        if err:
            return False, err
        return _try(JugadorModel.update, jugador_id, nombre.strip(), e, p, s, v, int(id_equipo))

    @staticmethod
    def eliminar(jugador_id: int) -> tuple[bool, str]:
        return _try(JugadorModel.delete, jugador_id)


# PARTIDOS
class PartidoController:

    @staticmethod
    def listar():
        return PartidoModel.get_all()

    @staticmethod
    def obtener(partido_id: int):
        return PartidoModel.get_by_id(partido_id)

    @staticmethod
    def crear(id_equipo1, id_equipo2, id_estadio,
              id_grupo, fecha_hora) -> tuple[bool, str]:
        err = _requerir(
            ("Equipo 1", id_equipo1), ("Equipo 2", id_equipo2),
            ("Estadio", id_estadio), ("Grupo", id_grupo),
            ("Fecha y hora", fecha_hora),
        )
        if err:
            return False, err
        if int(id_equipo1) == int(id_equipo2):
            return False, "Un equipo no puede jugar contra sí mismo."
        return _try(
            PartidoModel.insert,
            int(id_equipo1), int(id_equipo2),
            int(id_estadio), int(id_grupo), fecha_hora
        )

    @staticmethod
    def actualizar(partido_id: int, id_equipo1, id_equipo2,
                   id_estadio, id_grupo, fecha_hora) -> tuple[bool, str]:
        err = _requerir(
            ("Equipo 1", id_equipo1), ("Equipo 2", id_equipo2),
            ("Estadio", id_estadio), ("Grupo", id_grupo),
            ("Fecha y hora", fecha_hora),
        )
        if err:
            return False, err
        if int(id_equipo1) == int(id_equipo2):
            return False, "Un equipo no puede jugar contra sí mismo."
        return _try(
            PartidoModel.update,
            partido_id, int(id_equipo1), int(id_equipo2),
            int(id_estadio), int(id_grupo), fecha_hora
        )

    @staticmethod
    def eliminar(partido_id: int) -> tuple[bool, str]:
        return _try(PartidoModel.delete, partido_id)