# Requisitos — GAT (Etapa 0)

- RF-001 Registrar atividade espontânea com data e início; término opcional.
- RF-002 Concluir atividade posteriormente com horário de término editável.
- RF-003 Calcular duração; tratar virada de dia e sessões incompletas.
- RF-004 Registrar categoria, descrição, detalhe ('Sobre'), observações e link.
- RF-005 Visualizar atividades em cards e tabela, preservando filtros e preferência.
- RF-006 Consultar histórico e filtrar por período, categoria e texto.
- RF-007 Exibir dashboards de duração por categoria e período, com distinção entre contagem e tempo.
- RF-008 Importar dados Excel/CSV com prévia, validação, detecção de duplicatas e relatório de erros.
- RF-009 Exportar CSV e backup/restauração JSON versionado.
- RF-010 Permitir planejamento/agendamento apenas como recursos opcionais.
- RF-011 Registrar trilha de alterações e manter backups antes de migrações.
- RF-012 Manter arquitetura modular, testes automatizados e interface responsiva.

## Critérios transversais
- Preservar planilha de origem e banco existente.
- Sem perda silenciosa de registros inválidos; registrar linhas rejeitadas.
- Evitar contagem dupla de intervalos sobrepostos nos indicadores de tempo exclusivo.
- Dados pessoais e bancos reais não entram no repositório Git.
