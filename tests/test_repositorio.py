import json

import pytest

from dominio import Estado, Estudiante, Prioridad, Solicitud, TipoSolicitud
from repositorio import RepositorioJSON, RepositorioMemoria


def _crear_solicitud(id_: int, legajo: str = "12345") -> Solicitud:
    return Solicitud(
        id=id_,
        estudiante=Estudiante(nombre="Juan", apellido="Pérez", legajo=legajo),
        tipo=TipoSolicitud.BECA,
        prioridad=Prioridad.ALTA,
        detalle="Solicitud de prueba",
    )


class TestRepositorioJSON:
    def test_cargar_archivo_inexistente(self, tmp_path):
        repo = RepositorioJSON(str(tmp_path / "no_existe.json"))
        solicitudes, contador = repo.cargar()
        assert solicitudes == []
        assert contador == 1

    def test_guardar_y_cargar_roundtrip(self, tmp_path):
        ruta = str(tmp_path / "solicitudes.json")
        repo = RepositorioJSON(ruta)

        s1 = _crear_solicitud(1, "111")
        s2 = _crear_solicitud(2, "222")
        repo.guardar([s1, s2], contador=3)

        solicitudes, contador = repo.cargar()
        assert contador == 3
        assert len(solicitudes) == 2
        assert solicitudes[0].id == 1
        assert solicitudes[1].id == 2
        assert solicitudes[0].estudiante.legajo == "111"
        assert solicitudes[0].tipo == TipoSolicitud.BECA
        assert solicitudes[0].estado == Estado.PENDIENTE

    def test_guardar_crea_directorio(self, tmp_path):
        ruta = str(tmp_path / "subdir" / "solicitudes.json")
        repo = RepositorioJSON(ruta)
        repo.guardar([_crear_solicitud(1)], contador=2)
        assert (tmp_path / "subdir" / "solicitudes.json").exists()

    def test_cargar_archivo_corrupto(self, tmp_path):
        ruta = tmp_path / "corrupto.json"
        ruta.write_text("{esto no es json válido", encoding="utf-8")
        repo = RepositorioJSON(str(ruta))
        solicitudes, contador = repo.cargar()
        assert solicitudes == []
        assert contador == 1

    def test_formato_json_plano(self, tmp_path):
        """El JSON debe mantener el formato plano (strings, sin objetos anidados)."""
        ruta = str(tmp_path / "solicitudes.json")
        repo = RepositorioJSON(ruta)
        repo.guardar([_crear_solicitud(1)], contador=2)

        with open(ruta, "r", encoding="utf-8") as f:
            data = json.load(f)

        assert "solicitudes" in data
        assert "contador" in data
        s = data["solicitudes"][0]
        assert s["nombre"] == "Juan"
        assert s["apellido"] == "Pérez"
        assert s["legajo"] == "12345"
        assert s["tipo"] == "beca"           # string, no enum
        assert s["prioridad"] == "alta"      # string, no enum
        assert s["estado"] == "pendiente"    # string, no enum
        assert isinstance(s["id"], int)


class TestRepositorioMemoria:
    def test_cargar_vacio(self):
        repo = RepositorioMemoria()
        solicitudes, contador = repo.cargar()
        assert solicitudes == []
        assert contador == 1

    def test_guardar_y_cargar(self):
        repo = RepositorioMemoria()
        s1 = _crear_solicitud(1)
        repo.guardar([s1], contador=2)

        solicitudes, contador = repo.cargar()
        assert contador == 2
        assert len(solicitudes) == 1
        assert solicitudes[0].id == 1

    def test_cargar_devuelve_copia(self):
        """Modificar la lista devuelta no debe afectar el estado interno."""
        repo = RepositorioMemoria()
        repo.guardar([_crear_solicitud(1)], contador=2)
        lista1, _ = repo.cargar()
        lista1.append(_crear_solicitud(99))
        lista2, _ = repo.cargar()
        assert len(lista2) == 1  # el append sobre lista1 no afectó