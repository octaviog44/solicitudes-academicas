
# Commit 6: Extract Class -> reporte separado del gestor
from dominio import Solicitud


class ServicioReportes:
    def generar(self, solicitudes: list[Solicitud]) -> dict:
        por_estado: dict[str, int] = {}
        por_tipo: dict[str, int] = {}
        por_prioridad: dict[str, int] = {}

        for s in solicitudes:
            est = s.estado.value
            tip = s.tipo.value
            pri = s.prioridad.value
            por_estado[est] = por_estado.get(est, 0) + 1
            por_tipo[tip] = por_tipo.get(tip, 0) + 1
            por_prioridad[pri] = por_prioridad.get(pri, 0) + 1

        return {
            "total": len(solicitudes),
            "por_estado": por_estado,
            "por_tipo": por_tipo,
            "por_prioridad": por_prioridad,
        }