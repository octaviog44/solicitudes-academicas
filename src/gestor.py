# src/gestor.py
# Versión refactorizada - Commit 2: Extract Class -> Solicitud con invariantes
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

RUTA_DATOS = "datos/solicitudes.json"


class GestorSolicitudes:
    def __init__(self):
        self.solicitudes: list[Solicitud] = []
        self.contador = 1
        self.cargar()

    # ---------- persistencia mezclada con lógica ----------
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

    # ---------- LONG METHOD: hace TODO ----------
    def registrar_solicitud(self, nombre, apellido, legajo, tipo, prioridad, detalle):
        # validaciones mezcladas y repetidas
        if nombre == "" or apellido == "":
            print("ERROR: nombre y apellido obligatorios")
            return None
        if legajo == "" or not legajo.isdigit():
            print("ERROR: legajo inválido")
            return None

        tipo_enum = parse_tipo(tipo)
        if tipo_enum is None:
            print("ERROR: tipo inválido")
            return None

        prioridad_enum = parse_prioridad(prioridad)
        if prioridad_enum is None:
            print("ERROR: prioridad inválida")
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

    # ---------- lógica repetida (Duplicated Code) ----------
    def cambiar_estado(self, id_solicitud, nuevo_estado):
        estado_enum = parse_estado(nuevo_estado)
        if estado_enum is None:
            print("ERROR: estado inválido")
            return False
        for s in self.solicitudes:
            if s.id == id_solicitud:
                s.cambiar_estado(estado_enum)
                self.guardar()
                print(f"Solicitud #{id_solicitud} -> {estado_enum.value}")
                return True
        print("ERROR: solicitud no encontrada")
        return False

    def asignar_responsable(self, id_solicitud, responsable):
        if responsable == "":
            print("ERROR: responsable vacío")
            return False
        for s in self.solicitudes:
            if s.id == id_solicitud:
                try:
                    s.asignar_responsable(responsable)
                except ValueError as e:
                    print(f"ERROR: {e}")
                    return False
                self.guardar()
                print(f"Solicitud #{id_solicitud} asignada a {responsable}")
                return True
        print("ERROR: solicitud no encontrada")
        return False

    # ---------- FEATURE ENVY + lógica de filtrado mezclada ----------
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

    # ---------- reporte con formato hardcodeado y cálculo mezclado ----------
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