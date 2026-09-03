# Perfil STANDARD — default para changes M

## Cuándo elegir STANDARD
- Change de tamaño medio: 1-2 containers + 1-2 services nuevos.
- Módulo conocido pero cambio no trivial.
- Feature aditivo sobre contrato BE existente (no endpoints nuevos).
- No hay riesgo alto de regresión pero sí toca lógica de dominio.

## Ajustes respecto al método base

- **Fase 0 componentes**: obligatoria + **gate humano explícito**.
- **TDD granularidad**: **por task** — Red → Green → Refactor por cada task.
- **Explore**: reutilizar si el módulo tiene explore en engram de esta semana; sino full.
- **Spec + Design**: separados.
- **sdd-preview**: decide su propia cantidad de reviewers vía self-assessment según riesgo real. El perfil no fuerza número.
- **Verify**: normal — suite + build + smoke live. Sin adversarial extra salvo que design lo pida.
- **Apply**: batches libres (a criterio de `sdd-tasks`).
- **Storybook / MSW / fixtures**: cobertura completa.

## Nudges de `/clear`

- Entre fases mayores (design → tasks, tasks → apply).
- Entre batches del apply si el humano lo prefiere.

## Costo orden de magnitud

~250K tokens end-to-end.
