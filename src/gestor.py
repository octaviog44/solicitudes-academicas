# src/gestor.py
# Versión refactorizada - Commit 1: Replace Magic Strings -> Enums
import json
import os
from datetime import datetime

from dominio import (
    Estado,
    parse_estado,
    parse_prioridad,
    parse_tipo,
)

RUTA_DATOS = "datos/solicitudes.json"


class GestorSolicitudes:
    def __init__(self):
        self.solicitudes = []
        self.contador = 1
        self.cargar()

    # ---------- persistencia mezclada con lógica ----------
    def cargar(self):
        if os.path.exists(RUTA_DATOS):
            try:
                with open(RUTA_DATOS, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.solicitudes = data.get("solicitudes", [])
                    self.contador = data.get("contador", 1)
            except Exception:
                self.solicitudes = []
                self.contador = 1

    def guardar(self):
        os.makedirs("datos", exist_ok=True)
        with open(RUTA_DATOS, "w", encoding="utf-8") as f:
            json.dump(
                {"solicitudes": self.solicitudes, "contador": self.contador},
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

        # construcción con datos "primitivos" sueltos (Primitive Obsession)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        sol = {
            "id": self.contador,
            "nombre": nombre,
            "apellido": apellido,
            "legajo": legajo,
            "tipo": tipo_enum.value,
            "prioridad": prioridad_enum.value,
            "detalle": detalle,
            "estado": Estado.PENDIENTE.value,
            "responsable": None,
            "fecha": fecha,
        }
        self.contador += 1
        self.solicitudes.append(sol)
        self.guardar()
        print(f"Solicitud #{sol['id']} registrada")
        return sol

    # ---------- lógica repetida (Duplicated Code) ----------
    def cambiar_estado(self, id_solicitud, nuevo_estado):
        estado_enum = parse_estado(nuevo_estado)
        if estado_enum is None:
            print("ERROR: estado inválido")
            return False
        for s in self.solicitudes:
            if s["id"] == id_solicitud:
                s["estado"] = estado_enum.value
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
            if s["id"] == id_solicitud:
                s["responsable"] = responsable
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

        resultados = []
        for s in self.solicitudes:
            coincide = True
            if texto is not None:
                t = texto.lower()
                if not (
                    t in s["nombre"].lower()
                    or t in s["apellido"].lower()
                    or t in s["detalle"].lower()
                    or t in s["legajo"]
                ):
                    coincide = False
            if tipo is not None and (tipo_enum is None or s["tipo"] != tipo_enum.value):
                coincide = False
            if estado is not None and (estado_enum is None or s["estado"] != estado_enum.value):
                coincide = False
            if prioridad is not None and (prioridad_enum is None or s["prioridad"] != prioridad_enum.value):
                coincide = False
            if coincide:
                resultados.append(s)
        return resultados

    # ---------- reporte con formato hardcodeado y cálculo mezclado ----------
    def reporte(self):
        total = len(self.solicitudes)
        por_estado = {}
        por_tipo = {}
        por_prioridad = {}
        for s in self.solicitudes:
            por_estado[s["estado"]] = por_estado.get(s["estado"], 0) + 1
            por_tipo[s["tipo"]] = por_tipo.get(s["tipo"], 0) + 1
            por_prioridad[s["prioridad"]] = por_prioridad.get(s["prioridad"], 0) + 1

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
                f"#{s['id']} | {s['apellido']}, {s['nombre']} | "
                f"{s['tipo']} | {s['prioridad']} | {s['estado']} | "
                f"resp: {s['responsable']}"
            )