import json

from dominio import Estado, Prioridad, SolicitudRequest, TipoSolicitud
from gestor import GestorSolicitudes
from repositorio import RepositorioJSON


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


class TestFlujoCompletoConPersistencia:
    def test_flujo_completo_persistente(self, tmp_path):
        """Simula el uso real: registrar, cambiar estado, asignar, buscar,
        reportar, y reconstruir el gestor sobre el mismo archivo."""
        ruta = str(tmp_path / "solicitudes.json")

        # --- Sesión 1: cargar datos ---
        repo1 = RepositorioJSON(ruta)
        g1 = GestorSolicitudes(repo1)

        s1 = g1.registrar_solicitud(_request(nombre="Juan", apellido="Pérez", legajo="111"))
        s2 = g1.registrar_solicitud(_request(nombre="Ana", apellido="Gómez", legajo="222",
                                             tipo="examen", prioridad="media"))
        s3 = g1.registrar_solicitud(_request(nombre="Pedro", apellido="López", legajo="333",
                                             tipo="regularidad", prioridad="baja"))

        assert s1.id == 1
        assert s2.id == 2
        assert s3.id == 3

        # Cambiar estado y asignar responsable
        g1.cambiar_estado(1, "en_proceso")
        g1.asignar_responsable(1, "María López")

        # --- Sesión 2: reconstruir el gestor sobre el mismo archivo ---
        repo2 = RepositorioJSON(ruta)
        g2 = GestorSolicitudes(repo2)

        solicitudes = g2.listar()
        assert len(solicitudes) == 3

        # Verificar que los datos se recuperaron intactos
        recuperada = solicitudes[0]
        assert recuperada.id == 1
        assert recuperada.estudiante.nombre == "Juan"
        assert recuperada.estudiante.apellido == "Pérez"
        assert recuperada.estudiante.legajo == "111"
        assert recuperada.tipo == TipoSolicitud.BECA
        assert recuperada.prioridad == Prioridad.ALTA
        assert recuperada.estado == Estado.EN_PROCESO
        assert recuperada.responsable == "María López"

        # --- Búsqueda sobre los datos recuperados ---
        assert len(g2.buscar(texto="ana")) == 1
        assert len(g2.buscar(tipo="examen")) == 1
        assert len(g2.buscar(estado="en_proceso")) == 1
        assert len(g2.buscar(prioridad="baja")) == 1

        # --- Reporte sobre los datos recuperados ---
        reporte = g2.reporte()
        assert reporte["total"] == 3
        assert reporte["por_tipo"]["beca"] == 1
        assert reporte["por_tipo"]["examen"] == 1
        assert reporte["por_tipo"]["regularidad"] == 1
        assert reporte["por_estado"]["en_proceso"] == 1
        assert reporte["por_estado"]["pendiente"] == 2

    def test_contador_persiste_entre_sesiones(self, tmp_path):
        """El contador de IDs no se reinicia al reabrir el archivo."""
        ruta = str(tmp_path / "solicitudes.json")

        repo1 = RepositorioJSON(ruta)
        g1 = GestorSolicitudes(repo1)
        g1.registrar_solicitud(_request(legajo="111"))
        g1.registrar_solicitud(_request(legajo="222"))
        assert g1.listar()[-1].id == 2

        # Nueva sesión
        repo2 = RepositorioJSON(ruta)
        g2 = GestorSolicitudes(repo2)
        s3 = g2.registrar_solicitud(_request(legajo="333"))
        assert s3.id == 3  # continúa desde 3, no desde 1

    def test_formato_json_compatible_con_version_inicial(self, tmp_path):
        """El JSON debe tener el mismo formato plano que la versión inicial."""
        ruta = str(tmp_path / "solicitudes.json")
        repo = RepositorioJSON(ruta)
        g = GestorSolicitudes(repo)
        g.registrar_solicitud(_request())

        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Estructura raíz
        assert "solicitudes" in data
        assert "contador" in data
        assert data["contador"] == 2  # se incrementó tras registrar

        # Estructura de una solicitud
        s = data["solicitudes"][0]
        assert s["id"] == 1
        assert s["nombre"] == "Juan"
        assert s["apellido"] == "Pérez"
        assert s["legajo"] == "12345"
        assert s["tipo"] == "beca"
        assert s["prioridad"] == "alta"
        assert s["detalle"] == "Solicitud de beca completa"
        assert s["estado"] == "pendiente"
        assert s["responsable"] is None
        assert "fecha" in s

        # Verificar que los campos que antes eran strings siguen siéndolo
        assert isinstance(s["tipo"], str)
        assert isinstance(s["prioridad"], str)
        assert isinstance(s["estado"], str)
        assert isinstance(s["id"], int)