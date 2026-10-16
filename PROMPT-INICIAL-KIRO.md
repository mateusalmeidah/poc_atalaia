# Prompt para iniciar a PoC no Kiro

Copie e cole o texto abaixo no chat do Kiro depois de abrir este projeto.

---

Você está trabalhando em uma PoC acadêmica associada ao framework ATALAIA da UFS.

Antes de fazer qualquer alteração, leia integralmente:

- `AGENTS.md`
- `POC-01-ESCOPO.md`
- todos os arquivos em `.kiro/steering/`

## Sua primeira tarefa NÃO é implementar

Primeiro crie uma Kiro Spec chamada:

`poc-01-lgpd-lai`

A spec deve possuir as fases normais do Kiro:

1. requirements;
2. design;
3. tasks.

Salve-a em `.kiro/specs/poc-01-lgpd-lai/`.

### Requirements

Transforme os objetivos e CHKs de `POC-01-ESCOPO.md` em requisitos claros e verificáveis. Não amplie o escopo.

### Design

Desenhe uma arquitetura Python mínima. Deve conter:

- modelos de entrada/saída;
- detectores determinísticos;
- regras de decisão;
- geração de GOV-ADR;
- CLI;
- testes;
- tratamento de erro.

Não use LLM, API externa, Presidio, ARX ou banco de dados.

### Tasks

Quebre a implementação em tarefas pequenas, preferencialmente com testes associados.

## Ponto de controle obrigatório

Depois de criar `requirements.md`, `design.md` e `tasks.md`, PARE.

Mostre no chat:
- um resumo da spec;
- riscos ou ambiguidades encontrados;
- lista de arquivos que pretende criar;
- qualquer ponto em que sua proposta difira de `POC-01-ESCOPO.md`.

Não inicie a implementação até receber autorização explícita do usuário.

## Depois da autorização

Implemente a spec de forma incremental.

Regras obrigatórias:
- use apenas dados fictícios;
- não tome decisão jurídica final;
- `dado pessoal + interesse de transparência` deve escalar para humano;
- cada recomendação deve trazer motivos;
- todo GOV-ADR deve iniciar com decisão humana `PENDENTE`;
- execute a suíte de testes ao final de cada conjunto relevante de tarefas;
- não altere as instruções deste pacote para facilitar testes.

## Ao concluir

Preencha obrigatoriamente os arquivos em `saida_para_chatgpt/` conforme os templates existentes.

Inclua:
- o que foi implementado;
- estrutura final;
- resultados dos testes;
- exemplos executados;
- decisões tomadas;
- limitações;
- desvios da spec;
- próximos passos.

Não apague os templates; substitua os placeholders pelo conteúdo real.

Finalize informando ao usuário que a pasta `saida_para_chatgpt/` está pronta para ser enviada ao ChatGPT.
