import {
  analisar,
  gerarGovAdrMarkdown,
} from "./motor.js";
import {
  CASOS,
  EXPLICACAO_RECOMENDACAO,
  EXPLICACAO_REGRA,
} from "./casos.js";

const $ = (sel) => document.querySelector(sel);

const el = {
  botoes: $("#casos-botoes"),
  casoId: $("#caso-id"),
  titulo: $("#titulo"),
  descricao: $("#descricao"),
  analisar: $("#analisar"),
  resultado: $("#resultado"),
  govBloco: $("#govadr-bloco"),
  govadr: $("#govadr"),
  flow: $("#flow"),
  paridade: $("#paridade-grid"),
};

const CLASSE_REC = {
  ESCALAR_HUMANO: "escalar",
  REVISAR_DADOS_PESSOAIS: "pii",
  REVISAR_TRANSPARENCIA: "lai",
  PROSSEGUIR_SEM_TRATAMENTO_ESPECIAL: "neutro",
};

// --- Botões dos casos canônicos --------------------------------------------

CASOS.forEach((item, idx) => {
  const b = document.createElement("button");
  b.textContent = item.rotulo;
  b.dataset.chave = item.chave;
  b.addEventListener("click", () => {
    marcarSelecionado(b);
    carregarCaso(item.caso);
    rodar();
  });
  el.botoes.appendChild(b);
  if (idx === 0) b._primeiro = true;
});

function marcarSelecionado(botao) {
  el.botoes.querySelectorAll("button").forEach((x) => x.classList.remove("sel"));
  if (botao) botao.classList.add("sel");
}

function carregarCaso(caso) {
  el.casoId.value = caso.caso_id;
  el.titulo.value = caso.titulo;
  el.descricao.value = caso.descricao;
  el._metadados = caso.metadados || {};
}

// --- Análise + render -------------------------------------------------------

el.analisar.addEventListener("click", () => {
  marcarSelecionado(null);
  rodar();
});

function rodar() {
  const caso = {
    caso_id: el.casoId.value.trim() || "CASO-LIVRE",
    titulo: el.titulo.value.trim(),
    descricao: el.descricao.value.trim(),
    metadados: el._metadados || {},
  };
  const r = analisar(caso);
  renderResultado(r);
  renderGovAdr(r);
  animarFluxo(r);
}

function listaChips(valores, tipo) {
  if (!valores.length) return '<span class="chip">(nenhum)</span>';
  return valores
    .map((v) => `<span class="chip ${tipo}">${v}</span>`)
    .join("");
}

function renderResultado(r) {
  const cls = CLASSE_REC[r.recomendacao] || "neutro";
  const explicacaoRec = EXPLICACAO_RECOMENDACAO[r.recomendacao] || "";
  const regras = r.regras_acionadas
    .map((reg) => `<strong>${reg}</strong> — ${EXPLICACAO_REGRA[reg] || ""}`)
    .join("<br>");

  el.resultado.innerHTML = `
    <div class="rec-destaque ${cls}">${r.recomendacao}</div>
    <p class="nota">${explicacaoRec}</p>
    <div class="linha"><span class="rot">Dados pessoais</span>
      <span>${r.dados_pessoais_detectados ? "detectado" : "não"}</span></div>
    <div class="linha"><span class="rot">Sinais PII</span>
      <span>${listaChips(r.sinais_pii, "pii")}</span></div>
    <div class="linha"><span class="rot">Transparência</span>
      <span>${r.interesse_transparencia_detectado ? "detectado" : "não"}</span></div>
    <div class="linha"><span class="rot">Sinais LAI</span>
      <span>${listaChips(r.sinais_lai, "lai")}</span></div>
    <div class="linha"><span class="rot">Regra acionada</span>
      <span>${regras}</span></div>
    <strong>Motivos</strong>
    <ul class="motivos">${r.motivos.map((m) => `<li>${m}</li>`).join("")}</ul>
    ${
      r.revisao_humana_obrigatoria
        ? '<div class="flag-humano">Revisão humana obrigatória — a decisão final é de uma pessoa, não do motor.</div>'
        : ""
    }
  `;
}

function renderGovAdr(r) {
  el.govadr.textContent = gerarGovAdrMarkdown(r);
  el.govBloco.hidden = false;
}

// --- Animação do diagrama de fluxo -----------------------------------------

function animarFluxo(r) {
  const steps = ["entrada", "pii", "lai", "regra", "escala", "govadr"];
  const lis = {};
  el.flow.querySelectorAll("li").forEach((li) => {
    li.classList.remove("ativo", "alerta");
    lis[li.dataset.step] = li;
  });

  steps.forEach((step, i) => {
    setTimeout(() => {
      const li = lis[step];
      if (!li) return;
      if (step === "escala") {
        // Só acende a escalada quando houve conflito.
        if (r.recomendacao === "ESCALAR_HUMANO") li.classList.add("alerta");
      } else {
        li.classList.add("ativo");
      }
    }, i * 220);
  });
}

// --- Paridade com o motor Python -------------------------------------------

function mesmoConjunto(a, b) {
  return a.length === b.length && a.every((x) => b.includes(x));
}

function renderParidade() {
  CASOS.forEach((item) => {
    const r = analisar(item.caso);
    const okRec = r.recomendacao === item.esperado.recomendacao;
    const okPII = mesmoConjunto(r.sinais_pii, item.esperado.sinais_pii);
    const okLAI = mesmoConjunto(r.sinais_lai, item.esperado.sinais_lai);
    const ok = okRec && okPII && okLAI;

    const card = document.createElement("div");
    card.className = "card-par";
    card.innerHTML = `
      <h4>${item.caso.caso_id}</h4>
      <div class="status ${ok ? "ok" : "falha"}">
        ${ok ? "✓ idêntico ao esperado" : "✗ divergente"}
      </div>
      <p class="detalhe">
        recomendação: <code>${r.recomendacao}</code><br>
        PII: ${r.sinais_pii.join(", ") || "—"}<br>
        LAI: ${r.sinais_lai.join(", ") || "—"}
      </p>
    `;
    el.paridade.appendChild(card);
  });
}

// --- Inicialização ----------------------------------------------------------

renderParidade();
// Carrega o primeiro caso já analisado, para a tela não começar vazia.
const primeiro = el.botoes.querySelector("button");
if (primeiro) {
  marcarSelecionado(primeiro);
  carregarCaso(CASOS[0].caso);
  rodar();
}
