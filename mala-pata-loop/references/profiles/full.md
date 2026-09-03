# Perfil FULL — SDDs L / críticos / primer paso en un módulo

## Cuándo elegir FULL
- Change grande: múltiples containers + services + tipos + tests.
- Feature nuevo (no adapta código existente).
- Contrato BE nuevo (endpoints, migraciones, cambio de shape).
- Módulo que nunca trabajaste (necesita explore desde cero).
- Riesgo de regresión en flujos críticos (auth, permisos, PII, dinero).

## Ajustes respecto al método base

- **Fase 0 componentes**: obligatoria + **gate humano explícito** para aprobar el set de átomos/moléculas/organismos antes de Apply.
- **TDD granularidad**: **por task** — Red → Green → Refactor por cada task individual.
- **Explore**: full desde cero. Ignorar explores previos aunque existan (el módulo se re-audita).
- **Spec + Design**: separados. Corren como fases distintas (`sdd-spec` y `sdd-design`).
- **sdd-preview**: decide su propia cantidad de reviewers vía self-assessment en función del riesgo real. El perfil NO impone un número.
- **Verify**: pesado + adversarial. Verifica contra todos los criterios del spec, corre suite completa + build + smoke live + adversarial checks si aplican.
- **Apply**: batches chicos (3-4 tasks) + nudge `/clear` entre batches.
- **Storybook / MSW / fixtures**: cobertura completa de variantes nuevas.

## Nudges de `/clear`

- Después de cada fase mayor (`explore`, `propose`, `spec`, `design`, `tasks`, cada batch de `apply`, `verify`).
- Antes de arrancar Apply.

## Costo orden de magnitud

~500K tokens end-to-end.
