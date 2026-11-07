# src/consola_ui.py
# Commit 6: separación de la capa de presentación
from dominio import SolicitudRequest
from excepciones import SolicitudInvalidaError, SolicitudNoEncontradaError
from gestor import GestorSolicitudes


class ConsolaUI:
    def __init__(self, gestor: GestorSolicitudes):
        self.gestor = gestor

    def ejecutar(self):
        while True:
            self._mostrar_menu()
            op = input("Opción: ").strip()
            if op == "0":
                print("Chau")
                break
            try:
                self._procesar_opcion(op)
            except SolicitudInvalidaError as e:
                print(f"ERROR: {e}")
            except SolicitudNoEncontradaError as e:
                print(f"ERROR: {e}")

    # ---------- menú ----------
    def _mostrar_menu(self):
        print("\n--- GESTIÓN DE SOLICITUDES ACADÉMICAS ---")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar/filtrar")
        print("5. Listar todas")
        print("6. Reporte")
        print("0. Salir")

    # ---------- despacho ----------
    def _procesar_opcion(self, op: str):
        if op == "1":
            self._registrar()
        elif op == "2":
            self._cambiar_estado()
        elif op == "3":
            self._asignar_responsable()
        elif op == "4":
            self._buscar()
        elif op == "5":
            self._listar()
        elif op == "6":
            self._reporte()
        else:
            print("Opción inválida")

    # ---------- operaciones ----------
    def _registrar(self):
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        legajo = input("Legajo: ").strip()
        tipo = input("Tipo (beca/cambio_carrera/regularidad/examen/otro): ").strip()
        prioridad = input("Prioridad (alta/media/baja): ").strip()
        detalle = input("Detalle: ").strip()
        request = SolicitudRequest(
            nombre=nombre,
            apellido=apellido,
            legajo=legajo,
            tipo=tipo,
            prioridad=prioridad,
            detalle=detalle,
        )
        solicitud = self.gestor.registrar_solicitud(request)
        print(f"Solicitud #{solicitud.id} registrada")

    def _cambiar_estado(self):
        id_s = self._leer_id()
        if id_s is None:
            return
        estado = input("Nuevo estado (pendiente/en_proceso/resuelta/rechazada): ").strip()
        solicitud = self.gestor.cambiar_estado(id_s, estado)
        print(f"Solicitud #{solicitud.id} -> {solicitud.estado.value}")

    def _asignar_responsable(self):
        id_s = self._leer_id()
        if id_s is None:
            return
        responsable = input("Responsable: ").strip()
        solicitud = self.gestor.asignar_responsable(id_s, responsable)
        print(f"Solicitud #{solicitud.id} asignada a {solicitud.responsable}")

    def _buscar(self):
        texto = input("Texto (enter para omitir): ").strip() or None
        tipo = input("Tipo (enter para omitir): ").strip() or None
        estado = input("Estado (enter para omitir): ").strip() or None
        prioridad = input("Prioridad (enter para omitir): ").strip() or None
        resultados = self.gestor.buscar(texto, tipo, estado, prioridad)
        if not resultados:
            print("(sin resultados)")
        for s in resultados:
            print(
                f"#{s.id} | {s.estudiante.apellido}, {s.estudiante.nombre} | "
                f"{s.tipo.value} | {s.estado.value}"
            )

    def _listar(self):
        solicitudes = self.gestor.listar()
        if not solicitudes:
            print("(sin solicitudes)")
            return
        for s in solicitudes:
            print(
                f"#{s.id} | {s.estudiante.apellido}, {s.estudiante.nombre} | "
                f"{s.tipo.value} | {s.prioridad.value} | {s.estado.value} | "
                f"resp: {s.responsable}"
            )

    def _reporte(self):
        datos = self.gestor.reporte()
        print("=" * 40)
        print("REPORTE DE SOLICITUDES")
        print("=" * 40)
        print(f"Total: {datos['total']}")
        print("Por estado:")
        for k, v in datos["por_estado"].items():
            print(f"  {k}: {v}")
        print("Por tipo:")
        for k, v in datos["por_tipo"].items():
            print(f"  {k}: {v}")
        print("Por prioridad:")
        for k, v in datos["por_prioridad"].items():
            print(f"  {k}: {v}")
        print("=" * 40)

    # ---------- helpers ----------
    def _leer_id(self):
        try:
            return int(input("ID solicitud: ").strip())
        except ValueError:
            print("ID inválido")
            return None