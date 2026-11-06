# Sistema de Gestión de Solicitudes Académicas

Trabajo Práctico Integrador — **Metodología de Sistemas II**

> **Estado del repositorio:** versión inicial (tag `estado-inicial`).
> Esta versión funciona correctamente desde la perspectiva del usuario, pero
> contiene **deuda técnica y code smells deliberados** que serán diagnosticados
> y corregidos en etapas posteriores mediante refactoring seguro, aplicación de
> SOLID y Clean Code, pruebas y code review.

---

## 1. Descripción

Prototipo de un sistema de consola para gestionar **solicitudes académicas** de
estudiantes. Permite registrar solicitudes, clasificarlas por tipo y prioridad,
cambiar su estado, asignar un responsable, buscarlas y generar un reporte
básico.

El sistema persiste los datos en un archivo JSON local (`datos/solicitudes.json`)
que se genera automáticamente al primer uso.

### Actores

- **Estudiante / Usuario**: origina la solicitud (datos: nombre, apellido, legajo).
- **Responsable / Área**: persona a la que se le asigna la solicitud.
- **Operador**: usa el sistema para registrar, asignar y consultar (rol del usuario de consola).

### Entidades principales

- **Solicitud**: id, tipo, prioridad, detalle, estado, responsable, fecha.
- **Estudiante**: nombre, apellido, legajo (en esta versión, embebido en la solicitud).
- **Responsable / Área**: nombre del responsable asignado.

---

## 2. Funcionalidades

| # | Operación | Descripción |
|---|-----------|-------------|
| 1 | Registrar solicitud | Alta de una nueva solicitud con validaciones básicas |
| 2 | Cambiar estado | `pendiente` → `en_proceso` → `resuelta` / `rechazada` |
| 3 | Asignar responsable | Asigna un responsable a una solicitud existente |
| 4 | Buscar / filtrar | Filtra por texto libre, tipo, estado y prioridad |
| 5 | Listar | Muestra todas las solicitudes registradas |
| 6 | Reporte | Totales por estado, tipo y prioridad |

### Dominios válidos

- **Tipos:** `beca`, `cambio_carrera`, `regularidad`, `examen`, `otro`
- **Prioridades:** `alta`, `media`, `baja`
- **Estados:** `pendiente`, `en_proceso`, `resuelta`, `rechazada`

---

## 3. Tecnologías

- **Lenguaje:** Python 3.10+
- **Persistencia:** archivo JSON local (simulada, sin base de datos)
- **Dependencias externas:** ninguna (solo biblioteca estándar)
- **Interfaz:** consola (CLI)

---

## 4. Instalación y uso

### Requisitos

- Python 3.10 o superior

### Clonar el repositorio

```bash
git clone https://github.com/octaviog44/solicitudes-academicas.git
cd solicitudes-academicas