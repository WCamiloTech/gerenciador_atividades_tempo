# GAT — Etapa 0.2 — Modelo lógico de dados (proposta para validação)

## Princípio
O lançamento espontâneo é a operação principal. Planejamento é opcional. A atividade descreve o acontecimento; sessões registram intervalos temporais, inclusive múltiplos períodos associados à mesma atividade.

## Entidades

### categorias
- id: UUID, chave primária
- nome: texto obrigatório, único (comparação sem diferenciar maiúsculas/minúsculas)
- cor: texto opcional
- ativa: booleano

### atividades
- id: UUID, chave primária
- titulo: texto obrigatório (ex.: Estudo)
- descricao: texto opcional (ex.: Python: classes)
- sobre: texto opcional (compatibilidade com a planilha)
- categoria_id: UUID opcional, FK categorias
- status: em_andamento | pausada | finalizada | cancelada
- origem: espontanea | prevista | agendada (padrão espontanea)
- observacoes: texto opcional
- link: texto opcional
- criada_em, atualizada_em: timestamps
- excluida_em: timestamp opcional (exclusão lógica)

### sessoes_tempo
- id: UUID, chave primária
- atividade_id: UUID obrigatório, FK atividades
- inicio_em: timestamp obrigatório
- fim_em: timestamp opcional
- criada_em, atualizada_em: timestamps
- observacoes: texto opcional

### previsoes (recurso opcional, posterior)
- id: UUID, chave primária
- atividade_id: UUID obrigatório, FK atividades
- data_prevista: data opcional
- inicio_previsto, fim_previsto: timestamps opcionais
- observacoes: texto opcional

### historico_alteracoes
- id: UUID, chave primária
- entidade, entidade_id, operacao: textos obrigatórios
- antes_json, depois_json: JSON opcional
- registrada_em: timestamp obrigatório
- origem: interface | importacao | sistema

### importacoes
- id: UUID, chave primária
- nome_arquivo, hash_sha256: textos obrigatórios
- iniciada_em, concluida_em: timestamps
- total_linhas, importadas, ignoradas, rejeitadas: inteiros
- relatorio_json: JSON opcional

## Regras de negócio
1. Início pode existir sem fim; atividade em andamento permanece após fechar o navegador.
2. Fim deve ser posterior ou igual ao início; para atravessar meia-noite, usar datas completas.
3. Duração é derivada de fim - início, nunca um valor independente editável para sessões normais.
4. Registros sem término não entram no total consolidado; tempo decorrido pode aparecer como estimativa visual.
5. Intervalos sobrepostos são sinalizados; dashboards distinguem soma bruta e tempo exclusivo (união de intervalos).
6. Horários são persistidos em UTC e apresentados no fuso configurado; importações antigas sem fuso usam o fuso escolhido para a fonte.
7. Exclusão lógica preserva rastreabilidade; dados reais não são versionados no Git.
8. Migrações de banco são versionadas; testes usam banco temporário independente.
9. Importações preservam número da linha original e relatam registros inválidos, sem descartar silenciosamente.
10. Uma sessão em andamento por atividade, salvo decisão explícita posterior sobre paralelismo.

## Questões a validar
- Manter uma única atividade em andamento globalmente ou permitir simultâneas?
- A atividade 'Estudo' deve representar um lançamento diário ou um agrupamento reutilizável de várias sessões?
- Observações históricas 1–5 serão concatenadas com rótulos ou preservadas como itens separados na importação?
