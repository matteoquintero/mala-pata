# Perfil MINIMAL — fix chico / refactor conocido

> **MINIMAL ≠ `/mala-pata-organic`** (decisión deliberada, no duplicación): MINIMAL
> **corre el ciclo SDD** — versión liviana, pero con artefactos, fases y gates
> (trazabilidad en engram). Organic NO hace SDD en absoluto: una sola pasada
> directa sin artefactos de planeación. Si el cambio chico amerita rastro SDD →
> MINIMAL; si no amerita SDD → organic.

## Cuándo elegir MINIMAL
- Fix de bug puntual (1-3 archivos).
- Refactor mecánico (rename, mover, extraer).
- Migración de tipo (agregar campo, actualizar tipos generados desde contrato).
- Fix de regresión en módulo que se tocó esta semana.
- Cambio sin lógica de negocio nueva.

## Ajustes respecto al método base

- **Fase 0 componentes**: obligatoria — audit REUSA/ADAPTA/NUEVO **NO se salta**. Auto-approve si audit = 0 NUEVOS. **Si el audit marca ≥1 componente NUEVO, escalar a LITE** — no seguir en MINIMAL con componentes nuevos.
- **TDD granularidad**: **por feature**. Nunca por task en MINIMAL.
- **Explore**: skipeable si el módulo se tocó esta semana. Sino explore mínimo (1 pass grep).
- **Spec + Design**: **fusionados y cortos** (target 1-2 páginas markdown).
- **sdd-preview**: típicamente 0 reviewers vía su propio self-assessment (change mecánico, sin señales de riesgo).
- **Verify**: liviano — suite + build. Sin smoke live obligatorio salvo que toque UI visible. (Default por tamaño: sube a normal si `sdd-preview` detectó señales de riesgo — ver `_base.md`.)
- **Apply**: 1 solo batch (sin `/clear` entre tasks).
- **Storybook / MSW / fixtures**: solo si el change toca UI.

## Nudges de `/clear`

- Al gusto del humano. En un MINIMAL de verdad, el ciclo completo entra en una sesión sin necesidad de `/clear`.

## Costo orden de magnitud

~70K tokens end-to-end.
