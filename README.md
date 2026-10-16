# ATALAIA - PoC 0.1 no Kiro

PoC 0.1 - Motor determinístico de apoio à decisão LGPD/LAI.

> Protótipo acadêmico isolado. Não implementa Presidio, ARX, AMNESIA ou eMAG; não usa
> LLM, APIs externas, cloud ou banco de dados; usa apenas dados fictícios; e nunca toma
> decisão jurídica final.

## Instalação (ambiente de desenvolvimento)

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"
```

Como o pacote só usa a biblioteca padrão, também é possível rodar sem instalar,
exportando `PYTHONPATH=src`.

## Executar uma análise

```bash
python -m atalaia_governanca.cli analyze examples/caso_03.json
python -m atalaia_governanca.cli analyze examples/caso_03.json --json
python -m atalaia_governanca.cli analyze examples/caso_03.json --gov-adr
```

- `--json`: imprime a saída estruturada.
- `--gov-adr`: gera o GOV-ADR em `spec/decisoes/`.

## Rodar os testes (comando único)

```bash
pytest
```

## Fluxo

```
entrada JSON -> detecção de PII + LAI -> recomendação de governança
            -> escalada humana no conflito -> GOV-ADR (decisão humana PENDENTE)
```

## Recomendações possíveis

`PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL`, `REVISAR_DADOS_PESSOAIS`,
`REVISAR_TRANSPARENCIA`, `ESCALAR_HUMANO`. Nunca `PUBLICAR`, `RESTRINGIR` ou
`ANONIMIZAR`.
