# Próximos passos - preencher ao final

## Recomendações do Kiro

- Validar a taxonomia LAI e os padrões de PII com especialistas de domínio antes de
  qualquer uso além da PoC.
- Decidir a política de geração de GOV-ADR (opt-in via flag vs. automática).
- Manter o princípio fail-safe: na dúvida, escalar para humano.

## Dívida técnica

- Detector de CPF sem validação de dígito verificador.
- Taxonomia LAI pequena e baseada em palavras-chave fixas.
- Detecção de nome limitada a marcador explícito (sem NER).
- Sem internacionalização; mensagens e taxonomia em português.

## O que faria sentido para PoC 0.2

- Introduzir validação de CPF e mais formatos de PII (RG, CNPJ, data de nascimento).
- Avaliar integração controlada com uma biblioteca de PII (ex.: Presidio) como etapa
  futura, mantendo o motor determinístico como camada de governança.
- Enriquecer a taxonomia LAI e permitir configuração externa (arquivo de regras).
- Registrar histórico de decisões humanas sobre os GOV-ADRs (sair de `PENDENTE`).
- Relatório agregado de múltiplos casos.

## Arquivos que o ChatGPT deve analisar primeiro

1. `.kiro/specs/poc-01-lgpd-lai/requirements.md` — requisitos e CHKs.
2. `.kiro/specs/poc-01-lgpd-lai/design.md` — arquitetura e propriedades de correção.
3. `src/atalaia_governanca/rules.py` — tabela de decisão (núcleo da governança).
4. `src/atalaia_governanca/detectors.py` — detecção determinística.
5. `saida_para_chatgpt/02_TESTES_E_RESULTADOS.md` — evidência de execução.
6. `spec/decisoes/GOV-ADR-0003--caso-003.md` — exemplo de evidência de conflito.
