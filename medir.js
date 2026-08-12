#!/usr/bin/env node
// CRAQUE — bateria de medição. VERSIONADA, porque comparar número novo com número
// de documento antigo já nos enganou uma vez.
//
// Uso:  node ferramentas/medir.js [--carreiras=200] [--agente=humano] [--html=craque.html] [--json=saida.json]
//
// Método, e cada regra aqui foi paga com um erro:
//   · PÁGINA NOVA A CADA 4 CARREIRAS — VIDAS só sobe e nunca zera, então 100
//     carreiras na mesma página medem veterano com o bônus de reencarnação ligado.
//   · DUAS SEMENTES independentes — uma semente só esconde artefato.
//   · 200 carreiras por agente, não 100 — a distribuição é quase bimodal.

const path = require("path");
const { chromium } = require("playwright");
const { AGENTES } = require("./agentes.js");

const RAIZ = path.dirname(__dirname);
const arg = (n, d) => {
  const a = process.argv.find(x => x.startsWith(`--${n}=`));
  return a ? a.split("=").slice(1).join("=") : d;
};

const N = parseInt(arg("carreiras", "200"), 10);
const NOME_AGENTE = arg("agente", "humano");
const HTML = path.resolve(RAIZ, arg("html", "craque.html"));
const SAIDA = arg("json", null);
const SEMENTES = [123456789, 987654321];
const POR_SESSAO = 4;

// Os agentes vivem em Node e precisam rodar dentro da página: vão como fonte.
// `const` dentro de eval direto fica preso ao escopo do eval, então a última linha
// publica a tabela no window — sem isso o agente não é visível para quem chamou.
const FONTE_AGENTES = require("fs").readFileSync(path.join(__dirname, "agentes.js"), "utf8")
  .replace(/if \(typeof module[\s\S]*$/, "") + "\nwindow.__AGENTES=AGENTES;\n";

async function bateria(browser, semente, quantas) {
  const carreiras = [];
  const erros = [];
  for (let bloco = 0; bloco * POR_SESSAO < quantas; bloco++) {
    const page = await browser.newPage();
    page.on("pageerror", e => erros.push("PAGEERROR " + e.message));
    page.on("console", m => { if (m.type() === "error") erros.push(m.text()); });
    await page.goto("file://" + HTML);
    const r = await page.evaluate(({ fonte, nome, sem, quantas }) => {
      eval(fonte);
      const K = window.__craque;
      const agente = window.__AGENTES[nome];
      if (!agente) throw new Error("agente desconhecido: " + nome);
      K.semente(sem);
      document.getElementById("b-comeca").click();
      const out = [];
      for (let v = 0; v < quantas; v++) {
        // instrumentação: acompanha a fila e a agenda para saber o que veio de onde
        const vistas = [], retornos = [], ecos = [];
        // fioVencido() TIRA a marcação da agenda antes de devolver a carta, então
        // conferir a agenda no momento em que a carta aparece nunca acha nada.
        // O jeito certo é lembrar tudo o que já foi agendado na carreira.
        const jaAgendados = new Set();
        let n = 0, agendaMax = 0, abertos = 0;
        while (document.getElementById("t-fim").classList.contains("oculta") && n < 600) {
          const C = K.carta(), E = K.estado();
          for (const a of E.agenda) {
            if (!jaAgendados.has(a.id)) { jaAgendados.add(a.id); abertos++; }
          }
          if (C && !C._eco) {
            vistas.push(C.id);
            // abridor de fio curto entra pela agenda mas NÃO é batida de retorno:
            // é a primeira batida, e contá-la falsearia a métrica que o item C mede
            if (jaAgendados.has(C.id) && !/^curto_[a-z]+_b1$/.test(C.id)) {
              retornos.push({ id: C.id, em: E.rodada });
            }
            agendaMax = Math.max(agendaMax, E.agenda.length);
          } else if (C && C._eco) {
            const m = document.getElementById("eco-marca");
            ecos.push({ texto: C.texto, marca: m ? m.textContent : "?" });
          }
          K.escolher(agente(K));
          n++;
        }
        const E = K.estado();
        const elFinal = document.querySelector("#ficha .final");
        out.push({
          semente: sem, vida: E.vida, decisoes: E.rodada, era: E.era, idade: E.idade,
          temporadas: E.temporada, patamar: E.patamar,
          titulo: E.titulo ? E.titulo.id : null,
          medidores: { ...E.medidores },
          final: elFinal ? elFinal.textContent : null,
          moldura: getComputedStyle(document.documentElement).getPropertyValue("--moldura").trim(),
          agendaAberta: E.agenda.length, agendaMax, fiosAbertos: abertos,
          vistas, retornos, ecos,
          curtos: vistas.filter(x => /^curto_/.test(x)),
          motor: vistas.filter(x => ["capitao_partida", "transferencia_sobe",
                                     "transferencia_desce", "companheira_pedagio"].includes(x)),
        });
        document.getElementById("b-denovo").click();
      }
      return { carreiras: out, finais: [...K.vistos()], titulos: [...K.titulos()] };
    }, { fonte: FONTE_AGENTES, nome: NOME_AGENTE, sem: semente + bloco * 7919,
         quantas: Math.min(POR_SESSAO, quantas - bloco * POR_SESSAO) });
    carreiras.push(...r.carreiras);
    await page.close();
  }
  return { carreiras, erros };
}

const med = a => { const x = [...a].sort((p, q) => p - q); return x.length ? x[Math.floor(x.length / 2)] : 0; };
const pct = (a, f) => a.length ? (100 * a.filter(f).length / a.length) : 0;
const pctl = (a, p) => { const x = [...a].sort((u, v) => u - v); return x.length ? x[Math.min(x.length - 1, Math.floor(x.length * p))] : 0; };

function relatorio(carreiras) {
  const ERAS = ["base", "estouro", "travessia", "auge", "declinio", "legado"];
  const dec = carreiras.map(c => c.decisoes);
  const rep = carreiras.map(c => {
    const semMotor = c.vistas.filter(x => !c.motor.includes(x));
    return semMotor.length - new Set(semMotor).size;
  });
  const repMotor = carreiras.map(c => c.motor.length - new Set(c.motor).size);
  const primeiroRetorno = carreiras.map(c => c.retornos.length ? c.retornos[0].em : null).filter(x => x !== null);
  // sobreposição entre campanhas consecutivas, só na Base (14 primeiras cartas)
  const sobrep = [];
  for (let i = 1; i < carreiras.length; i++) {
    if (carreiras[i].vida <= carreiras[i - 1].vida) continue;   // sessão nova
    const a = new Set(carreiras[i - 1].vistas.slice(0, 14));
    const b = carreiras[i].vistas.slice(0, 14);
    if (!b.length) continue;
    sobrep.push(100 * b.filter(x => a.has(x)).length / b.length);
  }
  const todasVistas = new Set(carreiras.flatMap(c => c.vistas));
  return {
    n: carreiras.length,
    decisoes: { p10: pctl(dec, .1), p25: pctl(dec, .25), mediana: med(dec), p75: pctl(dec, .75), p90: pctl(dec, .9) },
    decisoes_vida1: med(carreiras.filter(c => c.vida === 1).map(c => c.decisoes)),
    termina_em: ERAS.reduce((o, e) => (o[e] = +pct(carreiras, c => c.era === e).toFixed(1), o), {}),
    repeticao: {
      pct_carreiras_com_repeticao: +pct(carreiras, (_, i) => rep[i] > 0).toFixed(1),
      media_por_carreira: +(rep.reduce((s, x) => s + x, 0) / carreiras.length).toFixed(2),
      media_cartas_de_motor: +(repMotor.reduce((s, x) => s + x, 0) / carreiras.length).toFixed(2),
    },
    sobreposicao_base_entre_campanhas: +(sobrep.reduce((s, x) => s + x, 0) / (sobrep.length || 1)).toFixed(1),
    linearidade: {
      fios_abertos_por_carreira: +(carreiras.reduce((s, c) => s + c.fiosAbertos, 0) / carreiras.length).toFixed(1),
      batidas_de_retorno_vividas: +(carreiras.reduce((s, c) => s + c.retornos.length, 0) / carreiras.length).toFixed(1),
      pct_sem_nenhuma_batida: +pct(carreiras, c => c.retornos.length === 0).toFixed(1),
      decisao_da_primeira_batida_p50: med(primeiroRetorno),
      fios_abertos_no_fim: +(carreiras.reduce((s, c) => s + c.agendaAberta, 0) / carreiras.length).toFixed(1),
    },
    fios_curtos: {
      cartas_por_carreira: +(carreiras.reduce((s, c) => s + c.curtos.length, 0) / carreiras.length).toFixed(2),
      pct_com_abridor: +pct(carreiras, c => c.curtos.some(x => /_b1$/.test(x)) || c.vistas.includes("mae_base_01")).toFixed(1),
      pct_que_fecharam: +pct(carreiras, c => c.curtos.some(x => /_b[23]$/.test(x))).toFixed(1),
      distintas_vistas: [...new Set(carreiras.flatMap(c => c.curtos))].length,
    },
    cobertura: { cartas_distintas_vistas: todasVistas.size },
    ecos_por_carreira: +(carreiras.reduce((s, c) => s + c.ecos.length, 0) / carreiras.length).toFixed(1),
    // quantas batidas de retorno chegam ANUNCIADAS. É o número que diz se a
    // marcação da linearidade está de fato na tela ou só no código.
    retorno_anunciado: (() => {
      const beats = carreiras.reduce((s, c) => s + c.retornos.length, 0);
      const voltou = carreiras.reduce((s, c) => s + c.ecos.filter(e => e.marca === "voltou").length, 0);
      return { batidas: beats, anunciadas: voltou, pct: beats ? +(100 * voltou / beats).toFixed(1) : 0 };
    })(),
    finais: {
      distintos: [...new Set(carreiras.map(c => c.final).filter(Boolean))].length,
      mais_frequente: +Object.values(carreiras.reduce((o, c) => (o[c.final] = (o[c.final] || 0) + 1, o), {}))
        .reduce((a, b) => Math.max(a, b), 0) * 100 / carreiras.length,
      dourados_pct: +pct(carreiras, c => (c.moldura || "").toLowerCase() === "#e8b93b").toFixed(1),
      verdes_pct: +pct(carreiras, c => (c.moldura || "").toLowerCase() === "#4e8c5a").toFixed(1),
    },
    titulos: { pct_com_titulo: +pct(carreiras, c => c.titulo).toFixed(1), distintos: [...new Set(carreiras.map(c => c.titulo).filter(Boolean))].length },
  };
}

(async () => {
  const browser = await chromium.launch();
  const todas = [], erros = [];
  for (const s of SEMENTES) {
    const r = await bateria(browser, s, Math.ceil(N / SEMENTES.length));
    todas.push(...r.carreiras); erros.push(...r.erros);
  }
  await browser.close();
  const rel = relatorio(todas);
  rel.agente = NOME_AGENTE;
  rel.html = path.basename(HTML);
  rel.erros_de_console = erros.length;
  console.log(JSON.stringify(rel, null, 1));
  if (erros.length) console.error("ERROS:", erros.slice(0, 5));
  if (SAIDA) require("fs").writeFileSync(SAIDA, JSON.stringify({ relatorio: rel, carreiras: todas }, null, 1));
})();
