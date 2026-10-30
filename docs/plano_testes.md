# GAT — Etapa 0.2 — Plano de testes automatizados

| ID | Cenário | Tipo | Resultado esperado |
|---|---|---|---|
| T-001 | Criar atividade sem término | API/integração | Registro persistido, situação em andamento |
| T-002 | Finalizar após reiniciar aplicação | integração | Término salvo e duração correta |
| T-003 | Início 23:40, fim 00:20 dia seguinte | unitário | 40 minutos |
| T-004 | Término anterior ao início | unitário/API | Validação impede intervalo inválido |
| T-005 | Sessões 09–10 e 09:30–11 | unitário | Bruto 150 min, exclusivo 120 min |
| T-006 | Alternar Blocos/Lista com filtro | Playwright | Mesmos registros e filtros |
| T-007 | Reabrir página | Playwright | Preferência de visualização mantida |
| T-008 | Importar linha inválida do Excel | integração | Linha reportada; nenhuma perda silenciosa |
| T-009 | Reimportar mesmo arquivo | integração | Duplicatas identificadas |
| T-010 | Exportar/restaurar backup JSON | integração | Dados equivalentes após restauração |

A suíte será implementada na Etapa 1 e ampliada em cada funcionalidade. Nenhum teste está marcado como executado nesta etapa documental.
