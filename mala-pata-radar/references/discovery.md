# Fase A del radar — descubrimiento SOLO engram, foco en ACTIVOS

> Esta fase NO usa git. Lee SOLO el ciclo del SDD en la memoria (engram) y arma
> la lista de **candidatos ACTIVOS** — los que NO están claramente cerrados ni
> cancelados. Esa lista pasa a la **Fase B** (mismo radar,
> `state-derivation.md`), que confirma merge/branch/stale con git.
>
> **La Fase A propone, la Fase B confirma.** Un candidato que en realidad ya se
> mergeó (sin `archive-report` en memoria) puede aparecer acá como activo; NO es
> un error — la Fase B lo reclasifica con git aguas abajo.
>
> Stack: memoria = engram MCP (`mem_search`, `mem_get_observation`).

## Límite conocido (declaralo SIEMPRE en el banner de salida)

`mem_search` es semántico (FTS5), topa en **20 resultados** por búsqueda y NO
tiene enumeración por topic_key ni paginación. **No existe forma de listar el
100% de los SDD con engram.** Por eso esta fase apunta al set ACTIVO (chico y
reciente, donde el recall alcanza), NO a un inventario exhaustivo. Si el humano
necesita la foto de un SDD específico que no apareció, que lo pase por lista
explícita (la Fase B lo toma directo, sin este límite).

---

## Fase 1 — Descubrir candidatos activos (engram, sistemático)

Corré búsquedas-ancla por las fases que indican ACTIVIDAD, con `limit: 20` y
`match_mode: "any"` (más recall):

```
mem_search(query="sdd apply-progress",  limit=20, match_mode="any")
mem_search(query="sdd verify-report",   limit=20, match_mode="any")
mem_search(query="sdd preview",          limit=20, match_mode="any")
mem_search(query="sdd tasks",            limit=20, match_mode="any")
mem_search(query="sdd kickoff",          limit=20, match_mode="any")
```
Si conocés el dominio, sumá el término (`sdd <dominio> preview`, etc.).
De cada hit, extraé `<change>` del título `sdd/<change>/<fase>`. Unión =
candidatos. **Loop-until-dry**: repetí con términos variados hasta que 2
búsquedas seguidas no aporten `<change>` nuevo.

## Fase 2 — Ciclo de cada candidato `C` (nunca un solo hit)

```
mem_search(query="C", limit=20)
```
Quedate con TODAS las `sdd/C/<fase>`. `fase(C)` = la más avanzada. Orden:
```
kickoff · explore · proposal · spec · design · tasks · preview
· apply-progress · verify-report · archive-report · state
```
Confirmá cierre/cancelación con el contenido:
```
mem_get_observation(id=<fase más avanzada>)
mem_get_observation(id=<state, si existe>)
```

## Fase 3 — Filtro (solo ciclo)

Descartá de la tabla (NO son candidatos activos):
- `cancelado`: `state`/decisión dice ABANDONADO → contalo aparte.
- `cerrado en ciclo`: existe `archive-report` → contalo aparte (la Fase B dirá si
  además está mergeado/limpio).

Los que quedan = **candidatos ACTIVOS**, con su 🚦:
| 🚦 | fase(C) |
|----|---------|
| 🟢 | apply-progress / verify-report (con código) |
| 🔵 | kickoff … preview (en planning) |

---

## Salida de esta fase — la LISTA, no una tabla

Esta fase NO imprime tabla propia: su resultado es la **lista filtrada de
candidatos activos** (+ el conteo de "otros vistos": archivados/cancelados),
que pasa directo a la Fase B (`state-derivation.md`). La ÚNICA tabla que ve el
humano es la final de `table-format.md`, ya diagnosticada con git.

Lo que esta fase aporta al banner final: el disclaimer **best-effort (engram
≤20/búsqueda)** cuando el descubrimiento corrió, y la línea de conteo
`Otros vistos (no exhaustivo): ✔️ <n> con archive-report · ❌ <m> cancelados.`

Si un dato no se pudo leer en vivo, `?`; NO inventes.
