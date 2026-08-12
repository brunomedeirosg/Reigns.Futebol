# CRAQUE — rodada de correções do diagnóstico

Executada em 11/08 sobre os seis problemas do `diagnostico-balanceamento.md`. Medido com os dez agentes de personalidade, duas sementes independentes, 2.000 carreiras antes e 2.000 depois.

---

## Os números, antes e depois

| Medida | Antes | Depois | Alvo | |
|---|---:|---:|---|:--:|
| Final mais frequente (agente realista) | 44,5% | **5,5%** | < 12% | ✅ |
| Final mais frequente (agregado dos dez) | 44,5% | 17,8% | < 12% | ⚠️ |
| Finais distintos vistos | 62 | **72** | mais | ✅ |
| Mortes por medidor: excesso / falta | 83 / 17 | **~40 / 60** | 70/30 a 55/45 | ✅ |
| Mortes por medidor, em % das carreiras | 32% | **40%** | manter ou subir | ✅ |
| Cartas nunca vistas (de 433) | 31 | **13 a 19** | < 10 | ⚠️ |
| Pico do histograma de duração | 20% (teto de idade) | **6,4%** | < 15% | ✅ |
| Decisões até a morte por monomania | 7 | 7 | > 15 | ❌ |
| Títulos conquistados (de 25) | 16 | 16 | mais | ❌ |
| Duração do agente realista | 73 dec · 9,6 min | **80 dec · 10,6 min** | 8 a 12 min | ✅ |

Validadores: `0 erros`, finais OK, paleta OK, zero erros de console em 4.000 carreiras.

---

## P1 — o final único da era Base ✅

**Feito:** bloco `familias_precoces` com 8 finais, um por medidor e extremo, consultado antes do contexto quando a morte é por medidor e a era é a Base. O antigo *"O que não passou da base"* virou o genérico de quando nenhum casa.

Os oito: *Cansado aos dezoito* · *Treinou até sobrar* · *Marcado no vestiário* · *Fenômeno da base* · *Dispensado* · *O afilhado* · *A passagem que faltou* · *Rico antes de estrear*.

**Efeito:** para o agente realista, o final mais frequente caiu de 44,5% para **5,5%**. O CR7 saiu de **1 final em 200 carreiras para 3**; o Gabigol de 2 para 3, e agora morre em *"Fenômeno da base"* — promessa nacional antes de ser jogador —, que ensina algo, ao contrário da tela genérica.

Os 17,8% que sobram no agregado são inteiramente o Gabigol morrendo sempre do mesmo jeito (96% das carreiras dele). Não é problema de jogador, é característica de um agente que só quer torcida.

## P2 — o teto matando 5× mais que o piso ✅

Aqui eu errei duas vezes antes de acertar, e vale registrar as duas.

**Tentativa 1 — amortecer o ganho só no teto.** Consertou a proporção (83/17 → 54/46) e **derrubou as mortes por medidor de 32% para 15,3% das carreiras**: as famílias ficaram mais famintas do que antes, e o teto de idade voltou a 37,5%. Mesma armadilha do amortecimento simétrico que já tínhamos descartado.

**Tentativa 2 — amortecer o ganho nos dois extremos com a mesma força.** Trouxe as mortes de volta a 31% e **inverteu a proporção para 21/79** — a imagem espelhada do problema original.

**O que ficou:** ganho amortecido nos dois extremos com **forças diferentes**, perda sempre inteira.

```js
const REND={teto:60,piso:26,folga:20,minimo:0.2};
// perda entra inteira, sempre, nos dois extremos
// ganho cheio no meio (±20); acima disso decai, mais rápido no piso que no teto
```

A descoberta que organizou tudo: **a força do piso controla o VOLUME de mortes por medidor; a razão entre as duas forças controla a PROPORÇÃO teto/piso.** Isso permitiu varrer seis combinações e escolher com número em vez de intuição.

**Resultado:** ~40/60, mortes por medidor em **40% das carreiras** (era 32%), e **todas as 8 famílias acionadas** — antes as quatro de piso somavam 4% de tudo.

Sobre a sua proposta: **não foi preciso escrever carta nenhuma.** A versão da sua ideia que sobreviveu ao diagnóstico — a perda inteira e o ganho enfraquecido — deu conta sozinha, e sem 12 cartas novas para manter. As "cartas de conta" ficam disponíveis se um dia quisermos empurrar o piso mais ainda.

## P3 — monomania matando em 7 decisões ❌ não resolvido

**O que eu recomendei no manual não funcionaria, e medir mostrou isso:** o teto de magnitude por carta na Base atinge **3 opções** do baralho inteiro. Seria quase inócuo. A causa não é a carta grande, é o **acúmulo monótono**.

Apliquei o rendimento decrescente esperando que resolvesse, e ele **não resolveu**: Gabigol e CR7 continuam em 7 decisões. O que melhorou foi a *qualidade* da morte — 1 final virou 3, e os finais agora são temáticos.

Por que não resolveu: o amortecimento só começa acima de 70, e ir de 50 a 70 com ganhos cheios já são quatro ou cinco cartas alinhadas. Para mover isso, a folga precisaria encolher para ~10, e aí toda carreira normal fica mais lenta.

**Fica em aberto**, com o que eu tentaria numa próxima: **pool de abertura** — as primeiras 6 a 8 cartas de toda carreira saem só de magnitude `padrao`. É a única das três soluções do manual que não foi testada, e é a que não depende de o jogador variar.

## P4 — conteúdo tardio ✅ parcial, e um bug de brinde

Você pediu as duas: reencarnação **e** portas mais cedo. As duas foram feitas, e a primeira exigiu três tentativas.

**O bug que apareceu no caminho, e é o achado desta rodada.** As 6 cartas do arco da companheira eram **inalcançáveis por ordenação**: `companheira_01` é carta *da* travessia e produz `com_companheira`; o motor empurrava `companheira_pedagio` *ao entrar* na travessia, checando essa flag. A flag chegava sempre depois do empurrão. Sem o pedágio não existem `companheira_veio_junto` nem `companheira_ficou`, e sem eles as outras cinco cartas nunca podiam aparecer. **Uma linha de ordem errada matava seis cartas há semanas.** Virou fio em `companheira_01` — o arco inteiro (16 cartas) agora aparece.

**Segundo órfão:** `capitao_partida`, peso 0, estava na lista de "chamadas pelo motor" do validador — mas **o motor nunca a chamava**. Passou a ser a decisiva da temporada, como o ritmo do GDD já previa.

**A reencarnação, e as duas versões erradas antes da certa:**

1. *Começar mais velho* (vida 2 aos 18, vida 3 aos 20, vida 4+ aos 22). Chegou-se mais ao Legado — e **as cartas nunca vistas foram de 31 para 100**, porque a era Base passou a ser pulada. Trocou a cauda pela cabeça.
2. *Pista mais longa* (veterano se aposenta mais tarde). Consertou o pico de aposentadoria e **não mexeu no Legado** (27%): o gargalo é sobreviver *até* os 33, não depois.
3. *Folga maior com a vida* — o veterano tem a mão mais firme, o amortecimento começa mais longe do meio. **Legado 27% → 38%, Declínio 35% → 49%.** Também tentei o contrário primeiro (folga menor) e o Legado caiu para 19%: com a perda sempre inteira, folga menor cria viés para baixo. O sinal era o oposto do que eu supunha.

**Cartas nunca vistas: 31 → 13.** As que sobram são batidas 2 e 3 de fio no declínio e no legado, que dependem de chegar lá.

## P5 — concentração de finais ✅ derivado, como previsto

**Finais distintos: 62 → 72.** Para o agente realista, o mais frequente é 5,5% e a distribuição por categoria ficou saudável: **40% medidor · 38% morte súbita · 15% natural · 6% escolha de vida**.

## P6 — o pico no teto de idade ✅

Aposentadoria distribuída: a chance cresce ao longo de quatro anos em vez de um corte seco. O pico de **20% numa idade só virou 6,4%**, espalhado dos 32 aos 39 (o topo depende da vida — veterano joga mais tempo).

---

## O que continua aberto

| Problema | Estado | O que eu tentaria |
|---|---|---|
| **P3** — monomania em 7 decisões | não resolvido | Pool de abertura: as primeiras 6 a 8 cartas só com magnitude `padrao` |
| **Títulos** — 16 de 25 conquistados | inalterado | Os 9 que faltam são de declínio e legado; agora que 38% dos veteranos chegam lá, medir de novo com mais carreiras antes de mexer |
| **13 cartas** ainda sem aparecer | de 31 para 13 | Mesma coisa: são batidas tardias de fio, e a reencarnação acabou de abrir o caminho |

## O que aprendi nesta rodada, e vale para a próxima

**Três dos meus palpites tinham o sinal errado**, e só a medição mostrou: amortecer só o teto piorou o volume; folga menor para o veterano encurtou a carreira; teto de magnitude por carta atingiria 3 cartas. Nenhum desses erros teria aparecido em leitura de código.

**E duas cartas estavam inalcançáveis por bug de ordenação, não por balanceamento.** A lista de "conteúdo nunca visto" deixou de ser um relatório de balanceamento e passou a ser o melhor detector de bug que este projeto tem — foi ela que achou o arco da companheira e a `capitao_partida`.
