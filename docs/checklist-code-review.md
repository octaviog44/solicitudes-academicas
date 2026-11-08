# Checklist de Code Review — TPI Metodología de Sistemas II

**Proyecto:** Sistema de Gestión de Solicitudes Académicas
**Revisor:** Octavio Guardamagna
**Fecha:** 7 de Noviembre 2026
**Alcance:** Revisión del código en el tag `estado-refactorizado` (versión final).

---

## Criterios de revisión

Cada ítem se evalúa como ✅ (cumple), ⚠️ (cumple parcialmente, requiere seguimiento) o ❌ (no cumple, requiere corrección).

### 1. Legibilidad y nombres

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 1.1 | Los nombres de clases, métodos y variables son expresivos y describen su propósito | ✅ | Se reemplazaron nombres genéricos (`s`, `g`, `data`) por nombres del dominio (`solicitud`, `gestor`, `solicitudes`). |
| 1.2 | Los nombres de métodos describen qué hacen, no cómo | ✅ | `registrar_solicitud`, `cambiar_estado`, `asignar_responsable`, `buscar`, `listar`, `reporte`. |
| 1.3 | No hay abreviaturas crípticas ni nombres de una sola letra en el código de producción | ✅ | Los índices de iteración usan nombres descriptivos; los `for` cortos usan `s` solo en comprensiones acotadas. |
| 1.4 | Los nombres de los tests describen el escenario y el resultado esperado | ✅ | Patrón `test_<acción>_<condición>_<resultado>` (ej. `test_registrar_legajo_invalido_lanza_error`). |

### 2. Funciones y métodos

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 2.1 | Las funciones son pequeñas y tienen un solo nivel de abstracción | ✅ | Se aplicó Extract Method (commit 3); `registrar_solicitud` delega validación, construcción y persistencia. |
| 2.2 | Cada función tiene un solo motivo para cambiar (SRP) | ✅ | Validación → `ValidadorSolicitud`; persistencia → `RepositorioSolicitudes`; presentación → `ConsolaUI`. |
| 2.3 | Las funciones no mezclan lógica de negocio con presentación | ✅ | El gestor no imprime; la UI no conoce la persistencia. |
| 2.4 | La cantidad de parámetros es razonable (≤ 3) o se agrupan en un objeto | ✅ | Se aplicó Introduce Parameter Object (commit 4): `registrar_solicitud(request)`. |

### 3. Manejo de errores

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 3.1 | Los errores se manejan con excepciones explícitas, no con valores de retorno ambiguos | ✅ | `SolicitudInvalidaError`, `SolicitudNoEncontradaError` (commit 6). |
| 3.2 | Las excepciones son específicas del dominio | ✅ | Heredan de `SolicitudError`, que hereda de `Exception`. |
| 3.3 | No se capturan excepciones genéricas (`except Exception`) en la lógica de negocio | ⚠️ | `RepositorioJSON.cargar()` captura `Exception` deliberadamente para tolerar archivos corruptos. Se documenta como decisión de diseño. |
| 3.4 | Los mensajes de error son claros y accionables | ✅ | `"legajo inválido"`, `"tipo inválido"`, `"solicitud no encontrada"`. |

### 4. Diseño y SOLID

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 4.1 | Cada clase tiene una única responsabilidad | ✅ | `Solicitud`, `ValidadorSolicitud`, `RepositorioJSON`, `ServicioReportes`, `ConsolaUI`. |
| 4.2 | Las dependencias apuntan a abstracciones, no a implementaciones concretas | ✅ | `GestorSolicitudes` depende de `RepositorioSolicitudes`, no de `RepositorioJSON` (DIP). |
| 4.3 | Los dominios cerrados se modelan con enumeraciones, no con strings mágicos | ✅ | `TipoSolicitud`, `Prioridad`, `Estado` (commit 1). |
| 4.4 | El modelo de dominio tiene invariantes explícitos | ✅ | `Estudiante.__post_init__`, `Solicitud.__init__`, `asignar_responsable` (commit 2). |
| 4.5 | No hay duplicación de lógica | ✅ | Validaciones centralizadas en `ValidadorSolicitud` (commit 3). |

### 5. Pruebas

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 5.1 | Hay pruebas automatizadas que cubren los flujos principales | ✅ | 62 tests, 62 pasando. |
| 5.2 | Las pruebas cubren los caminos de error, no solo los exitosos | ✅ | `test_registrar_legajo_invalido_lanza_error`, `test_cambiar_estado_id_inexistente_lanza_error`, etc. |
| 5.3 | Las pruebas son independientes entre sí y no dependen de estado compartido | ✅ | Cada test usa `RepositorioMemoria` o `tmp_path` (aislado por test). |
| 5.4 | Las pruebas del repositorio no ensucian el filesystem | ✅ | Se usa `tmp_path` de pytest. |

### 6. Persistencia y compatibilidad

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 6.1 | El formato del JSON se mantiene compatible con la versión inicial | ✅ | Verificado por `test_formato_json_compatible_con_version_inicial`. |
| 6.2 | La carga de datos existentes no se rompe tras la refactorización | ✅ | Verificado por `test_flujo_completo_persistente` y por verificación manual. |
| 6.3 | La persistencia está desacoplada de la lógica de negocio | ✅ | `RepositorioSolicitudes` + `RepositorioJSON` (commit 5). |

### 7. Repositorio y trazabilidad

| # | Criterio | Estado | Observación |
|---|---|---|---|
| 7.1 | Los commits son atómicos y describen un cambio concreto | ✅ | Un commit por refactoring, con prefijo `refactor:` o `test:`. |
| 7.2 | El historial permite reconstruir el proceso | ✅ | Tags `estado-inicial`, `refactor-01` a `refactor-06`, `estado-refactorizado`. |
| 7.3 | El README describe instalación, uso, funcionalidades y tecnologías | ✅ | Ver `README.md`. |
| 7.4 | El código no incluye datos reales ni información sensible | ✅ | Datos sintéticos de prueba. |

---

## Observaciones y acciones correctivas

### Observación 1: `RepositorioJSON.cargar()` captura `Exception`

- **Ubicación:** `src/repositorio.py`, método `cargar()`.
- **Motivo:** tolerar archivos JSON corruptos o con estructura inesperada sin romper el sistema.
- **Decisión:** se mantiene la captura genérica, pero se documenta como decisión de diseño. En una versión futura se podría registrar el error en un log en lugar de silenciarlo.
- **Estado:** ✅ Aceptado con observación.

### Observación 2: `ConsolaUI` concentra el parsing de entrada

- **Ubicación:** `src/consola_ui.py`.
- **Motivo:** es la capa de presentación, y el parsing de entrada es una responsabilidad propia de la UI.
- **Decisión:** se acepta. Si en el futuro se agrega otra interfaz (web, API), se extraerá un `InputParser` común.
- **Estado:** ✅ Aceptado.

### Observación 3: Los `parse_*` devuelven `None` en lugar de lanzar excepción

- **Ubicación:** `src/dominio.py`, funciones `parse_tipo`, `parse_prioridad`, `parse_estado`.
- **Motivo:** permiten al validador distinguir "valor inválido" de "valor ausente" sin lanzar excepción en el parseo.
- **Decisión:** se acepta. El validador es quien lanza `SolicitudInvalidaError`.
- **Estado:** ✅ Aceptado.

---

## Criterios de aceptación

La versión refactorizada se considera **aceptada** si cumple con:

1. Todos los ítems del checklist en estado ✅ o ⚠️ justificado.
2. La suite de pruebas pasa en su totalidad (62/62).
3. El comportamiento externo es idéntico al de la versión inicial (verificado manualmente y con tests).
4. El repositorio tiene trazabilidad completa (tags `estado-inicial` y `estado-refactorizado`).
5. El informe documenta el proceso, las decisiones y las evidencias.

**Resultado:** ✅ **Aceptado.**

---

## Firma

- **Revisor:** Octavio Guardamagna
- **Fecha:** 7 de Noviembre 2026
- **Versión revisada:** tag `estado-refactorizado`