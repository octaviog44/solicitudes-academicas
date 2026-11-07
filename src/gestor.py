# src/gestor.py
# Commit 6: excepciones de dominio + reporte separado + gestor sin UI
from dominio import (
    Estado,
    Estudiante,
    Solicitud,
    SolicitudRequest,
    parse_estado,
    parse_prioridad,
    parse_tipo,
)
from excepciones import SolicitudInvalidaError, SolicitudNoEncontradaError
from repositorio import RepositorioSolicitudes
from servicio_reportes import ServicioReportes
from validador import ValidadorSolicitud


class GestorSolicitudes:
    def __init__(self, repositorio: RepositorioSolicitudes):
        self.repositorio = repositorio
        self.validador = ValidadorSolicitud()
        self.reportes = ServicioReportes()
        self.solicitudes, self.contador = self.repositorio.cargar()

    def _persistir(self):
        self.repositorio.guardar(self.solicitudes, self.contador)

    def _buscar_por_id(self, id_solicitud: int) -> Solicitud:
        for s in self.solicitudes:
            if s.id == id_solicitud:
                return s
        raise SolicitudNoEncontradaError("solicitud no encontrada")

    # ---------- registro ----------
    def registrar_solicitud(self, request: SolicitudRequest) -> Solicitud:
        tipo_enum, prioridad_enum = self.validador.validar(request)
        estudiante = Estudiante(
            nombre=request.nombre,
            apellido=request.apellido,
            legajo=request.legajo,
        )
        solicitud = Solicitud(
            id=self.contador,
            estudiante=estudiante,
            tipo=tipo_enum,
            prioridad=prioridad_enum,
            detalle=request.detalle,
        )
        self.contador += 1
        self.solicitudes.append(solicitud)
        self._persistir()
        return solicitud

    # ---------- cambio de estado ----------
    def cambiar_estado(self, id_solicitud: int, nuevo_estado: str) -> Solicitud:
        estado_enum = self.validador.validar_estado(nuevo_estado)
        solicitud = self._buscar_por_id(id_solicitud)
        solicitud.cambiar_estado(estado_enum)
        self._persistir()
        return solicitud

    # ---------- asignación de responsable ----------
    def asignar_responsable(self, id_solicitud: int, responsable: str) -> Solicitud:
        self.validador.validar_responsable(responsable)
        solicitud = self._buscar_por_id(id_solicitud)
        solicitud.asignar_responsable(responsable)
        self._persistir()
        return solicitud

    # ---------- búsqueda ----------
    def buscar(self, texto=None, tipo=None, estado=None, prioridad=None) -> list[Solicitud]:
        tipo_enum = parse_tipo(tipo) if tipo is not None else None
        estado_enum = parse_estado(estado) if estado is not None else None
        prioridad_enum = parse_prioridad(prioridad) if prioridad is not None else None

        if tipo is not None and tipo_enum is None:
            return []
        if estado is not None and estado_enum is None:
            return []
        if prioridad is not None and prioridad_enum is None:
            return []

        return [
            s
            for s in self.solicitudes
            if s.coincide_con(
                texto=texto,
                tipo=tipo_enum,
                estado=estado_enum,
                prioridad=prioridad_enum,
            )
        ]

    # ---------- listado y reporte (delegando) ----------
    def listar(self) -> list[Solicitud]:
        return list(self.solicitudes)

    def reporte(self) -> dict:
        return self.reportes.generar(self.solicitudes)