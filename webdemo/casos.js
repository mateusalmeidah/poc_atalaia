// Os 4 casos canônicos (mesmos de examples/) + resultado esperado para a
// seção de paridade com o motor Python testado.

export const CASOS = [
  {
    chave: "caso_01",
    rotulo: "CASO-001 · só dado pessoal",
    caso: {
      caso_id: "CASO-001",
      titulo: "Solicitação de atualização cadastral",
      descricao:
        "O requerente informou o CPF 123.456.789-00 e o e-mail " +
        "fulano.ficticio@exemplo.test para atualizar seu cadastro.",
      metadados: { origem: "formulario_sintetico" },
    },
    esperado: {
      recomendacao: "REVISAR_DADOS_PESSOAIS",
      sinais_pii: ["CPF", "EMAIL"],
      sinais_lai: [],
    },
  },
  {
    chave: "caso_02",
    rotulo: "CASO-002 · só transparência",
    caso: {
      caso_id: "CASO-002",
      titulo: "Publicação de valor de contrato",
      descricao:
        "Pedido de divulgação do valor total do contrato de contratação " +
        "de serviços de limpeza do órgão.",
      metadados: { categoria: "gasto publico" },
    },
    esperado: {
      recomendacao: "REVISAR_TRANSPARENCIA",
      sinais_pii: [],
      sinais_lai: ["GASTO_PUBLICO", "CONTRATO"],
    },
  },
  {
    chave: "caso_03",
    rotulo: "CASO-003 · conflito",
    caso: {
      caso_id: "CASO-003",
      titulo: "Divulgação de beneficiário de auxílio",
      descricao:
        "Pedido para divulgar o benefício público pago, incluindo " +
        "nome: Beltrano Ficticio e o CPF 987.654.321-00 do beneficiário.",
      metadados: { categoria: "beneficio publico" },
    },
    esperado: {
      recomendacao: "ESCALAR_HUMANO",
      sinais_pii: ["CPF", "NOME"],
      sinais_lai: ["BENEFICIO_PUBLICO"],
    },
  },
  {
    chave: "caso_04",
    rotulo: "CASO-004 · neutro",
    caso: {
      caso_id: "CASO-004",
      titulo: "Atualização de horário de funcionamento",
      descricao:
        "Aviso informando o novo horário de funcionamento da biblioteca " +
        "durante o período de recesso.",
      metadados: { categoria: "comunicado_geral" },
    },
    esperado: {
      recomendacao: "PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL",
      sinais_pii: [],
      sinais_lai: [],
    },
  },
];

// Texto explicativo de cada recomendação, mostrado conforme o resultado.
export const EXPLICACAO_RECOMENDACAO = {
  REVISAR_DADOS_PESSOAIS:
    "Há sinais de dado pessoal e nenhum sinal de transparência. O caso segue " +
    "para revisão de proteção de dados (ponto de vista PDP).",
  REVISAR_TRANSPARENCIA:
    "Há sinal de interesse de transparência e nenhum dado pessoal. O caso " +
    "segue para revisão de transparência/LAI.",
  ESCALAR_HUMANO:
    "Dado pessoal e transparência aparecem juntos: conflito. O motor falha " +
    "para o lado seguro e escala para um humano decidir — nunca decide " +
    "divulgação ou restrição automaticamente.",
  PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL:
    "Nenhum sinal relevante foi detectado. O fluxo segue sem tratamento " +
    "especial, mas ainda gera saída auditável.",
};

export const EXPLICACAO_REGRA = {
  "R-CONFLITO": "PII ∧ LAI ⇒ ESCALAR_HUMANO (precedência; fail-safe).",
  "R-PII": "PII sem LAI ⇒ REVISAR_DADOS_PESSOAIS.",
  "R-LAI": "LAI sem PII ⇒ REVISAR_TRANSPARENCIA.",
  "R-NEUTRO": "Sem sinais ⇒ PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL.",
};
