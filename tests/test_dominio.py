
import pytest

from dominio import Estado, Estudiante, Prioridad, Solicitud, TipoSolicitud
from excepciones import SolicitudInvalidaError


class TestEstudiante:
    def test_creacion_valida(self):
        e = Estudiante(nombre="Ana", apellido="Gómez", legajo="999")
        assert e.nombre == "Ana"
        assert e.apellido == "Gómez"
        assert e.legajo == "999"

    def test_nombre_vacio_lanza_error(self):
        with pytest.raises(SolicitudInvalidaError, match="nombre y apellido"):
            Estudiante(nombre="", apellido="Gómez", legajo="999")

    def test_apellido_vacio_lanza_error(self):
        with pytest.raises(SolicitudInvalidaError, match="nombre y apellido"):
            Estudiante(nombre="Ana", apellido="", legajo="999")

    def test_legajo_no_numerico_lanza_error(self):
        with pytest.raises(SolicitudInvalidaError, match="legajo inválido"):
            Estudiante(nombre="Ana", apellido="Gómez", legajo="abc")


class TestSolicitud:
    def test_creacion_valida(self, solicitud_valida):
        s = solicitud_valida
        assert s.id == 1
        assert s.estado == Estado.PENDIENTE
        assert s.responsable is None
        assert s.tipo == TipoSolicitud.BECA
        assert s.prioridad == Prioridad.ALTA

    def test_id_no_positivo_lanza_error(self, estudiante_valido):
        with pytest.raises(SolicitudInvalidaError, match="id debe ser positivo"):
            Solicitud(
                id=0,
                estudiante=estudiante_valido,
                tipo=TipoSolicitud.BECA,
                prioridad=Prioridad.ALTA,
                detalle="test",
            )

    def test_cambiar_estado(self, solicitud_valida):
        solicitud_valida.cambiar_estado(Estado.EN_PROCESO)
        assert solicitud_valida.estado == Estado.EN_PROCESO

    def test_asignar_responsable(self, solicitud_valida):
        solicitud_valida.asignar_responsable("María López")
        assert solicitud_valida.responsable == "María López"

    def test_asignar_responsable_vacio_lanza_error(self, solicitud_valida):
        with pytest.raises(SolicitudInvalidaError, match="responsable vacío"):
            solicitud_valida.asignar_responsable("")

    def test_coincide_con_texto(self, solicitud_valida):
        assert solicitud_valida.coincide_con(texto="juan")
        assert solicitud_valida.coincide_con(texto="PÉREZ")
        assert solicitud_valida.coincide_con(texto="beca")
        assert not solicitud_valida.coincide_con(texto="xyz")

    def test_coincide_con_tipo(self, solicitud_valida):
        assert solicitud_valida.coincide_con(tipo=TipoSolicitud.BECA)
        assert not solicitud_valida.coincide_con(tipo=TipoSolicitud.EXAMEN)

    def test_coincide_con_estado(self, solicitud_valida):
        assert solicitud_valida.coincide_con(estado=Estado.PENDIENTE)
        assert not solicitud_valida.coincide_con(estado=Estado.RESUELTA)

    def test_coincide_con_prioridad(self, solicitud_valida):
        assert solicitud_valida.coincide_con(prioridad=Prioridad.ALTA)
        assert not solicitud_valida.coincide_con(prioridad=Prioridad.BAJA)

    def test_to_dict_formato(self, solicitud_valida):
        d = solicitud_valida.to_dict()
        assert d["id"] == 1
        assert d["nombre"] == "Juan"
        assert d["apellido"] == "Pérez"
        assert d["legajo"] == "12345"
        assert d["tipo"] == "beca"
        assert d["prioridad"] == "alta"
        assert d["estado"] == "pendiente"
        assert d["responsable"] is None
        assert "fecha" in d

    def test_from_dict_roundtrip(self, solicitud_valida):
        d = solicitud_valida.to_dict()
        recuperada = Solicitud.from_dict(d)
        assert recuperada.id == solicitud_valida.id
        assert recuperada.estudiante.nombre == solicitud_valida.estudiante.nombre
        assert recuperada.tipo == solicitud_valida.tipo
        assert recuperada.prioridad == solicitud_valida.prioridad
        assert recuperada.estado == solicitud_valida.estado