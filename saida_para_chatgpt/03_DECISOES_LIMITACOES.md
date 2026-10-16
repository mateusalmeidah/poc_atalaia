# Decisões e limitações - preencher ao final

## Decisões de implementação

- **Enums herdando de `str`** (`Recomendacao`, `SinalPII`, `SinalLAI`): serialização
  JSON direta e comparações legíveis em testes.
- **CPF por padrão textual sem validação de dígito verificador**: a PoC prova o fluxo de
  governança, não a robustez do classificador; evita falso-negativo em CPFs sintéticos.
- **Detecção LAI com limite de palavra (`\b`)**: necessária após observar falso-positivo
  por substring (`licitacao` dentro de `solicitacao`). Normalização remove acentos e
  caixa.
- **Geração de GOV-ADR fora do engine**, acionada por `--gov-adr` na CLI: respeita
  "não misturar evidência com código" e mantém o engine puro/determinístico.
- **Timestamp injetável** em `gerar_gov_adr(agora=...)`: permite testes determinísticos.
- **Sem dependências de runtime**: apenas biblioteca padrão; `pytest` só em dev.

## Ambiguidades encontradas

- O escopo diz que o marcador de nome entra "se necessário". Mantido como marcador
  explícito (`nome:`/`pessoa:`), sem NER, para não ampliar escopo.
- "Cada análise deve poder gerar GOV-ADR": interpretado como opt-in (flag `--gov-adr`),
  não geração automática em toda chamada. Decisão reversível.

## Limitações conhecidas

- Detectores são propositalmente simples: CPF sem validação, telefone em formatos
  comuns, taxonomia LAI pequena. Textos reais poderiam gerar falsos positivos/negativos.
- Sem NER: nomes só são detectados via marcador explícito.
- A detecção LAI é por palavra-chave; sinônimos ou grafias fora da taxonomia não são
  reconhecidos.
- Não há normalização semântica nem desambiguação de contexto.

## Desvios em relação à spec

- Nenhum desvio de escopo. As únicas escolhas além do texto literal são técnicas e estão
  documentadas acima (CPF sem dígito verificador; GOV-ADR opt-in via flag). Estrutura de
  pastas e nomes de módulos seguem exatamente a sugestão do escopo.

## Pontos que precisam de decisão humana/pesquisador

- Confirmar se a geração de GOV-ADR deve ser automática em toda análise ou permanecer
  opt-in.
- Definir se o detector de CPF deve passar a validar dígito verificador em PoCs futuras.
- Validar a taxonomia LAI (palavras-chave) com especialistas de domínio.
- Toda decisão final de divulgação/restrição permanece com o responsável humano
  (campo `Decisão humana: PENDENTE` nos GOV-ADRs).
