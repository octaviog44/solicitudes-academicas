
from enum import Enum


class TipoSolicitud(str, Enum):
    BECA = "beca"
    CAMBIO_CARRERA = "cambio_carrera"
    REGULARIDAD = "regularidad"
    EXAMEN = "examen"
    OTRO = "otro"


class Prioridad(str, Enum):
    ALTA = "alta"
    MEDIA = "media"
    BAJA = "baja"


class Estado(str, Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    RESUELTA = "resuelta"
    RECHAZADA = "rechazada"


def parse_tipo(valor: str) -> TipoSolicitud | None:
    """Devuelve el TipoSolicitud correspondiente o None si no es válido."""
    try:
        return TipoSolicitud(valor)
    except ValueError:
        return None


def parse_prioridad(valor: str) -> Prioridad | None:
    try:
        return Prioridad(valor)
    except ValueError:
        return None


def parse_estado(valor: str) -> Estado | None:
    try:
        return Estado(valor)
    except ValueError:
        return None