// Motor determinístico LGPD/LAI — porte fiel do pacote Python
// src/atalaia_governanca (models, detectors, rules, engine, gov_adr).
//
// Mesmos regex, mesma taxonomia e mesma tabela de decisão. Roda 100% no
// navegador, sem backend, sem APIs externas — fiel às restrições da PoC.

export const VERSAO_MOTOR = "0.1.0";

export const Recomendacao = Object.freeze({
  PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL: "PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL",
  REVISAR_DADOS_PESSOAIS: "REVISAR_DADOS_PESSOAIS",
  REVISAR_TRANSPARENCIA: "REVISAR_TRANSPARENCIA",
  ESCALAR_HUMANO: "ESCALAR_HUMANO",
});

// --- Detecção de PII --------------------------------------------------------

const RE_CPF = /\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b/;
const RE_EMAIL = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/;
const RE_TELEFONE = /(?<!\d)(?:\(\d{2}\)\s?|\d{2}[\s-])?\d{4,5}-\d{4}(?!\d)/;
const RE_NOME = /\b(?:nome|pessoa)\s*:\s*\S+/i;

export function detectarPII(texto) {
  const encontrados = [];
  const add = (s) => {
    if (!encontrados.includes(s)) encontrados.push(s);
  };
  if (RE_CPF.test(texto)) add("CPF");
  if (RE_EMAIL.test(texto)) add("EMAIL");
  if (RE_TELEFONE.test(texto)) add("TELEFONE");
  if (RE_NOME.test(texto)) add("NOME");
  return encontrados;
}

// --- Detecção de LAI --------------------------------------------------------

const TAXONOMIA_LAI = [
  ["GASTO_PUBLICO", ["gasto publico", "despesa publica", "valor total",
    "verba publica", "recurso publico", "orcamento"]],
  ["CONTRATO", ["contrato", "contratacao", "licitacao", "pregao"]],
  ["BENEFICIO_PUBLICO", ["beneficio publico", "beneficio social", "auxilio",
    "subsidio"]],
  ["DECISAO_ADMINISTRATIVA", ["decisao administrativa", "ato administrativo",
    "portaria", "processo administrativo"]],
  ["INTERESSE_COLETIVO", ["interesse coletivo", "interesse publico",
    "interesse da sociedade"]],
];

function normalizar(texto) {
  return texto
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "") // remove acentos
    .toLowerCase();
}

function escaparRegex(s) {
  return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

function contemPalavraChave(alvo, palavra) {
  // Limite de palavra para evitar falso-positivo por substring
  // (ex.: "licitacao" dentro de "solicitacao").
  const padrao = new RegExp("\\b" + escaparRegex(palavra) + "\\b");
  return padrao.test(alvo);
}

function textoMetadados(metadados) {
  const partes = [];
  for (const valor of Object.values(metadados || {})) {
    if (Array.isArray(valor)) partes.push(...valor.map(String));
    else partes.push(String(valor));
  }
  return partes.join(" ");
}

export function detectarLAI(texto, metadados = {}) {
  const alvo = normalizar(texto + " " + textoMetadados(metadados));
  const encontrados = [];
  for (const [sinal, palavras] of TAXONOMIA_LAI) {
    if (palavras.some((p) => contemPalavraChave(alvo, p))) {
      encontrados.push(sinal);
    }
  }
  return encontrados;
}

// --- Regras de decisão ------------------------------------------------------

export function decidir(sinaisPII, sinaisLAI) {
  const temPII = sinaisPII.length > 0;
  const temLAI = sinaisLAI.length > 0;
  const nomesPII = sinaisPII.join(", ");
  const nomesLAI = sinaisLAI.join(", ");

  if (temPII && temLAI) {
    return {
      recomendacao: Recomendacao.ESCALAR_HUMANO,
      motivos: [
        `Há sinais de dado pessoal (${nomesPII}).`,
        `Há sinal de interesse de transparência (${nomesLAI}).`,
        "Conflito entre proteção de dados e transparência exige revisão " +
          "humana; o motor não decide divulgação ou restrição.",
      ],
      regras_acionadas: ["R-CONFLITO"],
      revisao_humana_obrigatoria: true,
    };
  }
  if (temPII) {
    return {
      recomendacao: Recomendacao.REVISAR_DADOS_PESSOAIS,
      motivos: [`Há sinais de dado pessoal (${nomesPII}).`],
      regras_acionadas: ["R-PII"],
      revisao_humana_obrigatoria: true,
    };
  }
  if (temLAI) {
    return {
      recomendacao: Recomendacao.REVISAR_TRANSPARENCIA,
      motivos: [`Há sinal de interesse de transparência (${nomesLAI}).`],
      regras_acionadas: ["R-LAI"],
      revisao_humana_obrigatoria: false,
    };
  }
  return {
    recomendacao: Recomendacao.PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL,
    motivos: [
      "Nenhum sinal de dado pessoal ou de interesse de transparência foi " +
        "detectado.",
    ],
    regras_acionadas: ["R-NEUTRO"],
    revisao_humana_obrigatoria: false,
  };
}

// --- Motor ------------------------------------------------------------------

export function analisar(caso) {
  const texto = `${caso.titulo || ""}\n${caso.descricao || ""}`;
  const sinaisPII = detectarPII(texto);
  const sinaisLAI = detectarLAI(texto, caso.metadados || {});
  const decisao = decidir(sinaisPII, sinaisLAI);

  return {
    caso_id: caso.caso_id || "CASO",
    dados_pessoais_detectados: sinaisPII.length > 0,
    sinais_pii: sinaisPII,
    interesse_transparencia_detectado: sinaisLAI.length > 0,
    sinais_lai: sinaisLAI,
    recomendacao: decisao.recomendacao,
    revisao_humana_obrigatoria: decisao.revisao_humana_obrigatoria,
    motivos: decisao.motivos,
    regras_acionadas: decisao.regras_acionadas,
  };
}

// --- GOV-ADR (renderização em Markdown, decisão humana PENDENTE) ------------

function slugify(valor) {
  const sem = valor
    .normalize("NFKD")
    .replace(/[\u0300-\u036f]/g, "");
  return (
    sem.replace(/[^a-zA-Z0-9]+/g, "-").replace(/^-+|-+$/g, "").toLowerCase() ||
    "caso"
  );
}

export function gerarGovAdrMarkdown(resultado, numero = 1, agora = new Date()) {
  const pii = resultado.sinais_pii.join(", ") || "(nenhum)";
  const lai = resultado.sinais_lai.join(", ") || "(nenhum)";
  const regras =
    resultado.regras_acionadas.map((r) => `- ${r}`).join("\n") || "- (nenhuma)";
  const motivos =
    resultado.motivos.map((m) => `- ${m}`).join("\n") || "- (nenhum)";
  const revisao = resultado.revisao_humana_obrigatoria
    ? "Obrigatória"
    : "Não obrigatória";
  const num = String(numero).padStart(4, "0");
  const ts = agora.toISOString().slice(0, 19);

  return `# GOV-ADR-${num} -- ${resultado.caso_id}

- Timestamp: ${ts}
- Versão do motor: ${VERSAO_MOTOR}

## Contexto

Análise automatizada do caso \`${resultado.caso_id}\` pela PoC 0.1 LGPD/LAI.
Esta é uma recomendação de fluxo de governança, não um parecer jurídico.

## Sinais encontrados

- PII: ${pii}
- LAI: ${lai}

## Recomendação do motor

${resultado.recomendacao}

## Regras acionadas

${regras}

## Necessidade de revisão humana

${revisao}

## Decisão humana

PENDENTE

## Evidências

${motivos}
`;
}

export { slugify };
