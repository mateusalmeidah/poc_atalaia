# Estrutura e arquivos - preencher ao final

## Árvore final do projeto

```text
ATALAIA_POC01_KIRO/
├── .kiro/
│   ├── steering/
│   │   ├── governanca-atalaia.md
│   │   ├── product.md
│   │   ├── structure.md
│   │   └── tech.md
│   └── specs/
│       └── poc-01-lgpd-lai/
│           ├── requirements.md
│           ├── design.md
│           └── tasks.md
├── src/
│   └── atalaia_governanca/
│       ├── __init__.py
│       ├── models.py
│       ├── detectors.py
│       ├── rules.py
│       ├── engine.py
│       ├── gov_adr.py
│       └── cli.py
├── examples/
│   ├── caso_01.json
│   ├── caso_02.json
│   ├── caso_03.json
│   └── caso_04.json
├── spec/
│   └── decisoes/
│       ├── GOV-ADR-0001--caso-001.md
│       ├── GOV-ADR-0002--caso-002.md
│       ├── GOV-ADR-0003--caso-003.md
│       └── GOV-ADR-0004--caso-004.md
├── tests/
│   ├── test_detectors.py
│   ├── test_rules.py
│   ├── test_engine.py
│   ├── test_gov_adr.py
│   ├── test_cli.py
│   └── test_contrato_saida.py
├── saida_para_chatgpt/
│   ├── 00_RESUMO_EXECUTIVO.md
│   ├── 01_ESTRUTURA_E_ARQUIVOS.md
│   ├── 02_TESTES_E_RESULTADOS.md
│   ├── 03_DECISOES_LIMITACOES.md
│   └── 04_PROXIMOS_PASSOS.md
├── pyproject.toml
├── README.md
├── AGENTS.md
├── POC-01-ESCOPO.md
└── PROMPT-INICIAL-KIRO.md
```

## Arquivos criados

- Spec: `.kiro/specs/poc-01-lgpd-lai/{requirements,design,tasks}.md`
- Código: `src/atalaia_governanca/{__init__,models,detectors,rules,engine,gov_adr,cli}.py`
- Exemplos: `examples/caso_0{1,2,3,4}.json`
- Testes: `tests/test_{detectors,rules,engine,gov_adr,cli,contrato_saida}.py`
- Empacotamento/doc: `pyproject.toml`, `README.md`

## Arquivos alterados

- `README.md` (substituído o conteúdo inicial do pacote pela documentação da PoC).
- `saida_para_chatgpt/00..04` (placeholders substituídos por conteúdo real).

## Arquivos gerados automaticamente

- `spec/decisoes/GOV-ADR-0001--caso-001.md`
- `spec/decisoes/GOV-ADR-0002--caso-002.md`
- `spec/decisoes/GOV-ADR-0003--caso-003.md`
- `spec/decisoes/GOV-ADR-0004--caso-004.md`
