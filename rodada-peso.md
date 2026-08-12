# CRAQUE — Rodada do Peso

**Objetivo:** fazer as decisões importarem. Especificação alinhada com o Bruno em 07/08/2026, antes de qualquer código.

---

## 1. Diagnóstico, com números

Análise das 559 opções do baralho:

| Medida | Hoje | Problema |
|---|---|---|
| Amplitude (maior ÷ mediana) | **2,2×** | Não existe diferença sentida entre uma rotina e um arco |
| Magnitude mediana | 9 pontos | |
| Movimento visual da mediana | **~4 pixels** por barra | **A causa maior. Mesmo quando a escolha importa, você não vê acontecer.** |
| Opções que são troca (dá e tira) | 98,6% | Isso já está certo — a estrutura existe, falta escala |

A intuição do Bruno estava certa e o número diz onde: não é que as decisões sejam iguais, é que **as consequências são invisíveis**.

---

## 2. A decisão que muda tudo: classificar por consequência, não por tamanho

A ideia original era classificar as cartas pelo tamanho do delta. Medindo o baralho, apareceu um critério melhor e automático:

> **Uma carta é de legado porque muda o seu final, não porque move um número grande.**

Isso é derivável do próprio conteúdo, sem julgamento:

| Peso | Critério | Cartas | Fatia |
|---|---|---:|---:|
| **Legado** | produz flag que um final **dourado** lê, ou é morte súbita | 36 | 12,6% |
| **Importante** | produz flag que outro final lê, ou é nó de arco | 60 | 21,1% |
| **Padrão** | não deixa rastro no sistema | 189 | 66,3% |

O tamanho do delta passa a ser **consequência** da classificação, não a causa. E o validador pode cobrar isso sozinho: se uma carta produz uma flag de dourado e está com magnitude de rotina, é erro.

---

## 3. Os três pesos — amplitude 8×

Escolha do Bruno: ir fundo e medir.

| Peso | Magnitude por opção | Medidores | Quanto move a barra |
|---|---|---|---|
| Padrão | **2–5** | 1–2 | ~2px — um empurrãozinho |
| Importante | **12–18** | 2–3 | ~7px por barra — dá para ver |
| Legado | **20–30** | 2–3 | **um quarto da barra de uma vez** |

Amplitude vai de 2,2× para **8×**.

### O custo, dito com honestidade

Com o mix 66/21/13, a média por opção sobe de 7,4 para **8,7 (+18%)**, e a variância sobe ~60%. Duração de carreira cai aproximadamente com o inverso da variância: a mediana de **159 cartas deve cair para a faixa de 100 a 115** — cerca de 12 a 13 minutos, abaixo da meta de 15 a 20.

**Compensações, nesta ordem** (as duas primeiras não tocam em conteúdo):

1. **Temporada de 8 para 10 cartas.** Mais cartas por ano, carreira mais longa em cartas sem mudar nada do balanceamento. Sozinha, devolve ~25%.
2. **Suavizar o decaimento por idade** (hoje −2 / −4 / −7) para −2 / −3 / −5.
3. Só se as duas não bastarem: reduzir a fatia de legado de 13% para 9%, promovendo as cartas de flag menos crítica de volta para importante.

Meço depois de aplicar e trago os números antes de considerar fechado.

---

## 4. As barras precisam reagir

Sem isso, nada acima é percebido. Três mudanças de apresentação:

- **Rastro fantasma** — a barra deixa um traço translúcido de onde veio, que desvanece em 600 ms. É o que comunica *quanto* sem mostrar número.
- **Tremor curto** na barra que sofreu a maior mudança da carta.
- **Ícone pulsando** na cor do medidor, mais forte quanto maior o delta.

Regra do GDD preservada: **nunca um número na tela**.

---

## 5. Ecos de legado — 36 escritos à mão

Escolha do Bruno: um por carta, sem pool genérico.

Aparecem por ~1,6 s depois do arrasto, em cima da carta que sai. Regras de escrita:

- **Nunca dizem o que mudou.** "Ele vai lembrar disso", não "a diretoria caiu 20".
- **São específicos daquela carta.** "Sua mãe soube antes de você contar" bate mais que "Ficou marcado".
- **Máximo 60 caracteres.** É um sussurro, não uma explicação.
- **Nenhum se repete no baralho.**

Exemplos do tom pretendido: *"Anotaram."* · *"Essa porta não fecha mais."* · *"O vestiário inteiro viu."* · *"Daqui a dez anos alguém ainda cita isso."* · *"Você acabou de escolher que tipo de jogador é."*

---

## 6. A Decisiva — o arco de masmorra

Uma vez por temporada a partir da era Travessia, ocupando o lugar da carta decisiva que já existe no ritmo da temporada.

### Estrutura

```
PORTÃO   "Você foi escalado para a final continental."
         Jogar  →  entra no arco          Amarelar  →  sai (−torcida, +diretoria)

BEAT 1   primeiro tempo: arriscar o passe / segurar o jogo
BEAT 2   o zagueiro que te marca: revidar / engolir
BEAT 3   dor no músculo aos 60: pedir substituição / continuar
BEAT 4   últimos minutos: chamar a responsabilidade / dar para o outro

RESOLUÇÃO   desempenho oculto (−4 a +4) + FORMA
```

### As seis saídas

| Saída | Como se chega | O que rende |
|---|---|---|
| **Craque da final** | desempenho alto **e** FORMA alta | título, torcida enorme, flag `craque_da_final` |
| **Título com atuação apagada** | desempenho baixo, time venceu | título, torcida quase nada — *"ninguém vai lembrar que você jogou"* |
| **Herói machucado** | desempenho alto, beat 3 ignorado | título, FORMA despenca, flag `infiltracao_cronica` |
| **Derrota heroica** | desempenho alto, sem título | torcida sobe mesmo perdendo |
| **Derrota com culpa** | desempenho baixo | torcida despenca, flag `perdeu_a_final` |
| **Saiu no primeiro tempo** | beat 3 mal resolvido | sem título, FORMA despenca |

Poucos caminhos levam ao título, como o Bruno pediu.

### O que faz virar masmorra

**Durante o arco, os quatro medidores somem da tela** e dão lugar ao placar e ao relógio da partida. Você navega às cegas.

**Decisão minha, para o arco não virar injustiça:** os efeitos dos beats **acumulam e só são aplicados na resolução**. Você não morre no meio de uma final sem ver por quê — mas pode absolutamente morrer quando ela acaba.

---

## 7. Progressão — as três camadas

Escolha do Bruno: as três de uma vez, porque se reforçam.

### 7.1 Clube com nome e nível

Cinco patamares, clubes fictícios: **base** → **série B** → **grande do país** → **médio europeu** → **gigante europeu**. O rodapé passa a mostrar clube e patamar. Transferência deixa de ser um número na ficha e vira subir ou descer de vida.

### 7.2 Balanço de fim de temporada

Tela curta entre temporadas, com números derivados da sua FORMA **naquele recorte** — é o pedido literal do Bruno:

```
TEMPORADA 6 · GRÊMIO DE ITAPEVA · GRANDE DO PAÍS
34 jogos · 11 gols · 3º lugar

"A diretoria esperava mais de quem custou o que você custou."
```

A frase de julgamento sai de uma matriz FORMA × DIRETORIA × colocação. É o que transforma oito cartas soltas num ano de carreira.

### 7.3 Janela de transferências nomeada

No fim da temporada, quando FORMA e TORCIDA justificam, entra uma proposta que **diz o nome e o patamar do clube**. O jogador passa a ter um alvo concreto para querer.

---

## 8. Ordem de execução

1. Classificar as 285 cartas por consequência e reescalar para 2-5 / 12-18 / 20-30
2. Rastro fantasma, tremor e pulso nas barras
3. Temporada para 10 cartas, decaimento suavizado
4. **Medir** — e trazer os números antes de seguir
5. Escrever os 36 ecos à mão
6. Clubes, balanço de temporada e janela nomeada
7. A Decisiva
8. Medir de novo, com os agentes de sempre

O validador ganha duas regras novas: magnitude compatível com o peso declarado, e toda carta de legado precisa de eco.


---

## 9. Executado — etapas 1 a 4

### Classificação e escala

| Peso | Cartas | Fatia | Magnitude final |
|---|---:|---:|---|
| Legado | 36 | 12,6% | 20–30 (mediana 24) |
| Importante | 62 | 21,8% | 12–18 (mediana 15) |
| Padrão | 187 | 65,6% | 2–5 (mediana 4) |

Amplitude **6×** (era 2,2×). Média por opção subiu de 7,4 para 8,2 — bem menos que os 18% que eu temia, porque a fatia de padrão puxa para baixo. Deriva do baralho seguiu dentro do limite nos quatro medidores sem precisar de ajuste.

### Feedback visual

Cada barra agora deixa um **rastro fantasma** cobrindo exatamente o trecho percorrido, que desvanece em 750 ms. Verificado no DOM: uma carta de legado com `forma +18, diretoria +7` desenhou rastros de 18% e 7% da largura da barra. Além disso, ícone pulsa (mais forte acima de 10 pontos) e a barra mais atingida treme.

Em pixels: a decisão mediana de legado agora move **~22px** de barra. Antes, a decisão mediana do jogo movia 4px.

### Duração, depois de compensar

A temporada de 10 cartas passou do ponto (22,6 min). O ajuste certo não era o calendário e sim a **idade de parar**: 37 anos em vez de 39, que além de resolver é o que acontece com jogador de verdade. Temporada voltou a 8 cartas.

| Agente | Cartas (mediana) | Tempo | Meta |
|---|---:|---|---|
| Aleatório | 41 | 4,8 min | 40–70 cartas ✅ |
| Humano plausível | **150** | **17,5 min** | 15–20 min ✅ |
| Equilibrista | 152 | 17,7 min | ✅ |

Zero erros de console, zero travamentos.

### O que o validador passou a cobrar

- magnitude compatível com o `peso_dramatico` declarado;
- toda carta de legado precisa de `eco` — hoje isso gera 36 avisos, que é exatamente o backlog da próxima etapa.

---

## 9b. Segunda passada — "aumente o valor das respostas"

Pedido do Bruno depois de jogar: o rastro aparece, mas o impacto podia ser maior.

### As faixas subiram 4×

| Peso | Antes | Agora | Movimento de barra da mediana |
|---|---|---|---|
| Legado | 20–30 | **32–44** | ~30px — um terço da barra |
| Importante | 12–18 | **18–26** | ~11px |
| Padrão | 2–5 | **6–10** | ~4px |
| Opção segura de morte súbita | 4–15 | **8–26** | — |

Delta individual: mínimo 2, mediana 4, máximo 30.

**Erro que eu cometi no meio do caminho, dito na hora:** na primeira tentativa a faixa de padrão foi para 2–5. Consertei o teto e estraguei o piso — 65% das cartas passaram a mover 1 ou 2 pixels. A faixa de padrão precisa ser pequena *em relação ao legado*, não pequena em absoluto.

### Ombros macios: medido e descartado

Amortecer o delta perto dos extremos parecia óbvio. A varredura (fator 0,72 / 0,45 / 0,3 / 0,0) disse o contrário:

- **duração comprada: zero.** Quem controla o tamanho da carreira é a idade de parar (37), não o amortecimento;
- **custo com 0,72: mortes por medidor caíram para 0%**, o que tornava **40 dos 57 finais inalcançáveis**.

Removido. É o segundo caso da rodada em que a medição derrubou o palpite.

### Deriva: o efeito colateral do reescalonamento

O arredondamento do 4× reintroduziu deriva (FORMA +0,11 e TORCIDA +0,20, contra o limite de ±0,08). Corrigido por `ferramentas/balancear-deriva.py`: **20 ajustes de ±1 espalhados por 18 cartas diferentes**, no máximo um por carta por medidor, e só onde a faixa de magnitude e a simetria continuam válidas. Deriva final: FORMA +0,059 · TORCIDA +0,057 · DIRETORIA −0,016 · DINHEIRO +0,022.

### Números depois de tudo

| Agente | Cartas (mediana) | Tempo | Finais distintos |
|---|---:|---|---:|
| Aleatório | 22 | 2,6 min | 20 |
| **Humano plausível** | **150** | **17,5 min** ✅ | **21** |
| Equilibrista | 151 | 17,6 min | 6 |

Como a carreira acaba (400 carreiras do agente humano): **15,3% medidor no extremo · 59,8% fim natural · 25,0% morte súbita**.

Validadores: `0 erros`, finais OK, paleta OK. Os 156 avisos restantes são flags de conteúdo futuro e os 36 legados sem `eco` — que é a próxima etapa.

---

## 9c. Etapa 5 — os 36 ecos, escritos

Um por carta de legado, nenhum genérico, nenhum repetido. Maior tem **47 caracteres**, média **40** — abaixo do teto de 60, porque é um sussurro e não uma explicação.

Nenhum diz o que mudou. Alguns exemplos:

> *"O joelho tem memória melhor que a sua."*
> *"Ele disse nós. Você ouviu bem."*
> *"O vestiário feminino assistiu inteiro."*
> *"Ele perguntou uma vez. Não pergunta de novo."*
> *"Aquele campo em branco tem dono agora."*
> *"Março chega todo ano. A vaga, não."*

**Decisão que tomei sozinho e vale registrar:** escrevi eco para as **10 mortes súbitas** também, que o validador não cobrava. Quem morre já tem o final para ler; quem escolheu a opção segura saía sem nada, e a carta mais tensa do baralho era justamente a única que não deixava rastro. Agora deixa.

### Como aparece

Sussurro em itálico no centro da tela por **1,9 s**, sobre um véu escuro, com a carta nova **recuada em brilho** — para o eco não parecer legenda da carta seguinte. Some sozinho, e some antes se você já arrastar a próxima.

O eco só fala para quem continua jogando: se a escolha matou, o final assume.

### Ritmo medido

200 carreiras do agente humano: **mediana de 15 ecos por carreira de 150 cartas** — um a cada dez cartas. Custo de tempo: ~24 s numa carreira de 17,5 min.

Validadores: `0 erros`, `130 avisos` (eram 156 — os 26 avisos de legado sem eco sumiram), finais OK, paleta OK.

---

## 9d. Etapa 6 — os fios de três batidas (9 de 36)

### O que é um fio

```
BATIDA 1   a decisão            2 opções   — a carta de legado que já existe
BATIDA 2   a consequência       2 cartas   — 20 a 30 cartas depois
BATIDA 3   o acerto de contas   4 cartas   — na era seguinte, com eco
```

7 peças por fio, progressão 2 → 4, o jogador sempre vendo só duas opções. **9 fios prontos, 54 cartas novas** — `cartas/fios.json`.

| Fio | Nasce em | Assunto |
|---|---|---|
| joelho | base | o exame que ela pediu e você ignorou |
| apostas | estouro | o patrocínio que não sai mais |
| fundo | estouro | 40% dos seus direitos econômicos |
| cicatriz | travessia | o treino dobrado que o capitão te ensinou |
| microfone | auge | o que você disse, ou não disse, no ar |
| laranja | auge | a empresa em que você é sócio sem saber |
| sucessor | declínio | o moleque de dezoito na sua posição |
| aniversário | declínio | o sábado que era dia de jogo |
| licença | declínio | o curso de treinador com aula na sexta |

### A mecânica nova: `tiraFlags`

A batida 3 é o **único lugar do jogo onde uma marca pode ser desfeita**. Sem isso o fio seria só castigo com data marcada; com isso ele é a sua chance de responder — e responder custa caro, sempre no medidor que você menos quer perder.

Medido com dois agentes, 200 carreiras cada:

| Agente | Marcas desfeitas por carreira | Terminou sem escândalo |
|---|---:|---:|
| Humano plausível (não persegue redenção) | 0,71 | 16% |
| Agente que joga para se limpar | **2,04** | **23%** |

Existe caminho de redenção, ele é visível, e continua difícil — 23% e não 80%. Era exatamente o que faltava para os finais dourados dependerem de trajetória e não de sorte.

### A terceira batida troca de cargo

O joelho que você ignorou aos 17 volta pela **imprensa** aos 29, não pelo fisioterapeuta. Das 36 batidas 3, a maioria chega pela boca de outra pessoa — é o que faz a consequência parecer mundo, não punição.

### Os números

| Medida | Resultado |
|---|---|
| Batidas 1 por carreira | 4,1 |
| Batidas 2 (consequência) | 3,4 |
| Batidas 3 (acerto de contas) | 2,9 |
| Carreiras que fecham ao menos um fio inteiro | **83%** |
| Espera mediana entre batidas | **27 cartas** (~3 min) |
| Fios abertos no fim da carreira | 1,3 — o final assume, via flag |
| Desfechos de batida 3 vistos em 250 carreiras | 34 de 36 |

Duração e mortalidade não se moveram: humano **152 cartas / 17,7 min**, equilibrista 152, aleatório 25. Mortes: 19,0% medidor · 56,3% natural · 24,8% morte súbita.

### O que o validador passou a cobrar

- `fio.id` tem que existir, e a janela tem mínimo de 4 cartas;
- **o fio tem que poder fechar**: se a batida seguinte não atua em nenhuma era igual ou posterior à atual, é erro. Foi assim que apareceu o caso do fio do aniversário, que exigia era seguinte para uma carta que só existe no declínio — nas eras finais não existe "era seguinte", e o `proximaEra` cai fora em vez de fingir;
- carta de `peso: 0` que ninguém chama é **carta inalcançável**, erro;
- `tiraFlags` que desfaz flag inexistente é erro de digitação, não licença poética;
- cobertura por era passou a ignorar cartas de peso 0 — elas não cobrem era nenhuma;
- as cartas de fio ganharam **checagem de deriva própria** (elas ficam fora da conta do baralho por ter peso 0). Achou de primeira: os fios empurravam TORCIDA em **+1,61 por carta**. Corrigido para +0,24 com 253 ajustes de ±1 espalhados pelas 54.

---

## 9e. Etapa 6 completa — as 36 cartas de legado abrem fio

### A decisão que trocou 162 cartas por 54

O plano dizia 27 fios privados, 162 cartas. Ao começar a escrever, a aritmética mostrou o problema: **cinco cartas do arco das apostas ganhariam cinco acertos de contas separados pelo mesmo pecado.** Isso não é consequência, é repetição — e daria 52 cartas de apostas num baralho onde o cargo já tinha 22.

O que fiz em vez disso: **fio com várias portas de entrada.** Um fio, muitas cartas que o abrem; a primeira que abre é a que vale, e o motor descarta as marcações seguintes.

| Fio novo | Portas | Cartas novas |
|---|---:|---:|
| apostas tardio | 5 | 6 |
| o empresário | 2 | 6 |
| a voz | 4 | 6 |
| a herança | 3 | 6 |
| entram em fios que já existiam (joelho, fundo, aniversário) | 3 | **0** |
| mortes súbitas, 3 peças cada | 10 | 30 |

**54 cartas novas em vez de 162.** O arco das apostas passou a ser uma espinha longa com cinco entradas em vez de cinco espinhas curtas. Baralho: 339 → **393 cartas**.

### Morte súbita tem fio de 3 peças, não de 7

Regra honesta: **a opção que te matou não tem consequência, tem final.** Então a batida 1 de uma carta de morte só ramifica de um lado — o de quem sobreviveu — e o fio é 1 consequência + 2 acertos de contas. Eram as cartas mais tensas do baralho e as únicas que não deixavam rastro em quem escapou.

### O erro que o balanço de flags pegou em mim

Contei quantas opções **põem** cada marca de escândalo e quantas a **desfazem**:

```
calou                    46 põem      10 tiram
investigacao_apostas     10 põem       2 tiram
forcou_saida              6 põem       0 tiram
```

Eu tinha usado `calou` como marcador genérico de "não quis conversa" em 42 opções de fio. Só que `calou` bloqueia `carreira_limpa` — então, sem perceber, eu tinha **matado o caminho de redenção enquanto escrevia as cartas que deviam criá-lo**. Corrigido: `calou` só fica onde você tinha o microfone numa coisa que importava e não usou (21 removidos), e as marcas que ninguém desfazia ganharam remoção.

Efeito, medido antes e depois: carreiras terminando sem escândalo foram de **11% para 29%**.

### O número que importa: finais dourados

Parei de medir o proxy e fui medir o que decide a coisa — quantas carreiras chegam a um final de moldura dourada, em 400 carreiras por agente:

| Agente | Dourados | Quantos dos 8 |
|---|---:|---:|
| Humano plausível | **0,8%** | 1 |
| Jogando para se limpar | **3,8%** | 2 |

**A redenção paga quase 5×** e o dourado continua raro, que é o ponto. Mas o número expõe uma coisa estrutural que não é bug dos fios: **6 dos 8 dourados nunca aparecem**, porque cada dourado pertence a uma família de morte por medidor — e só 19% das carreiras morrem por medidor. Os outros 81% caem em fim natural ou morte súbita, que não têm família dourada. O teto de dourado é baixo por construção, não por dificuldade.

Isso é decisão sua, não minha: dá para dar dourado ao fim natural, ou aceitar que dourado é coisa de quem morre no extremo. Deixo medido e à sua escolha.

### Os números finais

| Medida | Resultado |
|---|---|
| Batidas 1 por carreira | 11,8 |
| Batidas 2 (consequência) | 8,3 |
| Batidas 3 (acerto de contas) | **7,1** |
| Carreiras que fecham ao menos um fio inteiro | **84%** |
| Espera mediana entre batidas | 23 cartas |
| Desfechos de batida 3 vistos em 250 carreiras | 66 de 68 |
| Marcas desfeitas por carreira (humano / redenção) | 2,1 / 4,8 |

Duração: humano **154 cartas / 18,0 min**, equilibrista 156 / 18,2, aleatório 22. Validadores: `0 erros`, `138 avisos`, finais OK, paleta OK.

---

## 9f. Etapa 7 — progressão: clube, ano e janela

### 7.1 Clube com nome e patamar

Cinco patamares (`clubes.json`), **35 clubes inventados** — nenhum nome real, por decisão de projeto. O rodapé passou a mostrar clube e patamar em vez de era e temporada: a era já é dita pela paleta, e o clube é a informação que faltava.

```
acesso  →  segunda divisão  →  grande do país  →  médio europeu  →  gigante europeu
```

### 7.2 Balanço de fim de temporada

Tela curta entre temporadas, com **jogos, gols e colocação derivados da FORMA daquele recorte** — o pedido literal — mais uma frase de julgamento saída de uma matriz FORMA × DIRETORIA × colocação. 27 frases, nove tons, do "Campeão, e a foto que vai ficar é a sua" ao "A diretoria esperava mais de quem custou o que você custou".

É sobreposição, não pausa de estado: a carta seguinte já foi sorteada atrás dela. Mantém o loop testável e deixa o jogador ler no tempo dele.

### 7.3 Janela de transferências nomeada

Duas cartas com `{clube}`, `{clube_novo}` e `{patamar_novo}` resolvidos em tempo de jogo. A proposta tem nome e patamar; a opção que aceita é a única do jogo que troca de clube.

**A régua sobe com o patamar** — no acesso basta um ano decente, no médio europeu é preciso um ano de p90:

```
barra de FORMA   = 48 + patamar × 5
barra de TORCIDA = 42 + patamar × 4    (título dispensa as duas)
```

### O que a medição corrigiu

Na primeira versão a promoção pedia FORMA ≥ 62 fixo. Resultado: **71,6% das carreiras morriam no acesso** e 0% chegava a gigante — o jogador nunca subia de vida. Em vez de chutar outro número, medi **2.963 viradas de temporada**:

```
                p10  p25  p50  p75  p90
FORMA            39   45   51   58   64
TORCIDA          40   47   54   62   70
colocação         6   10   13   15   18
```

FORMA ≥ 62 é o topo de 12% dos anos. Com as barras recalculadas sobre essa distribuição:

| Patamar no fim da carreira | Antes | Agora |
|---|---:|---:|
| acesso | 71,6% | **25,2%** |
| segunda divisão | 22,0% | 32,0% |
| grande do país | 4,8% | 28,4% |
| médio europeu | 1,6% | 11,2% |
| gigante europeu | 0,0% | **3,2%** |

2,58 janelas oferecidas e 1,85 transferências por carreira; 15,8 balanços de temporada. Duração intacta: humano **154 cartas / 18,0 min**.

### O acaso bonito

O dourado **"O nome do estádio"** exige `transferencias: max 0`. Antes da janela, essa condição era decorativa — ninguém trocava de clube. Agora ela significa **recusar as 2,6 propostas da carreira**, uma por uma, sabendo o nome e o patamar do clube que você está dispensando. A camada de progressão transformou uma condição morta no dourado mais difícil dos oito.

---

## 10. Próximas etapas

6c. Decidir se **fim natural também merece família dourada** — hoje 81% das carreiras não podem chegar a dourado nenhum
7b. A arte: 15 retratos + variantes de arquétipo + 6 fundos de era + 14 ilustrações de final + ícones
7. Clubes com patamar, balanço de fim de temporada e janela de transferências nomeada
8. A Decisiva: árvore de 4 níveis, 16 desfechos, 6 fins precoces, 5 com título — rara e conquistada

---

## 9g. Correções do Bruno — 11/08

Quatro ressalvas depois de jogar. As quatro eram reais.

### 1. A interface entregava a decisão antes de ela ser tomada

O rótulo vermelho e o medidor tremendo numa opção fatal ficavam bonitos e **destruíam a carta**: ninguém escolhe o lado que a tela marcou como ruim. A carta mais tensa do baralho virava uma placa de trânsito.

**Removido inteiro** — a classe `.fatal` saiu do CSS, dos rótulos e dos medidores.

A regra do GDD que exigia morte telegrafada **continua valendo, e agora só de um jeito: pelo texto.** A previsão do tempo é ruim, a maionese ficou fora da geladeira a tarde inteira, o campo do objeto está em branco. O aviso está na prosa, e ler a prosa é o jogo.

### 2. O eco era o mesmo nos dois caminhos

Defeito meu, e dos grandes: um eco que não muda com a escolha **não promete consequência nenhuma, só decora**. Eu tinha escrito 108 ecos no nível da carta.

Agora são **206 ecos no nível da opção**, todos distintos, um por caminho:

| Carta | Um caminho | O outro |
|---|---|---|
| `fisio_base_01` | "O joelho tem memória melhor que a sua." | "Três semanas paradas custaram a peneira." |
| `valdir_auge_03` | "Dez anos terminaram no terceiro toque." | "Ele disse nós. Você ouviu bem." |
| `filho_declinio_01` | "Ele vai lembrar do sábado, não do gol." | "O gol saiu. Ele estava dormindo." |
| `imprensa_auge_01` | "O garoto viu o que você fez com o microfone." | "O garoto também viu o que você não fez." |

Lado fatal não tem eco: quem morre lê o final.

**O validador passou a cobrar:** eco no nível da carta é **erro**; eco repetido entre duas opções quaisquer do baralho é **erro**; eco em lado fatal é **erro**.

### 3. O eco virou carta de texto

Sussurro de 1,9 s some antes de ser lido — você estava certo. Agora o eco é **uma carta**, sem retrato, sem rótulo e sem consequência, assinada por uma palavra no pé: *ficou*. Fica na tela até você arrastar, e **arrastar para qualquer um dos lados faz a mesma coisa** — verificado: os quatro medidores ficam intactos.

### 4. A carta do roupeiro que falava de um clube que não existia

Achada e consertada: `roupeiro_travessia_01` agradecia a camisa do clube novo sem exigir que você tivesse trocado de clube. Passou a exigir `trocou_de_clube`, que o motor escreve quando você aceita uma proposta da janela.

Varri o baralho pela mesma classe de furo e achei mais quatro:

| Carta | Pressuposto | Correção |
|---|---|---|
| `valdir_auge_03` | "o clube que te comprou" | exige `trocou_de_clube` |
| `mae_travessia_01` | "errou o fuso de novo" | exige `jogou_na_europa` |
| `companheira_distancia_01` | "fuso de quatro horas" | exige `jogou_na_europa` |
| `fio_joelho_b3bb` | "o médico do clube novo" | reescrita — gatear quebraria o fio |

**Regra nova no validador**, para isso não voltar: toda expressão que pressupõe estado do motor (*clube novo, fuso, no exterior, o clube que te comprou, clube anterior*) tem que ter a flag correspondente em `requer`. É a checagem que eu não tinha e que você fez com o olho.

### O custo em tempo, medido honestamente

A carta de eco e o balanço de temporada são **leitura**, não decisão — contar 7 s para as duas coisas inflava o total. Medindo separado:

| | Quantidade | Segundos cada | Tempo |
|---|---:|---:|---|
| Decisões | 133 | 7 | 15,5 min |
| Cartas de eco | 17 | 3 | 0,8 min |
| Balanços de ano | 18 | 5 | 1,5 min |
| **Total** | | | **17,9 min** ✅ |

Com temporada de 8 cartas isso dava 20,7 min — fora da meta. **Temporada foi para 7 cartas**, que é o ajuste certo: cortar decisão, não cortar leitura. A cobertura por era só melhorou (consumo menor). Idade de parar também caiu de 37 para 36, dentro da faixa realista de 35 a 37.

Estado: `0 erros`, finais OK, paleta OK. Mortes 23,5% medidor · 58,3% natural · 18,3% morte súbita. Fios: 87% das carreiras fecham ao menos um inteiro.

*(Os segundos por carta são estimativa minha, não medição de jogador real — é a única parte deste número que não é medida.)*

---

## 9h. Rodada da dificuldade — 11/08

Pedido do Bruno: as carreiras estão longas e iguais; aumentar o peso das decisões e pôr mais mortes instantâneas, temáticas por era.

### O diagnóstico foi pior do que "as decisões são leves"

500 carreiras medidas na versão anterior:

```
decisões:  p10 37 · p25 124 · MEDIANA 133 · p75 133 · p90 133
70% das carreiras batiam o teto de idade
por medidor 10% · natural 71% · morte súbita 19%
```

Não era distribuição, era **paredão**: 71% das carreiras terminavam em *exatamente* 133 decisões. **Era o calendário que encerrava a carreira, não o jogador** — e é a mesma causa de 6 dos 8 dourados serem inalcançáveis, porque dourado exige morte por medidor.

### O que controla o tamanho da carreira (e o que não controla)

Testei os dois candidatos. Só um funciona:

| Alavanca | Efeito medido |
|---|---|
| **Variância dos deltas** | 1,00 → 133 decisões · 1,45 → 84 · 1,67 → 46 · **1,49 → 68** |
| Decaimento por idade mais cedo (30 → 28 anos) | **alongou** a carreira: 84 → 91, e o teto subiu de 26,6% para 31% |

O segundo resultado é o interessante: **pressão que o jogador consegue responder não mata — ela dirige.** Uma queda previsível de FORMA vira gradiente, e o jogador corrige na direção do meio, longe das duas bordas. Revertido.

Fator final: **1,49 acumulado**, calibrado em quatro medições. Faixas novas: padrão **8–15**, importante **26–40**, legado **46–67**, opção segura de morte **13–40**.

### Bug de processo que isso expôs

As faixas estavam **duplicadas** em `validar-cartas.py` e em `balancear-deriva.py`. Depois do reescalonamento uma ficou velha, e o balanceador passou a **rejeitar todo candidato em silêncio** porque media pela régua antiga — sem erro, sem aviso, só sem fazer nada. Agora existe `ferramentas/faixas.json` como fonte única e os dois leem de lá.

### As 24 mortes súbitas

Eram 10, com cobertura torta: base 2, estouro 2, travessia 2, auge 4, declínio 1 e **legado 0** — a era mais dramática do jogo não tinha nenhuma. Escrevi **14 novas, com final próprio cada**, fechando **4 por era**. O tema muda com a era, e é isso que faz a piada:

| Era | Você morre de | Exemplos |
|---|---|---|
| Base | moleque | descer na pista para comprar salgado; pelada de coturno na véspera |
| Estouro | novo-rico | garupa de mil cilindradas às 3h; bicicleta de terno na piscina de bolinhas |
| Travessia | estrangeiro | treinar de manga curta a −8°; visto vencido cruzando a fronteira |
| Auge | importante | jet ski até a ilha; helicóptero na véspera da final |
| Declínio | teimoso | a terceira infiltração com quem atende à noite; a cápsula dos quatro quilos |
| Legado | saudoso | jogo de veterano contra um lateral de 22; a chuteira da estreia no último treino |

**Peso de sorteio 4, e isso foi medido.** Com o peso normal (9), as 24 cartas levavam **43% das carreiras** a acabar em acidente burro — o que apaga o jogo de medidores e afunda os dourados de novo. Com peso 4 a fatia é 32% e, em 500 carreiras, **todas as 24 aparecem**. Carta rara vista ao longo de várias carreiras vale mais que carta comum vista sempre na mesma.

### Onde chegou

```
decisões:  p10 16 · p25 32 · MEDIANA 68 · p75 119 · p90 133
teto de idade: 14,4%   (era 70%)
por medidor 47% · morte súbita 32% · fim natural 21%
```

| | Quantidade | Tempo |
|---|---:|---|
| Decisões | 69 | 8,1 min |
| Cartas de eco | 6 | 0,3 min |
| Balanços de ano | 9 | 0,8 min |
| **Total** | | **9,1 min** ✅ |

**As eras finais viraram prêmio:** base 100% · estouro 90% · travessia 61% · auge 47% · declínio 32% · legado 23%. Conteúdo tardio deixou de ser passagem obrigatória, o que é o argumento a favor da reencarnação.

### O efeito colateral que era o objetivo escondido

Os dourados **abriram**. Mortes por medidor foram de 19% para 47%, e com elas:

| Agente | Dourados antes | Agora | Quantos dos 8 |
|---|---:|---:|---|
| Humano plausível | 0,8% | **1,0%** | 1 → **3** |
| Jogando para se limpar | 3,8% | **5,3%** | 2 |

Em 500 carreiras o jogo mostrou **57 finais distintos** e as 24 cartas de morte, todas. A dificuldade maior resolveu o problema estrutural que eu tinha registrado como pendência na etapa anterior — sem precisar mexer em `finais.json`.

Validadores: `0 erros`, finais OK, paleta OK, cobertura por era ≥ 2,2× em todas.

---

## 9i. Quatro adendos do Bruno — 11/08 (tarde)

### 1. O clube do rodapé não trocava — e eram cinco cartas, não uma

`valdir_base_04`, na base: *"tem um clube menor onde você estreia em três meses"*. A opção gravava a flag, **contava a transferência na ficha** e não trocava o clube. Cartas anteriores à camada de progressão, prometendo mudança de vida e entregando nada.

Consertei com um mecanismo em vez de um remendo: a opção declara `"aceitaProposta": {"delta": -1}` e o motor **gera a proposta quando a carta aparece** — assim o texto pode dizer o nome e o patamar do clube:

> "Ele diz que aqui você é o quarto da fila e que no **Esportivo Areia Branca** você estreia em três meses. É **divisão de acesso**, e ele diz isso na frente do Seu Nivaldo."

Detalhe que apareceu na hora de implementar: **no patamar 0 não existe "clube menor"** — existe outro clube do mesmo patamar. A transferência lateral passou a ser válida: troca o clube, não troca o degrau.

**E a regra nova do validador achou mais três** com o mesmo defeito: `diretor_declinio_02` (empréstimo), `valdir_declinio_02` e `valdir_declinio_03`. Agora é erro contar transferência sem `aceitaProposta`.

### 2. Fios curtos, dentro da era

Os fios longos entregam a consequência 25 cartas depois; o jogador precisava entender **na primeira era** que a escolha muda o destino. **12 fios curtos**, dois por era, janela de 3 a 8 cartas — e **seis deles podem encerrar a carreira por escolha**, com final de **moldura verde**: não é derrota, é outra vida.

O do estudo é o exemplo que você deu, ligado na carta que já existia (`mae_base_01` → "Volto pra escola"):

```
mãe pergunta quando você volta a estudar   →  "Volto pra escola"
   ↓ 3 a 8 cartas
treino mudou para as sete, a escola é às sete e meia
   ↓ 4 a 9 cartas
vestibular domingo às oito · teste do profissional domingo às oito
   → "Vou fazer a prova"  =  FIM: "Passou em primeira chamada"
```

Os seis finais de escolha: faculdade, a oficina do tio, voltar antes de precisar voltar, o microfone do outro lado (a TV aos 28), andando normal aos cinquenta, a escolinha do bairro. Todos são **bons finais** — só não são de jogador. **9,3% das carreiras** terminam num deles.

### 3. Bolinha de impacto

Círculo acima do ícone do medidor, três tamanhos, aparece no arrasto: **5px** (delta até 9), **9px** (até 19), **14px com brilho** (acima). Diz *quanto*, nunca para que lado — não muda de cor, de forma nem de posição com o sinal.

Detalhe de implementação que custou uma iteração: a bolinha crescendo **empurrava a barra do medidor para baixo**. Caixa fixa de 14px com escala por `transform`: o tamanho muda, o layout não.

### 4. Títulos, revelados no momento

**21 títulos** em `titulos.json`. Aparecem no alto da tela, ao lado do nome, **no instante em que são conquistados**. O primeiro que casa **trava** — um título por vida, e ele não muda depois, porque título que muda no meio é placar, não identidade. Coleção separada dos finais, mostrada na ficha final.

**O erro que a primeira versão tinha, e o número que o mostrou:** com os títulos de medidor no meio da lista, **58% das carreiras terminavam como "O Ídolo" ou "O Moleque"** e só 11 dos 21 títulos apareciam. Como o título trava, um genérico conquistado na segunda temporada apaga todos os específicos para sempre. Correção: **títulos de flag vêm antes dos de medidor**, e os de medidor ganharam idade mínima e corte mais alto. Depois: 14 dos 21 vistos, e o mais comum caiu de 31% para 14,5%.

### O custo em duração, e como foi pago

Os fios curtos derrubaram a mediana de 68 para 47 decisões. Duas causas, encontradas medindo em vez de chutando:

1. **Eu pus cartas de magnitude `legado` (46–67) na era Base.** Um golpe de 60 pontos na primeira era é quase fatal. E elas não são legado: o peso delas é a **escolha de sair**, não o delta. Reclassificadas para `importante`, com o lado que fica reescalado.
2. Abridores com peso 9 dominavam as eras iniciais. Peso 3: continuam aparecendo (1,66 carta de fio curto por carreira, e **as 24 aparecem** em 600 carreiras) e param de dominar.

Descartado pelo caminho: a hipótese de que os finais de escolha encurtavam a carreira. Mediana **com** eles 56, **sem** eles 57 — não eram a causa.

Depois disso, dois ajustes finos de escala (×0,95 duas vezes, fator acumulado **1,344**) para voltar à faixa:

| | Quantidade | Tempo |
|---|---:|---|
| Decisões | 60 | 7,0 min |
| Cartas de eco | 6 | 0,3 min |
| Balanços de ano | 8 | 0,7 min |
| **Total** | | **8,0 min** ✅ (meta 8–12) |

Estado: **433 cartas · 68 finais · 21 títulos**. `0 erros`, finais OK, paleta OK. Fim de carreira: 32,8% medidor · 34,8% morte súbita · 23,0% natural · **9,3% escolha de vida**. 75,5% das carreiras conquistam título; em 600 carreiras o jogo mostrou **59 finais e 14 títulos distintos**.

### Adendo 4b — a carreira começa sem apelido

O apelido era sorteado no início da vida e aparecia entre aspas desde a primeira carta, o que é o oposto de conquista. Agora **ninguém nasce com apelido**: cada um dos 25 títulos carrega o seu, e os dois chegam juntos.

```
começo da carreira        GABI
depois da decisão         GABI "CADERNO"   ( O Universitário )
```

Nenhuma carta usava `{apelido}` no texto, então nada quebrou — e o token passou a cair no nome enquanto não houver apelido.

**Um número obrigou a segunda metade da correção.** Com os 21 títulos que existiam, o primeiro chegava na **decisão 36 de 60** (mediana) e **26% das carreiras terminavam sem nenhum** — um HUD que passa metade da carreira vazio não é identidade, é espaço em branco. Escrevi quatro títulos alcançáveis logo, ligados a flags que a base e o estouro já produziam:

| Título | Apelido | Como se ganha |
|---|---|---|
| O Arrimo | Conta | o salário da base virou o salário da casa |
| O Difícil | Cara | disse não para dinheiro fácil na primeira vez |
| O Duro | Casco | joga com o joelho inchado desde os dezessete |
| O Tudo ou Nada | Aposta | largou a escola porque não existia plano B |

Depois: título na **decisão 16** (mediana), **88,3%** das carreiras conquistam um, e a conquista acontece na base ou no estouro em 87% dos casos. O mais comum caiu para 18,5%, e em 600 carreiras aparecem 14 títulos distintos e 63 finais.
