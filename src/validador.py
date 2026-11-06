
# Commit 3: Extract Method -> validaciones centralizadas
from dominio import (
    Estado,
    Prioridad,
    TipoSolicitud,
    parse_estado,
    parse_prioridad,
    parse_tipo,
)


class ValidadorSolicitud:
    """Centraliza las validaciones de datos de entrada del dominio."""

    def validar_datos_basicos(self, nombre: str, apellido: str, legajo: str) -> None:
        if not nombre or not apellido:
            raise ValueError("nombre y apellido obligatorios")
        if not legajo or not legajo.isdigit():
            raise ValueError("legajo inválido")

    def validar_tipo(self, tipo: str) -> TipoSolicitud:
        tipo_enum = parse_tipo(tipo)
        if tipo_enum is None:
            raise ValueError("tipo inválido")
        return tipo_enum

    def validar_prioridad(self, prioridad: str) -> Prioridad:
        prioridad_enum = parse_prioridad(prioridad)
        if prioridad_enum is None:
            raise ValueError("prioridad inválida")
        return prioridad_enum

    def validar_estado(self, estado: str) -> Estado:
        estado_enum = parse_estado(estado)
        if estado_enum is None:
            raise ValueError("estado inválido")
        return estado_enum

    def validar_responsable(self, responsable: str) -> None:
        if not responsable:
            raise ValueError("responsable vacío")