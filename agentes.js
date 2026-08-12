// CRAQUE — agentes de simulação, VERSIONADOS.
//
// Estavam em /tmp e morriam com a sessão. Consequência: cada rodada reconstruía
// o agente a partir da descrição em prosa e os números deixavam de ser
// comparáveis com os dos documentos anteriores. Agora vivem aqui.
//
// Cada agente é uma função (K) -> "esquerda" | "direita", onde K é window.__craque.
// Nenhum agente lê o futuro: só o que a tela mostra (medidores, rótulos, e os
// medidores que o realce acenderia). Isso é de propósito — agente que lê o delta
// exato mede um jogo que ninguém joga.

const MEDIDORES = ["forma", "torcida", "diretoria", "dinheiro"];

// efeitos que o arrasto revelaria naquele lado (o jogador vê QUAIS medidores
// mexem e o tamanho pela bolinha; não vê o sinal)
function efeitosDe(o) {
  if (!o) return {};
  if (o.morte) return {};
  if (o.tipo === "risco") return { ...o.sucesso.efeitos, ...o.falha.efeitos };
  return o.efeitos || {};
}

// ---------------------------------------------------------------- aleatório
// GDD §7.1: escolhe 50/50. É o piso de referência.
function aleatorio(K) {
  return K.rnd() < 0.5 ? "esquerda" : "direita";
}

// ---------------------------------------------------------------- humano
// diagnostico-linearidade.md §0: lê a frase e só olha os medidores quando algum
// está visivelmente perto da borda (<30 ou >70). Fora disso, decide pelo gosto,
// que aqui é uma moeda. É o agente de referência do projeto.
function humano(K) {
  const E = K.estado(), C = K.carta();
  if (C._eco) return K.rnd() < 0.5 ? "esquerda" : "direita";
  const risco = MEDIDORES.filter(k => E.medidores[k] < 30 || E.medidores[k] > 70);
  if (!risco.length) return K.rnd() < 0.5 ? "esquerda" : "direita";
  const vale = lado => {
    const o = C[lado];
    if (o.morte) return -999;              // o texto telegrafa; ele desvia
    const ef = efeitosDe(o);
    let s = 0;
    for (const k of risco) {
      const d = ef[k] || 0;
      s += E.medidores[k] < 30 ? d : -d;   // quer subir o que está no chão, descer o que está no teto
    }
    return s;
  };
  const e = vale("esquerda"), d = vale("direita");
  if (e === d) return K.rnd() < 0.5 ? "esquerda" : "direita";
  return e > d ? "esquerda" : "direita";
}

// ---------------------------------------------------------------- equilibrista
// O agente antigo, mantido para comparar com os documentos velhos: soma
// |valor-50|^1.6 dos quatro medidores e minimiza. Ninguém joga assim, e era ele
// que produzia os números otimistas.
function equilibrista(K) {
  const E = K.estado(), C = K.carta();
  if (C._eco) return "direita";
  const custo = lado => {
    const o = C[lado];
    if (o.morte) return 1e6;
    const ef = efeitosDe(o);
    let s = 0;
    for (const k of MEDIDORES) {
      const v = Math.max(0, Math.min(100, E.medidores[k] + (ef[k] || 0)));
      s += Math.pow(Math.abs(v - 50), 1.6);
    }
    return s;
  };
  return custo("esquerda") <= custo("direita") ? "esquerda" : "direita";
}

// ---------------------------------------------------------------- guloso
// GDD §7.1: sempre maximiza o medidor mais baixo.
function guloso(K) {
  const E = K.estado(), C = K.carta();
  if (C._eco) return "direita";
  const pior = MEDIDORES.reduce((a, b) => E.medidores[a] <= E.medidores[b] ? a : b);
  const g = lado => {
    const o = C[lado];
    if (o.morte) return -999;
    return efeitosDe(o)[pior] || 0;
  };
  return g("esquerda") >= g("direita") ? "esquerda" : "direita";
}

// ---------------------------------------------------------------- monomaníaco
// Fábrica: o P3 do diagnóstico de balanceamento. Persegue um medidor só e nunca
// escolhe opção fatal. Mede em quantas decisões a monomania mata.
function monomaniaco(alvo) {
  return K => {
    const E = K.estado(), C = K.carta();
    if (C._eco) return "direita";
    const g = lado => {
      const o = C[lado];
      if (o.morte) return -999;
      return efeitosDe(o)[alvo] || 0;
    };
    return g("esquerda") >= g("direita") ? "esquerda" : "direita";
  };
}

const AGENTES = {
  aleatorio, humano, equilibrista, guloso,
  mono_forma: monomaniaco("forma"),
  mono_torcida: monomaniaco("torcida"),
  mono_diretoria: monomaniaco("diretoria"),
  mono_dinheiro: monomaniaco("dinheiro"),
};

if (typeof module !== "undefined") module.exports = { AGENTES, MEDIDORES, efeitosDe };
