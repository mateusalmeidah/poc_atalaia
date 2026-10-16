// Verificação de paridade do motor JS com os resultados esperados (Python).
// Executar: node webdemo/_verifica_paridade.mjs
import { analisar } from "./motor.js";
import { CASOS } from "./casos.js";

function mesmo(a, b) {
  return a.length === b.length && a.every((x) => b.includes(x));
}

let falhas = 0;
for (const item of CASOS) {
  const r = analisar(item.caso);
  const ok =
    r.recomendacao === item.esperado.recomendacao &&
    mesmo(r.sinais_pii, item.esperado.sinais_pii) &&
    mesmo(r.sinais_lai, item.esperado.sinais_lai);
  console.log(
    `${ok ? "OK " : "FAIL"} ${item.caso.caso_id} -> ${r.recomendacao} ` +
      `PII[${r.sinais_pii}] LAI[${r.sinais_lai}]`
  );
  if (!ok) falhas++;
}
console.log(falhas === 0 ? "\nParidade OK (4/4)" : `\n${falhas} divergência(s)`);
process.exit(falhas === 0 ? 0 : 1);
