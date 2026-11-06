
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


# ---------- Modelo de dominio ----------
from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class Estudiante:
    nombre: str
    apellido: str
    legajo: str

    def __post_init__(self):
        if not self.nombre or not self.apellido:
            raise ValueError("nombre y apellido son obligatorios")
        if not self.legajo.isdigit():
            raise ValueError("legajo inválido")


class Solicitud:
    def __init__(
        self,
        id: int,
        estudiante: Estudiante,
        tipo: TipoSolicitud,
        prioridad: Prioridad,
        detalle: str,
        estado: Estado = Estado.PENDIENTE,
        responsable: str | None = None,
        fecha: datetime | None = None,
    ):
        if id <= 0:
            raise ValueError("id debe ser positivo")
        self.id = id
        self.estudiante = estudiante
        self.tipo = tipo
        self.prioridad = prioridad
        self.detalle = detalle
        self.estado = estado
        self.responsable = responsable
        self.fecha = fecha or datetime.now()

    # ---- comportamiento de negocio ----
    def cambiar_estado(self, nuevo_estado: Estado) -> None:
        self.estado = nuevo_estado

    def asignar_responsable(self, responsable: str) -> None:
        if not responsable:
            raise ValueError("responsable vacío")
        self.responsable = responsable

    # ---- búsqueda: el modelo sabe si coincide con un filtro ----
    def coincide_con(
        self,
        texto: str | None = None,
        tipo: TipoSolicitud | None = None,
        estado: Estado | None = None,
        prioridad: Prioridad | None = None,
    ) -> bool:
        if texto is not None:
            t = texto.lower()
            if not (
                t in self.estudiante.nombre.lower()
                or t in self.estudiante.apellido.lower()
                or t in self.detalle.lower()
                or t in self.estudiante.legajo
            ):
                return False
        if tipo is not None and self.tipo != tipo:
            return False
        if estado is not None and self.estado != estado:
            return False
        if prioridad is not None and self.prioridad != prioridad:
            return False
        return True

    # ---- serialización: mismo formato plano que antes ----
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.estudiante.nombre,
            "apellido": self.estudiante.apellido,
            "legajo": self.estudiante.legajo,
            "tipo": self.tipo.value,
            "prioridad": self.prioridad.value,
            "detalle": self.detalle,
            "estado": self.estado.value,
            "responsable": self.responsable,
            "fecha": self.fecha.strftime("%Y-%m-%d %H:%M"),
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Solicitud":
        estudiante = Estudiante(
            nombre=data["nombre"],
            apellido=data["apellido"],
            legajo=data["legajo"],
        )
        return cls(
            id=data["id"],
            estudiante=estudiante,
            tipo=TipoSolicitud(data["tipo"]),
            prioridad=Prioridad(data["prioridad"]),
            detalle=data["detalle"],
            estado=Estado(data["estado"]),
            responsable=data.get("responsable"),
            fecha=datetime.strptime(data["fecha"], "%Y-%m-%d %H:%M"),
        )

    def __repr__(self) -> str:
        return (
            f"Solicitud(id={self.id}, "
            f"estudiante={self.estudiante.apellido}, "
            f"tipo={self.tipo.value}, estado={self.estado.value})"
        )    