import pytest

from dominio import Estado, Prioridad, SolicitudRequest, TipoSolicitud
from excepciones import SolicitudInvalidaError, SolicitudNoEncontradaError
from gestor import GestorSolicitudes
from repositorio import RepositorioMemoria


def _request(**overrides) -> SolicitudRequest:
    base = dict(
        nombre="Juan",
        apellido="Pérez",
        legajo="12345",
        tipo="beca",
        prioridad="alta",
        detalle="Solicitud de beca completa",
    )
    base.update(overrides)
    return SolicitudRequest(**base)


class TestGestorRegistro:
    def test_registrar_solicitud_valida(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        solicitud = g.registrar_solicitud(_request())

        assert solicitud.id == 1
        assert solicitud.estado == Estado.PENDIENTE
        assert solicitud.tipo == TipoSolicitud.BECA
        assert solicitud.prioridad == Prioridad.ALTA
        assert solicitud.responsable is None

    def test_registrar_incrementa_contador(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        s1 = g.registrar_solicitud(_request(legajo="111"))
        s2 = g.registrar_solicitud(_request(legajo="222"))
        assert s1.id == 1
        assert s2.id == 2

    def test_registrar_nombre_vacio_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        with pytest.raises(SolicitudInvalidaError, match="nombre y apellido"):
            g.registrar_solicitud(_request(nombre=""))

    def test_registrar_legajo_invalido_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        with pytest.raises(SolicitudInvalidaError, match="legajo inválido"):
            g.registrar_solicitud(_request(legajo="abc"))

    def test_registrar_tipo_invalido_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        with pytest.raises(SolicitudInvalidaError, match="tipo inválido"):
            g.registrar_solicitud(_request(tipo="xyz"))

    def test_registrar_prioridad_invalida_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        with pytest.raises(SolicitudInvalidaError, match="prioridad inválida"):
            g.registrar_solicitud(_request(prioridad="xyz"))

    def test_registrar_persiste_en_repositorio(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())

        # Reconstruir un nuevo gestor con el mismo repo: debe ver la solicitud
        g2 = GestorSolicitudes(repo_memoria)
        assert len(g2.listar()) == 1
        assert g2.listar()[0].id == 1


class TestGestorCambioEstado:
    def test_cambiar_estado_valido(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())

        actualizada = g.cambiar_estado(1, "en_proceso")
        assert actualizada.estado == Estado.EN_PROCESO

    def test_cambiar_estado_invalido_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())
        with pytest.raises(SolicitudInvalidaError, match="estado inválido"):
            g.cambiar_estado(1, "xyz")

    def test_cambiar_estado_id_inexistente_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())
        with pytest.raises(SolicitudNoEncontradaError, match="solicitud no encontrada"):
            g.cambiar_estado(999, "resuelta")


class TestGestorResponsable:
    def test_asignar_responsable_valido(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())

        actualizada = g.asignar_responsable(1, "María López")
        assert actualizada.responsable == "María López"

    def test_asignar_responsable_vacio_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())
        with pytest.raises(SolicitudInvalidaError, match="responsable vacío"):
            g.asignar_responsable(1, "")

    def test_asignar_responsable_id_inexistente_lanza_error(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())
        with pytest.raises(SolicitudNoEncontradaError, match="solicitud no encontrada"):
            g.asignar_responsable(999, "María")


class TestGestorBusqueda:
    def _gestor_con_datos(self):
        repo = RepositorioMemoria()
        g = GestorSolicitudes(repo)
        g.registrar_solicitud(_request(nombre="Juan", apellido="Pérez", legajo="111",
                                        tipo="beca", prioridad="alta", detalle="beca completa"))
        g.registrar_solicitud(_request(nombre="Ana", apellido="Gómez", legajo="222",
                                        tipo="examen", prioridad="media", detalle="examen final"))
        g.registrar_solicitud(_request(nombre="Pedro", apellido="López", legajo="333",
                                        tipo="regularidad", prioridad="baja", detalle="regularidad"))
        return g

    def test_buscar_sin_filtros_devuelve_todo(self):
        g = self._gestor_con_datos()
        assert len(g.buscar()) == 3

    def test_buscar_por_texto(self):
        g = self._gestor_con_datos()
        resultado = g.buscar(texto="ana")
        assert len(resultado) == 1
        assert resultado[0].estudiante.nombre == "Ana"

    def test_buscar_por_texto_sin_resultados(self):
        g = self._gestor_con_datos()
        assert g.buscar(texto="zzz") == []

    def test_buscar_por_tipo(self):
        g = self._gestor_con_datos()
        resultado = g.buscar(tipo="examen")
        assert len(resultado) == 1
        assert resultado[0].tipo == TipoSolicitud.EXAMEN

    def test_buscar_por_estado(self):
        g = self._gestor_con_datos()
        # Todos arrancan pendientes
        assert len(g.buscar(estado="pendiente")) == 3

    def test_buscar_por_prioridad(self):
        g = self._gestor_con_datos()
        resultado = g.buscar(prioridad="alta")
        assert len(resultado) == 1

    def test_buscar_filtro_invalido_devuelve_vacio(self):
        g = self._gestor_con_datos()
        assert g.buscar(tipo="xyz") == []
        assert g.buscar(estado="xyz") == []
        assert g.buscar(prioridad="xyz") == []


class TestGestorListadoYReporte:
    def test_listar_vacio(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        assert g.listar() == []

    def test_listar_con_solicitudes(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request(legajo="111"))
        g.registrar_solicitud(_request(legajo="222"))
        assert len(g.listar()) == 2

    def test_reporte_vacio(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        reporte = g.reporte()
        assert reporte["total"] == 0
        assert reporte["por_estado"] == {}
        assert reporte["por_tipo"] == {}
        assert reporte["por_prioridad"] == {}

    def test_reporte_con_datos(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request(legajo="111", tipo="beca", prioridad="alta"))
        g.registrar_solicitud(_request(legajo="222", tipo="beca", prioridad="media"))
        g.registrar_solicitud(_request(legajo="333", tipo="examen", prioridad="alta"))

        reporte = g.reporte()
        assert reporte["total"] == 3
        assert reporte["por_tipo"]["beca"] == 2
        assert reporte["por_tipo"]["examen"] == 1
        assert reporte["por_prioridad"]["alta"] == 2
        assert reporte["por_prioridad"]["media"] == 1
        assert reporte["por_estado"]["pendiente"] == 3

    def test_reporte_refleja_cambios_de_estado(self, repo_memoria):
        g = GestorSolicitudes(repo_memoria)
        g.registrar_solicitud(_request())
        g.cambiar_estado(1, "resuelta")
        reporte = g.reporte()
        assert reporte["por_estado"]["resuelta"] == 1
        assert reporte["por_estado"].get("pendiente", 0) == 0