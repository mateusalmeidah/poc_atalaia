# Requirements Document

PoC 0.1 - Motor de apoio à decisão LGPD/LAI.

## Introduction

Esta PoC implementa um motor **determinístico, auditável e testável** de apoio à decisão
no dilema LGPD/LAI. O motor recebe um caso sintético, detecta sinais de dado pessoal (PII)
e de interesse de transparência (LAI), produz uma **recomendação de fluxo de governança**
(nunca um parecer jurídico), escala conflitos para revisão humana e registra a análise em
um GOV-ADR. A contribuição está na orquestração da decisão e da evidência, não na
sofisticação do classificador.

Escopo fechado conforme `POC-01-ESCOPO.md` e `AGENTS.md`. Sem LLM, APIs externas, cloud,
banco de dados, Presidio, ARX, AMNESIA ou eMAG. Apenas dados fictícios.

## Glossary

- **PII**: sinais de dado pessoal (CPF, e-mail, telefone, marcador explícito de pessoa).
- **LAI**: sinais de interesse de transparência (gasto público, contrato, benefício,
  decisão administrativa, informação de interesse coletivo).
- **GOV-ADR**: registro Markdown auditável de uma análise e sua justificativa.
- **Recomendação de fluxo**: um dos valores de `PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL`,
  `REVISAR_DADOS_PESSOAIS`, `REVISAR_TRANSPARENCIA`, `ESCALAR_HUMANO`.

## Requirements

### Requisito 1 - Detecção determinística de PII (CHK-01)

**História:** Como validador técnico, quero que o motor detecte padrões mínimos de dado
pessoal de forma determinística, para que a análise seja reprodutível e testável.

#### Critérios de aceite

1. QUANDO o texto de um caso contém um CPF em formato textual reconhecível ENTÃO o sistema
   DEVE marcar `dados_pessoais_detectados = true` e incluir `CPF` em `sinais_pii`.
2. QUANDO o texto contém um e-mail ENTÃO o sistema DEVE incluir `EMAIL` em `sinais_pii`.
3. QUANDO o texto contém um telefone em formato reconhecível ENTÃO o sistema DEVE incluir
   `TELEFONE` em `sinais_pii`.
4. QUANDO o texto contém um marcador explícito de nome/pessoa ENTÃO o sistema DEVE incluir
   `NOME` em `sinais_pii`.
5. QUANDO o mesmo tipo de sinal aparece múltiplas vezes ENTÃO o sistema DEVE listar o tipo
   uma única vez em `sinais_pii`.
6. QUANDO nenhum padrão de PII é encontrado ENTÃO o sistema DEVE retornar
   `dados_pessoais_detectados = false` e `sinais_pii = []`.
7. A detecção NÃO DEVE usar NER, LLM ou serviços externos; apenas regex/padrões locais.

### Requisito 2 - Detecção determinística de sinais de transparência/LAI (CHK-02)

**História:** Como validador técnico, quero que o motor detecte sinais mínimos de interesse
de transparência a partir de uma taxonomia explícita, para que a análise seja auditável.

#### Critérios de aceite

1. O sistema DEVE reconhecer os sinais da taxonomia: `GASTO_PUBLICO`, `CONTRATO`,
   `BENEFICIO_PUBLICO`, `DECISAO_ADMINISTRATIVA`, `INTERESSE_COLETIVO`.
2. QUANDO o texto ou metadados contêm palavras-chave associadas a um sinal da taxonomia
   ENTÃO o sistema DEVE incluir esse sinal em `sinais_lai`.
3. QUANDO há sinais de transparência ENTÃO o sistema DEVE retornar
   `interesse_transparencia_detectado = true`.
4. QUANDO nenhum sinal de transparência é encontrado ENTÃO o sistema DEVE retornar
   `interesse_transparencia_detectado = false` e `sinais_lai = []`.
5. A detecção PODE combinar palavras-chave do texto e metadados simples da entrada.
6. QUANDO o mesmo sinal é acionado por múltiplas palavras-chave ENTÃO o sistema DEVE
   listar o sinal uma única vez.

### Requisito 3 - Escalada obrigatória em conflito (CHK-03)

**História:** Como responsável pela governança, quero que casos com dado pessoal e
interesse de transparência simultâneos sejam escalados para humano, para falhar para o
lado seguro.

#### Critérios de aceite

1. QUANDO `dados_pessoais_detectados = true` E `interesse_transparencia_detectado = true`
   ENTÃO o sistema DEVE retornar `recomendacao = ESCALAR_HUMANO`.
2. QUANDO ocorre o conflito ENTÃO o sistema DEVE retornar
   `revisao_humana_obrigatoria = true`.
3. QUANDO ocorre o conflito ENTÃO o sistema NÃO DEVE emitir qualquer decisão de
   divulgação ou restrição.

### Requisito 4 - Não decidir juridicamente (CHK-04)

**História:** Como encarregado de dados, quero garantir que o motor nunca tome decisão
final automática, para preservar o julgamento humano.

#### Critérios de aceite

1. O conjunto de recomendações possíveis DEVE ser exatamente
   `{PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL, REVISAR_DADOS_PESSOAIS, REVISAR_TRANSPARENCIA, ESCALAR_HUMANO}`.
2. O sistema NÃO DEVE produzir `PUBLICAR`, `RESTRINGIR` ou `ANONIMIZAR` como recomendação.
3. O sistema NÃO DEVE afirmar conformidade com LGPD ou LAI em nenhuma saída.
4. QUANDO apenas PII é detectada ENTÃO a recomendação DEVE ser `REVISAR_DADOS_PESSOAIS`.
5. QUANDO apenas transparência é detectada ENTÃO a recomendação DEVE ser
   `REVISAR_TRANSPARENCIA`.
6. QUANDO nada é detectado ENTÃO a recomendação DEVE ser
   `PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL`.

### Requisito 5 - Explicabilidade (CHK-05)

**História:** Como auditor, quero que toda análise traga os motivos e regras acionadas,
para que a recomendação seja explicável.

#### Critérios de aceite

1. Toda análise DEVE retornar uma lista `motivos` não vazia descrevendo por que a
   recomendação foi produzida.
2. Toda análise DEVE registrar as regras acionadas de forma rastreável até os sinais
   detectados.
3. QUANDO um sinal contribui para a recomendação ENTÃO o motivo correspondente DEVE
   referenciar esse sinal.

### Requisito 6 - Geração de GOV-ADR (CHK-06)

**História:** Como responsável institucional, quero que cada análise possa gerar um
GOV-ADR com decisão humana inicialmente `PENDENTE`, para manter trilha de evidência.

#### Critérios de aceite

1. O sistema DEVE poder gerar um arquivo Markdown em
   `spec/decisoes/GOV-ADR-NNNN--<slug>.md`.
2. O GOV-ADR DEVE conter: contexto, sinais encontrados, recomendação do motor, regras
   acionadas, necessidade de revisão humana, decisão humana `PENDENTE`, evidências,
   timestamp e versão do motor.
3. A decisão humana DEVE iniciar sempre como `PENDENTE`.
4. O número `NNNN` DEVE ter 4 dígitos com zero à esquerda e o `<slug>` DEVE derivar do
   identificador do caso.
5. O formato do GOV-ADR DEVE ser estável e legível por humanos.

### Requisito 7 - Apenas dados fictícios (CHK-07)

**História:** Como pesquisador, quero garantir que nenhum exemplo ou teste contenha dado
pessoal real, para respeitar as restrições éticas e legais.

#### Critérios de aceite

1. Todos os fixtures em `examples/` e `tests/` DEVEM conter apenas dados sintéticos.
2. O relatório final DEVE declarar explicitamente a ausência de dados reais.
3. CPFs usados em exemplos DEVEM ser claramente fictícios.

### Requisito 8 - Suíte de testes por comando único (CHK-08)

**História:** Como validador, quero executar toda a suíte com um único comando
documentado e vê-la passar, para comprovar os critérios de aceite.

#### Critérios de aceite

1. A suíte DEVE ser executável por um único comando documentado (`pytest`).
2. A suíte DEVE cobrir CHK-01 a CHK-07.
3. A saída do pytest DEVE ser registrada em
   `saida_para_chatgpt/02_TESTES_E_RESULTADOS.md`.
4. A suíte DEVE terminar sem falhas.

### Requisito 9 - Entrada/saída e CLI

**História:** Como usuário, quero rodar a análise de um caso via CLI e receber resultado
legível e estruturado, para validar o fluxo ponta a ponta.

#### Critérios de aceite

1. O sistema DEVE aceitar um caso em JSON contendo no mínimo `caso_id`, `titulo`,
   `descricao` e opcionalmente `metadados`.
2. QUANDO o comando `analyze <arquivo.json>` é executado ENTÃO o sistema DEVE imprimir
   um resultado legível no terminal.
3. O sistema DEVE produzir saída estruturada equivalente ao modelo de `AGENTS.md`
   (`caso_id`, `dados_pessoais_detectados`, `sinais_pii`,
   `interesse_transparencia_detectado`, `sinais_lai`, `recomendacao`,
   `revisao_humana_obrigatoria`, `motivos`, `gov_adr`).
4. QUANDO solicitado ENTÃO a CLI DEVE gerar o GOV-ADR correspondente e referenciar seu
   caminho na saída.

### Requisito 10 - Tratamento de erro

**História:** Como usuário, quero mensagens de erro claras quando a entrada é inválida,
para corrigir rapidamente sem comportamento indefinido.

#### Critérios de aceite

1. QUANDO o arquivo de entrada não existe ENTÃO o sistema DEVE emitir mensagem de erro
   clara e encerrar com código de saída diferente de zero.
2. QUANDO o JSON é inválido ENTÃO o sistema DEVE emitir mensagem de erro clara indicando
   o problema de parsing.
3. QUANDO campos obrigatórios estão ausentes ENTÃO o sistema DEVE indicar quais campos
   faltam.
4. O sistema NÃO DEVE produzir rastreamento de pilha bruto como única resposta a erro
   de entrada.
