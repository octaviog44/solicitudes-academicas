# tests/test_validador.py
import pytest

from dominio import Estado, Prioridad, SolicitudRequest, TipoSolicitud
from excepciones import SolicitudInvalidaError
from validador import ValidadorSolicitud


class TestValidadorSolicitud:
    def setup_method(self):
        self.validador = ValidadorSolicitud()

    # ---------- validar() completo ----------
    def test_validar_request_valido(self, request_valido):
        tipo, prioridad = self.validador.validar(request_valido)
        assert tipo == TipoSolicitud.BECA
        assert prioridad == Prioridad.ALTA

    def test_validar_nombre_vacio(self):
        request = SolicitudRequest(
            nombre="", apellido="Pérez", legajo="123",
            tipo="beca", prioridad="alta", detalle="x",
        )
        with pytest.raises(SolicitudInvalidaError, match="nombre y apellido"):
            self.validador.validar(request)

    def test_validar_apellido_vacio(self):
        request = SolicitudRequest(
            nombre="Juan", apellido="", legajo="123",
            tipo="beca", prioridad="alta", detalle="x",
        )
        with pytest.raises(SolicitudInvalidaError, match="nombre y apellido"):
            self.validador.validar(request)

    def test_validar_legajo_vacio(self):
        request = SolicitudRequest(
            nombre="Juan", apellido="Pérez", legajo="",
            tipo="beca", prioridad="alta", detalle="x",
        )
        with pytest.raises(SolicitudInvalidaError, match="legajo inválido"):
            self.validador.validar(request)

    def test_validar_legajo_no_numerico(self):
        request = SolicitudRequest(
            nombre="Juan", apellido="Pérez", legajo="abc",
            tipo="beca", prioridad="alta", detalle="x",
        )
        with pytest.raises(SolicitudInvalidaError, match="legajo inválido"):
            self.validador.validar(request)

    def test_validar_tipo_invalido(self):
        request = SolicitudRequest(
            nombre="Juan", apellido="Pérez", legajo="123",
            tipo="xyz", prioridad="alta", detalle="x",
        )
        with pytest.raises(SolicitudInvalidaError, match="tipo inválido"):
            self.validador.validar(request)

    def test_validar_prioridad_invalida(self):
        request = SolicitudRequest(
            nombre="Juan", apellido="Pérez", legajo="123",
            tipo="beca", prioridad="xyz", detalle="x",
        )
        with pytest.raises(SolicitudInvalidaError, match="prioridad inválida"):
            self.validador.validar(request)

    # ---------- validar_estado ----------
    def test_validar_estado_valido(self):
        for valor in ["pendiente", "en_proceso", "resuelta", "rechazada"]:
            estado = self.validador.validar_estado(valor)
            assert estado == Estado(valor)

    def test_validar_estado_invalido(self):
        with pytest.raises(SolicitudInvalidaError, match="estado inválido"):
            self.validador.validar_estado("xyz")

    # ---------- validar_responsable ----------
    def test_validar_responsable_valido(self):
        # No debe lanzar excepción
        self.validador.validar_responsable("María López")

    def test_validar_responsable_vacio(self):
        with pytest.raises(SolicitudInvalidaError, match="responsable vacío"):
            self.validador.validar_responsable("")