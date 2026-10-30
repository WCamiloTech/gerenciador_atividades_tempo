# Padrões de desenvolvimento

1. Consultar requisitos, checklist e histórico antes de alterar código.
2. Implementar alterações pequenas, modulares e testáveis.
3. Antes de migrações: backup consistente do SQLite e teste de restauração.
4. Rodar pytest, Vitest, Playwright e regressão conforme módulos disponíveis.
5. Registrar resultados reais, pendências, data/hora com fuso, hashes SHA-256 e commit.
6. Não marcar etapa como aplicada sem evidências de testes e validação.
7. Separar dados reais, segredos e backups do Git.
8. Para entrega, preparar ZIP em Downloads, instruções de instalação, rollback e commit Conventional Commits.
9. Preferir scripts idempotentes e importação transacional com modo prévia.
10. Registrar ideias novas sem implementá-las fora do escopo aprovado.
