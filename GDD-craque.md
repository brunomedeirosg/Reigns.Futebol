# CRAQUE — Documento de Design de Jogo (GDD)

**Versão:** 1.2 — protótipo jogável, com peso dramático e feedback visual
**Gênero:** narrativa por cartas / swipe, gestão de recursos
**Plataforma:** navegador (desktop + mobile), single-player, offline
**Idioma:** português brasileiro
**Sessão-alvo:** 8 a 12 minutos por carreira (várias carreiras por sessão)
**Documentos irmãos:** `cargos.md` + `cargos.json` (elenco) · `finais.md` + `finais.json` (finais) · `arte/README-nomenclatura.md` (guia de arte)
**Referência-mãe:** *Reigns* (Nerial/Devolver, 2016)

---

## 1. Visão geral

Você é um garoto de 17 anos na base de um clube. Cada carta é uma decisão: um treinador, um empresário, um jornalista, sua mãe, um patrocinador de casa de apostas, um zagueiro que quer te quebrar. Arrasta para a esquerda ou para a direita. Não existe escolha certa — existe escolha que te mantém em campo mais uma temporada.

A carreira termina quando um dos quatro medidores estoura, para cima ou para baixo. Aí o jogo não recomeça do zero: você assume a próxima promessa da mesma base, num mundo que ainda lembra o que você fez.

**Pitch de uma linha:** *Reigns* com chuteira — a carreira inteira de um jogador de futebol resolvida em dois gestos do polegar.

### 1.1 Pilares de design

| Pilar | O que significa na prática |
|---|---|
| **Duas escolhas, nenhuma limpa** | Toda carta oferece dois caminhos que ganham algo e custam algo. Se uma opção é obviamente melhor, a carta está mal escrita e deve ser reescrita. |
| **A carreira é o relógio** | O tempo só anda para a frente. Idade, contrato e desgaste são irreversíveis. Não existe "recomeçar a temporada". |
| **Humor ácido, mundo sério** | A trajetória é realista (base → primeiro time → Europa → seleção → declínio). A sátira está nas pessoas ao redor: agentes, dirigentes, imprensa, torcida, marcas. |
| **Legibilidade instantânea** | O jogador entende uma carta em menos de 4 segundos. Texto curto, personagem reconhecível, consequência sugerida por ícones — nunca por números. |
| **Morrer é conteúdo** | Cada final tem nome, imagem e ficha de carreira. Perder gera vontade de contar para alguém. |

### 1.2 O que este jogo **não** é

- Não é um *Football Manager*: não há escalação, tática nem tabela.
- Não há árvore de habilidades nem construção de personagem numérica visível.
- Não há multiplayer, gacha ou economia de tempo real (sem "espere 4h").

---

## 2. Core loop

```
   ┌──────────────────────────────────────────────────┐
   │  1. Sorteia carta elegível (era + flags + meters) │
   │  2. Mostra personagem + situação (≤ 220 chars)    │
   │  3. Jogador arrasta ← ou →                        │
   │     · durante o arrasto, ícones mostram QUAIS     │
   │       medidores mexem — nunca quanto              │
   │  4. Aplica deltas, flags, encadeamentos           │
   │  5. Avança o calendário (+1 rodada)               │
   │  6. Checa: medidor em 0 ou 100? → FIM             │
   │     Fim de temporada? → cartas de intervalo       │
   └──────────────────────────────────────────────────┘
```

**Duração de uma partida:** o alvo é **8 a 12 minutos**, medido em decisões (~7 s cada) mais as cartas de eco (~3 s) e os balanços de ano (~5 s):

| | Decisões | Tempo |
|---|---:|---|
| p10 — morreu de bobeira | 16 | ~2 min |
| p25 | 32 | ~4 min |
| **mediana** | **68** | **9,1 min** |
| p75 | 119 | ~15 min |
| p90 — sobreviveu a tudo | 133 | ~17 min |

**A regra que veio da medição:** quem controla o tamanho da carreira é a **variância dos deltas**, não o calendário e não o decaimento por idade. Com os deltas na escala original, **70% das carreiras batiam o teto de idade e terminavam em exatamente 133 decisões** — não era uma distribuição, era um paredão, e por isso todas as partidas tinham a mesma duração. Antecipar o decaimento por idade foi testado e **alongou** a carreira: pressão que o jogador consegue responder vira gradiente e o faz corrigir para o meio. Pressão que mata é variância.

**Mistura de causas de fim, alvo e medida:**

| Como acaba | Alvo | Medido |
|---|---:|---:|
| Medidor no extremo (é onde vivem os dourados) | ~50% | 47% |
| Morte súbita | ~30% | 32% |
| Chegou ao fim inteiro | ~20% | 21% |

### 2.1 Os quatro medidores

Todos começam em **50** de 100. Chegar a **0** ou a **100** encerra a carreira — o excesso mata tanto quanto a falta. Essa é a regra central e não deve ser suavizada.

| Medidor | Ícone | O que representa | Família em 0 | Família em 100 |
|---|---|---|---|---|
| **FORMA** | ⚡ | Corpo, técnica, ritmo de jogo | *O corpo cobrou* | *Passou do ponto* |
| **TORCIDA** | 📣 | Amor da arquibancada e das redes | *Viraram* | *Não é mais seu* |
| **DIRETORIA** | 👔 | Relação com clube, treinador, federação | *Fora dos planos* | *Deixou de ser gente* |
| **DINHEIRO** | 💰 | Patrimônio, contratos, dívidas | *Acabou* | *A ganância* |

Cada célula da tabela é uma **família de cinco finais**, não um final só — o final específico sai das suas flags. Ver a seção 3.5 e `finais.md`.

**Por que quatro:** cada carta pode mexer confortavelmente em 1 ou 2 medidores. Com quatro barras, o jogador consegue segurar o estado do jogo na cabeça sem consultar a tela. Cinco medidores foram descartados: aumentam o custo cognitivo e tornam o balanceamento de cauda muito instável.

**Antagonismos desenhados** (o que gera as decisões difíceis):

- FORMA ↔ DINHEIRO — jogar machucado rende bônus; poupar-se custa contrato.
- TORCIDA ↔ DIRETORIA — falar o que a arquibancada quer ouvir irrita quem assina o cheque.
- TORCIDA ↔ FORMA — o mito precisa jogar sempre; o corpo precisa de descanso.
- DIRETORIA ↔ DINHEIRO — ser bonzinho com o clube significa aceitar menos.

### 2.2 Recursos ocultos (não aparecem como barra)

| Recurso | Faixa | Papel |
|---|---|---|
| `idade` | 17 → 40 | Avança 1 por temporada. Depois dos 30, FORMA sofre decaimento passivo. |
| `temporada` | 1 → ~20 | Índice do calendário. |
| `contrato` | 0 → 5 anos | Cai 1 por temporada. Chegar a 0 sem renovar dispara o arco *fim de contrato*. |
| `lesao` | 0 → 3 rodadas | Enquanto > 0, bloqueia cartas de jogo e trava ganhos de FORMA. |
| `moral_publica` | -5 → +5 | Memória curta da imprensa. Modula a intensidade das cartas de mídia. |
| `flags` | conjunto | Marcas de memória: `joelho_ignorado`, `recusou_apostas`, `padrinho_do_kaique`, `companheira_ficou`... |
| `estatisticas` | contadores | Gols, títulos, cartões, transferências, seleções. Só aparecem no final. |

O jogador nunca vê esses valores diretamente — vê os efeitos deles no texto das cartas. Isso preserva a sensação de que o mundo reage, sem transformar o jogo em planilha.

---

## 3. Estrutura da carreira

A carreira é dividida em seis **eras**. A era determina que cartas são elegíveis, que personagens aparecem e qual é a pressão dominante.

| # | Era | Idade | Cartas | Pressão dominante | Cargos em cena |
|---|---|---|---|---|---|
| 1 | **A Base** | 17–19 | 16–20 | Sobreviver ao corte | `coord_base`, `mae`, `parceiro`, `empresario`, `roupeiro`, `fisio` |
| 2 | **O Estouro** | 19–22 | 20–24 | Ser notado sem queimar | `treinador`, `imprensa`, `capitao`, `apostas`, `diretor`, `parceiro` |
| 3 | **A Travessia** | 22–26 | 26–32 | Adaptação e legitimidade | `diretor`, `companheira`, `organizada`, `imprensa` |
| 4 | **O Auge** | 26–30 | 26–32 | Manter tudo de pé ao mesmo tempo | `capitao`, `apostas`, `imprensa`, `diretor`, `companheira` |
| 5 | **O Declínio** | 30–34 | 24–30 | Aceitar ou negar o fim | `fisio`, `sucessor`, `filho`, `empresario` sem poder |
| 6 | **O Legado** | 34+ | 10–14 | Escolher como sair | `coord_base`, `roupeiro`, `sucessor`, `imprensa` |

**Quantas carreiras chegam a cada era** (500 carreiras medidas): base 100% · estouro 90% · travessia 61% · auge 47% · declínio 32% · legado 23%. As eras finais são **prêmio de quem jogou bem**, não passagem obrigatória — é o que faz o conteúdo tardio valer a pena e o que dá motivo para a reencarnação.

**Transição de era:** ocorre por idade **e** por gatilho narrativo (ex.: só entra em *A Travessia* quem aceitou uma transferência internacional). Quem recusa a Europa segue uma variante nacional da era 3, com cartas próprias — isso é conteúdo, não punição.

### 3.1 Ritmo da temporada

Uma temporada = **7 a 9 cartas**, distribuídas assim:

```
[pré-temporada: 1]  [rotina + eventos: 4–6]  [decisiva: 1]  [pós-temporada: 1]
```

Sete cartas por ano é pouco, e é de propósito: com 17 temporadas possíveis, o ano tem que passar rápido para que a carreira caiba em 20 minutos. O jogador precisa sentir que **o tempo está fugindo** — é a emoção central da era 5.

- **Pré-temporada** — preparação física, meta pessoal, chegada de reforço.
- **Rotina + eventos** — o miolo: mistura de cartas genéricas da era, arcos ativos e reações a flags.
- **Carta decisiva** — a final, o clássico, o jogo do rebaixamento. Resolve com base em FORMA + aleatoriedade controlada, e o resultado alimenta TORCIDA/DIRETORIA/estatísticas.
- **Pós-temporada** — janela de transferências, balanço, `idade++`, `contrato--`.

### 3.1b Morte súbita

**24 cartas, quatro por era, cada uma com final próprio.** A cobertura era torta (base 2, estouro 2, travessia 2, auge 4, declínio 1, legado 0) e a era mais dramática do jogo não tinha nenhuma. O tema muda com a era e é isso que faz a piada funcionar: **na base você morre de moleque** (a van, a pelada de coturno), **no estouro você morre de novo-rico** (a garupa de mil cilindradas, a bicicleta de terno no estúdio), **na travessia você morre de estrangeiro** (menos oito graus de manga curta, o visto vencido na fronteira), **no auge você morre de importante** (o jet ski, o helicóptero, o monitor do VAR), **no declínio você morre de teimoso** (a terceira infiltração, a cápsula que resolve quatro quilos), **no legado você morre de saudade** (o jogo de veterano, os últimos quinze minutos, a chuteira da estreia).

**Peso de sorteio 4, não 8.** Medido: com peso 9 as 24 cartas levavam **43% das carreiras** a acabar em acidente burro, o que apaga o jogo de medidores e afunda os dourados. Com peso 4 a fatia é 32% e, em 500 carreiras, **as 24 cartas aparecem todas** — variedade igual, risco proporcional. Carta rara vista muitas vezes ao longo de várias carreiras é melhor que carta comum vista sempre na mesma.

Um dos quatro medidores estourar não é a única forma de a carreira acabar. **Cerca de dez cartas do baralho têm uma opção que encerra tudo na hora**, independente de você estar com 80 em tudo. São as cartas de tipo `morte_subita`, e existem para que o jogador nunca se sinta seguro.

Quatro regras que fazem a diferença entre tensão e injustiça:

1. **A opção fatal está telegrafada.** No texto e no rótulo. O jogador precisa saber que está fazendo uma besteira — a piada é ter feito mesmo assim. Nenhuma morte pode ser surpresa gratuita.
2. **Nunca as duas opções são fatais.** Sempre existe a saída.
3. **A opção segura nunca é estritamente melhor.** Se fosse, a escolha era falsa. A opção suicida oferece ganho grande e real; é uma tentação, não uma pegadinha.
4. **Chance 1,0 é morte certa; chance menor é aposta** e exige um bloco `sobrevive` com recompensa alta. Das dez cartas, três são morte certa (o empurrão no árbitro, o monitor do VAR, a aposta no próprio jogo) e sete são apostas entre 50% e 80%.

Com pesos baixos, uma ou duas dessas aparecem por carreira. O tom é humor ácido: ninguém morre de tragédia grandiosa — morre da maionese que ficou fora da geladeira, do carro batido a vinte por hora no estacionamento do próprio clube, dos duzentos reais apostados para ganhar uma discussão de vestiário.

Cada uma tem seu final nomeado, listado em `finais.json` sob `mortes_subitas`, e todas compartilham duas ilustrações: `final_morte_burra` e `final_morte_banido`.

### 3.2 A partida (mecânica especial)

Uma vez por temporada, uma carta de **jogo decisivo** troca o swipe binário por uma resolução com risco explícito:

```
chance_de_heroi = clamp(0.15 + (FORMA - 50) / 160 + bônus_flags, 0.05, 0.85)
```

- Opção A (**"Assume a responsabilidade"**): rola contra `chance_de_heroi`. Sucesso → +TORCIDA forte, +estatística, chance de flag `gol_da_final`. Fracasso → −TORCIDA forte, `moral_publica--`.
- Opção B (**"Joga para o time"**): resultado morno garantido, sem glória e sem queda.

É a única aleatoriedade visível do jogo, e é deliberada: futebol tem sorte, e o jogador precisa sentir isso pelo menos uma vez por ano.

### 3.3 Arcos multi-carta

Um arco é uma sequência de 3 a 6 cartas ligadas por flags, com espaçamento mínimo entre elas para não parecer corredor. Arcos previstos para a v1:

1. **O empresário Valdir** — o cara que te descobriu e nunca mais te larga. Percorre todas as eras. Termina em sociedade, ruptura ou processo.
2. **A lesão que ninguém viu** — dor no joelho ignorada na era 2 que cobra juros na era 5.
3. **A transferência dos sonhos** — proposta, contraproposta, empresário, pai, torcida. 5 cartas.
4. **A seleção** — convocação, estreia, eliminação, o técnico que não gosta de você.
5. **A casa de apostas** — patrocínio fácil, dinheiro fácil, pergunta desconfortável, investigação.
6. **A família** — a mãe que não quer sair da cidade, o pai doente, o filho que só vê você pela TV.
7. **A voz** — o que você diz sobre política, racismo, arbitragem. O arco que mais separa TORCIDA de DIRETORIA.
8. **O sucessor** — o moleque de 18 anos que ocupa sua vaga e pede seu conselho.

### 3.3b Fios de três batidas

O arco liga cartas por flag e por proximidade. O **fio** faz outra coisa: pega uma carta de legado e devolve ela na sua cara duas vezes, muito depois, com a sua escolha embutida.

```
BATIDA 1   a decisão            2 opções   — a carta de legado que já existe
BATIDA 2   a consequência       2 cartas   — 20 a 30 cartas depois
BATIDA 3   o acerto de contas   4 cartas   — na era seguinte
```

São **7 peças por fio** e a progressão 2 → 4 é a mesma que a Decisiva usa. O jogador nunca vê mais de duas opções; o que ele vê depende de tudo que escolheu antes no fio.

**Três regras que fazem o fio funcionar:**

1. **A batida 2 chega longe o bastante para você ter esquecido o número e perto o bastante para lembrar a cena.** Medido: mediana de 27 cartas entre batidas.
2. **A batida 3 é a única carta do jogo que pode desfazer uma marca** (`tiraFlags`). É o que separa consequência de castigo: o fio não é a sua sentença, é a sua chance de responder.
3. **A batida 3 quase sempre troca de cargo.** A consequência chega pela boca de outra pessoa — o joelho que você ignorou aos 17 volta pela imprensa aos 29, não pelo fisioterapeuta.

Cartas de fio têm `peso: 0` e chegam por uma **agenda** (`E.agenda`), não pelo sorteio. A agenda zera na reencarnação: cada vida tem os seus próprios fios abertos.

**Fio com várias portas de entrada.** Um fio não pertence a uma carta, pertence a um assunto. As cinco cartas de legado do arco das apostas abrem o *mesmo* fio tardio — você não recebe cinco acertos de contas pelo mesmo pecado. A primeira porta que abre é a que vale; o motor descarta as marcações cuja batida já foi vivida. Foi isso que trocou 162 cartas por 54 e deu ao arco uma espinha longa em vez de cinco curtas.

**Morte súbita tem fio de 3 peças, não de 7.** A opção que te matou não tem consequência, tem final. Então a batida 1 de uma carta de morte só ramifica do lado de quem sobreviveu: 1 consequência + 2 acertos de contas.

### 3.3c-bis Fios curtos e a saída do futebol

O fio longo entrega a consequência 25 cartas depois. Isso é ótimo e é lento: o jogador precisa entender **na primeira era** que a escolha dele muda o destino, não só o número na barra. Daí os **fios curtos**: 12 fios, dois por era, janela de 3 a 8 cartas, que nascem e morrem dentro da mesma era.

**Seis deles podem encerrar a carreira por escolha** — o campo `encerra` aponta para um final do bloco `escolhas_de_vida`, de **moldura verde**. Não é morte e não é aposentadoria: é o jogador saindo do futebol porque quis, e o final é bom. Faculdade, a oficina do tio, voltar para casa antes de precisar, a TV aos vinte e oito, andar normal aos cinquenta, a escolinha do bairro.

Regra de magnitude que isso obrigou a escrever: **a carta que encerra não é de legado.** O peso dela é a escolha de sair, não o delta — e delta de legado (42 a 61) numa era inicial é quase fatal. Resolução de fio curto é `importante`, e o lado que encerra não tem delta nenhum.

### 3.3d Títulos

**A carreira começa sem nada.** No alto da tela aparece só o nome do jogador — sem apelido e sem título. O apelido não é sorteado: ninguém nasce com apelido. Ele vem **junto com o título**, no instante em que a escolha que o mereceu é feita, porque o mundo te dá um nome e uma reputação na mesma carta:

```
começo da carreira        GABI
depois da decisão         GABI "CADERNO"   ( O Universitário )
```

O jogador ganha **um título por vida**, exibido no alto da tela ao lado do nome, **no instante em que a escolha que o mereceu é feita** — não no fim da carreira. Depois de conquistado ele **trava**: título que muda no meio vira placar, e a identidade daquela vida deixaria de ser fixa. Vidas diferentes podem repetir o mesmo título; a coleção é de títulos distintos já vistos, como a de finais.

`titulos.json` tem 25, e **a ordem da lista é a prioridade**. Quatro deles existem só para o título chegar cedo — O Arrimo, O Difícil, O Duro e O Tudo ou Nada, todos alcançáveis na base ou no estouro. Sem eles, medido: o título chegava na **decisão 36 de 60** (mediana) e 26% das carreiras terminavam sem nenhum; com eles, chega na **decisão 16** e só 11,7% ficam sem. Um HUD que passa metade da carreira vazio não é identidade, é espaço em branco. A regra que a medição obrigou: **títulos de flag vêm antes dos de medidor.** Com os de medidor no meio da lista, 58% das carreiras terminavam com um de dois títulos genéricos e só 11 dos 21 apareciam — porque o título trava, e um genérico conquistado na segunda temporada apaga todos os específicos para sempre.

### 3.3e A bolinha de impacto

Durante o arrasto, um círculo aparece acima do ícone de cada medidor afetado, em **três tamanhos**: 5px até delta 9, 9px até 19, 14px com brilho acima disso. Diz **quanto**, nunca para que lado — não muda de cor, de forma nem de posição com o sinal.

Três tamanhos porque três é o que o olho distingue sem comparar. E caixa de tamanho fixo com escala por `transform`, porque uma bolinha que cresce no fluxo empurra a barra do medidor para baixo.

### 3.3f A carta de eco

O eco não é sobreposição: é **uma carta de texto**, sem retrato, sem rótulo e sem consequência. Fica na tela até o jogador arrastar, e arrastar para qualquer um dos lados faz a mesma coisa. Assinada só por uma palavra no pé: *ficou*.

Duas correções que a versão de sobreposição tinha e esta não:

1. **Sussurro de 1,9 s some antes de ser lido.** Aqui quem controla o tempo é o jogador.
2. **O eco era o mesmo nos dois lados.** Um eco que não muda com a escolha não promete consequência nenhuma. Agora ele vive na opção: são 206 ecos em 108 cartas de legado, todos distintos.

**Regra de escrita para `calou` (e para qualquer marca que os finais leem como derivada).** `calou` significa *você tinha o microfone numa coisa que importava e não usou* — não significa "não quis conversa". Usá-la como marcador genérico de recusa parece inofensivo e não é: `calou` bloqueia `carreira_limpa`, então cada uso descuidado fecha silenciosamente o caminho para os finais dourados. Marca lida por final derivado é orçamento, não tempero.

### 3.3c Progressão: clube, patamar e a janela

O jogador precisa sentir que a carreira **vai a algum lugar**. Três camadas, todas ligadas aos medidores que já existem — nenhum recurso novo.

**Clube com patamar.** Cinco patamares, 35 clubes fictícios em `clubes.json`: acesso → segunda divisão → grande do país → médio europeu → gigante europeu. O rodapé mostra clube e patamar (a era já é dita pela paleta). Transferência deixa de ser um número na ficha e passa a ser subir ou descer de vida.

**Ritmo:** 7 cartas por temporada. Foi 8 até a carta de eco e o balanço de ano entrarem — os dois somam ~2,5 min de leitura por carreira, e o ajuste certo foi cortar decisões, não cortar leitura.

**Balanço de fim de temporada.** Sobreposição curta entre temporadas: jogos, gols e colocação **derivados da FORMA naquele recorte**, mais uma frase de julgamento de uma matriz FORMA × DIRETORIA × colocação. É o que transforma oito cartas soltas num ano de carreira. É sobreposição e não pausa de estado — a carta seguinte já foi sorteada atrás dela, o que mantém o loop testável.

**Janela nomeada.** No fim de temporada, quando o ano justifica, entra uma carta de proposta com o **nome e o patamar** do clube (tokens `{clube_novo}` e `{patamar_novo}`). A régua sobe com o patamar: `FORMA ≥ 48 + patamar×5` e `TORCIDA ≥ 42 + patamar×4`, ou um título, que dispensa as duas. Esses cortes vêm da distribuição medida em 2.963 viradas de temporada, não de palpite — a primeira versão usava um corte fixo e deixava 71% das carreiras morrendo no acesso.

### 3.4 Meta-progressão: a reencarnação

Quando a carreira acaba, você não assume outra pessoa. **É a mesma alma, outro corpo, outro moleque de dezessete anos no mesmo alojamento.** O jogo nunca anuncia isso — o jogador descobre.

#### A descoberta, vida a vida

| Vida | O que o jogo faz | O que o jogador sente |
|---|---|---|
| **1ª** | Tela de morte, ficha de carreira, botão "de novo". Nada mais. | "Beleza, é um roguelike, recomeça." |
| **2ª** | Três cartas de déjà-vu entram no baralho, sem explicação ("você já sonhou com esse corredor"). O Seu Otávio erra o seu nome — e o nome que ele diz é o da sua vida anterior. | "Peraí." |
| **3ª** | O Seu Otávio para de errar. Ele te chama pelo apelido da primeira vida e continua dobrando camisa como se nada fosse. Aparece a primeira carta que cita um evento da sua vida passada. | "Ele sabe." |
| **4ª+** | O jogo passa a nomear a sua marca de alma na tela inicial. Cartas de arco podem referenciar como você morreu antes. O Valdir aparece com a mesma corrente e a mesma idade. | "Nada disso é acidente." |

A regra de ouro é: **nunca escrever uma carta que explique a reencarnação.** O Seu Otávio nunca diz "você já viveu". Ele diz "você continua entrando com o pé errado, menino" — e volta a dobrar camisa.

#### A marca de alma

O medidor que te matou vira um traço mecânico na vida seguinte. **Só uma marca fica ativa por vida** — a da morte imediatamente anterior. Toda marca é bênção e maldição na mesma frase:

| Morte anterior | Marca | Efeito |
|---|---|---|
| FORMA 0 | **Corpo lembrado** | Ganhos de FORMA ×1,25 — e perdas de FORMA também ×1,25 |
| FORMA 100 | **Fome antiga** | Começa com FORMA 60; em troca, o decaimento por idade começa aos 27 em vez de 30 |
| TORCIDA 0 | **Cara de vilão** | Ganhos e perdas de TORCIDA ×0,7. Você fica imune ao ódio e incapaz de ser amado |
| TORCIDA 100 | **Carisma herdado** | Ganhos de TORCIDA ×1,3; todo ganho de TORCIDA custa 1 de DIRETORIA |
| DIRETORIA 0 | **Ficha suja** | Começa com DIRETORIA 40; ganhos de DINHEIRO ×1,2 |
| DIRETORIA 100 | **Filho do clube** | Começa com DIRETORIA 65; recusar transferência é impossível sem perder 10 de TORCIDA |
| DINHEIRO 0 | **Medo de passar fome** | Ganhos de DINHEIRO ×1,3; recusar uma carta de dinheiro custa 4 de FORMA |
| DINHEIRO 100 | **Ganância antiga** | Ganhos de DINHEIRO ×1,25 — inclusive nas cartas que te matam |

A marca é o motor da rejogabilidade: cada vida tem uma inclinação diferente, herdada do erro anterior. Morrer de ganância te faz *mais* ganancioso na vida seguinte. É a piada mais amarga do jogo e é o coração dele.

#### O que mais persiste

- **Galeria de finais** — 44 finais, dos quais 11 dourados. Completar é a meta de longo prazo.
- **Fichas de carreira** — o álbum. Cada vida deixa uma figurinha, com moldura dourada, prata, cinza ou preta.
- **O mundo lembra** — se você terminou uma vida com o final *Estátua*, a estátua existe no clube da vida seguinte, e há uma carta em que você passa por ela sem saber por quê.
- **Cartas desbloqueadas** — os quatro finais de contexto liberam arcos que só existem para quem já viveu aquilo.

**Não persiste:** medidores, dinheiro, relações. Cada vida começa em 50/50/50/50, com a marca aplicada por cima.

### 3.5 Finais

Um medidor no extremo não determina um final fixo — determina uma **família de finais**, e as suas flags escolhem qual. É o que impede que acumular dinheiro até 100 termine em "ficou rico e parou de jogar", que soaria a vitória.

A estrutura é simétrica: **8 famílias × 5 finais**, e cada família tem exatamente

```
1 dourado (3+ fatores combinados)  +  3 condicionais  +  1 genérico sem condição
```

Um dourado não significa "você venceu". Significa **você chegou ao extremo pelo caminho difícil**: morrer de FORMA 0 tendo cuidado do corpo a vida inteira e ganhado três títulos é uma morte diferente de morrer por ter ignorado uma dor aos dezoito anos. Cada medidor passa a ter duas mortes ruins e uma boa, o que dá ao jogador um alvo em toda direção, e não só na do equilíbrio.

Com os finais de contexto, de fim natural e de morte súbita, são **57 finais sobre 14 ilustrações** — os finais de uma família compartilham arte e mudam nome, texto e moldura. Dados em `finais.json`, versão legível em `finais.md`, validação em `ferramentas/validar-finais.py`.

### 3.6 O elenco é feito de cargos

O jogo não tem personagens — tem **cargos**, funções dramáticas que o futebol produz sempre: sempre haverá um empresário, sempre um capitão de saída, sempre alguém do departamento médico dizendo o número exato de semanas. Quem ocupa o cargo é outra história, e é aí que a reencarnação mora.

| Persistência | Cargos | Comportamento entre vidas |
|---|---|---|
| **eterno** | `empresario`, `roupeiro` | A mesma pessoa, sempre. Não envelhece, não muda. **São as duas únicas pistas da reencarnação.** |
| **rotativo** | `capitao`, `treinador`, `imprensa`, `diretor`, `fisio`, `apostas`, `coord_base` | Pessoa nova a cada vida, sorteada, nunca repetindo a anterior. |
| **íntimo** | `mae`, `companheira`, `filho`, `sucessor` | Pessoa nova porque *você* é uma pessoa nova. Não é sorteio: é consequência de ter renascido. |
| **institucional** | `organizada` | Nunca foi gente. Não muda porque não é gente. |

**Só dois cargos são eternos, e é a raridade que faz a pista funcionar.** Se metade do elenco fosse fixa, ninguém repararia. Sendo dois, o jogador atento percebe que existem duas pessoas fora do ciclo — e isso é assustador do jeito certo.

As cartas são escritas contra o **cargo**, não contra a pessoa, e usam o token `{nome}` onde precisam citar quem está ali. Dois cargos (`capitao` e `treinador`) têm **arquétipos**: instâncias que mudam valores, não só nome, e por isso ganham cartas próprias. O sorteio do cargo é a única aleatoriedade estrutural do jogo fora da carta de partida decisiva.

Detalhe completo em `cargos.md`; dados em `cargos.json`.

---

## 4. Economia de cartas

### 4.1 Números-alvo da v1

| Item | Meta v1 | Observação |
|---|---|---|
| Cartas totais | **285** | 250 comuns + 35 de arquétipo, em 15 cargos. **Todas escritas.** Fonte: `cartas/<cargo>.json` |
| Cartas por partida | 110–140 | Cobertura de ~60% do baralho por vida — o resto é combustível da reencarnação |
| Arcos | 8 | 3–6 cartas cada |
| Finais nomeados | 57 | 8 famílias × 5 + 4 de contexto + 3 de fim natural + 10 de morte súbita, sobre 14 ilustrações |
| Cargos | 15 | 2 eternos, 7 rotativos, 5 íntimos, 1 institucional |

**Regra de repetição:** uma carta genérica só volta a ficar elegível depois de 25 cartas. Cartas de arco e cartas únicas nunca repetem (`unico: true`).

### 4.2 Faixas de delta

**A magnitude vem do peso dramático, e o peso dramático vem da consequência.** Uma carta é de legado porque muda o seu final, não porque move um número grande — o tamanho do delta é resultado da classificação, não causa dela. E a classificação é derivável do próprio conteúdo, sem julgamento: basta olhar se a flag que a carta produz é lida por algum final.

| Peso | Critério | Magnitude por opção | Fatia |
|---|---|---|---:|
| **Legado** | produz flag que um final **dourado** lê | ±46 a ±67 | 12,6% |
| **Importante** | produz flag que outro final ou outra carta lê | ±26 a ±40 | 21,8% |
| **Padrão** | não deixa rastro no sistema | ±8 a ±15 | 65,6% |

As faixas vivem em **`ferramentas/faixas.json`**, que é fonte única. Estavam duplicadas no validador e no balanceador, uma ficou velha depois de um reescalonamento, e o balanceador passou a rejeitar todo candidato silenciosamente porque media pela régua antiga.

Amplitude de **4,8× entre a decisão mediana de legado e a de padrão** (era 2,2×). O **fator acumulado de dificuldade é 1,49** sobre a escala original, calibrado em quatro medições (1,00 → mediana de 133 decisões · 1,45 → 84 · 1,67 → 46 · 1,49 → 68). A opção segura de uma morte súbita fica fora dessa tabela, na faixa 13–40: ali o peso está na morte, não no delta.

**Por que o piso é 8 e não 2.** Numa primeira tentativa a faixa de padrão foi para 2–5. O teto ficou certo e o piso estragou: 65% das cartas passaram a mover 1 ou 2 pixels de barra — invisível de novo, exatamente o defeito que a rodada queria consertar. A faixa de padrão precisa ser pequena *em relação ao legado*, não pequena em absoluto.

**Ombros macios: testado e descartado.** A ideia era amortecer o delta perto de 0 e de 100 para a carreira não morrer de sopetão. Varredura com fator 0,72 / 0,45 / 0,3 / 0,0: o amortecimento **não comprou duração nenhuma** (quem controla o tamanho da carreira é a idade de parar, aos 37) e, com 0,72, zerou as mortes por medidor — o que apagava 40 dos 57 finais do jogo. Removido.

**Regra de ouro do balanceamento:** a soma dos deltas absolutos das duas opções de uma carta deve ser aproximadamente igual. Se a esquerda mexe 18 pontos no total, a direita deve mexer entre 14 e 22. Opções assimétricas em magnitude viram escolha óbvia.

**Segunda regra:** nenhuma opção deve mexer os quatro medidores. Duas é o padrão, três é exceção.

**Terceira regra — deriva neutra do baralho.** Somando as cartas *repetíveis* de uma era, ponderadas pelo peso e assumindo escolha 50/50, cada medidor deve derivar no máximo **±0,15 ponto por carta jogada**. Uma deriva de +1,0 em TORCIDA significa que o jogador vira ídolo sem tomar uma única decisão — e morre por excesso em cerca de 50 cartas, achando que fez algo errado.

Essa regra é invisível a olho nu: cada carta individual parece justa, e o viés só aparece na soma. É por isso que o validador (`ferramentas/validar-cartas.py`) mede a deriva a cada build. Todo decaimento pretendido — a queda de FORMA depois dos 30 — deve vir do **calendário**, nunca do baralho, para que possa ser ajustado num lugar só. Cartas `unico` e `catastrofica` ficam fora da conta: aparecem uma vez por carreira e não formam tendência.

**A regra vale no baralho inteiro, nunca por personagem.** O Valdir empurra DINHEIRO para cima porque ele *é* o dinheiro; a Dra. Kênia empurra FORMA para baixo porque ela *é* a conta do corpo. Tentar zerar a deriva de cada arquivo de personagem destruiria a identidade mecânica de todos eles. O validador imprime a deriva por arquivo como informação e só **cobra** a regra no baralho merged.

### 4.3 Pressão por era

Para que a carreira tenha curva, o gerador aplica um viés por era ao sortear o baralho:

| Era | Viés |
|---|---|
| 1–2 | Deltas positivos ligeiramente mais frequentes. O jogador está subindo. |
| 3–4 | Neutro, mas com maior variância. O auge é instável. |
| 5–6 | Decaimento passivo: `FORMA -2` por temporada após os 30, `-3` após os 34. Cartas de recuperação ficam mais raras. |

O declínio precisa ser sentido como inevitável, não como injusto. O jogador deve conseguir *administrar* a queda — escolher onde gastar o que sobrou — mas não revertê-la.

### 4.4 Schema de dados da carta

```json
{
  "id": "travessia_imprensa_03",
  "era": ["travessia", "auge"],
  "personagem": "reporter_bia",
  "peso": 8,
  "unico": false,
  "cooldown": 25,
  "requer": {
    "flags":    ["jogou_na_europa"],
    "semFlags": ["aposentado_selecao"],
    "medidores": { "torcida": { "min": 30 } },
    "idade":     { "min": 22, "max": 31 }
  },
  "texto": "Você errou um pênalti e sumiu das redes por três dias. Ela quer saber por quê.",
  "esquerda": {
    "rotulo": "Falo a verdade",
    "efeitos": { "torcida": 9, "diretoria": -7 },
    "flags": ["sincero_com_imprensa"],
    "estatisticas": {},
    "encadeia": null
  },
  "direita": {
    "rotulo": "Nota oficial do clube",
    "efeitos": { "diretoria": 8, "torcida": -6 },
    "flags": [],
    "encadeia": "travessia_imprensa_04"
  }
}
```

**Campos:**

- `peso` — probabilidade relativa dentro do baralho elegível.
- `cooldown` — quantas cartas até poder repetir (ignorado se `unico`).
- `requer` — todas as condições devem ser verdadeiras. Ausência de um campo = sem restrição.
- `tipo` — `rotina`, `evento`, `arco`, `partida` ou `catastrofica`. Define a faixa de delta esperada e se a carta entra na conta de deriva.
- `encadeia` — força esta carta específica na próxima rodada (ou em 2–4 rodadas, se `atraso` for definido).
- `efeitos` — inteiros somados ao medidor, com clamp em [0, 100] **após** checar morte.
- `peso_dramatico` — `padrao`, `importante` ou `legado`. Vem da consequência (§4.2) e define a faixa de delta.
- `fio` — em uma opção: `{ "id": "carta_da_batida_seguinte", "em": [20, 30], "proximaEra": true }`. Agenda aquela carta para voltar entre 20 e 30 cartas depois, e só a partir da era seguinte se `proximaEra`. Não é `encadeia`: `encadeia` é a próxima carta, `fio` é daqui a muito tempo.
- `tiraFlags` — remove flags do estado. **Só aparece na terceira batida de um fio.** É o único lugar do jogo onde uma marca pode ser desfeita, e é o que faz o acerto de contas valer mais que atmosfera.
- `peso: 0` — a carta nunca é sorteada; só chega por `fio`, por `encadeia` ou pelo motor. Cartas de peso 0 ficam fora da conta de cobertura por era e têm checagem de deriva própria.
- `eco` — **por OPÇÃO, nunca por carta.** Frase de até 60 caracteres que vira uma **carta de texto** depois da escolha (§3.3d). Cada caminho tem a sua: um eco igual nos dois lados não promete consequência, só decora. Nunca diz o que mudou; diz que ficou. Não se repete no baralho inteiro. Lado fatal não tem eco — quem morre lê o final.

**Flags do motor:** algumas flags não vêm de cartas — são escritas pelo próprio motor em transições de estado (`jogou_na_europa`, `capitao`, `lesionado`, `contrato_vencido`). Elas precisam estar declaradas numa lista única, senão o validador as acusa como referência quebrada.

### 4.5 Diretrizes de escrita

- **Texto da carta:** máximo 220 caracteres. Duas frases. A primeira dá a situação, a segunda faz a pergunta implícita.
- **Rótulos das opções:** máximo 22 caracteres. Primeira pessoa. Devem soar como *fala*, não como comando de menu. "Assino agora" e não "Aceitar contrato".
- **A morte é telegrafada pelo TEXTO, nunca pela interface.** A previsão do tempo é ruim, a maionese ficou fora da geladeira, o campo do objeto está em branco — o aviso está na prosa, e ler a prosa é o jogo. Rótulo vermelho e medidor tremendo antes do arrasto foram testados e removidos: viram placa de "não vá por aqui", ninguém escolhe o lado marcado, e a carta mais tensa do baralho morre de graça.
- **Nunca explique a consequência no texto.** Se a carta diz "isso vai irritar a diretoria", ela já jogou por você.
- **O eco promete, não informa.** "O vestiário inteiro ouviu a sua resposta" funciona; "a diretoria caiu 20" quebra a regra de nunca mostrar número e ainda entrega o jogo. O eco existe para o jogador desconfiar de que aquilo volta — não para conferir o saldo.
- **O humor está na voz do personagem, não em piada.** O dirigente que fala em "ativo de alta liquidez" sobre um menino de 19 anos é engraçado sem precisar de punchline.
- **O texto não pode afirmar o que o jogo não garante.** Uma carta que diz "a camisa do clube novo" numa carreira em que o jogador nunca saiu do primeiro clube quebra a ficção mais do que qualquer bug de número. Toda expressão que pressupõe estado do motor (*clube novo, fuso, no exterior, o clube que te comprou*) precisa da flag correspondente em `requer` — e o validador agora avisa quando falta.
- **Nomes reais são proibidos.** Clubes, jogadores, ligas, marcas e competições são todos fictícios e genéricos ("o clube inglês", "a Federação", "o torneio continental"). Isso é decisão de projeto, não sugestão — evita disputa de direitos de imagem e de marca, e ainda deixa a projeção do jogador mais livre.

---

## 5. UX e interface

### 5.1 Tela de jogo

```
┌─────────────────────────────────┐
│   ⚡   📣   👔   💰              │  ← 4 barras, topo, sempre visíveis
│                                 │
│      ┌───────────────────┐      │
│      │                   │      │
│      │     RETRATO       │      │  ← carta arrastável
│      │                   │      │
│      ├───────────────────┤      │
│      │  "texto da carta" │      │
│      └───────────────────┘      │
│                                 │
│   ← rótulo         rótulo →     │  ← só aparece durante o arrasto
│                                 │
│   Temporada 4 · 23 anos · CLUBE │  ← rodapé discreto
└─────────────────────────────────┘
```

- **Feedback de arrasto:** a partir de ~15% do deslocamento, o rótulo da opção aparece e os ícones dos medidores afetados pulsam. **Nunca** mostrar o valor.
- **Zona morta:** menos de 25% do deslocamento volta ao centro sem efeito. Evita escolha acidental.
- **Controles alternativos:** setas ←/→ do teclado, clique nas metades da tela, e botões explícitos em modo acessível.
- **Sem menus durante a partida.** Pausa mostra apenas: som, acessibilidade, abandonar carreira.

### 5.2 Direção de arte

- Ilustração em vetor de alto contraste, paleta reduzida (4 a 6 cores por era), silhuetas fortes que leem bem em 320px de largura.
- Cada era muda a paleta de fundo: base = verde-barro e cal; Europa = cinza-azulado; auge = dourado saturado; declínio = âmbar frio.
- 12 retratos de personagem + 6 fundos de era + 18 ilustrações de final = **36 artes** para a v1. É o maior custo de produção do projeto e deve ser orçado desde já.
- Alternativa de baixo custo para o protótipo: retratos monocromáticos gerados a partir de formas geométricas + tipografia forte. Funciona, tem identidade, e não trava o desenvolvimento à espera de arte.

### 5.3 Áudio

Trilha mínima: um loop ambiente por era, ruído de arquibancada modulado por TORCIDA (quanto maior, mais alto), e três efeitos — arrasto, confirmação, morte. Áudio é opcional na v1, mas o ruído de arquibancada reagindo ao medidor é o item de maior retorno por esforço do projeto inteiro.

### 5.4 Acessibilidade

- Modo botão (sem gesto) para quem não usa arrasto.
- Contraste mínimo 4.5:1 em todo texto; medidores diferenciados por ícone e posição, nunca só por cor.
- Tipografia escalável até 150% sem quebra de layout.
- Todo texto em elementos semânticos, com `aria-live` anunciando mudanças de medidor no modo acessível.

---

## 6. Arquitetura técnica

### 6.1 Stack recomendada

| Camada | Escolha | Por quê |
|---|---|---|
| Runtime | HTML + CSS + TypeScript, sem framework de UI | O jogo tem uma tela. Um framework aqui é peso morto. |
| Build | Vite | Rápido, zero configuração, gera bundle estático. |
| Dados | JSON por era (`cartas/base.json`, `cartas/auge.json`...) | Permite editar conteúdo sem tocar em código; validável por schema. |
| Estado | Máquina de estados própria (reducer puro) | Determinismo, testabilidade e replay a partir de uma seed. |
| Persistência | `localStorage` | Meta-progressão e save de carreira em andamento. |
| Hospedagem | Qualquer host estático | Sem servidor, sem banco, sem custo recorrente. |

**Nota sobre `localStorage`:** funciona no navegador e no deploy final, mas **não** dentro do painel de artefatos do Claude. Se o protótipo for testado por lá, o estado precisa ficar em memória. Manter a persistência isolada atrás de uma interface `Storage` resolve os dois casos com uma troca de implementação.

### 6.2 Estrutura de arquivos

```
craque/
├── index.html
├── src/
│   ├── main.ts              # bootstrap e loop de render
│   ├── engine/
│   │   ├── state.ts         # tipos do estado + estado inicial
│   │   ├── reducer.ts       # aplicarEscolha(estado, lado) → estado
│   │   ├── deck.ts          # elegibilidade, peso, cooldown, sorteio
│   │   ├── rng.ts           # PRNG com seed (mulberry32)
│   │   ├── calendario.ts    # rodada, temporada, era, idade
│   │   └── finais.ts        # resolução de morte → final nomeado
│   ├── ui/
│   │   ├── carta.ts         # arrasto, física, feedback
│   │   ├── medidores.ts
│   │   └── ficha.ts         # tela de final + card compartilhável
│   └── dados/
│       ├── cartas/<slug>.json   # um arquivo por personagem, mesmo slug da arte
│       ├── personagens.json
│       └── finais.json
├── tests/
│   ├── balanceamento.test.ts  # simulação de 10.000 carreiras
│   └── schema.test.ts         # valida todo JSON contra o schema
└── ferramentas/
    └── editor-cartas.html     # editor local de cartas, arquivo único
```

### 6.3 Núcleo do estado

```ts
type Medidores = { forma: number; torcida: number; diretoria: number; dinheiro: number }

type Estado = {
  medidores: Medidores
  idade: number
  temporada: number
  rodada: number
  era: Era
  contrato: number
  lesao: number
  clube: Clube
  flags: Set<string>
  estatisticas: Record<string, number>
  historico: string[]     // ids das cartas vistas, para cooldown
  fila: string[]          // cartas encadeadas pendentes
  seed: number
}
```

O reducer é **puro**: `(estado, escolha) → estado`. Toda aleatoriedade vem do PRNG com seed guardada no estado. Consequência prática: qualquer carreira pode ser reproduzida a partir da seed + sequência de escolhas — o que torna o teste de balanceamento e o relato de bug triviais.

### 6.4 Ferramenta de autoria

O gargalo do projeto não é código, é **conteúdo**: 220 cartas bem escritas e balanceadas. Vale construir cedo um editor local de arquivo único que:

- lista as cartas com filtro por era, personagem e arco;
- valida deltas contra a regra de simetria e avisa quando uma opção é obviamente melhor;
- mostra o grafo de flags (quem produz, quem consome) e aponta flags órfãs;
- exporta o JSON final.

Sem isso, a partir da carta 80 o balanceamento vira adivinhação.

---

## 7. Balanceamento e testes

### 7.0 Validador de cartas (já existe)

`ferramentas/validar-cartas.py` roda em qualquer arquivo de cartas e checa as regras deste documento: simetria das opções, número de medidores por opção, limites de texto e rótulo, faixas de delta por tipo, encadeamentos quebrados, grafo de flags e deriva por medidor. Uso:

```bash
python3 ferramentas/validar-cartas.py cartas-exemplo.json
```

Erros quebram o build; avisos não. Deve entrar no CI junto com a simulação da seção 7.1. Rodado sobre as 24 cartas de exemplo, ele já apontou duas coisas que a leitura manual não pegou: três cartas classificadas como rotina com magnitude de evento, e uma deriva de TORCIDA que só existia na soma.

### 7.0b O que a simulação encontrou (executada)

O protótipo foi rodado em navegador headless com agentes automatizados. Quatro achados mudaram o jogo, e nenhum deles teria aparecido em documento:

**1. Os deltas eram o dobro do que deviam ser.** Na primeira execução, uma carreira aleatória durava 18 cartas — dois minutos. O problema não era deriva (ela estava neutra), era **variância**: com ±6 a ±14 por carta numa faixa de 0 a 100, o passeio aleatório encosta num extremo rápido demais. Todos os 1.412 deltas do baralho foram reescalados por 0,5 — transformação linear que preserva simetria, deriva e tensões — e as faixas por tipo e o limite de deriva acompanharam. A carreira aleatória foi de 18 para 47 cartas.

**2. O equilibrista ganhava o final dourado mais difícil em 99% das partidas.** *Aposentadoria no dia certo* exigia era Legado e os quatro medidores entre 40 e 70 — exatamente o que um jogador que só equilibra faz sem esforço. A correção foi acrescentar **2 títulos** à condição: títulos exigem FORMA alta, o que conflita diretamente com ficar parado em 50. O final caiu para 0,8% — dentro da meta de 0,5% a 3%.

**3. 42% das carreiras terminavam em "Sucata".** O fim natural da carreira (chegar aos 39 vivo) não tinha final próprio e caía no genérico da família FORMA 0 — um jogador que nunca chegou perto do zero recebia "o corpo já disse não". Criou-se o bloco **`fim_natural`** com três finais: *O último jogo* (com título), *Uma carreira inteira* (sem título nem convocação — o que acontece com a esmagadora maioria) e *Fim de linha*.

**4. Os oito dourados de família não são para quem sobrevive.** Um jogador equilibrado nunca encosta num extremo, então nunca os alcança. Um caçador que corre para o extremo morre na carta 32, antes de juntar as flags. O caminho é o terceiro: **sobreviver até o Declínio acumulando as flags certas e só então soltar um medidor** — testado, e o dourado de DINHEIRO 0 aparece em 18% das carreiras desse agente. É literalmente "chegou ao extremo pelo caminho difícil".

### 7.1 Simulação automatizada

Um teste roda 10.000 carreiras com três agentes artificiais e verifica a distribuição de resultados:

| Agente | Comportamento | Expectativa |
|---|---|---|
| **Aleatório** | escolhe 50/50 | morre em média entre as cartas 40 e 70 |
| **Guloso** | sempre maximiza o medidor mais baixo | chega à era 4–5, morre entre 120 e 180 cartas |
| **Equilibrista** | minimiza o desvio-padrão entre medidores | é o que mais se aproxima do teto; se ele sobreviver indefinidamente, o decaimento por idade está fraco |

**Critérios de aprovação:**

- Nenhum medidor responde por mais de 35% das mortes (evita "o jogo é sobre dinheiro").
- Menos de 5% das carreiras terminam antes da carta 20 (frustração precoce).
- Menos de 2% passam de 220 cartas (jogo sem fim).
- A carreira mediana do agente guloso deve alcançar a era 4.

### 7.2 Teste com pessoas

Cinco jogadores, sessão gravada, sem instrução prévia. O que observar:

- Em qual carta o jogador entende que 100 também mata? (meta: antes da carta 15 — se demorar mais, o *onboarding* precisa de uma carta explícita)
- Quantas cartas até a primeira hesitação real de mais de 3 segundos? (meta: antes da 10)
- Ele lê o texto ou já decidiu pelo retrato? (se ignora o texto, os retratos estão fortes demais ou o texto longo demais)
- Ao morrer, ele diz "de novo" ou fecha? Essa é a única métrica que importa.

---

## 8. Roadmap

| Fase | Entrega | Esforço estimado |
|---|---|---|
| **F0 — Vertical slice** | ~~HTML de arquivo único~~ **CONCLUÍDO** — `craque.html`, 189 KB, jogo inteiro: 285 cartas, 54 finais, arrasto, eras, reencarnação e marca de alma | — |
| **F1 — Motor** | Vite + TS, reducer puro, JSON externo, calendário, flags, encadeamento, seed. | 3–5 dias |
| **F2 — Conteúdo v1** | ~~285 cartas, 15 cargos, 54 finais~~ **CONCLUÍDO** | — |
| **F3 — Sensação** | Arte, áudio de arquibancada reativo, animação de morte, ficha de carreira compartilhável. | 1–2 semanas |
| **F4 — Meta** | Linhagem, galeria de finais, recordes persistentes, save/load. | 3–5 dias |
| **F5 — Polimento** | Acessibilidade, PWA offline, tela responsiva, testes de balanceamento no CI. | 1 semana |

**Recomendação:** ir para F0 imediatamente. Vinte cartas e um arrasto respondem em dois dias uma pergunta que nenhum documento responde — se o jogo é gostoso na mão.

---

## 9. Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Conteúdo insuficiente → repetição visível | Alto | Editor de cartas desde a F1; meta rígida de 220 cartas antes de qualquer polimento |
| Balanceamento vira adivinhação | Alto | Simulação automatizada rodando desde a F1, não no fim |
| Escolhas óbvias matam a tensão | Alto | Regra de simetria de deltas validada pela ferramenta, não pelo olho |
| Uso de nomes reais de clubes/jogadores | Médio-alto | Proibição total no guia de escrita; tudo fictício e genérico |
| Custo de arte trava o desenvolvimento | Médio | Estilo geométrico de baixo custo como plano A do protótipo |
| Declínio percebido como injusto | Médio | Cartas de declínio devem oferecer escolhas de *como cair*, nunca só perdas |

---

## 10. Decisões fechadas (07/08/2026)

1. **Morte por DINHEIRO 100** — vira família de finais trágicos ligados à ganância, com um único final bom, caro e condicionado. Detalhe em `finais.md`. ✅
2. **Meta-loop** — reencarnação, com descoberta gradual e marca de alma herdada da morte anterior. Seção 3.4. ✅
3. **Tutorial explícito** — não. Reavaliar depois do teste com pessoas, se a morte por excesso confundir. ✅
4. **Modo carreira curta** — não. A carreira inteira já cabe em 15–20 minutos. ✅
5. **Duração** — 15 a 20 minutos por carreira. Temporada encolhida para 7–9 cartas. ✅
6. **Estilo de arte** — vetor geométrico de alto contraste. Guia em `arte/README-nomenclatura.md`. ✅
7. **Método de produção de conteúdo** — cargo por cargo, seguindo as cotas de `cargos.json`. ✅

8. **Nara fica** e passa a controlar a porta da carreira internacional — a transição para a era Travessia é forçada por uma carta dela. ✅
9. **O eco do capitão fica**, resolvido por elenco rotativo de 4 arquétipos, sorteados por vida sem repetir o anterior. ✅
10. **Finais simétricos** — 8 famílias × 5, cada uma com um dourado multi-fator. ✅

### Ainda em aberto

11. **Elenco por cargos, não por nomes** — 14 cargos, 41 instâncias, quatro tipos de persistência entre vidas. ✅
12. **Sem pressa para a v1** — a meta de cartas passa a ser a que os arcos exigirem (hoje 249), não um teto arbitrário. ✅
13. **Só entram cartas e finais que funcionam** — nenhum final pode depender de flag inexistente. ✅

### Ainda em aberto

14. **A Base fica em 3 temporadas.** O gargalo de variedade foi resolvido por oferta, não por encurtamento: novo cargo `parceiro` (o colega de alojamento), `coord_base` de 12 para 18 cartas, `roupeiro` completo, e mais cartas de Base em `mae` e `fisio`. A Base saiu de 11 para **44 cartas elegíveis** — folga de 2,2x. ✅
15. **Morte súbita** — cerca de dez cartas podem encerrar a carreira na hora, com humor ácido e sempre telegrafadas. Seção 3.1b. ✅

16. **Baralho completo.** 285 cartas em 15 cargos, 54 finais, cobertura de 2,2x a 3,1x em todas as seis eras, zero dourados de fonte única. O conteúdo saiu da fase de design. ✅

17. **Protótipo jogável.** `craque.html` — arquivo único, sem dependências, roda offline. Gerado por `ferramentas/build-html.py` a partir dos JSON; o HTML nunca é editado à mão. ✅
18. **Escala de deltas pela metade**, depois da simulação. Seção 7.0b. ✅

### Ainda em aberto

- **Arte.** 15 retratos base + variações de arquétipo + 6 fundos de era + 14 ilustrações de final + ícones. Ordem de produção sugerida em `arte/README-nomenclatura.md`, seção 6.
- **Simulação de balanceamento.** Só dá para medir a taxa real de cada final dourado e a duração mediana da carreira quando o motor existir. Alvos anotados em `finais.md` §8.
- **4 cargos ainda por escrever**, 81 cartas: `roupeiro`, `coord_base` (metade feita), `capitao` e `treinador` (os dois com arquétipo, 63 cartas juntos). Ver `cargos.md`, seção 4.

---

## Apêndice A — Cartas de exemplo

As 24 cartas do arquivo `cartas-exemplo.json` estão prontas para uso e cobrem as eras 1, 2 e 5, o arco do empresário Valdir, uma carta de partida decisiva e uma carta catastrófica. Servem como referência de tom, de tamanho de texto e de faixa de delta para todo o resto do conteúdo. Passam no validador sem erros.

Aviso honesto sobre elas: 24 cartas são **pequenas demais** para que a deriva por era signifique alguma coisa — o validador marca a medição como informativa abaixo de peso total 150. Os números de deriva só viram sinal confiável perto das 220 cartas da v1. O que as cartas de exemplo provam é o *formato* e o *tom*, não o balanceamento final.

## Apêndice B — Finais nomeados (v1)

| # | Final | Gatilho |
|---|---|---|
| 1 | Sucata | FORMA 0 |
| 2 | Estourado | FORMA 100 |
| 3 | Persona non grata | TORCIDA 0 |
| 4 | Refém do ídolo | TORCIDA 100 |
| 5 | Rescisão amigável | DIRETORIA 0 |
| 6 | Patrimônio do clube | DIRETORIA 100 |
| 7 | Quebrado | DINHEIRO 0 |
| 8 | Sócio-investidor | DINHEIRO 100 |
| 9 | O que não passou da base | qualquer morte na era 1 |
| 10 | A promessa | morte na era 2 com TORCIDA > 70 |
| 11 | O eterno emprestado | 4+ transferências e morte na era 3 |
| 12 | Camisa 10 de um clube só | morte na era 6 sem nunca ter trocado de clube |
| 13 | O ídolo que virou dirigente | era 6, DIRETORIA > 75 |
| 14 | O comentarista | era 6, `moral_publica` alta, sem título |
| 15 | O técnico | era 6, flag `curso_de_treinador` |
| 16 | Estátua | era 6, 3+ títulos e TORCIDA > 80 |
| 17 | O nome no processo | flag `investigacao_apostas` |
| 18 | Aposentadoria no dia certo | era 6, os quatro medidores entre 40 e 70 |
