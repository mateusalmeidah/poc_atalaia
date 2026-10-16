# Implementation Plan: PoC 0.1 LGPD/LAI

## Overview

Plano incremental de implementação do motor determinístico LGPD/LAI. Cada bloco de
produção vem acompanhado dos seus testes; a suíte deve ser executada ao final de cada
conjunto relevante de tarefas.

## Tasks

- [x] 1. Preparar estrutura do projeto e empacotamento
  - Criar `pyproject.toml` (nome do pacote, Python 3.11+, pytest como dev), `README.md`
    com o comando único de testes, pastas `src/atalaia_governanca/`, `tests/`,
    `examples/`, `spec/decisoes/`.
  - Criar `__init__.py` com `VERSAO_MOTOR = "0.1.0"`.
  - _Requisitos: 8, 9_

- [x] 2. Implementar modelos de entrada/saída
  - [x] 2.1 Definir enums `Recomendacao`, `SinalPII`, `SinalLAI` (herança `str, Enum`).
    - _Requisitos: 4.1, 4.2, 1, 2_
  - [x] 2.2 Definir dataclasses `Caso` e `Resultado` com `to_dict()`.
    - _Requisitos: 9.3, 5_
  - [x] 2.3 Definir `CasoInvalidoError` e `carregar_caso(path)` com validação de campos.
    - _Requisitos: 10.1, 10.2, 10.3_
  - [x] 2.4 Teste de contrato de saída (enum fechado, campos presentes).
    - _Requisitos: 4.1, 4.2, 5.1_

- [x] 3. Implementar detectores de PII
  - [x] 3.1 Regex de CPF, EMAIL, TELEFONE e marcador NOME; dedup preservando ordem.
    - _Requisitos: 1.1, 1.2, 1.3, 1.4, 1.5, 1.7_
  - [x] 3.2 Testes positivos, negativos e de deduplicação de PII.
    - _Requisitos: 1.1-1.6_

- [x] 4. Implementar detectores de LAI
  - [x] 4.1 Taxonomia -> palavras-chave; normalização (lowercase + sem acento);
    combinar texto e metadados; dedup.
    - _Requisitos: 2.1, 2.2, 2.5, 2.6_
  - [x] 4.2 Testes positivos, negativos e de combinação texto+metadados.
    - _Requisitos: 2.1-2.6_

- [x] 5. Implementar regras de decisão
  - [x] 5.1 `decidir(...)` com a tabela de decisão, motivos e `regras_acionadas`;
    precedência do conflito.
    - _Requisitos: 3.1, 3.2, 3.3, 4.4, 4.5, 4.6, 5.1, 5.2, 5.3_
  - [x] 5.2 Testes cobrindo os 4 ramos + ausência de PUBLICAR/RESTRINGIR/ANONIMIZAR.
    - _Requisitos: 3, 4_

- [x] 6. Implementar o motor de orquestração
  - [x] 6.1 `analisar(caso) -> Resultado` integrando detectores + regras.
    - _Requisitos: 9.3, 5_
  - [x] 6.2 Testes de integração dos casos mínimos CASO-001..004.
    - _Requisitos: 1, 2, 3, 4, 5_

- [x] 7. Implementar geração de GOV-ADR
  - [x] 7.1 `slugify`, `proximo_numero`, `gerar_gov_adr` com template estável e
    decisão humana `PENDENTE`; `agora` injetável.
    - _Requisitos: 6.1, 6.2, 6.3, 6.4, 6.5_
  - [x] 7.2 Testes de numeração, slug, seções obrigatórias e `PENDENTE`.
    - _Requisitos: 6_

- [x] 8. Implementar a CLI
  - [x] 8.1 `analyze <arquivo.json> [--gov-adr] [--json]` com saída legível e
    estruturada; tratamento de erro com mensagens claras e código de saída.
    - _Requisitos: 9.1, 9.2, 9.3, 9.4, 10.1, 10.2, 10.3, 10.4_
  - [x] 8.2 Testes de CLI: saída dos casos, flags e cenários de erro.
    - _Requisitos: 9, 10_

- [x] 9. Criar exemplos sintéticos
  - Criar `examples/caso_01.json` (só PII), `caso_02.json` (só transparência),
    `caso_03.json` (conflito), `caso_04.json` (neutro). CPFs claramente fictícios.
  - _Requisitos: 7.1, 7.3_

- [x] 10. Fechamento e evidências
  - [x] 10.1 Executar `pytest` e garantir suíte verde.
    - _Requisitos: 8.1, 8.2, 8.4_
  - [x] 10.2 Executar os 4 exemplos pela CLI gerando GOV-ADRs em `spec/decisoes/`.
    - _Requisitos: 6, 9_
  - [x] 10.3 Preencher `saida_para_chatgpt/` (00..04) substituindo placeholders,
    incluindo saída do pytest e declaração de ausência de dados reais.
    - _Requisitos: 7.2, 8.3_

## Task Dependency Graph

Ondas de execução (tarefas na mesma onda podem ser paralelizadas):

```json
{
  "waves": [
    { "wave": 1, "tasks": ["1"] },
    { "wave": 2, "tasks": ["2"] },
    { "wave": 3, "tasks": ["3", "4", "5"] },
    { "wave": 4, "tasks": ["6"] },
    { "wave": 5, "tasks": ["7"] },
    { "wave": 6, "tasks": ["8"] },
    { "wave": 7, "tasks": ["9"] },
    { "wave": 8, "tasks": ["10"] }
  ]
}
```

- 1 é pré-requisito de tudo.
- 2 habilita 3, 4 e 5 (independentes entre si).
- 6 depende de 3, 4 e 5.
- 7, 8, 9, 10 são sequenciais após 6.

## Notes

- Não ampliar o escopo além de `POC-01-ESCOPO.md`.
- Usar apenas dados fictícios; CPFs claramente falsos.
- Nenhuma decisão jurídica final automática; conflito PII+LAI sempre escala.
- Rodar `pytest` ao final de cada bloco relevante.

