# src/main.py
# Commit 6: punto de entrada delgado
from consola_ui import ConsolaUI
from gestor import GestorSolicitudes
from repositorio import RepositorioJSON

RUTA_DATOS = "datos/solicitudes.json"


def main():
    repositorio = RepositorioJSON(RUTA_DATOS)
    gestor = GestorSolicitudes(repositorio)
    ui = ConsolaUI(gestor)
    ui.ejecutar()


if __name__ == "__main__":
    main()