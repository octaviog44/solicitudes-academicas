# src/repositorio.py
# Commit 5: Move Method -> persistencia fuera del gestor
import json
import os
from abc import ABC, abstractmethod

from dominio import Solicitud


class RepositorioSolicitudes(ABC):
    """Contrato de persistencia para solicitudes."""

    @abstractmethod
    def cargar(self) -> tuple[list[Solicitud], int]:
        """Devuelve (solicitudes, contador)."""

    @abstractmethod
    def guardar(self, solicitudes: list[Solicitud], contador: int) -> None:
        """Persiste la lista de solicitudes y el contador."""


class RepositorioJSON(RepositorioSolicitudes):
    """Implementación concreta sobre un archivo JSON local."""

    def __init__(self, ruta: str):
        self.ruta = ruta

    def cargar(self) -> tuple[list[Solicitud], int]:
        if not os.path.exists(self.ruta):
            return [], 1
        try:
            with open(self.ruta, "r", encoding="utf-8") as f:
                data = json.load(f)
                solicitudes = [
                    Solicitud.from_dict(s) for s in data.get("solicitudes", [])
                ]
                contador = data.get("contador", 1)
                return solicitudes, contador
        except Exception:
            return [], 1

    def guardar(self, solicitudes: list[Solicitud], contador: int) -> None:
        os.makedirs(os.path.dirname(self.ruta), exist_ok=True)
        with open(self.ruta, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "solicitudes": [s.to_dict() for s in solicitudes],
                    "contador": contador,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

class RepositorioMemoria(RepositorioSolicitudes):
    """Implementación en memoria, útil para tests y demos sin persistencia."""

    def __init__(self):
        self._solicitudes: list[Solicitud] = []
        self._contador: int = 1

    def cargar(self) -> tuple[list[Solicitud], int]:
        return list(self._solicitudes), self._contador

    def guardar(self, solicitudes: list[Solicitud], contador: int) -> None:
        self._solicitudes = list(solicitudes)
        self._contador = contador