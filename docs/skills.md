# Qué hace cada skill y en qué se apoya

mala-pata es una capa de **flujo** sobre gentle-ai (el motor) y frameworks probados de la comunidad.
No inventamos la rueda — la orquestamos. El pipe es: **research → triage → (organic | loop | roadmap) → `*-start`**.

| Skill | Qué hace | En qué se apoya |
|---|---|---|
| **research** | Afina una idea cruda antes de ejecutarla; da un veredicto (proceder / afinar / reconsiderar) y escribe un doc. Es el diamante 1 (Discover→Define). | Double Diamond · Heilmeier Catechism (8 preguntas) · JTBD · codegraph + web para investigar |
| **triage** | La puerta de entrada: lee el pedido y decide el carril (organic / loop / roadmap). No ejecuta, rutea. | Gate de forma (Qué/Done/Decisiones) · INVEST (Testable) |
| **organic** | Genera el kickoff de un cambio ya entendido (ODD). | Clean Architecture · SOLID · DDD/Hexagonal · gentle-ai (motor ODD) |
| **organic-start** | Corre el ciclo ODD: worktree → explorar → implementar task por task con work-unit commits y RDD por commit. | gentle-ai (ODD + RDD) · TDD del proyecto |
| **loop** | Genera el kickoff de un SDD, cuando hay que diseñar antes de codear. Gate de entrada con Definition of Ready. | Example Mapping / Three Amigos · INVEST · gentle-ai (motor SDD) |
| **loop-start** | Corre el SDD fase por fase (explore → propose → spec → design → tasks → preview → apply → verify → archive) con gate humano por fase. | gentle-ai (agentes sdd-*) · Clean Arch/SOLID/DDD |
| **loop-orchestrate** | Planifica un lote de SDDs en paralelo (olas, conflictos, splits). Read-only. | git · gentle-ai |
| **loop-orchestrate-start** | Lanza el lote en paralelo (un worktree + una sesión por kickoff), serializando el apply. | git worktrees · gentle-ai |
| **roadmap** | Descompone un objetivo grande en un DAG de fases; cada fase la re-decide triage al llegar. | MECE · regla del 100% · Gap analysis · JTBD · checklist de dominio · codegraph + web |
| **radar** | Descubre y diagnostica los ciclos activos contra git en vivo (fase, merge, stale, gates). Read-only. | git (fuente de verdad) · engram |
| **walkthrough** | De un PR o roadmap arma un recorrido de prueba y lo proyecta en dos carriles (QA interno + doc cliente). | Diátaxis · BDD / Given-When-Then (living documentation) |
| **states** | Dibuja la máquina de estados real de un feature desde el código, para ver transiciones rotas de un vistazo. | archify (lifecycle) · codegraph · fidelidad / ortogonal / mínimo (statecharts) |
| **sdd-preview** | Gate humano entre tasks y apply: resumen en cristiano, anti-sello, frena hasta aprobar. | Invención propia (lo único que NO es framework de la comunidad) |

> Diagramas de este flujo: `docs/flujo-mala-pata.html` (el flujo + la fundación) y `docs/guias-por-skill.html` (guías por skill).
