# src/main.py
from gestor import GestorSolicitudes


def main():
    g = GestorSolicitudes()
    while True:
        print("\n--- GESTIÓN DE SOLICITUDES ACADÉMICAS ---")
        print("1. Registrar solicitud")
        print("2. Cambiar estado")
        print("3. Asignar responsable")
        print("4. Buscar/filtrar")
        print("5. Listar todas")
        print("6. Reporte")
        print("0. Salir")
        op = input("Opción: ").strip()

        if op == "1":
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            legajo = input("Legajo: ").strip()
            tipo = input("Tipo (beca/cambio_carrera/regularidad/examen/otro): ").strip()
            prioridad = input("Prioridad (alta/media/baja): ").strip()
            detalle = input("Detalle: ").strip()
            g.registrar_solicitud(nombre, apellido, legajo, tipo, prioridad, detalle)
        elif op == "2":
            try:
                id_s = int(input("ID solicitud: ").strip())
            except ValueError:
                print("ID inválido")
                continue
            estado = input("Nuevo estado (pendiente/en_proceso/resuelta/rechazada): ").strip()
            g.cambiar_estado(id_s, estado)
        elif op == "3":
            try:
                id_s = int(input("ID solicitud: ").strip())
            except ValueError:
                print("ID inválido")
                continue
            resp = input("Responsable: ").strip()
            g.asignar_responsable(id_s, resp)
        elif op == "4":
            texto = input("Texto (enter para omitir): ").strip() or None
            tipo = input("Tipo (enter para omitir): ").strip() or None
            estado = input("Estado (enter para omitir): ").strip() or None
            prioridad = input("Prioridad (enter para omitir): ").strip() or None
            res = g.buscar(texto, tipo, estado, prioridad)
            if not res:
                print("(sin resultados)")
            for s in res:
                print(f"#{s['id']} | {s['apellido']}, {s['nombre']} | {s['tipo']} | {s['estado']}")
        elif op == "5":
            g.listar()
        elif op == "6":
            g.reporte()
        elif op == "0":
            print("Chau")
            break
        else:
            print("Opción inválida")


if __name__ == "__main__":
    main()