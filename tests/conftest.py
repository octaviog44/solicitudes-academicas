
import pytest

from dominio import Estado, Estudiante, Prioridad, Solicitud, SolicitudRequest, TipoSolicitud
from repositorio import RepositorioMemoria


@pytest.fixture
def estudiante_valido():
    return Estudiante(nombre="Juan", apellido="Pérez", legajo="12345")


@pytest.fixture
def solicitud_valida(estudiante_valido):
    return Solicitud(
        id=1,
        estudiante=estudiante_valido,
        tipo=TipoSolicitud.BECA,
        prioridad=Prioridad.ALTA,
        detalle="Solicitud de beca completa",
    )


@pytest.fixture
def request_valido():
    return SolicitudRequest(
        nombre="Juan",
        apellido="Pérez",
        legajo="12345",
        tipo="beca",
        prioridad="alta",
        detalle="Solicitud de beca completa",
    )


@pytest.fixture
def repo_memoria():
    return RepositorioMemoria()