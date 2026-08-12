#!/usr/bin/env python3
"""
Compila o CRAQUE num único arquivo HTML jogável.

Uso:  python3 ferramentas/build-html.py

Lê cartas/*.json, finais.json, cargos.json e arte/paleta.json, embute tudo
como JSON no HTML e escreve craque.html na raiz. Rodar de novo depois de
qualquer mudança de conteúdo — o HTML nunca é editado à mão.
"""
import glob
import json
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def carregar():
    cartas = []
    for arq in sorted(glob.glob(os.path.join(RAIZ, "cartas", "*.json"))):
        cartas.extend(json.load(open(arq, encoding="utf-8"))["cartas"])
    return {
        "cartas": cartas,
        "finais": json.load(open(os.path.join(RAIZ, "finais.json"), encoding="utf-8")),
        "cargos": json.load(open(os.path.join(RAIZ, "cargos.json"), encoding="utf-8")),
        "paleta": json.load(open(os.path.join(RAIZ, "arte", "paleta.json"), encoding="utf-8")),
        "clubes": json.load(open(os.path.join(RAIZ, "clubes.json"), encoding="utf-8")),
        "titulos": json.load(open(os.path.join(RAIZ, "titulos.json"), encoding="utf-8")),
    }


CSS = r"""
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;overflow:hidden;-webkit-tap-highlight-color:transparent}
body{
  font-family:"Inter","Segoe UI",system-ui,-apple-system,sans-serif;
  background:var(--fundo);color:var(--texto);
  display:flex;align-items:center;justify-content:center;
  transition:background .8s ease;user-select:none;
}
#palco{width:min(100vw,430px);height:min(100vh,860px);position:relative;display:flex;flex-direction:column;padding:14px}

/* ---------- identidade: nome sempre, título quando conquistado ---------- */
#identidade{display:flex;align-items:baseline;justify-content:center;gap:9px;
  padding:2px 2px 6px;min-height:19px;flex-wrap:wrap}
#identidade .quem-eu{font-size:11px;letter-spacing:.13em;text-transform:uppercase;color:var(--texto2);opacity:.8}
#identidade .titulo{font-size:13px;font-weight:750;letter-spacing:.05em;color:var(--texto);
  padding:1px 9px;border:1.5px solid var(--texto);border-radius:99px;line-height:1.35}
#identidade .titulo{white-space:nowrap}
#identidade.revela .titulo{animation:selo 1400ms cubic-bezier(.2,1,.3,1)}
@keyframes selo{
  0%{opacity:0;transform:translateY(-7px);box-shadow:0 0 0 0 var(--texto)}
  22%{opacity:1;transform:translateY(0);box-shadow:0 0 0 7px rgba(255,255,255,0)}
  55%{box-shadow:0 0 22px 2px var(--texto)}
  100%{opacity:1;transform:none;box-shadow:none}
}

/* ---------- medidores ---------- */
#medidores{display:flex;gap:10px;padding:2px 2px 14px}
.med{position:relative}
.med{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;transition:transform .18s ease}
.med svg{width:22px;height:22px;display:block;transition:opacity .18s,transform .18s}
/* bolinha de impacto: aparece no arrasto e diz o TAMANHO da consequência.
   Nunca diz o sinal — nem por cor, nem por posição, nem por forma. */
.med .bola{width:14px;height:14px;border-radius:50%;opacity:0;transform:scale(0);
  transition:transform .14s cubic-bezier(.2,1.2,.3,1),opacity .14s ease;margin:-3px 0 -1px}
.med.imp1 .bola{transform:scale(.36);opacity:.9}
.med.imp2 .bola{transform:scale(.64);opacity:.95}
.med.imp3 .bola{transform:scale(1);opacity:1}
.med .trilho{width:100%;height:7px;border-radius:99px;background:rgba(0,0,0,.38);overflow:hidden;position:relative}
.med .fantasma{position:absolute;top:0;height:100%;border-radius:99px;opacity:0}
.med .fantasma.vivo{animation:some .75s ease-out forwards}
@keyframes some{0%{opacity:.75}70%{opacity:.45}100%{opacity:0}}
.med .barra{position:absolute;top:0;left:0;height:100%;border-radius:99px;
  transition:width .5s cubic-bezier(.2,.85,.25,1)}
.med.bateu .trilho{animation:sacode .34s cubic-bezier(.36,.07,.19,.97)}
@keyframes sacode{0%,100%{transform:translateX(0)}20%{transform:translateX(-3px)}
  45%{transform:translateX(3px)}70%{transform:translateX(-2px)}}
.med.subiu svg{animation:pulsa .5s ease-out}
.med.caiu svg{animation:pulsa .5s ease-out}
@keyframes pulsa{0%{transform:scale(1)}35%{transform:scale(1.45)}100%{transform:scale(1)}}
.med.forte svg{animation:pulsaForte .62s ease-out}
@keyframes pulsaForte{0%{transform:scale(1)}30%{transform:scale(1.9)}60%{transform:scale(1.15)}100%{transform:scale(1)}}
.med.apagado svg{opacity:.32}
.med.aceso{transform:translateY(-3px)}
.med.aceso svg{opacity:1;transform:scale(1.18)}
.med.perigo .barra{animation:pisca .9s infinite}
@keyframes pisca{0%,100%{opacity:1}50%{opacity:.35}}
@keyframes treme{0%,100%{transform:translateX(0)}25%{transform:translateX(-2px)}75%{transform:translateX(2px)}}

/* ---------- carta ---------- */
#area{flex:1;position:relative;display:flex;align-items:center;justify-content:center}
#carta{
  position:absolute;width:100%;max-width:320px;height:min(100%,500px);z-index:1;
  display:flex;flex-direction:column;
  background:var(--superficie);border:3px solid var(--traco);border-radius:18px;
  overflow:hidden;cursor:grab;box-shadow:0 18px 40px rgba(0,0,0,.45);
  will-change:transform;touch-action:none;
}
#carta.solta{transition:transform .32s cubic-bezier(.3,1.3,.5,1),opacity .32s}
#carta.saindo{transition:transform .3s ease-in,opacity .3s ease-in}
#retrato{width:100%;flex:1 1 auto;min-height:0;display:block;background:var(--fundo)}
#texto{flex:0 0 auto;padding:12px 18px 18px;font-size:15px;line-height:1.45}
#quem{flex:0 0 auto;padding:11px 18px 0;font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--texto2);opacity:.85}

/* ---------- rótulos ---------- */
.rotulo{
  position:absolute;top:38%;z-index:6;font-size:15px;font-weight:700;letter-spacing:.01em;
  padding:9px 14px;border-radius:11px;border:2px solid var(--texto);
  background:var(--fundo);color:var(--texto);box-shadow:0 6px 18px rgba(0,0,0,.5);
  opacity:0;transition:opacity .14s;pointer-events:none;max-width:42%;line-height:1.25;
}
#rotE{left:0;transform:rotate(-7deg)}
#rotD{right:0;transform:rotate(7deg)}

/* ---------- rodapé ---------- */
#rodape{display:flex;justify-content:space-between;align-items:center;padding:12px 4px 4px;font-size:11.5px;color:var(--texto2);letter-spacing:.05em}
#dica{text-align:center;font-size:11px;color:var(--texto2);opacity:.55;padding-bottom:6px;height:16px}

/* ---------- balanço de fim de temporada ---------- */
#b-cabeca{font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--texto2)}
#b-patamar{font-size:22px;font-weight:700;letter-spacing:.01em;margin-top:-6px}
#balanco .grade{display:flex;gap:26px;margin:4px 0 2px}
#balanco .cel{display:flex;flex-direction:column;align-items:center;gap:3px}
#balanco .cel b{font-size:27px;font-weight:700;line-height:1}
#balanco .cel span{font-size:9.5px;color:var(--texto2);letter-spacing:.08em;text-transform:uppercase}
#b-frase{font-size:16px;line-height:1.4;font-style:italic;max-width:22em;opacity:.92}

/* ---------- eco de legado: carta de texto, sem personagem ---------- */
/* Vira carta porque sussurro de 1,9s some antes de ser lido. Aqui o jogador
   controla o tempo: fica na tela até ele arrastar. Arrastar não decide nada —
   os dois lados fazem a mesma coisa, e é de propósito. */
#carta.so-texto{background:var(--fundo);border-style:solid;border-color:var(--texto2);
  align-items:center;justify-content:center;box-shadow:0 14px 34px rgba(0,0,0,.4)}
#carta.so-texto #eco-texto{
  padding:0 30px;text-align:center;font-size:21px;line-height:1.42;
  font-style:italic;letter-spacing:.01em;color:var(--texto);max-width:15em;
}
#carta.so-texto #eco-marca{
  position:absolute;bottom:22px;left:0;right:0;text-align:center;
  font-size:10.5px;letter-spacing:.22em;text-transform:uppercase;color:var(--texto2);opacity:.5;
}
#carta.so-texto.entrando{animation:ecoEntra .42s cubic-bezier(.2,.9,.3,1)}
@keyframes ecoEntra{0%{opacity:0;transform:scale(.96)}100%{opacity:1;transform:scale(1)}}

/* ---------- telas ---------- */
.tela{position:absolute;inset:0;background:var(--fundo);display:flex;flex-direction:column;
  align-items:center;justify-content:center;padding:22px;text-align:center;z-index:20;gap:15px}
.tela.oculta{display:none}
h1{font-size:34px;letter-spacing:.2em;font-weight:800}
h2{font-size:23px;line-height:1.22;font-weight:750}
p{font-size:14.5px;line-height:1.55;color:var(--texto2);max-width:330px}
button{
  font:inherit;font-size:14.5px;font-weight:650;padding:12px 26px;border-radius:11px;
  border:2px solid var(--texto);background:transparent;color:var(--texto);cursor:pointer;
  transition:background .15s,color .15s
}
button:hover{background:var(--texto);color:var(--fundo)}
button.sec{border-color:var(--texto2);color:var(--texto2);font-size:12.5px;padding:9px 18px}

/* ---------- ficha ---------- */
#ficha{width:100%;max-width:310px;border:5px solid var(--moldura);border-radius:14px;
  background:var(--superficie);padding:17px;text-align:left}
#ficha .nome{font-size:20px;font-weight:800;line-height:1.15}
#ficha .sub{font-size:11.5px;color:var(--texto2);letter-spacing:.1em;text-transform:uppercase;margin-top:3px}
#ficha .grade{display:grid;grid-template-columns:1fr 1fr 1fr;gap:9px;margin:15px 0}
#ficha .cel{background:rgba(0,0,0,.26);border-radius:8px;padding:8px 6px;text-align:center}
#ficha .cel b{display:block;font-size:19px;font-weight:800}
#ficha .cel span{font-size:9.5px;color:var(--texto2);letter-spacing:.07em;text-transform:uppercase}
#ficha .final{border-top:2px solid var(--moldura);padding-top:11px;font-size:16px;font-weight:750;color:var(--moldura)}
#marca{font-size:12.5px;color:var(--texto2);max-width:320px;line-height:1.5}
#galeria{display:flex;flex-wrap:wrap;gap:5px;justify-content:center;max-width:340px}
.pino{width:9px;height:9px;border-radius:2px;background:rgba(255,255,255,.14)}
.pino.viu{background:var(--dourado)}
"""

JS = r"""
// ======================= PRNG com seed =======================
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);
  t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
let rnd = mulberry32(123456789);
const sorteia = arr => arr[Math.floor(rnd()*arr.length)];

// ======================= constantes =======================
const MEDIDORES=["forma","torcida","diretoria","dinheiro"];
const ORDEM_ERAS=["base","estouro","travessia","auge","declinio","legado"];
// Reencarnação NÃO adianta a idade inicial: testado, e pular a Base levou as cartas
// nunca vistas de 31 para 100. O bónus é PISTA MAIS LONGA — o veterano se aposenta
// mais tarde, então atravessa as mesmas eras e chega mais longe.
const IDADE_INICIAL=v=>17;
const IDADE_PARAR=v=>v<=1?33:v===2?34:v===3?35:36;
const ERA_POR_IDADE=i=>i<19?"base":i<22?"estouro":i<26?"travessia":i<30?"auge":i<33?"declinio":"legado";
const CARTAS_POR_TEMPORADA=7;

const MARCAS={
 forma_0:{id:"corpo_lembrado",nome:"Corpo lembrado",desc:"Ganhos e perdas de FORMA são 25% maiores.",mult:{forma:1.25}},
 forma_100:{id:"fome_antiga",nome:"Fome antiga",desc:"Começa com FORMA 60, mas o corpo cobra a partir dos 27.",inicio:{forma:60},decaiCedo:true},
 torcida_0:{id:"cara_de_vilao",nome:"Cara de vilão",desc:"TORCIDA se move 30% menos. Imune ao ódio, incapaz de ser amado.",mult:{torcida:0.7}},
 torcida_100:{id:"carisma_herdado",nome:"Carisma herdado",desc:"Ganhos de TORCIDA 30% maiores, e cada um custa 1 de DIRETORIA.",mult:{torcida:1.3},pedagio:true},
 diretoria_0:{id:"ficha_suja",nome:"Ficha suja",desc:"Começa com DIRETORIA 40, mas ganha 20% mais DINHEIRO.",inicio:{diretoria:40},mult:{dinheiro:1.2}},
 diretoria_100:{id:"filho_do_clube",nome:"Filho do clube",desc:"Começa com DIRETORIA 65. Você nasceu devendo lealdade a um escudo.",inicio:{diretoria:65}},
 dinheiro_0:{id:"medo_de_passar_fome",nome:"Medo de passar fome",desc:"Ganhos de DINHEIRO 30% maiores.",mult:{dinheiro:1.3}},
 dinheiro_100:{id:"ganancia_antiga",nome:"Ganância antiga",desc:"DINHEIRO sobe 25% mais rápido. Inclusive nas cartas que te matam.",mult:{dinheiro:1.25}},
};
const NOMES=["Rafa","Juninho","Tico","Léo","Dedé","Vina","Kaio","Bidu","Neném","Zaca","Piu","Gabi"];
// O apelido não é sorteado: vem do título conquistado. Ninguém nasce com apelido.

// ======================= estado =======================
let E=null, VIDAS=0, MARCA_ATUAL=null, ULTIMO_ELENCO={}, VISTOS_FINAIS=new Set(), CARTA=null;

function novoJogo(){
  VIDAS++;
  // o saco recebe as cartas da vida que acabou de terminar
  if(E&&E.historico) SACO=new Set(E.historico);
  const m=MARCA_ATUAL?MARCAS[MARCA_ATUAL]:null;
  E={
    medidores:{forma:50,torcida:50,diretoria:50,dinheiro:50},
    // P4 — a reencarnação passa a dar ACESSO, não só a marca de alma. Medido: só 27%
    // das carreiras chegavam ao Legado, e 31 cartas nunca apareciam. Cada vida
    // completada começa mais velho: a era é função da idade, então quem insiste
    // atravessa o conteúdo já visto e alcança o tardio. Vida 1 aos 17, vida 2 aos 18,
    // vida 3 aos 20 (Estouro), vida 4+ aos 22 (Travessia).
    idade:IDADE_INICIAL(VIDAS),temporada:1,rodada:0,era:"base",contrato:2,lesao:0,
    flags:new Set(),estatisticas:{gols:0,jogos:0,titulos:0,selecoes:0,transferencias:0},
    historico:[],fila:[],agenda:[],vida:VIDAS,marca:m,jaAgendou:false,retornoEco:null,
    patamar:0,clube:sorteia(DADOS.clubes.clubes[0]),proposta:null,ultimoBalanco:null,ecoPendente:null,
    titulo:null,
    nome:sorteia(NOMES),apelido:null,elenco:{},arquetipos:{},
  };
  E.era=ERA_POR_IDADE(E.idade);
  if(m&&m.inicio) Object.assign(E.medidores,m.inicio);
  const _e=$("eco"); if(_e){ clearTimeout(mostrarEco._t); _e.classList.remove("vivo"); _e.textContent="" }
  escalarElenco();
  agendarCurto();
  proxima();
}

function escalarElenco(){
  for(const [slug,cfg] of Object.entries(DADOS.cargos.cargos)){
    let esc=cfg.elenco;
    if(cfg.persistencia==="eterno"||cfg.persistencia==="institucional"){
      E.elenco[slug]=esc[0];
    }else{
      let pool=esc;
      if(cfg.persistencia==="rotativo"&&ULTIMO_ELENCO[slug]&&esc.length>1)
        pool=esc.filter(x=>x.id!==ULTIMO_ELENCO[slug]);
      // peso quando declarado (arquétipos)
      const total=pool.reduce((s,x)=>s+(x.peso||1),0);
      let r=rnd()*total, pick=pool[0];
      for(const x of pool){ r-=(x.peso||1); if(r<=0){pick=x;break} }
      E.elenco[slug]=pick; ULTIMO_ELENCO[slug]=pick.id;
    }
    if(cfg.com_arquetipo) E.arquetipos[slug]=E.elenco[slug].id;
  }
}

// ======================= elegibilidade e sorteio =======================
// NENHUMA CARTA SORTEADA REPETE NA MESMA CAMPANHA.
// O cooldown de 25 parecia uma trava e era uma licença: a carreira mediana tem 47
// decisões, então 25 significa "pode repetir uma vez". Medido: 36% das carreiras
// repetiam alguma carta, concentradas nas marcadas com três eras, que ficam
// elegíveis por mais tempo — e não havia escassez nenhuma (35 a 100 cartas no pool
// em toda era menos o Legado). Agora a repetição é o fallback de escassez, não o
// comportamento normal: `relaxado` só é ligado quando o pool seca de verdade.
//
// Cartas que chegam por FILA ou por AGENDA continuam na regra antiga: as do motor
// (a decisiva, as duas da janela) são uma carta só cada e precisam voltar. As
// variantes delas são a próxima fase — enquanto não existirem, proibi-las de
// repetir apagaria a decisiva da segunda temporada em diante, silenciosamente.
function cumpre(c,relaxado){
  if(!c.era.includes(E.era)) return false;
  if(c.arquetipo && E.arquetipos[c.cargo]!==c.arquetipo) return false;
  const ultimo=E.historico.lastIndexOf(c.id);
  if(ultimo>=0){
    if(c.unico || !relaxado) return false;
    if(E.historico.length-ultimo<(c.cooldown||25)) return false;
  }
  const r=c.requer; if(!r) return true;
  if(r.flags && !r.flags.every(f=>E.flags.has(f))) return false;
  if(r.semFlags && r.semFlags.some(f=>E.flags.has(f))) return false;
  if(r.idade && (E.idade<(r.idade.min??-99) || E.idade>(r.idade.max??999))) return false;
  if(r.vida && E.vida<(r.vida.min??0)) return false;
  if(r.medidores) for(const [k,v] of Object.entries(r.medidores))
    if(E.medidores[k]<(v.min??-99)||E.medidores[k]>(v.max??999)) return false;
  return true;
}

// ======================= fios de três batidas =======================
// Uma carta de legado não termina quando você arrasta. Ela marca duas voltas:
// a consequência (20 a 30 cartas depois) e o acerto de contas (era seguinte).
// O eco prometeu que aquilo ficava — a agenda é quem cumpre a promessa.
function agendar(fio,eco){
  if(!fio) return;
  let min=(fio.em&&fio.em[0])??20, max=(fio.em&&fio.em[1])??30;
  // A PRIMEIRA CONTA DA CARREIRA CHEGA CEDO.
  // Medido: a primeira batida de retorno caía na decisão 29 (mediana) e 32% das
  // carreiras não viam nenhuma — e como um quarto das carreiras morre no Estouro,
  // perto da decisão 30, muita gente jogava inteiro sem nunca receber uma conta.
  // O fio só ensina que o jogo lembra se ele cobrar antes de a carreira acabar.
  if(!E.jaAgendou && min>10){ min=6; max=10; }
  E.jaAgendou=true;
  E.agenda.push({
    id:fio.id,
    em:E.rodada+min+Math.floor(rnd()*(max-min+1)),
    eraMin:fio.proximaEra?ORDEM_ERAS.indexOf(E.era)+1:-1,
    // o eco de QUEM ABRIU o fio viaja com a marcação: é com esta frase que a
    // batida de retorno vai se apresentar, e é o que dá legenda à linearidade
    eco:eco||null,
  });
}

// OS ABRIDORES DE FIO CURTO NÃO SÃO SORTEADOS — SÃO AGENDADOS.
// Peso não era a alavanca certa. Com peso 3 num pool de 47 cartas de peso ~9, um
// abridor tinha 1,4% de chance por sorteio: 18% em 14 cartas de Base, e medido
// 1,42 carta de fio curto por carreira contra 12 fios escritos. Com peso 9 (a
// tentativa anterior) eles dominavam a era e derrubaram a mediana de 68 para 47.
// O motor agenda UM por era, na segunda ou terceira carta: entrega garantida e
// dose exata, sem tocar em faixa de magnitude nenhuma.
//
// SÓ ENTRA NA AGENDA O FIO QUE NÃO OFERECE SAÍDA DO FUTEBOL, e isso foi medido no
// meio da rodada: agendando um abridor qualquer por era, 44% das carreiras
// terminavam num final verde (eram 12,5%) e a mediana caiu de 47 para 27 decisões.
// Sair do futebol é conteúdo bom e tem que continuar raro. O que precisa ser
// garantido é o fio que só cobra — e existe exatamente um desses em cada era.
// A varredura é feita no grafo, não numa lista: se um dia um fio agendado ganhar
// um `encerra`, ele sai da agenda sozinho.
function abreSaida(id,visto){
  visto=visto||new Set();
  if(visto.has(id)) return false;
  visto.add(id);
  const c=DADOS.cartas.find(x=>x.id===id);
  if(!c) return false;
  for(const lado of ["esquerda","direita"]){
    const o=c[lado];
    if(o.encerra) return true;
    if(o.fio && abreSaida(o.fio.id,visto)) return true;
  }
  return false;
}
function agendarCurto(){
  const cand=DADOS.cartas.filter(c=>/^curto_[a-z]+_b1$/.test(c.id)
    && c.era.includes(E.era)
    && !E.historico.includes(c.id)
    && !E.agenda.some(a=>a.id===c.id)
    && !abreSaida(c.id));
  if(!cand.length) return;
  const pick=cand[Math.floor(rnd()*cand.length)];
  E.agenda.push({id:pick.id,em:E.rodada+2+Math.floor(rnd()*2),eraMin:-1,eco:null});
}

// um fio vencido tem prioridade sobre o sorteio
function fioVencido(){
  let achado=null;
  for(let i=E.agenda.length-1;i>=0;i--){
    const a=E.agenda[i], f=DADOS.cartas.find(c=>c.id===a.id);
    // um fio pode ter várias portas de entrada. Se a batida já foi vivida,
    // a marcação é descartada em vez de ficar travada para sempre na agenda:
    // você não recebe dois acertos de contas pelo mesmo pecado.
    if(!f || (f.unico && E.historico.includes(f.id))){ E.agenda.splice(i,1); continue }
    if(achado) continue;
    if(E.rodada<a.em) continue;
    if(a.eraMin>=0 && ORDEM_ERAS.indexOf(E.era)<a.eraMin) continue;
    if(cumpre(f,true)){ E.retornoEco=a.eco||null; E.agenda.splice(i,1); achado=f; }
  }
  return achado;
}

// O SACO: memória de peso entre carreiras.
// A sobreposição da Base entre campanhas consecutivas era de 28,7% medidos, e isso
// é aritmética honesta — 14 cartas sorteadas de ~47, duas vezes, dá 30%. Escrever
// cem cartas novas de Base compraria o mesmo efeito que estas duas linhas.
// Peso reduzido, nunca zerado: zerar cria previsibilidade inversa — o jogador
// aprenderia que o que ele viu na vida passada não volta nunca.
let SACO=new Set();
// 0,35 derrubou a sobreposição da Base de 34,1% para 22,6% medidos; 0,2 é o que
// falta para chegar perto dos 15% sem virar proibição — carta vista na vida passada
// tem que poder voltar, senão o jogador aprende a regra pelo avesso.
const FATOR_SACO=0.2;
const pesoDe=c=>(c.peso??8)*(SACO.has(c.id)?FATOR_SACO:1);

function proxima(){
  if(E.ecoPendente){ const t=E.ecoPendente; E.ecoPendente=null; mostraCartaEco(t); return; }
  if(E.fila.length){
    const id=E.fila.shift(); const f=DADOS.cartas.find(c=>c.id===id);
    if(f && cumpre(f,true)){ mostra(f); return; }
  }
  const fio=fioVencido();
  if(fio){
    // A BATIDA DE RETORNO SE APRESENTA.
    // A linearidade existia nos dados e era invisível na tela: chegava uma carta
    // igual a qualquer outra, e o jogador teria que lembrar de uma decisão de trinta
    // cartas atrás E adivinhar que esta era a resposta. Agora a promessa é cobrada
    // com as mesmas palavras: o eco que disse "ficou" volta assinado "voltou".
    if(E.retornoEco){
      const t=E.retornoEco; E.retornoEco=null;
      E.fila.unshift(fio.id);
      mostraCartaEco(t,"voltou"); return;
    }
    mostra(fio); return;
  }
  let elegiveis=DADOS.cartas.filter(c=>(c.peso??8)>0 && cumpre(c,false));
  // fallback de escassez: só o Legado chega perto disso (pool p10 de 13 cartas).
  // Antes, a repetição ERA o fallback e valia sempre; agora ela é o último recurso.
  if(elegiveis.length<6) elegiveis=DADOS.cartas.filter(c=>(c.peso??8)>0 && cumpre(c,true));
  if(!elegiveis.length){ // nunca deve acontecer; se acontecer, empurra o calendário
    if(E.era==="legado"){ fim(resolverFinal(null,null)); return; }
    E.idade++; E.era=ERA_POR_IDADE(E.idade); proxima(); return;
  }
  const total=elegiveis.reduce((s,c)=>s+pesoDe(c),0);
  let r=rnd()*total, pick=elegiveis[0];
  for(const c of elegiveis){ r-=pesoDe(c); if(r<=0){pick=c;break} }
  mostra(pick);
}

// ======================= aplicação de escolha =======================
// Sem amortecimento perto dos extremos: foi testado com fator 0,3 / 0,45 / 0,72 e
// não comprava duração nenhuma (a idade de parar já faz isso) — só tirava impacto,
// e zerava as mortes por medidor, apagando 40 dos 57 finais.
// RENDIMENTO DECRESCENTE PERTO DO TETO, SÓ NO GANHO.
// Diagnóstico que obrigou isso: (a) uma estratégia coerente estourava um medidor em
// 7 decisões, porque nada resistia ao acúmulo monótono; (b) 83% das mortes por medidor
// eram por EXCESSO contra 17% por falta — o piso é defendido pelo interesse próprio do
// jogador, o teto não é defendido por ninguém.
//
// É DIFERENTE do amortecimento que testamos e descartamos: aquele valia nos dois
// sentidos e nos dois extremos, zerou as mortes por medidor e apagou 40 finais.
// Este vale só para GANHO e só acima de 70. A perda continua inteira, e o piso
// continua sem rede — de propósito.
// A regra final, depois de duas tentativas erradas:
//   O GANHO vale menos quanto mais longe do meio você está, para os DOIS lados.
//   A PERDA entra sempre inteira.
//
// Não é o amortecimento simétrico que descartamos — aquele enfraquecia a PERDA perto
// dos extremos, o que zerava as mortes por medidor. E não é só teto: amortecer só o
// ganho no teto consertou a proporção (54/46) mas derrubou as mortes por medidor de
// 32% para 15,3% das carreiras e devolveu 37,5% para o teto de idade.
//
// Amortecer o ganho nos DOIS extremos faz as duas coisas de uma vez: ninguém empurra
// um medidor até 100 em três cliques, E ninguém se resgata do chão de graça. É o
// "o mundo para de ajudar quem está no chão" implementado sem carta nova nenhuma.
// As duas pontas têm força DIFERENTE, e isso é medido, não estético: amortecer só o
// teto deixou a proporção em 54/46 mas derrubou as mortes por medidor para 15% das
// carreiras; amortecer as duas com a mesma força trouxe as mortes de volta a 31% e
// inverteu a proporção para 21/79. A força do piso controla o VOLUME de mortes por
// medidor; a razão entre as duas forças controla a PROPORÇÃO teto/piso.
const REND={teto:60,piso:26,folga:20,minimo:0.2};

function rendimento(k,v){
  if(v<=0) return v;                       // perda entra inteira, sempre, nos dois extremos
  const atual=E.medidores[k], d=Math.abs(atual-50);
  // Bónus de reencarnação: a folga CRESCE com a vida. Com a perda sempre inteira e o
  // ganho amortecido acima da folga, o sistema tem viés para baixo perto das bordas —
  // então folga maior significa menos viés e carreira mais longa. Testei o contrário
  // primeiro (folga menor) e o Legado caiu de 27% para 19%: o sinal era o oposto.
  const folga=REND.folga+Math.min(9,(E.vida-1)*3);
  if(d<=folga) return v;                   // no meio da barra, ganho cheio
  const div=atual>50?REND.teto:REND.piso;
  const f=Math.max(REND.minimo,1-(d-folga)/div);
  return Math.round(v*f) || (v>0?1:0);
}

function aplicar(efeitos){
  const m=E.marca;
  for(let [k,v] of Object.entries(efeitos||{})){
    if(m&&m.mult&&m.mult[k]) v=Math.round(v*m.mult[k]);
    if(m&&m.pedagio&&k==="torcida"&&v>0) E.medidores.diretoria-=1;
    E.medidores[k]+=rendimento(k,v);
  }
}

function escolher(lado){
  if(CARTA._eco){ proxima(); return; }   // carta de eco não decide nada, dos dois lados
  ANTES={...E.medidores};
  const o=CARTA[lado];
  // morte súbita
  if(o.morte){
    const chance=o.morte.chance??1.0;
    if(rnd()<chance){ fim(DADOS.finais.mortes_subitas.find(f=>f.id===o.morte.final)); return; }
    const s=o.sobrevive||{}; aplicar(s.efeitos); (s.flags||[]).forEach(f=>E.flags.add(f));
  }
  // carta de partida (risco)
  else if(o.tipo==="risco"){
    const chance=Math.max(.05,Math.min(.85,0.15+(E.medidores.forma-50)/160));
    const r=rnd()<chance?o.sucesso:o.falha;
    aplicar(r.efeitos); (r.flags||[]).forEach(f=>E.flags.add(f));
    for(const [k,v] of Object.entries(r.estatisticas||{})) E.estatisticas[k]=(E.estatisticas[k]||0)+v;
  }
  else{
    aplicar(o.efeitos); (o.flags||[]).forEach(f=>E.flags.add(f));
    for(const [k,v] of Object.entries(o.estatisticas||{})) E.estatisticas[k]=(E.estatisticas[k]||0)+v;
    if(o.lesao) E.lesao=o.lesao;
  }
  if(o.aceitaProposta) aplicarProposta();
  else if((CARTA.id&&CARTA.id.startsWith("transferencia_")) || (E.proposta&&E.proposta.daCarta)) E.proposta=null;
  // encerramento por ESCOLHA, não por morte: o fio curto que tira você do futebol
  if(o.encerra){ const f=DADOS.finais.escolhas_de_vida.find(x=>x.id===o.encerra); if(f){ fim(f); return; } }
  // o acerto de contas é o único lugar do jogo onde uma marca pode ser desfeita:
  // é o que faz a terceira batida de um fio valer mais que atmosfera
  (o.tiraFlags||[]).forEach(f=>E.flags.delete(f));
  for(const [k,v] of Object.entries(CARTA.estatisticas||{})) E.estatisticas[k]=(E.estatisticas[k]||0)+v;
  if(o.encadeia) E.fila.push(o.encadeia);
  agendar(o.fio,o.eco);   // a batida seguinte do fio, e o eco com que ela vai se apresentar
  if(CARTA.id==="capitao_bracadeira"||/^capitao_\w+_03$/.test(CARTA.id)) E.flags.add("viveu_arco_capitao");

  E.historico.push(CARTA.id);
  E.rodada++;
  if(E.lesao>0) E.lesao--;

  checarTitulo();
  const morto=checarMorte(); if(morto){ fim(morto); return; }
  if(E.rodada%CARTAS_POR_TEMPORADA===0){ if(viraTemporada()===false) return; }
  const morto2=checarMorte(); if(morto2){ fim(morto2); return; }
  // o eco só existe para quem continua jogando — quem morreu já tem o final para ler
  E.ecoPendente = o.eco || null;
  proxima();
}

// ======================= títulos =======================
// O jogador ganha UM título por vida, no momento em que a escolha que o mereceu é
// feita — não no fim. Depois de conquistado ele trava: mudar de título no meio
// transformaria conquista em placar, e a identidade da vida deixaria de ser fixa.
const VISTOS_TITULOS=new Set();

function casaTitulo(t){
  const c=t.condicoes||{};
  if(c.flags && !c.flags.every(f=>E.flags.has(f))) return false;
  if(c.semFlags && c.semFlags.some(f=>E.flags.has(f))) return false;
  if(c.era && !c.era.includes(E.era)) return false;
  if(c.idade && (E.idade<(c.idade.min??-99) || E.idade>(c.idade.max??999))) return false;
  if(c.medidores) for(const [k,v] of Object.entries(c.medidores))
    if(E.medidores[k]<(v.min??-99) || E.medidores[k]>(v.max??999)) return false;
  if(c.estatisticas) for(const [k,v] of Object.entries(c.estatisticas)){
    const x=E.estatisticas[k]||0;
    if(x<(v.min??-99) || x>(v.max??9999)) return false;
  }
  return true;
}

function checarTitulo(){
  if(E.titulo) return;                       // trava: um por vida
  for(const t of DADOS.titulos.titulos){     // a ordem da lista é a prioridade
    if(casaTitulo(t)){
      E.titulo=t; E.apelido=t.apelido||null; VISTOS_TITULOS.add(t.id);
      desenhaIdentidade(true);
      return;
    }
  }
}

function desenhaIdentidade(revelando){
  const el=$("identidade"); if(!el) return;
  const t=E.titulo;
  el.innerHTML=`<span class="quem-eu">${E.nome}${E.apelido?` "${E.apelido}"`:``}</span>`+
    (t?`<span class="titulo">${t.nome}</span>`:``);
  if(revelando&&t){
    el.classList.remove("revela"); void el.offsetWidth; el.classList.add("revela");
    const d=$("dica"); if(d){ d.textContent=t.desc; clearTimeout(desenhaIdentidade._t);
      desenhaIdentidade._t=setTimeout(()=>{ if(d.textContent===t.desc) d.textContent="" },3600); }
  }
}

// ======================= progressão: clube, ano e janela =======================
const PATAMARES=DADOS.clubes.patamares;

// a colocação sai da FORMA daquele recorte — é o pedido literal: o desempenho da
// temporada é o seu atributo naquele momento, não uma rolagem solta
function colocacaoDe(f,patamar){
  const forca=f+patamar*6-8;
  const base=forca>=80?1:forca>=66?3:forca>=52?6:forca>=38?11:16;
  const span=forca>=80?2:forca>=66?3:5;
  return Math.min(20,base+Math.floor(rnd()*span));
}

function julgar(col,titulo,f,d,patamar){
  const J=DADOS.clubes.julgamentos;
  if(titulo) return sorteia(J.titulo);
  if(col>=18) return sorteia(J.rebaixado);
  if(f>=68) return sorteia(d>=55?J.otimo_com_diretoria:J.otimo_sem_diretoria);
  if(f>=54) return sorteia(J.bom);
  if(f>=40) return sorteia(patamar>=3?J.medio_caro:J.medio);
  return sorteia(d>=60?J.ruim_com_diretoria:J.ruim);
}

function mostrarBalanco(){
  const b=E.ultimoBalanco; if(!b||!$("balanco")) return;
  $("b-cabeca").textContent=`temporada ${b.temporada} · ${b.clube}`;
  $("b-patamar").textContent=PATAMARES[b.patamar].nome;
  $("b-linha").innerHTML=
    `<div class="cel"><b>${b.jogos}</b><span>jogos</span></div>`+
    `<div class="cel"><b>${b.gols}</b><span>gols</span></div>`+
    `<div class="cel"><b>${b.colocacao}º</b><span>${b.titulo?"campeão":"na tabela"}</span></div>`;
  $("b-frase").textContent=b.frase;
  $("balanco").classList.remove("oculta");
}

// a janela: uma proposta com NOME e PATAMAR, para o jogador ter um alvo concreto
// A régua sobe junto com o patamar: no acesso basta um ano decente, no médio
// europeu é preciso um ano de p90. Os cortes vêm da distribuição medida em 2.963
// viradas de temporada (FORMA p50=51/p75=58/p90=64; TORCIDA p50=54/p75=62), e não
// de palpite — foi medindo que apareceu que 71% das carreiras morriam no acesso.
function abrirJanela(){
  const m=E.medidores, b=E.ultimoBalanco;
  const sobe=E.patamar<PATAMARES.length-1, desce=E.patamar>0;
  const barF=48+E.patamar*5, barT=42+E.patamar*4;
  let destino=null;
  if(sobe && E.idade<=32 && (b&&b.titulo || (m.forma>=barF && m.torcida>=barT)) && rnd()<0.40)
    destino=E.patamar+1;
  else if(desce && (m.forma<=36||m.diretoria<=28) && rnd()<0.35) destino=E.patamar-1;
  if(destino===null){ E.proposta=null; return; }
  const pool=DADOS.clubes.clubes[destino].filter(c=>c!==E.clube);
  E.proposta={clube:sorteia(pool),patamar:destino,sobe:destino>E.patamar};
  E.fila.push(destino>E.patamar?"transferencia_sobe":"transferencia_desce");
}

// Algumas cartas são transferência na narrativa e são anteriores à camada de
// progressão: prometiam clube novo e não trocavam nada. Elas declaram
// "aceitaProposta": {"delta": -1} e o motor gera a proposta quando a carta APARECE,
// para o texto poder dizer o nome do clube.
function prepararProposta(c){
  if(E.proposta) return;
  for(const lado of ["esquerda","direita"]){
    const a=c[lado]&&c[lado].aceitaProposta;
    if(a&&typeof a==="object"&&a.delta!==undefined){
      const destino=Math.max(0,Math.min(PATAMARES.length-1,E.patamar+a.delta));
      const pool=DADOS.clubes.clubes[destino].filter(x=>x!==E.clube);
      if(!pool.length) return;
      E.proposta={clube:sorteia(pool),patamar:destino,sobe:destino>E.patamar,daCarta:true};
      return;
    }
  }
}

function aplicarProposta(){
  if(!E.proposta) return;
  E.clube=E.proposta.clube; E.patamar=E.proposta.patamar;
  E.estatisticas.transferencias++;
  E.contrato=3; E.flags.add("trocou_de_clube");
  if(E.patamar>=3) E.flags.add("jogou_na_europa");
  E.proposta=null;
}

function viraTemporada(){
  E.temporada++; E.idade++; E.contrato--;
  // o corpo sempre vence no fim: o decaimento acelera e não dá para compensar para sempre
  const cedo=E.marca&&E.marca.decaiCedo, base=cedo?27:30;
  if(E.idade>=base+6) E.medidores.forma-=12;
  else if(E.idade>=base+3) E.medidores.forma-=8;
  else if(E.idade>=base) E.medidores.forma-=5;
  // P6 — aposentadoria distribuída. O corte seco aos 36 fazia 20% das carreiras
  // pararem exatamente no mesmo lugar, por calendário e não por acontecimento.
  // Agora a chance cresce dos 33 aos 36, e a última temporada é surpresa.
  const pararDe=IDADE_PARAR(E.vida), pararAte=pararDe+3;
  const fase=(E.idade-pararDe)/(pararAte-pararDe);   // 0 no primeiro ano, 1 no último
  if(E.idade>=pararAte || (fase>0 && rnd()<0.15+fase*0.55)){
    fim(resolverFinal(null,null)); return false;
  }
  // gols acompanham a forma: quem está bem marca, quem está mal aparece pouco
  const f=E.medidores.forma;
  const gols = f>70 ? 4+Math.floor(rnd()*9) : f>50 ? 2+Math.floor(rnd()*6) : Math.floor(rnd()*3);
  const jogos = Math.max(6, Math.round((18+rnd()*16)*(0.5+f/100)));
  E.estatisticas.gols += gols;
  E.estatisticas.jogos += jogos;
  const titulo = E.medidores.forma>62 && E.medidores.diretoria>48 && rnd()<0.26;
  if(titulo) E.estatisticas.titulos++;
  // o ano vira um ano: número de jogos, gols, colocação e uma frase de julgamento
  const col=colocacaoDe(f,E.patamar);
  E.ultimoBalanco={temporada:E.temporada-1,clube:E.clube,patamar:E.patamar,
    jogos,gols,colocacao:titulo?1:col,titulo,
    frase:julgar(titulo?1:col,titulo,f,E.medidores.diretoria,E.patamar)};
  mostrarBalanco();
  abrirJanela();
  // a decisiva da temporada, prevista no ritmo do GDD §3.1
  if(["estouro","travessia","auge"].includes(E.era) && rnd()<0.35) E.fila.push("capitao_partida");
  const nova=ERA_POR_IDADE(E.idade);
  if(nova!==E.era){
    E.era=nova;
    agendarCurto();   // um abridor de fio curto por era, agendado e não sorteado
    if(nova==="travessia"){
      if(E.estatisticas.transferencias>0) E.flags.add("jogou_na_europa");
      // o pedágio da companheira era empurrado aqui e nunca disparava: a flag
      // com_companheira só existe numa carta DA travessia, então chegava depois
      // deste ponto. Virou fio em companheira_01, que é onde a decisão acontece.
    }
  }
  if(E.contrato<=0){ E.flags.add("contrato_vencido"); E.contrato=2; }
}

function checarMorte(){
  for(const k of MEDIDORES){
    if(E.medidores[k]<=0) return resolverFinal(k,0);
    if(E.medidores[k]>=100) return resolverFinal(k,100);
  }
  return null;
}

// ======================= finais =======================
function derivadas(){
  const sujas=["investigacao_apostas","laranja","deve_pro_valdir","fundo_comprou_direitos","patrocinio_apostas"];
  const d=new Set();
  if(!sujas.some(f=>E.flags.has(f))) d.add("sem_escandalo");
  if(d.has("sem_escandalo")&&!["forcou_saida","calou"].some(f=>E.flags.has(f))) d.add("carreira_limpa");
  return d;
}
function bate(cond){
  const der=derivadas(); const tem=f=>E.flags.has(f)||der.has(f);
  if(cond.flags && !cond.flags.every(tem)) return false;
  if(cond.flags_qualquer && !cond.flags_qualquer.some(tem)) return false;
  if(cond.sem_flags && cond.sem_flags.some(tem)) return false;
  if(cond.era && !cond.era.includes(E.era)) return false;
  if(cond.idade && (E.idade<(cond.idade.min??-99)||E.idade>(cond.idade.max??999))) return false;
  if(cond.marca_de_alma && (!E.marca||E.marca.id!==cond.marca_de_alma)) return false;
  if(cond.medidores) for(const [k,v] of Object.entries(cond.medidores))
    if(E.medidores[k]<(v.min??-99)||E.medidores[k]>(v.max??999)) return false;
  if(cond.medidores_entre) for(const k of MEDIDORES)
    if(E.medidores[k]<cond.medidores_entre.min||E.medidores[k]>cond.medidores_entre.max) return false;
  if(cond.estatisticas) for(const [k,v] of Object.entries(cond.estatisticas)){
    const x=E.estatisticas[k]||0;
    if(x<(v.min??-99)||x>(v.max??99999)) return false;
  }
  return true;
}
function resolverFinal(medidor,extremo){
  // Morte por medidor na primeira era tem família própria. Sem isso, 44,5% de todas
  // as carreiras terminavam na MESMA tela: o final da Base morava no bloco contexto,
  // que é consultado antes das famílias, e a condição dele era só era=base.
  // A ordem contexto-antes-de-família continua certa — um garoto de 17 não pode
  // receber "Santo de gesso" —, o que faltava era a Base ter mais de um final.
  // O Estouro ganhou a mesma coisa em 12/08, e pelo mesmo motivo: é onde 26 a 31%
  // de TODAS as carreiras terminam — a maior fatia do jogo — e ele caía no genérico.
  // Escolha do Bruno: dar finais próprios em vez de baixar a mortalidade, que
  // desfaria a rodada de dificuldade.
  const PRECOCES={base:DADOS.finais.familias_precoces,estouro:DADOS.finais.familias_estouro};
  const bloco=PRECOCES[E.era];
  if(medidor!==null && bloco){
    const slot=bloco[medidor+"_"+extremo];
    // um slot pode ser um final só ou uma lista com condições, como as famílias
    // grandes. Foi preciso: com um final por slot, DINHEIRO 100 no Estouro sozinho
    // era 14,5% de todas as carreiras — o defeito do P1 um andar abaixo.
    if(Array.isArray(slot)){
      for(const f of slot) if(!f.condicoes || bate(f.condicoes)) return f;
      return slot[slot.length-1];
    }
    return slot || bloco.generico;
  }
  for(const f of DADOS.finais.contexto) if(bate(f.condicoes)) return f;
  if(medidor===null){ // fim natural da carreira: tem família própria
    for(const f of DADOS.finais.fim_natural) if(bate(f.condicoes)) return f;
    return DADOS.finais.fim_natural[DADOS.finais.fim_natural.length-1];
  }
  const fam=DADOS.finais.familias[medidor+"_"+extremo];
  E._familia=fam;
  for(const f of fam.finais) if(bate(f.condicoes)) return f;
  return fam.finais[fam.finais.length-1];
}

// ======================= render =======================
const $=id=>document.getElementById(id);
function corDe(slug){ return DADOS.paleta.cargos[slug]||"#888" }
function paletaEra(){ return DADOS.paleta.eras[E?E.era:"base"] }

function aplicaTema(){
  const p=paletaEra(), r=document.documentElement.style;
  r.setProperty("--fundo",p.fundo); r.setProperty("--superficie",p.superficie);
  r.setProperty("--traco",p.traco); r.setProperty("--texto",p.texto);
  r.setProperty("--texto2",p.texto_secundario); r.setProperty("--destaque",p.destaque);
  r.setProperty("--dourado",DADOS.paleta.molduras_ficha.dourada);
}

// retrato geométrico procedural, derivado do slug do cargo
function retrato(slug){
  const p=paletaEra(), cor=corDe(slug);
  let h=0; for(const ch of slug) h=(h*31+ch.charCodeAt(0))>>>0;
  const largo=64+(h%26), alturaOmbro=250+(h>>3)%40, raio=52+(h>>6)%16;
  const claro=["#3A3A3C","#1A1A1A","#6B4E8C","#4A6741"].includes(cor);
  const contorno=claro?p.texto_secundario:p.traco;
  const olhoY=232-(h>>9)%10;
  return `<svg id="retrato" viewBox="0 0 512 640" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg">
    <rect width="512" height="640" fill="${p.fundo}"/>
    <circle cx="256" cy="${180+(h>>4)%18}" r="${140+(h>>2)%20}" fill="${p.superficie}" opacity=".45"/>
    <path d="M ${256-largo*2.6} 640 L ${256-largo*1.5} ${alturaOmbro+120} Q 256 ${alturaOmbro+52} ${256+largo*1.5} ${alturaOmbro+120} L ${256+largo*2.6} 640 Z"
      fill="${cor}" stroke="${contorno}" stroke-width="8" stroke-linejoin="round"/>
    <circle cx="256" cy="${alturaOmbro-raio-6}" r="${raio+14}" fill="${cor}" stroke="${contorno}" stroke-width="8"/>
    <rect x="${256-raio*0.5}" y="${olhoY}" width="${raio*0.34}" height="9" rx="4" fill="${contorno}"/>
    <rect x="${256+raio*0.16}" y="${olhoY}" width="${raio*0.34}" height="9" rx="4" fill="${contorno}"/>
    <rect x="0" y="596" width="512" height="44" fill="${cor}" opacity=".22"/>
  </svg>`;
}

const ICONES={
 forma:'<path d="M13 2 4 14h6l-1 8 9-12h-6z"/>',
 torcida:'<path d="M3 10v4h3l5 4V6L6 10zM16 8a5 5 0 0 1 0 8M19 5a9 9 0 0 1 0 14"/>',
 diretoria:'<path d="M12 3 8 6l4 4 4-4zM12 10l-2 11h4z"/>',
 dinheiro:'<path d="M12 2v20M8 6h6a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h7"/>',
};
let ANTES=null;   // medidores antes da última escolha, para o rastro fantasma

function desenhaMedidores(){
  $("medidores").innerHTML=MEDIDORES.map(k=>{
    const cor=DADOS.paleta.medidores[k].cor, v=Math.max(0,Math.min(100,E.medidores[k]));
    const perigo=(v<=15||v>=85)?" perigo":"";
    const fechado=k==="diretoria"||k==="dinheiro";
    return `<div class="med apagado${perigo}" data-m="${k}">
      <svg viewBox="0 0 24 24" fill="${fechado?cor:'none'}" stroke="${cor}" stroke-width="2"
        stroke-linecap="round" stroke-linejoin="round">${ICONES[k]}</svg>
      <div class="bola" style="background:${cor}"></div>
      <div class="trilho">
        <div class="fantasma" style="background:${cor}"></div>
        <div class="barra" style="width:${v}%;background:${cor}"></div>
      </div></div>`;
  }).join("");
}

// desenha de onde cada barra veio e reage proporcionalmente ao tamanho do golpe
function reagirMedidores(){
  if(!ANTES) return;
  let maior=0, alvo=null;
  document.querySelectorAll(".med").forEach(el=>{
    const k=el.dataset.m;
    const de=Math.max(0,Math.min(100,ANTES[k])), pra=Math.max(0,Math.min(100,E.medidores[k]));
    const d=Math.abs(pra-de);
    if(d>maior){maior=d;alvo=el}
    if(d<0.5) return;
    const f=el.querySelector(".fantasma");
    // o fantasma cobre o trecho percorrido: é o que comunica QUANTO sem mostrar número
    f.style.left=Math.min(de,pra)+"%"; f.style.width=d+"%";
    f.classList.remove("vivo"); void f.offsetWidth; f.classList.add("vivo");
    el.classList.add(pra>de?"subiu":"caiu");
    if(d>=10) el.classList.add("forte");
    setTimeout(()=>el.classList.remove("subiu","caiu","forte"),700);
  });
  if(alvo && maior>=10){ alvo.classList.add("bateu"); setTimeout(()=>alvo.classList.remove("bateu"),400); }
}

function nomeDe(slug){ const i=E.elenco[slug]; return i?i.nome:"" }
function papelDe(slug){ return DADOS.cargos.cargos[slug].nome_do_cargo }
function interpola(t){
  return t.replace(/\{nome\}/g,nomeDe(CARTA.cargo))
          .replace(/\{apelido\}/g,E.apelido||E.nome)
          .replace(/\{clube\}/g,E.clube)
          .replace(/\{clube_novo\}/g,E.proposta?E.proposta.clube:"")
          .replace(/\{patamar_novo\}/g,E.proposta?PATAMARES[E.proposta.patamar].nome:"");
}

// a carta de eco: só texto, sem retrato, sem rótulo, sem consequência
// marca "ficou" = a promessa, logo depois da escolha.
// marca "voltou" = a cobrança, na frente da batida de retorno. Mesma frase, palavra
// diferente no pé: é o mínimo que dá legenda à linearidade sem explicar nada.
function mostraCartaEco(texto,marca){
  CARTA={_eco:true,id:"__eco",cargo:null,texto:texto,era:[E.era],
         esquerda:{rotulo:"",efeitos:{}},direita:{rotulo:"",efeitos:{}}};
  desenhaMedidores(); reagirMedidores();
  desenhaIdentidade(false);
  const el=$("carta");
  el.innerHTML=`<div id="eco-texto">${texto}</div><div id="eco-marca">${marca||"ficou"}</div>`;
  el.className="so-texto entrando"; el.style.transform=""; el.style.opacity=1;
  $("rotE").textContent=""; $("rotD").textContent="";
  $("dica").textContent="arraste para seguir";
}

function mostra(c){
  CARTA=c; prepararProposta(c); aplicaTema(); desenhaMedidores(); reagirMedidores(); desenhaIdentidade(false);
  $("carta").innerHTML=retrato(c.cargo)+
    `<div id="quem">${nomeDe(c.cargo)} · ${papelDe(c.cargo)}</div><div id="texto">${interpola(c.texto)}</div>`;
  $("carta").className=""; $("carta").style.transform="";
  $("carta").style.opacity=1;
  $("rotE").textContent=c.esquerda.rotulo; $("rotD").textContent=c.direita.rotulo;
  $("rodape").innerHTML=`<span>${E.clube}</span><span>${E.idade} anos · ${PATAMARES[E.patamar].curto}</span>`;
  $("dica").textContent = E.rodada<3 ? "arraste a carta para os lados" : "";
}

// destaca quais medidores mexem — nunca quanto
function realce(lado){
  const meds=[...document.querySelectorAll(".med")];
  meds.forEach(m=>{m.classList.remove("aceso","imp1","imp2","imp3")});
  if(!lado||!CARTA||CARTA._eco) return;
  const o=CARTA[lado];
  // opção fatal não se anuncia: quem avisa é o texto da carta, não a interface
  if(o.morte){ return; }
  const ef=o.tipo==="risco" ? {...o.sucesso.efeitos,...o.falha.efeitos} : (o.efeitos||{});
  // A bolinha diz QUANTO, nunca para que lado. Três tamanhos, porque três é o que
  // o olho distingue sem comparar — e as três faixas são as do peso dramático.
  meds.forEach(m=>{
    const d=ef[m.dataset.m];
    if(d===undefined) return;
    m.classList.add("aceso");
    const a=Math.abs(d);
    m.classList.add(a<=9?"imp1":a<=19?"imp2":"imp3");
  });
}

// ======================= arrasto =======================
let arrastando=false, x0=0, dx=0;
const LIMITE=()=>Math.min(110,$("area").clientWidth*0.27);
function comeca(x){ if($("carta").classList.contains("saindo"))return;
  arrastando=true;x0=x;dx=0;
  $("carta").className=(CARTA&&CARTA._eco)?"so-texto":""; }
function move(x){
  if(!arrastando)return;
  dx=x-x0;
  const rot=dx/17, op=1-Math.min(Math.abs(dx)/460,.32);
  $("carta").style.transform=`translateX(${dx}px) rotate(${rot}deg)`;
  $("carta").style.opacity=op;
  const p=Math.min(Math.abs(dx)/LIMITE(),1);
  const lado=Math.abs(dx)<14?null:(dx<0?"esquerda":"direita");
  $("rotE").style.opacity=dx<-14?p:0; $("rotD").style.opacity=dx>14?p:0;
  realce(lado);
}
function solta(){
  if(!arrastando)return; arrastando=false;
  const lim=LIMITE();
  $("rotE").style.opacity=0; $("rotD").style.opacity=0; realce(null);
  if(Math.abs(dx)<lim){ $("carta").className=(CARTA&&CARTA._eco)?"so-texto solta":"solta"; $("carta").style.transform=""; $("carta").style.opacity=1; return }
  const lado=dx<0?"esquerda":"direita", fora=dx<0?-620:620;
  $("carta").className=(CARTA&&CARTA._eco)?"so-texto saindo":"saindo";
  $("carta").style.transform=`translateX(${fora}px) rotate(${fora/16}deg)`;
  $("carta").style.opacity=0;
  setTimeout(()=>escolher(lado),210);
}
function liga(){
  const c=$("carta");
  c.addEventListener("pointerdown",e=>{c.setPointerCapture(e.pointerId);comeca(e.clientX)});
  c.addEventListener("pointermove",e=>move(e.clientX));
  c.addEventListener("pointerup",solta); c.addEventListener("pointercancel",solta);
  addEventListener("keydown",e=>{
    if($("t-fim").classList.contains("oculta")===false){ if(e.key==="Enter") $("b-denovo").click(); return }
    if(e.key==="ArrowLeft"||e.key==="ArrowRight"){
      const lado=e.key==="ArrowLeft"?"esquerda":"direita", fora=e.key==="ArrowLeft"?-620:620;
      if($("carta").classList.contains("saindo"))return;
      realce(lado);
      $("carta").className="saindo";
      $("carta").style.transform=`translateX(${fora}px) rotate(${fora/16}deg)`;
      $("carta").style.opacity=0; setTimeout(()=>escolher(lado),210);
    }
  });
}

// ======================= fim de carreira =======================
function fim(final){
  VISTOS_FINAIS.add(final.id);
  const molduras=DADOS.paleta.molduras_ficha;
  document.documentElement.style.setProperty("--moldura",molduras[final.moldura]||molduras.cinza);
  const anos=`${17}–${E.idade}`;
  $("ficha").innerHTML=`
    <div class="nome">${E.nome}${E.apelido?` "${E.apelido}"`:``}</div>
    <div class="sub">${E.titulo?E.titulo.nome:"sem título"} · ${anos} anos · vida ${E.vida}</div>
    <div class="grade">
      <div class="cel"><b>${E.estatisticas.jogos}</b><span>jogos</span></div>
      <div class="cel"><b>${E.estatisticas.gols}</b><span>gols</span></div>
      <div class="cel"><b>${E.estatisticas.titulos}</b><span>títulos</span></div>
      <div class="cel"><b>${E.estatisticas.selecoes}</b><span>seleção</span></div>
      <div class="cel"><b>${E.estatisticas.transferencias+1}</b><span>clubes</span></div>
      <div class="cel"><b>${E.temporada}</b><span>temporadas</span></div>
    </div>
    <div class="final">${final.nome}</div>`;
  $("f-texto").textContent=final.texto;

  // marca de alma da próxima vida
  let chave=null;
  for(const k of MEDIDORES){
    if(E.medidores[k]<=0) chave=k+"_0"; else if(E.medidores[k]>=100) chave=k+"_100";
  }
  MARCA_ATUAL=chave&&MARCAS[chave]?chave:MARCA_ATUAL;
  const prox=MARCA_ATUAL?MARCAS[MARCA_ATUAL]:null;
  $("marca").textContent = (VIDAS>=3&&prox) ? `Marca da próxima vida — ${prox.nome}: ${prox.desc}` : "";

  const escolhas=DADOS.finais.escolhas_de_vida||[];
  const precoces=Object.values(DADOS.finais.familias_precoces||{});
  // um slot do Estouro pode ser lista (variantes condicionais), então achata
  const estouro=Object.values(DADOS.finais.familias_estouro||{}).flat();
  const naturais=DADOS.finais.fim_natural||[];
  const total=DADOS.finais.mortes_subitas.length+DADOS.finais.contexto.length+escolhas.length+
    precoces.length+estouro.length+naturais.length+
    Object.values(DADOS.finais.familias).reduce((s,f)=>s+f.finais.length,0);
  const ids=[...Object.values(DADOS.finais.familias).flatMap(f=>f.finais.map(x=>x.id)),
             ...DADOS.finais.contexto.map(x=>x.id),...DADOS.finais.mortes_subitas.map(x=>x.id),
             ...escolhas.map(x=>x.id),...precoces.map(x=>x.id),...estouro.map(x=>x.id),
             ...naturais.map(x=>x.id)];
  $("galeria").innerHTML=ids.map(i=>`<div class="pino ${VISTOS_FINAIS.has(i)?"viu":""}"></div>`).join("");
  $("g-conta").textContent=`${VISTOS_FINAIS.size} de ${total} finais · `+
    `${VISTOS_TITULOS.size} de ${DADOS.titulos.titulos.length} títulos`;
  $("t-fim").classList.remove("oculta");
}

// ======================= boot =======================
$("b-comeca").onclick=()=>{ $("t-inicio").classList.add("oculta"); novoJogo(); };
$("b-denovo").onclick=()=>{ $("t-fim").classList.add("oculta"); $("balanco").classList.add("oculta"); novoJogo(); };
// o balanço é sobreposição, não pausa de estado: a carta seguinte já foi sorteada
// atrás dele. Isso mantém o loop testável e deixa o jogador ler no tempo dele.
$("b-segue").onclick=()=>$("balanco").classList.add("oculta");
aplicaTema(); liga();
// API para testes automatizados
window.__craque={estado:()=>E,escolher,proxima,novoJogo,vistos:()=>VISTOS_FINAIS,carta:()=>CARTA,
                 titulos:()=>VISTOS_TITULOS,realce,rend:REND,
                 semente:n=>{rnd=mulberry32(n>>>0)},
                 // os agentes de teste sorteiam pelo MESMO PRNG do jogo: sem isso a
                 // carreira não é reproduzível a partir da semente, e comparar duas
                 // baterias deixa de ser possível
                 rnd:()=>rnd(),
                 balanco:()=>E&&E.ultimoBalanco};
"""


def html(d):
    dados = json.dumps({
        "cartas": d["cartas"],
        "finais": d["finais"],
        "cargos": d["cargos"],
        "paleta": d["paleta"],
        "clubes": d["clubes"],
        "titulos": d["titulos"],
    }, ensure_ascii=False, separators=(",", ":"))
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>CRAQUE</title>
<style>{CSS}</style>
</head>
<body>
<div id="palco">
  <div id="identidade"></div>
  <div id="medidores"></div>
  <div id="area">
    <div id="rotE" class="rotulo"></div>
    <div id="rotD" class="rotulo"></div>
    <div id="carta"></div>
  </div>
  <div id="dica"></div>
  <div id="rodape"></div>

  <div class="tela oculta" id="balanco">
    <div id="b-cabeca"></div>
    <div id="b-patamar"></div>
    <div id="b-linha" class="grade"></div>
    <p id="b-frase"></p>
    <button id="b-segue">Próxima temporada</button>
  </div>

  <div class="tela" id="t-inicio">
    <h1>CRAQUE</h1>
    <p>Você tem dezessete anos e está na base de um clube.<br>
    Cada carta é uma decisão. Não existe escolha certa —<br>existe escolha que te mantém em campo mais uma temporada.</p>
    <p style="opacity:.65">Quatro medidores. Chegar a zero mata.<br><b>Chegar a cem também.</b></p>
    <button id="b-comeca">Começar</button>
  </div>

  <div class="tela oculta" id="t-fim">
    <div id="ficha"></div>
    <p id="f-texto"></p>
    <p id="marca"></p>
    <div id="galeria"></div>
    <p id="g-conta" style="font-size:11px;letter-spacing:.1em"></p>
    <button id="b-denovo">De novo</button>
  </div>
</div>
<script>const DADOS={dados};</script>
<script>{JS}</script>
</body>
</html>
"""


def main():
    d = carregar()
    saida = os.path.join(RAIZ, "craque.html")
    open(saida, "w", encoding="utf-8").write(html(d))
    kb = os.path.getsize(saida) / 1024
    fj = d["finais"]
    nf = (sum(len(f["finais"]) for f in fj["familias"].values())
          + len(fj["contexto"]) + len(fj["mortes_subitas"])
          + len(fj.get("fim_natural", [])) + len(fj.get("escolhas_de_vida", []))
          + len(fj.get("familias_precoces", {}))
          + sum(len(v) if isinstance(v, list) else 1
                for v in fj.get("familias_estouro", {}).values()))
    print(f"craque.html — {kb:.0f} KB · {len(d['cartas'])} cartas · {nf} finais · "
          f"{len(d['cargos']['cargos'])} cargos")


if __name__ == "__main__":
    main()
