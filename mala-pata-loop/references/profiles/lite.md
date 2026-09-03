# Perfil LITE — S/M en módulo conocido

## Cuándo elegir LITE
- Change chico o mediano.
- Módulo caliente (ya trabajado esta semana o hace poco).
- Adapta atoms/molecules existentes (no crea componentes nuevos genuinos).
- Extiende un service existente (no crea service nuevo).
- Sin riesgo de regresión en flujos críticos.

## Ajustes respecto al método base

- **Fase 0 componentes**: obligatoria — audit REUSA/ADAPTA/NUEVO **NO se salta**. Diferencia con FULL/STANDARD: el gate humano es **auto-approve si el audit marca 0 componentes NUEVOS**; si hay ≥1 NUEVO, el gate humano es explícito.
- **TDD granularidad**: **por feature** — agrupá tasks relacionados (service + selector + wiring de container) y escribí tests al cerrar el grupo. Excepción: lógica pura (VOs, selectors, algoritmos) sigue por task.
- **Explore**: reutilizar explores previos del mismo módulo si existen en engram; sino explore mínimo (grep-first).
- **Spec + Design**: **fusionados** en un solo artefacto `sdd/<change>/spec-design`. `sdd-design` incluye escenarios que en STANDARD irían en spec.
- **sdd-preview**: decide su propio self-assessment; para LITE típicamente 0 salvo que aparezca alguna señal de riesgo real.
- **Verify**: liviano — suite + build + smoke live. Sin adversarial. (Default por tamaño: sube a normal si `sdd-preview` detectó señales de riesgo — ver `_base.md`.)
- **Apply**: batches libres.
- **Storybook / MSW / fixtures**: solo variantes nuevas críticas.

## Nudges de `/clear`

- Entre spec-design y apply.
- Al gusto del humano en el resto.

## Costo orden de magnitud

~120K tokens end-to-end.
