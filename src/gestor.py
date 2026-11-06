# src/gestor.py
# Versión refactorizada - Commit 3: Extract Method -> ValidadorSolicitud
import json
import os

from dominio import (
    Estado,
    Estudiante,
    Solicitud,
    parse_estado,
    parse_prioridad,
    parse_tipo,
)
from validador import ValidadorSolicitud

RUTA_DATOS = "datos/solicitudes.json"


class GestorSolicitudes:
    def __init__(self):
        self.solicitudes: list[Solicitud] = []
        self.contador = 1
        self.validador = ValidadorSolicitud()
        self.cargar()

    # ---------- persistencia ----------
    def cargar(self):
        if os.path.exists(RUTA_DATOS):
            try:
                with open(RUTA_DATOS, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.solicitudes = [
                        Solicitud.from_dict(s) for s in data.get("solicitudes", [])
                    ]
                    self.contador = data.get("contador", 1)
            except Exception:
                self.solicitudes = []
                self.contador = 1

    def guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open(RUTA_DATOS, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "solicitudes": [s.to_dict() for s in self.solicitudes],
                    "contador": self.contador,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

    # ---------- registro ----------
    def registrar_solicitud(self, nombre, apellido, legajo, tipo, prioridad, detalle):
        try:
            self.validador.validar_datos_basicos(nombre, apellido, legajo)
            tipo_enum = self.validador.validar_tipo(tipo)
            prioridad_enum = self.validador.validar_prioridad(prioridad)
        except ValueError as e:
            print(f"ERROR: {e}")
            return None

        try:
            estudiante = Estudiante(nombre=nombre, apellido=apellido, legajo=legajo)
            solicitud = Solicitud(
                id=self.contador,
                estudiante=estudiante,
                tipo=tipo_enum,
                prioridad=prioridad_enum,
                detalle=detalle,
            )
        except ValueError as e:
            print(f"ERROR: {e}")
            return None

        self.contador += 1
        self.solicitudes.append(solicitud)
        self.guardar()
        print(f"Solicitud #{solicitud.id} registrada")
        return solicitud

    # ---------- cambio de estado ----------
    def cambiar_estado(self, id_solicitud, nuevo_estado):
        try:
            estado_enum = self.validador.validar_estado(nuevo_estado)
        except ValueError as e:
            print(f"ERROR: {e}")
            return False

        for s in self.solicitudes:
            if s.id == id_solicitud:
                s.cambiar_estado(estado_enum)
                self.guardar()
                print(f"Solicitud #{id_solicitud} -> {estado_enum.value}")
                return True
        print("ERROR: solicitud no encontrada")
        return False

    # ---------- asignación de responsable ----------
    def asignar_responsable(self, id_solicitud, responsable):
        try:
            self.validador.validar_responsable(responsable)
        except ValueError as e:
            print(f"ERROR: {e}")
            return False

        for s in self.solicitudes:
            if s.id == id_solicitud:
                s.asignar_responsable(responsable)
                self.guardar()
                print(f"Solicitud #{id_solicitud} asignada a {responsable}")
                return True
        print("ERROR: solicitud no encontrada")
        return False

    # ---------- búsqueda ----------
    def buscar(self, texto=None, tipo=None, estado=None, prioridad=None):
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

    # ---------- reporte ----------
    def reporte(self):
        total = len(self.solicitudes)
        por_estado = {}
        por_tipo = {}
        por_prioridad = {}
        for s in self.solicitudes:
            est = s.estado.value
            tip = s.tipo.value
            pri = s.prioridad.value
            por_estado[est] = por_estado.get(est, 0) + 1
            por_tipo[tip] = por_tipo.get(tip, 0) + 1
            por_prioridad[pri] = por_prioridad.get(pri, 0) + 1

        print("=" * 40)
        print("REPORTE DE SOLICITUDES")
        print("=" * 40)
        print(f"Total: {total}")
        print("Por estado:")
        for k, v in por_estado.items():
            print(f"  {k}: {v}")
        print("Por tipo:")
        for k, v in por_tipo.items():
            print(f"  {k}: {v}")
        print("Por prioridad:")
        for k, v in por_prioridad.items():
            print(f"  {k}: {v}")
        print("=" * 40)

    # ---------- listado ----------
    def listar(self):
        if not self.solicitudes:
            print("(sin solicitudes)")
            return
        for s in self.solicitudes:
            print(
                f"#{s.id} | {s.estudiante.apellido}, {s.estudiante.nombre} | "
                f"{s.tipo.value} | {s.prioridad.value} | {s.estado.value} | "
                f"resp: {s.responsable}"
            )