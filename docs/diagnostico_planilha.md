# Diagnóstico inicial — Pasta2.xlsx

- Aba: Registro.
- Título na linha 1, área de resumos e instruções acima da tabela.
- Cabeçalhos na linha 15; registros começam na linha 16.
- Campos: Dia, Mês, Ano, Mês/Ano, Data2, Horário_Inicio, Horário Fim, Tempo_Min, Temp_H, Atividade_Descrição, Tipo, Sobre, Observações_1, Observações_2, Observações_3, Observações_4, Observações_5, Link.
- Categorias observadas: Estudos, Trabalho, Pessoal.
- Célula N3 contém resultado de fórmula com erro #NAME? no arquivo armazenado; não usar células-resumo como fonte da migração.
- Datas e horas podem estar armazenadas como números seriais Excel; converter explicitamente e testar precisão de minutos.
- Linhas com fórmulas, resumos ou células vazias não devem ser importadas como registros.

## Verificações pendentes antes da migração
- Mapear registros sem data, descrição, categoria ou horário.
- Detectar durações negativas, sobreposições, datas inconsistentes e duplicatas.
- Verificar fórmula e formatação de Tempo_Min e Temp_H, inclusive cruzamento da meia-noite.
- Estabelecer política para múltiplas observações e links.
