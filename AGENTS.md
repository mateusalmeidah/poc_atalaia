# Contexto permanente - ATALAIA PoC 0.1

## 1. Contexto do projeto

ATALAIA é um framework de desenvolvimento assistido por IA da UFS orientado por especificação e governança.

Conceitos do ATALAIA que esta PoC deve respeitar:

- a spec é a fonte da verdade;
- nada crítico segue sem revisão humana identificável;
- evidência deve nascer do próprio trabalho;
- rigor deve ser proporcional ao risco;
- decisões críticas não devem depender de uma IA sozinha;
- GOV-ADR registra decisões relevantes e sua justificativa;
- o Vigia é a ideia de verificação determinística de regras/evidências;
- dados pessoais pertencem ao ponto de vista PDP;
- histórias de conformidade pertencem ao tipo HC.

A PoC deve permanecer **externa e desacoplada** do framework oficial. Não modificar o site, plugin, repositório ou implementação oficial do ATALAIA.

## 2. Objetivo científico desta PoC

Demonstrar que uma camada de governança pode:

1. receber um caso simplificado;
2. detectar sinais objetivos de dado pessoal;
3. detectar sinais de possível interesse de transparência/LAI;
4. produzir uma **recomendação**, nunca um parecer jurídico;
5. escalar casos sensíveis ou ambíguos para revisão humana;
6. registrar a análise em um GOV-ADR;
7. gerar evidências reprodutíveis por testes.

A contribuição está na **orquestração da decisão e da evidência**, não em reinventar motores de anonimização.

## 3. Restrições obrigatórias

- Não usar dados reais de alunos, servidores, pacientes, cidadãos ou processos.
- Usar somente dados sintéticos/fictícios.
- Não chamar APIs externas, LLMs remotos ou serviços em nuvem.
- Não implementar Presidio/ARX/eMAG nesta PoC.
- Não afirmar "conforme à LGPD" ou "conforme à LAI".
- Não produzir uma decisão jurídica final automática.
- Casos com dado pessoal + interesse de transparência devem, por padrão, exigir revisão humana.
- Toda recomendação deve explicar quais sinais/regras a produziram.
- Toda saída relevante deve ser testável.
- O código deve ser simples, legível e documentado.

## 4. Linguagem e stack

Preferência:
- Python 3.11+
- pytest
- biblioteca padrão sempre que razoável

Evitar dependências desnecessárias.

## 5. Modelo de resultado

O sistema deve produzir algo semanticamente equivalente a:

```json
{
  "caso_id": "CASO-001",
  "dados_pessoais_detectados": true,
  "sinais_pii": ["CPF", "EMAIL"],
  "interesse_transparencia_detectado": true,
  "sinais_lai": ["GASTO_PUBLICO"],
  "recomendacao": "ESCALAR_HUMANO",
  "revisao_humana_obrigatoria": true,
  "motivos": [
    "Há sinais de dado pessoal",
    "Há sinal de interesse de transparência"
  ],
  "gov_adr": "spec/decisoes/GOV-ADR-0001--caso-001.md"
}
```

O formato exato pode mudar durante o design, mas esses conceitos devem permanecer.

## 6. Filosofia de automação

Use automação determinística para:
- regex/padrões simples;
- validação de campos;
- regras de decisão;
- testes;
- geração de arquivos;
- validação da estrutura.

Reserve julgamento humano para:
- conflitos entre proteção e transparência;
- ambiguidade contextual;
- exceções;
- decisão final de divulgação/restrição.

## 7. Entrega obrigatória

Ao concluir, preencher `saida_para_chatgpt/` com:
- `00_RESUMO_EXECUTIVO.md`
- `01_ESTRUTURA_E_ARQUIVOS.md`
- `02_TESTES_E_RESULTADOS.md`
- `03_DECISOES_LIMITACOES.md`
- `04_PROXIMOS_PASSOS.md`

Não encerrar a PoC sem esses arquivos.
