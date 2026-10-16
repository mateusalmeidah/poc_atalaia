# PoC 0.1 - Motor de apoio à decisão LGPD/LAI

## 1. Pergunta da PoC

É possível representar, de forma determinística, auditável e testável, um fluxo mínimo de governança que reconheça sinais de dado pessoal e de interesse de transparência e encaminhe situações potencialmente conflitantes para revisão humana?

## 2. O que entra nesta versão

### Entrada

Um caso sintético contendo, no mínimo:

- identificador;
- título;
- descrição textual;
- opcionalmente metadados simples.

### Detecção mínima de sinais de dado pessoal

Implementar detecção determinística simples para exemplos sintéticos, como:

- CPF por padrão textual;
- e-mail;
- telefone;
- marcador explícito de nome/pessoa, se necessário para manter a PoC simples.

Não tentar criar um NER completo.

### Detecção mínima de sinais de transparência/LAI

Usar uma taxonomia pequena e explícita de sinais, por exemplo:

- gasto público;
- contrato/contratação;
- benefício público;
- decisão administrativa;
- informação de interesse coletivo.

A detecção pode combinar palavras-chave e metadados de entrada.

### Motor de recomendação

O motor deve produzir apenas recomendações de fluxo, como:

- `PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL`
- `REVISAR_DADOS_PESSOAIS`
- `REVISAR_TRANSPARENCIA`
- `ESCALAR_HUMANO`

Para a PoC 0.1, **não criar automaticamente `PUBLICAR`, `RESTRINGIR` ou `ANONIMIZAR` como decisão final**. Essas ações podem aparecer apenas como sugestões futuras no GOV-ADR.

### GOV-ADR

Cada análise deve poder gerar um arquivo Markdown em:

`spec/decisoes/GOV-ADR-NNNN--<slug>.md`

Conteúdo mínimo:

- contexto;
- sinais encontrados;
- recomendação do motor;
- regras acionadas;
- necessidade de revisão humana;
- decisão humana: `PENDENTE`;
- evidências;
- timestamp;
- versão do motor.

## 3. O que NÃO entra nesta versão

- Presidio;
- ARX;
- AMNESIA;
- scrubadub;
- eMAG/WCAG;
- integração com CI institucional;
- integração com ATALAIA oficial;
- uso de LLM;
- decisão jurídica automatizada;
- dados reais.

## 4. Estrutura esperada

Estrutura sugerida, ajustável durante o design:

```text
atalaia-governanca-poc/
├── .kiro/
│   ├── steering/
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
├── tests/
├── saida_para_chatgpt/
├── pyproject.toml
└── README.md
```

## 5. Casos mínimos de teste

### CASO-001 - apenas dado pessoal

Texto sintético com CPF/e-mail, sem indício de interesse público.

Esperado:
- dado pessoal: sim;
- transparência: não;
- recomendação: revisão de dados pessoais;
- revisão humana: sim.

### CASO-002 - apenas transparência

Texto sintético sobre valor total de contrato público sem dado pessoal.

Esperado:
- dado pessoal: não;
- transparência: sim;
- recomendação: revisão de transparência;
- GOV-ADR registra o motivo.

### CASO-003 - conflito potencial

Texto sintético contendo pessoa identificável + informação de gasto/benefício público.

Esperado:
- dado pessoal: sim;
- transparência: sim;
- recomendação: `ESCALAR_HUMANO`;
- nenhuma decisão final de divulgação/restrição.

### CASO-004 - neutro

Texto sem PII e sem sinal de interesse de transparência.

Esperado:
- ambos falsos;
- fluxo simples;
- ainda deve gerar saída auditável.

## 6. Critérios de aceite - estilo ATALAIA

### CHK-01
O sistema detecta de forma determinística os padrões mínimos de PII definidos para a PoC.

**Prova:** testes automatizados.

### CHK-02
O sistema detecta sinais mínimos de interesse de transparência a partir da taxonomia definida.

**Prova:** testes automatizados.

### CHK-03
Quando dado pessoal e transparência aparecem juntos, o sistema retorna `ESCALAR_HUMANO`.

**Prova:** teste específico do CASO-003.

### CHK-04
O sistema nunca toma decisão final automática de publicar, restringir ou anonimizar.

**Prova:** testes de enum/contrato de saída.

### CHK-05
Toda análise retorna motivos/regras acionadas.

**Prova:** teste do objeto/JSON de saída.

### CHK-06
Toda análise pode gerar GOV-ADR com decisão humana inicialmente `PENDENTE`.

**Prova:** teste de geração e conteúdo do Markdown.

### CHK-07
Nenhum exemplo/teste contém dado pessoal real.

**Prova:** revisão dos fixtures e declaração no relatório final.

### CHK-08
A suíte de testes executa por um único comando documentado e termina verde.

**Prova:** saída do pytest registrada em `saida_para_chatgpt/02_TESTES_E_RESULTADOS.md`.

## 7. Resultado esperado

Ao final, deve ser possível executar algo semelhante a:

```bash
python -m atalaia_governanca.cli analyze examples/caso_03.json
```

e receber:
- resultado legível no terminal;
- saída estruturada;
- GOV-ADR correspondente;
- testes verdes.

O objetivo é provar o **fluxo de governança e evidência**, não a sofisticação do classificador.
