# Testes e resultados - preencher ao final

## Comando de teste

```bash
pytest
```

## Resultado completo/resumido

```text
============================= 38 passed in 0.42s ==============================
```

Todos os 38 testes passam. Cobertura por arquivo:

- `test_detectors.py` (13): CHK-01, CHK-02 — positivos, negativos, dedup, acentuação,
  metadados.
- `test_rules.py` (6): CHK-03, CHK-04, CHK-05 — tabela de decisão e ausência de ações
  finais.
- `test_engine.py` (4): integração dos casos mínimos CASO-001..004.
- `test_gov_adr.py` (5): CHK-06 — numeração, slug, seções, `PENDENTE`, timestamp.
- `test_cli.py` (6): Req 9 e Req 10 — saída legível/JSON, `--gov-adr`, erros.
- `test_contrato_saida.py` (4): CHK-04/CHK-05 — enum fechado, motivos sempre presentes.

## Casos executados

### CASO-001

Apenas PII. `sinais_pii = [CPF, EMAIL]`, `sinais_lai = []`,
recomendação `REVISAR_DADOS_PESSOAIS`, revisão humana obrigatória.
GOV-ADR: `spec/decisoes/GOV-ADR-0001--caso-001.md`.

### CASO-002

Apenas transparência. `sinais_pii = []`, `sinais_lai = [GASTO_PUBLICO, CONTRATO]`,
recomendação `REVISAR_TRANSPARENCIA`, sem revisão humana obrigatória.
GOV-ADR: `spec/decisoes/GOV-ADR-0002--caso-002.md`.

### CASO-003

Conflito. `sinais_pii = [CPF, NOME]`, `sinais_lai = [BENEFICIO_PUBLICO]`,
recomendação `ESCALAR_HUMANO`, revisão humana obrigatória, nenhuma decisão de
divulgação/restrição.
GOV-ADR: `spec/decisoes/GOV-ADR-0003--caso-003.md`.

### CASO-004

Neutro. `sinais_pii = []`, `sinais_lai = []`,
recomendação `PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL`, saída auditável mesmo sem sinais.
GOV-ADR: `spec/decisoes/GOV-ADR-0004--caso-004.md`.

## GOV-ADRs gerados

Quatro arquivos em `spec/decisoes/`, todos com decisão humana `PENDENTE`. Exemplo
(CASO-003):

```markdown
# GOV-ADR-0003 -- CASO-003

- Timestamp: 2026-10-06T23:58:43
- Versão do motor: 0.1.0

## Recomendação do motor
ESCALAR_HUMANO

## Regras acionadas
- R-CONFLITO

## Necessidade de revisão humana
Obrigatória

## Decisão humana
PENDENTE
```

## Declaração de dados fictícios (CHK-07)

Todos os exemplos e testes usam exclusivamente dados sintéticos. Os CPFs
(`123.456.789-00`, `987.654.321-00`) são claramente fictícios, assim como e-mails
(`@exemplo.test`) e nomes (`Beltrano Ficticio`). Nenhum dado real de pessoa foi
utilizado.
