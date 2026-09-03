# Formato FIJO de la torre de control (contrato inmutable)

> Este formato NO cambia. Mismo banner, mismas 7 columnas en el mismo orden,
> mismo léxico de semáforo, mismo orden de filas. Es memoria mecánica: el
> humano reacciona sin releer.

## 1. Banner de frescura (obligatorio, siempre arriba)

```
🗼 CONTROL TOWER · <n> SDD · <YYYY-MM-DD HH:MM>
Fresh: fetched <repo>@<sha7>[ · <repo2>@<sha7>] · integración=<branch> · memoria live · READ-ONLY
```

Prueba visual de que NO es cache: los SHA son los de la branch de integración
recién traída en esta corrida.

## 2. Tabla (exactamente estas 7 columnas, este orden)

| # | 🚦 | SDD | Fase | Git | Depende | 👉 Próxima acción |
|---|----|-----|------|-----|---------|-------------------|

- **#** — índice.
- **🚦** — un solo símbolo del léxico cerrado (§3).
- **SDD** — change-name en `code`.
- **Fase** — fase más avanzada alcanzada del pipeline (§4), con progreso si es
  parcial. Ej: `preview ✅`, `apply 12/18`, `verify ✅`.
- **Git** — realidad de branch/merge: `sin branch` · `branch viva` · `worktree`
  · `PR#N mergeado` · `en <integr>` · `stale +A/-B` (adelante/atrás de integr).
- **Depende** — otro SDD de la lista del que depende (+ `⛔` si ese aún no
  está mergeado) o `—`.
- **👉 Próxima acción** — UN solo paso imperativo (qué hay que hacer ya).

## 3. Léxico del semáforo (cerrado — nunca agregar símbolos nuevos)

| 🚦 | Estado | El humano reacciona |
|----|--------|---------------------|
| 🔴 | **Acción tuya YA** — listo p/PR, o apply/verify hecho sin cerrar | hacé el paso |
| 🟡 | **Gate humano** — espera tu aprobación/decisión (preview, o verify con hallazgos) | revisá y aprobá |
| 🟠 | **Parqueado/bloqueado** — depende de otro SDD sin merge, branch stale, o pausa | desbloqueá |
| ⚫ | **Sin instrucción** — ciclo trabado, no hay próximo paso claro | definí qué sigue |
| 🟢 | **En curso** — avanza normal, próxima fase auto-corrible | corré la próxima fase |
| ✅ | **Mergeado, falta limpieza** (🧹) — código en integración pero worktree/branch vivos | limpiá |
| ✔️ | **Cerrado** — mergeado + limpio | nada |
| ❌ | **Cancelado** — state = ABANDONADO | nada |

## 4. Pipeline de fases (orden canónico del ciclo)

```
kickoff → explore → propose → spec → design → tasks → preview(gate)
→ apply → verify → archive → PR → merge → limpieza
```

## 5. Orden de filas (SIEMPRE por urgencia)

```
🔴 → 🟡 → 🟠 → ⚫ → 🟢 → ✅ → ✔️ → ❌
```

El ojo del humano va directo a lo de arriba.

## 6. Bloque de evidencia (debajo de la tabla, obligatorio)

Una línea por SDD, para que el estado sea auditable:

```
Evidencia:
- <SDD> — memoria: <#id/topic_key> · git: <branch|sha7|PR#N> · <base de 1 línea del veredicto>
```

## Ejemplo (ilustra el formato; los datos son de muestra)

```
🗼 CONTROL TOWER · 5 SDD · 2026-07-30 17:40
Fresh: fetched <repo>@3f090a3 · integración=development · memoria live · READ-ONLY
```

| # | 🚦 | SDD | Fase | Git | Depende | 👉 Próxima acción |
|---|----|-----|------|-----|---------|-------------------|
| 1 | 🔴 | `cartas-datos-instancia-firme` | apply ✅ 18/18 | branch viva, sin PR | — | verify → archive → PR |
| 2 | 🟡 | `gate-verde` | preview ✅ | worktree | — | gate humano: aprobar apply |
| 3 | 🟠 | `foo-bar` | tasks ✅ | sin branch | #1 ⛔ | espera merge de #1 |
| 4 | ✅ | `mora-actuarial` | merge ✅ PR#426 | en development | — | 🧹 limpiar worktree/branch |
| 5 | ❌ | `reintegro-pila` | cancelado (preview) | — | — | ninguna |

```
Evidencia:
- cartas-datos-instancia-firme — memoria: sdd/.../apply-progress #7311 · git: feature/... (no en development) · 18/18 tasks, sin PR
- gate-verde — memoria: sdd/.../preview #… · git: worktree presente · preview aprobado sin apply
- foo-bar — memoria: sdd/.../tasks #… · git: sin branch · depende de #1 no mergeado
- mora-actuarial — memoria: archive-report #7078 · git: PR#426 en development, branch borrada · mergeado
- reintegro-pila — memoria: state #7284 = ABANDONADO · git: sin branch · cancelado en preview
```
