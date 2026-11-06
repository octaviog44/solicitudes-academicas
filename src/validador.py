# src/validador.py
# Commit 4: Introduce Parameter Object -> SolicitudRequest
from dominio import (
    Estado,
    Prioridad,
    SolicitudRequest,
    TipoSolicitud,
    parse_estado,
    parse_prioridad,
    parse_tipo,
)


class ValidadorSolicitud:
    """Centraliza las validaciones de datos de entrada del dominio."""

    def validar(self, request: SolicitudRequest) -> tuple[TipoSolicitud, Prioridad]:
        """Valida el request completo. Devuelve (tipo, prioridad) ya convertidos."""
        self._validar_datos_basicos(request)
        tipo_enum = self._validar_tipo(request.tipo)
        prioridad_enum = self._validar_prioridad(request.prioridad)
        return tipo_enum, prioridad_enum

    def validar_estado(self, estado: str) -> Estado:
        estado_enum = parse_estado(estado)
        if estado_enum is None:
            raise ValueError("estado inválido")
        return estado_enum

    def validar_responsable(self, responsable: str) -> None:
        if not responsable:
            raise ValueError("responsable vacío")

    # ---- privados ----
    def _validar_datos_basicos(self, request: SolicitudRequest) -> None:
        if not request.nombre or not request.apellido:
            raise ValueError("nombre y apellido obligatorios")
        if not request.legajo or not request.legajo.isdigit():
            raise ValueError("legajo inválido")

    def _validar_tipo(self, tipo: str) -> TipoSolicitud:
        tipo_enum = parse_tipo(tipo)
        if tipo_enum is None:
            raise ValueError("tipo inválido")
        return tipo_enum

    def _validar_prioridad(self, prioridad: str) -> Prioridad:
        prioridad_enum = parse_prioridad(prioridad)
        if prioridad_enum is None:
            raise ValueError("prioridad inválida")
        return prioridad_enum