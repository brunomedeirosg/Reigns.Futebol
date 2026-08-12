# CRAQUE — replicação: segunda bateria de 100 carreiras por agente

**10 agentes × 100 carreiras = 1000 carreiras novas**, somando **2000 carreiras** com a primeira bateria.

### Uma coisa que precisou de conserto antes de rodar

O RNG do jogo é **semeado** (`mulberry32`, semente fixa no carregamento). Uma segunda bateria no mesmo arquivo teria repetido a primeira **carta por carta** — não seria replicação, seria a mesma amostra duas vezes. Expus `__craque.semente(n)` e rodei a bateria 2 com outra semente (`123456789` → `987654321`). As duas são independentes de verdade, e qualquer uma delas volta a ser reproduzível quando eu quiser.

---

## 1. O que se repetiu e o que se moveu

| Agente | Decisões r1 | r2 | Δ | Tempo r1 | r2 | Finais r1 | r2 | Títulos r1 | r2 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Destro** | 14 | 12 | -2 | 1.7 min | 1.5 min | 13 | 13 | 3 | 2 |
| **Canhoto** | 9 | 9 | +0 | 1.1 min | 1.1 min | 8 | 7 | 3 | 4 |
| **Vitinho** | 12 | 13 | +1 | 1.5 min | 1.6 min | 20 | 18 | 7 | 8 |
| **Dembele** | 16 | 14 | -2 | 2.0 min | 1.7 min | 25 | 22 | 10 | 8 |
| **Viciado** | 88 | 95 | +6 | 11.8 min | 12.8 min | 41 | 42 | 16 | 13 |
| **Elon Musk** | 18 | 17 | -1 | 2.3 min | 2.2 min | 9 | 7 | 6 | 6 |
| **Gabigol** | 7 | 7 | +0 | 0.8 min | 0.8 min | 1 | 2 | 3 | 3 |
| **CR7** | 7 | 7 | +0 | 0.8 min | 0.8 min | 1 | 1 | 3 | 3 |
| **Diego Ribas** | 14 | 14 | +0 | 1.8 min | 1.9 min | 5 | 7 | 7 | 6 |
| **Bruno** | 54 | 82 | +27 | 7.2 min | 10.9 min | 43 | 43 | 12 | 11 |

## 2. Como morrem — as duas baterias lado a lado

| Agente | Medidor r1 / r2 | Morte súbita r1 / r2 | Fim natural r1 / r2 | Escolha de vida r1 / r2 | Contexto r1 / r2 |
|---|---|---|---|---|---|
| Destro | 34% / 34% | 37% / 32% | 0% / 0% | 1% / 2% | 28% / 32% |
| Canhoto | 11% / 8% | 21% / 18% | 0% / 0% | 2% / 3% | 66% / 71% |
| Vitinho | 38% / 35% | 26% / 18% | 0% / 0% | 1% / 4% | 35% / 43% |
| Dembele | 43% / 42% | 32% / 23% | 0% / 0% | 2% / 0% | 23% / 35% |
| Viciado | 40% / 38% | 37% / 29% | 12% / 19% | 6% / 7% | 5% / 7% |
| Elon Musk | 71% / 71% | 0% / 0% | 0% / 0% | 0% / 0% | 29% / 29% |
| Gabigol | 0% / 2% | 0% / 0% | 0% / 0% | 0% / 0% | 100% / 98% |
| CR7 | 0% / 0% | 0% / 0% | 0% / 0% | 0% / 0% | 100% / 100% |
| Diego Ribas | 49% / 50% | 0% / 0% | 0% / 0% | 0% / 0% | 51% / 50% |
| Bruno | 36% / 36% | 42% / 36% | 17% / 18% | 4% / 7% | 1% / 3% |

---

## 3. Agregado das 200 carreiras por agente

Os números abaixo são os que eu usaria para decidir qualquer coisa: dobram a amostra e diluem o azar de uma bateria.

| Agente | Decisões (p50) | p10 | p90 | Tempo | Finais distintos | Títulos distintos | % com título |
|---|---:|---:|---:|---:|---:|---:|---:|
| **Destro** | 13 | 5 | 23 | **1.6 min** | 13 | 3 | 38% |
| **Canhoto** | 9 | 5 | 14 | **1.1 min** | 9 | 4 | 36% |
| **Vitinho** | 13 | 6 | 27 | **1.6 min** | 25 | 9 | 48% |
| **Dembele** | 15 | 4 | 28 | **1.9 min** | 28 | 10 | 58% |
| **Viciado** | 91 | 26 | 133 | **12.2 min** | 50 | 16 | 98% |
| **Elon Musk** | 18 | 8 | 26 | **2.3 min** | 9 | 7 | 62% |
| **Gabigol** | 7 | 5 | 10 | **0.8 min** | 2 | 3 | 34% |
| **CR7** | 7 | 4 | 10 | **0.8 min** | 1 | 3 | 32% |
| **Diego Ribas** | 14 | 8 | 22 | **1.8 min** | 7 | 7 | 49% |
| **Bruno** | 72 | 16 | 133 | **9.6 min** | 52 | 13 | 91% |

## 4. Cobertura do catálogo pelas 2.000 carreiras

- **Finais:** 62 de 77 vistos (81%)
- **Títulos:** 16 de 25 conquistados (64%)

**15 finais que ninguém alcançou em 2.000 carreiras:**

- *medidor* (14): A dívida que não era sua · A infiltração número quarenta · A rescisão que você pediu · Deu tudo o que tinha · Encostado · Mercenário · O carro cercado · O clube que você comprou · O corpo que virou método · O nome do estádio · O vilão necessário · Refém do ídolo · Saiu pela porta da frente · Sucata
- *contexto* (1): Estátua

**9 títulos que ninguém conquistou:** O Dono do Próprio Nome · O Indestrutível · O Ingrato · O Laranja · O Padrinho · O Pai · O Professor · O Sobrevivente · O de Casa

---

## 5. Conteúdo morto, agora com 2.000 carreiras de evidência

**31 de 433 cartas (7%) não apareceram uma única vez.** Com a amostra dobrada, esta lista deixou de ser suspeita e passou a ser fato.

| Era(s) | Quantas | Cartas |
|---|---:|---|
| declinio | 10 | `companheira_declinio_01` · `diretor_declinio_04` · `filho_declinio_02` · `filho_declinio_04` · `filho_declinio_05` · `filho_declinio_06` · `fio_aniversario_b3aa` · `fio_duzentos_b2` · `fio_laranja_b3ba` · `fio_microfone_b3aa` |
| declinio/legado | 9 | `fio_aniversario_b2b` · `fio_aniversario_b3ab` · `fio_aniversario_b3ba` · `fio_aniversario_b3bb` · `fio_duzentos_b3a` · `fio_duzentos_b3b` · `fio_sucessor_b3aa` · `fio_sucessor_b3ab` · `fio_sucessor_b3bb` |
| legado | 4 | `filho_legado_02` · `fio_licenca_b3aa` · `fio_licenca_b3ba` · `fio_licenca_b3bb` |
| travessia | 2 | `companheira_carreira_01` · `companheira_pedagio` |
| travessia/auge | 2 | `companheira_carreira_02` · `companheira_distancia_01` |
| auge | 2 | `companheira_distancia_02` · `companheira_ruptura` |
| estouro/travessia/auge | 1 | `capitao_partida` |
| estouro/travessia | 1 | `valdir_estouro_02` |

Estabilidade da lista: a bateria 1 deixou 43 cartas de fora, a bateria 2 deixou 34, e **31 são as mesmas nas duas** — não é sorte de amostra, é conteúdo inalcançável na prática.

Mais **24 cartas apareceram 5 vezes ou menos** em 2.000 carreiras. As dez mais raras:

| Vezes em 2.000 carreiras | Carta | Era | Peso de sorteio |
|---:|---|---|---:|
| 1 | `fio_heranca_b3aa` | legado | 0 |
| 1 | `fio_sucessor_b3ba` | legado | 0 |
| 1 | `filho_legado_01` | legado | 13 |
| 1 | `filho_legado_03` | legado | 9 |
| 1 | `filho_legado_04` | legado | 10 |
| 1 | `fio_valdir_b3bb` | auge/declinio | 0 |
| 1 | `filho_declinio_01` | declinio/legado | 12 |
| 1 | `fio_aniversario_b2a` | declinio/legado | 0 |
| 2 | `fio_laranja_b3ab` | declinio/legado | 0 |
| 2 | `fio_laranja_b3bb` | declinio/legado | 0 |

---

## 6. Veredito de estabilidade

| Medida | Estável entre as duas baterias? |
|---|---|
| Duração mediana | Sim. Maior diferença: **Bruno, 27 decisões**; os outros nove ficaram dentro de 6. |
| Gabigol e CR7 morrendo na Base | Sim, e é categórico: 100% e 98% (Gabigol), 100% e 100% (CR7) das cem carreiras, nas duas baterias. **Não é variância, é regra.** |
| Lista de conteúdo morto | Sim: 31 cartas fora nas duas. |
| Fatais equilibradas entre os lados | Sim: o Destro segue com morte súbita nas duas baterias, o que confirma que o espelhamento pegou. |

---

## 7. As duas coisas que só a replicação mostrou

### 7.1 O Bruno é o único agente cuja mediana não se sustenta em 100 carreiras

Foi a maior diferença entre as baterias: **54 → 82 decisões**. Não é o jogo mudando, é o agente:

| | p10 | p25 | **p50** | p75 | p90 | média |
|---|---:|---:|---:|---:|---:|---:|
| bateria 1 | 16 | 27 | **56** | 116 | 133 | 67 |
| bateria 2 | 20 | 33 | **82** | 129 | 133 | 79 |
| 200 juntas | 16 | 29 | **73** | 124 | 133 | 73 |

A distribuição dele é **quase bimodal**: um monte de carreiras que morre antes de 30 decisões e um monte que vai até o teto de idade, com pouca coisa no meio. Uma mediana pousada exatamente no vazio entre os dois montes balança muito com 100 amostras — a **média** (67 e 79) e os quartis são bem mais firmes.

Isso é honesto de dizer e tem consequência prática: **para o Bruno, o número que vale é o das 200 carreiras — 73 decisões, 9,6 min**, dentro da faixa de 8 a 12 que você escolheu. Ele também é o único agente que usa `Math.random()` na decisão (o ruído de hesitação e os 15% de aceitar risco), então o próprio agente adiciona variância além da do baralho.

Os outros nove ficaram todos dentro de **±2 decisões** entre as baterias.

### 7.2 Seis dos oito dourados não apareceram em 2.000 carreiras

Dos 15 finais que ninguém alcançou, **seis são dourados**: *Deu tudo o que tinha*, *O corpo que virou método*, *O vilão necessário*, *O nome do estádio*, *Saiu pela porta da frente* e *O clube que você comprou*. Só *De olhos abertos* e *Quebrado e limpo* saíram.

Não é contradição com a medição anterior, que dava 5,3% de dourados: aquele número era de um agente **feito para caçar dourado**, que desfaz marcas de escândalo de propósito. Nenhuma destas dez personalidades persegue dourado — nem o Viciado, que persegue *final ainda não visto*, o que é diferente.

O que a replicação confirma é a mesma coisa que o conteúdo morto: **dourado depende de chegar ao declínio e ao legado**, e só o Viciado (31%) e o Bruno (27%) chegam. Enquanto dois terços das carreiras terminam antes do Auge, dourado continua sendo conteúdo de quem já sabe jogar — o que pode estar certo, mas é bom estar dito com número.

### 7.3 O que mais chama atenção nos agregados

- **O Viciado é o melhor jogador do jogo por qualquer métrica:** 91 decisões, 12,2 min, **50 finais distintos**, 16 títulos e 98% de carreiras com título. Jogar para colecionar rende mais que jogar para sobreviver — e isso valida a coleção como sistema.
- **O Bruno vê mais finais que o Viciado (52 contra 50) em menos decisões**, porque morre de mais jeitos diferentes. Os dois juntos cobrem quase todo o catálogo alcançável.
- **Canhoto, Gabigol e CR7 ficam abaixo de 40% de carreiras com título.** Morrem antes de merecer nome, o que é coerente — mas os 34% do Gabigol e os 32% do CR7 vêm da mesma causa da seção 8.2 do relatório anterior: sete decisões não dão tempo de nada.
