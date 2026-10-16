# Design Document

PoC 0.1 - Motor de apoio à decisão LGPD/LAI.

## Overview

Arquitetura Python mínima, determinística e sem dependências externas além de `pytest`
(dev). O fluxo é um pipeline linear:

```
JSON do caso -> models.Caso -> detectors (PII + LAI) -> rules (decisão) -> engine
            -> Resultado -> (opcional) gov_adr -> Markdown
            -> cli (impressão + saída estruturada)
```

Princípios aplicados: spec como fonte da verdade, determinismo, explicabilidade,
escalada no conflito, decisão final sempre humana.

## Architecture

### Estrutura de pastas

```text
.
├── src/atalaia_governanca/
│   ├── __init__.py          # expõe VERSAO_MOTOR e API pública
│   ├── models.py            # dataclasses de entrada/saída + enums
│   ├── detectors.py         # detecção determinística de PII e LAI
│   ├── rules.py             # regras de decisão -> recomendação + motivos
│   ├── engine.py            # orquestra detectores + regras
│   ├── gov_adr.py           # geração do Markdown GOV-ADR
│   └── cli.py               # interface de linha de comando
├── examples/
│   ├── caso_01.json         # só PII
│   ├── caso_02.json         # só transparência
│   ├── caso_03.json         # conflito
│   └── caso_04.json         # neutro
├── spec/decisoes/           # GOV-ADRs gerados (saída de evidência)
├── tests/
│   ├── test_detectors.py
│   ├── test_rules.py
│   ├── test_engine.py
│   ├── test_gov_adr.py
│   ├── test_cli.py
│   └── test_contrato_saida.py
├── saida_para_chatgpt/      # relatório final (já existe)
├── pyproject.toml
└── README.md
```

## Data Models

Modelos de entrada/saída definidos em `models.py`.

### Enums

```python
class Recomendacao(str, Enum):
    PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL = "PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL"
    REVISAR_DADOS_PESSOAIS = "REVISAR_DADOS_PESSOAIS"
    REVISAR_TRANSPARENCIA = "REVISAR_TRANSPARENCIA"
    ESCALAR_HUMANO = "ESCALAR_HUMANO"

class SinalPII(str, Enum):
    CPF = "CPF"; EMAIL = "EMAIL"; TELEFONE = "TELEFONE"; NOME = "NOME"

class SinalLAI(str, Enum):
    GASTO_PUBLICO = "GASTO_PUBLICO"
    CONTRATO = "CONTRATO"
    BENEFICIO_PUBLICO = "BENEFICIO_PUBLICO"
    DECISAO_ADMINISTRATIVA = "DECISAO_ADMINISTRATIVA"
    INTERESSE_COLETIVO = "INTERESSE_COLETIVO"
```

Herdar de `str, Enum` mantém os valores serializáveis em JSON diretamente.

### Dataclasses

```python
@dataclass
class Caso:
    caso_id: str
    titulo: str
    descricao: str
    metadados: dict = field(default_factory=dict)

@dataclass
class Resultado:
    caso_id: str
    dados_pessoais_detectados: bool
    sinais_pii: list[str]
    interesse_transparencia_detectado: bool
    sinais_lai: list[str]
    recomendacao: str
    revisao_humana_obrigatoria: bool
    motivos: list[str]
    regras_acionadas: list[str]
    gov_adr: str | None = None
    def to_dict(self) -> dict: ...
```

`regras_acionadas` dá rastreabilidade (Req 5). `gov_adr` é preenchido só quando o arquivo
é gerado.

## Components and Interfaces

### Detectores (detectors.py)

Funções puras, sem estado, baseadas em regex compilado a nível de módulo.

- `detectar_pii(texto: str) -> list[SinalPII]`
  - CPF: `\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b` (apenas padrão textual; sem validação de
    dígito verificador para manter PoC simples e previsível).
  - EMAIL: regex padrão de e-mail.
  - TELEFONE: `\b(?:\(?\d{2}\)?\s?)?\d{4,5}-?\d{4}\b`.
  - NOME: marcador explícito, ex.: tokens `nome:` / `pessoa:` no texto ou metadados.
  - Dedup preservando ordem de descoberta.
- `detectar_lai(texto: str, metadados: dict) -> list[SinalLAI]`
  - Dicionário taxonomia -> conjunto de palavras-chave (lowercase, sem acento).
  - Combina texto + valores de metadados relevantes.
  - Dedup preservando ordem da taxonomia.

Normalização: lowercase + remoção de acentos para o casamento de LAI (via
`unicodedata`), mantendo a biblioteca padrão.

### Regras de decisão (rules.py)

`decidir(sinais_pii, sinais_lai) -> (Recomendacao, motivos, regras_acionadas, revisao)`

Tabela de decisão (determinística e exaustiva):

| PII | LAI | Recomendação | Revisão humana |
|-----|-----|--------------|----------------|
| sim | sim | ESCALAR_HUMANO | true |
| sim | não | REVISAR_DADOS_PESSOAIS | true |
| não | sim | REVISAR_TRANSPARENCIA | false |
| não | não | PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL | false |

- Cada ramo adiciona motivos citando os sinais e um identificador de regra
  (ex.: `R-CONFLITO`, `R-PII`, `R-LAI`, `R-NEUTRO`).
- O ramo de conflito tem precedência (fail-safe: escalar, não decidir).
- Nenhum ramo emite PUBLICAR/RESTRINGIR/ANONIMIZAR.

### Motor (engine.py)

`analisar(caso: Caso) -> Resultado`

1. Concatena `titulo + descricao` para busca textual.
2. Chama detectores.
3. Chama `rules.decidir`.
4. Monta `Resultado` com flags, sinais (como strings), motivos e regras.
5. Não gera GOV-ADR por si; a geração é responsabilidade explícita de quem chama
   (CLI com flag ou função dedicada), mantendo separação código/evidência.

### GOV-ADR (gov_adr.py)

- `proximo_numero(dir_decisoes) -> int`: varre `GOV-ADR-\d{4}--` e retorna o próximo.
- `slugify(caso_id) -> str`: minúsculas, hífens, ASCII.
- `gerar_gov_adr(resultado, dir_decisoes, agora=None) -> Path`: escreve o Markdown com
  seções fixas e decisão humana `PENDENTE`. `agora` injetável para testes determinísticos.

Template (estável):

```markdown
# GOV-ADR-0001 -- CASO-001

- Timestamp: 2026-01-01T00:00:00
- Versão do motor: 0.1.0

## Contexto
...

## Sinais encontrados
- PII: CPF, EMAIL
- LAI: GASTO_PUBLICO

## Recomendação do motor
ESCALAR_HUMANO

## Regras acionadas
- R-CONFLITO: ...

## Necessidade de revisão humana
Obrigatória

## Decisão humana
PENDENTE

## Evidências
- motivos ...
```

### CLI (cli.py)

- Executável via `python -m atalaia_governanca.cli`.
- Subcomando `analyze <arquivo.json> [--gov-adr] [--json]`.
- `argparse` da biblioteca padrão.
- Fluxo: carrega JSON -> valida -> `engine.analisar` -> imprime legível; com `--json`
  imprime o dict; com `--gov-adr` gera o arquivo e mostra o caminho.
- Erros tratados (Req 10) com mensagem clara e `sys.exit(código != 0)`.

## Correctness Properties

Propriedades invariantes que os testes devem garantir:

### Property 1: Enum fechado
`recomendacao` sempre pertence a
`{PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL, REVISAR_DADOS_PESSOAIS, REVISAR_TRANSPARENCIA, ESCALAR_HUMANO}`
e nunca a `PUBLICAR/RESTRINGIR/ANONIMIZAR`.
**Validates: Requirements 4.1, 4.2**

### Property 2: Fail-safe no conflito
PII ∧ LAI ⇒ `ESCALAR_HUMANO` e `revisao_humana_obrigatoria = true`.
**Validates: Requirements 3.1, 3.2**

### Property 3: Explicabilidade
`motivos` nunca vazio para qualquer entrada válida.
**Validates: Requirements 5.1**

### Property 4: Determinismo
A mesma entrada produz sempre o mesmo resultado (sem estado global, sem fonte de
aleatoriedade; timestamp injetável).
**Validates: Requirements 6.1**

### Property 5: GOV-ADR PENDENTE
Todo GOV-ADR gerado inicia a decisão humana como `PENDENTE`.
**Validates: Requirements 6.3**

### Property 6: Dedup
`sinais_pii` e `sinais_lai` nunca contêm valores repetidos.
**Validates: Requirements 1.5, 2.6**

## Error Handling

- `CasoInvalidoError` para campos ausentes/entrada malformada.
- `carregar_caso(path)` cobre: arquivo inexistente (`FileNotFoundError` -> mensagem),
  JSON inválido (`json.JSONDecodeError` -> mensagem), campos obrigatórios ausentes.
- A CLI captura essas exceções e converte em mensagem amigável + código de saída.

## Testing Strategy

- `test_detectors.py`: CHK-01, CHK-02 (positivos, negativos, dedup).
- `test_rules.py`: CHK-03, CHK-04 (tabela de decisão completa + ausência de ações finais).
- `test_engine.py`: integração dos 4 casos mínimos (CASO-001..004).
- `test_gov_adr.py`: CHK-06 (numeração, slug, decisão PENDENTE, seções obrigatórias).
- `test_cli.py`: Req 9 e Req 10 (saída, flags, erros).
- `test_contrato_saida.py`: CHK-04/CHK-05 (enum fechado, motivos sempre presentes).
- Fixtures só com dados fictícios (CHK-07); CPFs claramente falsos.

## Decisões de design

1. **Enums `str`** para serialização JSON direta e comparação legível em testes.
2. **CPF sem validação de dígito** — a PoC prova fluxo, não robustez do detector; evita
   falso negativo em CPFs sintéticos.
3. **Geração de GOV-ADR fora do engine** — respeita "não misturar evidência com código"
   e torna o engine puro/testável.
4. **Sem dependências de runtime** — só biblioteca padrão; `pytest` apenas em dev.
5. **`agora` injetável** no GOV-ADR para timestamp determinístico nos testes.

