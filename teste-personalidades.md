# CRAQUE — teste de balanceamento com dez personalidades

**10 agentes × 100 carreiras = 1000 carreiras simuladas.** Baralho de 433 cartas, 77 finais, 25 títulos. Zero erros de console em todas.

Tempo estimado com o modelo de sempre: decisão 7 s, carta de eco 3 s, balanço de ano 5 s. Os segundos por carta são estimativa, não medição de jogador real — é a única parte destes números que não é medida.

---

## 1. Panorama

| Agente | Decisões (p50) | p10 | p90 | Idade final | Tempo médio | Finais distintos | Títulos distintos | % com título |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **Destro** | 14 | 6 | 24 | 18 | **1.7 min** | 13 | 3 | 39% |
| **Canhoto** | 9 | 5 | 15 | 18 | **1.1 min** | 8 | 3 | 34% |
| **Vitinho** | 12 | 6 | 25 | 18 | **1.5 min** | 20 | 7 | 41% |
| **Dembele** | 16 | 4 | 30 | 19 | **2.0 min** | 25 | 10 | 54% |
| **Viciado** | 88 | 26 | 133 | 29 | **11.8 min** | 41 | 16 | 99% |
| **Elon Musk** | 18 | 9 | 26 | 19 | **2.3 min** | 9 | 6 | 58% |
| **Gabigol** | 7 | 5 | 11 | 17 | **0.8 min** | 1 | 3 | 32% |
| **CR7** | 7 | 4 | 10 | 17 | **0.8 min** | 1 | 3 | 30% |
| **Diego Ribas** | 14 | 8 | 23 | 18 | **1.8 min** | 5 | 7 | 50% |
| **Bruno** | 54 | 16 | 133 | 24 | **7.2 min** | 43 | 12 | 86% |

## 2. Como cada um morre

| Agente | Medidor no extremo | Morte súbita | Fim natural | Escolha de vida | Contexto |
|---|---:|---:|---:|---:|---:|
| Destro | 34% | 37% | 0% | 1% | 28% |
| Canhoto | 11% | 21% | 0% | 2% | 66% |
| Vitinho | 38% | 26% | 0% | 1% | 35% |
| Dembele | 43% | 32% | 0% | 2% | 23% |
| Viciado | 40% | 37% | 12% | 6% | 5% |
| Elon Musk | 71% | 0% | 0% | 0% | 29% |
| Gabigol | 0% | 0% | 0% | 0% | 100% |
| CR7 | 0% | 0% | 0% | 0% | 100% |
| Diego Ribas | 49% | 0% | 0% | 0% | 51% |
| Bruno | 36% | 42% | 17% | 4% | 1% |

---

## 3. Finais alcançados, agente por agente

### Destro

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 28% | O que não passou da base | contexto | cinza |
| 21% | Duzentos metros | morte_subita | preta |
| 17% | Filho do clube | medidor | cinza |
| 8% | Campo de terra, coturno, véspera | morte_subita | preta |
| 8% | Institucional | medidor | cinza |
| 4% | Vinte por hora | morte_subita | preta |
| 3% | À disposição de ninguém | medidor | cinza |
| 3% | Persona non grata | medidor | cinza |
| 3% | A tatuagem | morte_subita | preta |
| 2% | Insaciável | medidor | preta |
| 1% | Menos oito graus não negociam | morte_subita | preta |
| 1% | A oficina do seu tio | escolha_de_vida | verde |
| 1% | A máquina | medidor | cinza |

### Canhoto

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 66% | O que não passou da base | contexto | cinza |
| 12% | O empurrão | morte_subita | preta |
| 9% | A intoxicação mais cara do futebol brasileiro | morte_subita | preta |
| 6% | A estátua antes da hora | medidor | cinza |
| 3% | Sem clube | medidor | cinza |
| 2% | Passou em primeira chamada | escolha_de_vida | verde |
| 1% | Estourado | medidor | preta |
| 1% | À disposição de ninguém | medidor | cinza |

### Vitinho

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 35% | O que não passou da base | contexto | cinza |
| 18% | A estátua antes da hora | medidor | cinza |
| 7% | O empurrão | morte_subita | preta |
| 6% | Campo de terra, coturno, véspera | morte_subita | preta |
| 5% | Laranja | medidor | preta |
| 5% | Duzentos metros | morte_subita | preta |
| 3% | Sem clube | medidor | cinza |
| 3% | Aos vinte e quatro | medidor | cinza |
| 2% | A tatuagem | morte_subita | preta |
| 2% | A intoxicação mais cara do futebol brasileiro | morte_subita | preta |
| 2% | Institucional | medidor | cinza |
| 2% | A casa caiu | medidor | preta |
| 2% | Rico e aposentado aos trinta | medidor | cinza |
| 2% | Mil cilindradas, três da manhã | morte_subita | preta |
| 1% | Passou em primeira chamada | escolha_de_vida | verde |
| 1% | Penhora | medidor | preta |
| 1% | Filho do clube | medidor | cinza |
| 1% | À disposição de ninguém | medidor | cinza |
| 1% | Bicicleta na piscina de bolinhas | morte_subita | preta |
| 1% | Vinte por hora | morte_subita | preta |

### Dembele

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 23% | O que não passou da base | contexto | cinza |
| 12% | A estátua antes da hora | medidor | cinza |
| 7% | O empurrão | morte_subita | preta |
| 6% | Laranja | medidor | preta |
| 6% | Bicicleta na piscina de bolinhas | morte_subita | preta |
| 6% | Campo de terra, coturno, véspera | morte_subita | preta |
| 6% | Duzentos metros | morte_subita | preta |
| 4% | À disposição de ninguém | medidor | cinza |
| 4% | Sem clube | medidor | cinza |
| 3% | Aos vinte e quatro | medidor | cinza |
| 3% | Institucional | medidor | cinza |
| 2% | Vinte por hora | morte_subita | preta |
| 2% | A intoxicação mais cara do futebol brasileiro | morte_subita | preta |
| 2% | A máquina | medidor | cinza |
| 2% | Penhora | medidor | preta |
| 2% | Estourado | medidor | preta |
| 2% | Rico e aposentado aos trinta | medidor | cinza |
| 1% | A tatuagem | morte_subita | preta |
| 1% | Patrimônio do clube | medidor | cinza |
| 1% | Onze dias vencido | morte_subita | preta |
| 1% | Voltou antes de precisar voltar | escolha_de_vida | verde |
| 1% | Mil cilindradas, três da manhã | morte_subita | preta |
| 1% | Passou em primeira chamada | escolha_de_vida | verde |
| 1% | A casa caiu | medidor | preta |
| 1% | O nome no processo | medidor | preta |

### Viciado

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 8% | A estátua antes da hora | medidor | cinza |
| 7% | Laranja | medidor | preta |
| 6% | O garoto-propaganda | medidor | cinza |
| 6% | Uma carreira inteira | natural | cinza |
| 5% | O último jogo | natural | prata |
| 4% | Quarenta mil pessoas e um gramado encharcado | morte_subita | preta |
| 4% | Camisa 10 de um clube só | contexto | dourada |
| 4% | Santo de gesso | medidor | cinza |
| 3% | O estádio cheio que você escolheu | morte_subita | preta |
| 3% | Bicicleta na piscina de bolinhas | morte_subita | preta |
| 3% | A casa caiu | medidor | preta |
| 3% | Duzentos reais | morte_subita | preta |
| 3% | Patrimônio do clube | medidor | cinza |
| 2% | O áudio de trinta e sete segundos | morte_subita | preta |
| 2% | A live que ficou salva | morte_subita | preta |
| 2% | Trezentos e sessenta dias | morte_subita | preta |
| 2% | À disposição de ninguém | medidor | cinza |
| 2% | Quatro quilos em três dias | morte_subita | preta |
| 2% | O microfone do outro lado | escolha_de_vida | verde |
| 2% | O helicóptero | morte_subita | preta |
| 2% | Conheço o mar | morte_subita | preta |
| 2% | Juros do joelho | medidor | cinza |
| 2% | Campo de terra, coturno, véspera | morte_subita | preta |
| 2% | O lateral de vinte e dois | morte_subita | preta |
| 2% | A procuração | morte_subita | preta |
| 2% | A escolinha do bairro | escolha_de_vida | verde |
| 1% | Quem aplica atende à noite | morte_subita | preta |
| 1% | Estrangeiro em casa | medidor | cinza |
| 1% | Andando normal aos cinquenta | escolha_de_vida | verde |
| 1% | Penhora | medidor | preta |
| 1% | O posto do primo | medidor | preta |
| 1% | Os últimos quinze minutos | morte_subita | preta |
| 1% | O que não passou da base | contexto | cinza |
| 1% | A chuteira da estreia | morte_subita | preta |
| 1% | A máquina | medidor | cinza |
| 1% | Menos oito graus não negociam | morte_subita | preta |
| 1% | Institucional | medidor | cinza |
| 1% | A oficina do seu tio | escolha_de_vida | verde |
| 1% | Fim de linha | natural | cinza |
| 1% | Mil cilindradas, três da manhã | morte_subita | preta |
| 1% | A tatuagem | morte_subita | preta |

### Elon Musk

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 29% | O que não passou da base | contexto | cinza |
| 28% | Rico e aposentado aos trinta | medidor | cinza |
| 19% | A casa caiu | medidor | preta |
| 16% | Laranja | medidor | preta |
| 2% | A estátua antes da hora | medidor | cinza |
| 2% | Aos vinte e quatro | medidor | cinza |
| 2% | À disposição de ninguém | medidor | cinza |
| 1% | Sem clube | medidor | cinza |
| 1% | Estourado | medidor | preta |

### Gabigol

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 100% | O que não passou da base | contexto | cinza |

### CR7

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 100% | O que não passou da base | contexto | cinza |

### Diego Ribas

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 51% | O que não passou da base | contexto | cinza |
| 40% | Filho do clube | medidor | cinza |
| 6% | Patrimônio do clube | medidor | cinza |
| 2% | Aos vinte e quatro | medidor | cinza |
| 1% | O garoto-propaganda | medidor | cinza |

### Bruno

| % | Final | Categoria | Moldura |
|---:|---|---|---|
| 7% | Uma carreira inteira | natural | cinza |
| 7% | O último jogo | natural | prata |
| 6% | Laranja | medidor | preta |
| 5% | O garoto-propaganda | medidor | cinza |
| 5% | A tatuagem | morte_subita | preta |
| 5% | Bicicleta na piscina de bolinhas | morte_subita | preta |
| 4% | Mil cilindradas, três da manhã | morte_subita | preta |
| 4% | Onze dias vencido | morte_subita | preta |
| 3% | A intoxicação mais cara do futebol brasileiro | morte_subita | preta |
| 3% | O empurrão | morte_subita | preta |
| 3% | A estátua antes da hora | medidor | cinza |
| 3% | Vinte por hora | morte_subita | preta |
| 3% | O nome no processo | medidor | preta |
| 3% | A casa caiu | medidor | preta |
| 3% | Fim de linha | natural | cinza |
| 2% | Menos oito graus não negociam | morte_subita | preta |
| 2% | Duzentos metros | morte_subita | preta |
| 2% | Patrimônio do clube | medidor | cinza |
| 2% | À disposição de ninguém | medidor | cinza |
| 2% | Conheço o mar | morte_subita | preta |
| 2% | A live que ficou salva | morte_subita | preta |
| 2% | A oficina do seu tio | escolha_de_vida | verde |
| 2% | Campo de terra, coturno, véspera | morte_subita | preta |
| 1% | A escolinha do bairro | escolha_de_vida | verde |
| 1% | Santo de gesso | medidor | cinza |
| 1% | Sem clube | medidor | cinza |
| 1% | De olhos abertos | medidor | dourada |
| 1% | Queimado no mercado | medidor | preta |
| 1% | Quebrado | medidor | cinza |
| 1% | Quem aplica atende à noite | morte_subita | preta |
| 1% | Bandeira | medidor | cinza |
| 1% | O posto do primo | medidor | preta |
| 1% | Rico e aposentado aos trinta | medidor | cinza |
| 1% | Camisa 10 de um clube só | contexto | dourada |
| 1% | Institucional | medidor | cinza |
| 1% | O estádio cheio que você escolheu | morte_subita | preta |
| 1% | A máquina | medidor | cinza |
| 1% | Os últimos quinze minutos | morte_subita | preta |
| 1% | Persona non grata | medidor | cinza |
| 1% | Voltou antes de precisar voltar | escolha_de_vida | verde |
| 1% | Estourado | medidor | preta |
| 1% | Quarenta mil pessoas e um gramado encharcado | morte_subita | preta |
| 1% | O lateral de vinte e dois | morte_subita | preta |

---

## 4. Títulos conquistados

| Título | Destro | Canhoto | Vitinho | Dembele | Viciado | Elon Musk | Gabigol | CR7 | Diego Ribas | Bruno |
|---|---|---|---|---|---|---|---|---|---|---|
| A Voz | 2% | — | — | — | 2% | — | — | — | — | — |
| O Arrimo | — | 3% | 5% | 7% | 15% | — | 3% | 4% | 4% | 17% |
| O Campeão | — | — | — | — | 1% | — | — | — | — | — |
| O Difícil | 10% | — | 5% | 4% | 21% | — | — | — | 3% | 22% |
| O Duro | — | 11% | 12% | 13% | 8% | 17% | 11% | 14% | 14% | 5% |
| O Embaixador | — | — | — | 4% | 19% | 9% | — | — | 3% | 2% |
| O Encostado | — | — | 1% | 3% | 1% | — | — | — | — | — |
| O Mercenário | — | — | — | 1% | 1% | 2% | — | — | — | 1% |
| O Moleque | — | — | — | — | 1% | 1% | — | — | — | 1% |
| O Método | — | — | — | — | 1% | — | — | — | — | 1% |
| O Profissional | — | — | — | 1% | 2% | — | — | — | 1% | 2% |
| O Teimoso | — | — | 2% | 1% | 2% | 3% | — | — | — | 3% |
| O Tudo ou Nada | 27% | — | 8% | 11% | 18% | 26% | — | 12% | 2% | 21% |
| O Universitário | — | 20% | 8% | 9% | 5% | — | 18% | — | 23% | 10% |
| O Vendido | — | — | — | — | 1% | — | — | — | — | 1% |
| O Ídolo | — | — | — | — | 1% | — | — | — | — | — |
| *sem título* | 61% | 66% | 59% | 46% | 1% | 42% | 68% | 70% | 50% | 14% |

**9 títulos que nenhum dos dez conquistou:** O Laranja · O Padrinho · O Indestrutível · O Ingrato · O Dono do Próprio Nome · O Pai · O de Casa · O Professor · O Sobrevivente

Quando o título chega (número da decisão):

| Agente | p25 | mediana | p75 |
|---|---:|---:|---:|
| Destro | 5 | **8** | 18 |
| Canhoto | 2 | **5** | 7 |
| Vitinho | 7 | **10** | 17 |
| Dembele | 4 | **11** | 15 |
| Viciado | 10 | **17** | 28 |
| Elon Musk | 3 | **10** | 16 |
| Gabigol | 2 | **3** | 6 |
| CR7 | 2 | **4** | 7 |
| Diego Ribas | 4 | **8** | 12 |
| Bruno | 5 | **16** | 26 |

---

## 5. Até onde cada um chega

| Agente | Base | Estouro | Travessia | Auge | Declinio | Legado | Transferências (p50) |
|---|---|---|---|---|---|---|---|
| Destro | 100% | 43% | 1% | 0% | 0% | 0% | 0 |
| Canhoto | 100% | 11% | 0% | 0% | 0% | 0% | 0 |
| Vitinho | 100% | 44% | 1% | 0% | 0% | 0% | 0 |
| Dembele | 100% | 55% | 7% | 2% | 0% | 0% | 0 |
| Viciado | 100% | 97% | 82% | 69% | 47% | 31% | 1 |
| Elon Musk | 100% | 71% | 3% | 0% | 0% | 0% | 0 |
| Gabigol | 100% | 0% | 0% | 0% | 0% | 0% | 0 |
| CR7 | 100% | 0% | 0% | 0% | 0% | 0% | 0 |
| Diego Ribas | 100% | 49% | 1% | 0% | 0% | 0% | 0 |
| Bruno | 100% | 90% | 63% | 44% | 35% | 27% | 1 |

Patamar de clube no fim da carreira:

| Agente | acesso | segunda | grande do país | médio europeu | gigante |
|---|---|---|---|---|---|
| Destro | 100% | 0% | 0% | 0% | 0% |
| Canhoto | 89% | 10% | 1% | 0% | 0% |
| Vitinho | 86% | 13% | 1% | 0% | 0% |
| Dembele | 76% | 23% | 1% | 0% | 0% |
| Viciado | 81% | 14% | 4% | 1% | 0% |
| Elon Musk | 71% | 27% | 2% | 0% | 0% |
| Gabigol | 100% | 0% | 0% | 0% | 0% |
| CR7 | 100% | 0% | 0% | 0% | 0% |
| Diego Ribas | 93% | 7% | 0% | 0% | 0% |
| Bruno | 45% | 35% | 12% | 7% | 1% |

---

## 6. Cartas enfrentadas

| Agente | Cartas distintas vistas | % do baralho | Cartas por carreira (p50) |
|---|---:|---:|---:|
| Destro | 99 de 433 | 23% | 14 |
| Canhoto | 68 de 433 | 16% | 9 |
| Vitinho | 114 de 433 | 26% | 12 |
| Dembele | 160 de 433 | 37% | 16 |
| Viciado | 384 de 433 | 89% | 88 |
| Elon Musk | 111 de 433 | 26% | 18 |
| Gabigol | 49 de 433 | 11% | 7 |
| CR7 | 47 de 433 | 11% | 7 |
| Diego Ribas | 103 de 433 | 24% | 14 |
| Bruno | 384 de 433 | 89% | 54 |

### Destro — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 51 | 51% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 48 | 48% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 40 | 40% | `coord_base_12` | base/estouro | coord_base | importante |
| 38 | 38% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 37 | 37% | `roupeiro_base_05` | base | roupeiro | padrao |
| 35 | 35% | `parceiro_base_01` | base | parceiro | importante |
| 35 | 35% | `parceiro_base_04` | base | parceiro | padrao |
| 34 | 34% | `parceiro_base_08` | base | parceiro | padrao |
| 34 | 34% | `roupeiro_base_02` | base | roupeiro | padrao |
| 33 | 33% | `mae_base_05` | base/estouro | mae | padrao |
| 31 | 31% | `parceiro_base_09` | base | parceiro | importante |
| 31 | 31% | `valdir_base_01` | base | empresario | importante |

### Canhoto — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 38 | 38% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 36 | 36% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 36 | 36% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 27 | 27% | `roupeiro_base_04` | base | roupeiro | padrao |
| 27 | 27% | `coord_base_01` | base | coord_base | padrao |
| 27 | 27% | `parceiro_base_08` | base | parceiro | padrao |
| 26 | 26% | `parceiro_base_01` | base | parceiro | importante |
| 25 | 25% | `parceiro_base_04` | base | parceiro | padrao |
| 25 | 25% | `mae_base_03` | base | mae | padrao |
| 25 | 25% | `coord_base_08` | base | coord_base | padrao |
| 25 | 25% | `coord_base_09` | base | coord_base | padrao |
| 24 | 24% | `coord_base_05` | base | coord_base | padrao |

### Vitinho — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 53 | 53% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 50 | 50% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 43 | 43% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 42 | 42% | `parceiro_base_04` | base | parceiro | padrao |
| 40 | 40% | `coord_base_09` | base | coord_base | padrao |
| 40 | 40% | `coord_base_12` | base/estouro | coord_base | importante |
| 39 | 39% | `valdir_base_01` | base | empresario | importante |
| 37 | 37% | `mae_base_05` | base/estouro | mae | padrao |
| 36 | 30% | `transferencia_sobe` | base/estouro/travessia/auge/declinio/legado | empresario | importante |
| 34 | 34% | `coord_base_01` | base | coord_base | padrao |
| 31 | 31% | `parceiro_base_01` | base | parceiro | importante |
| 30 | 30% | `parceiro_base_08` | base | parceiro | padrao |

### Dembele — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 49 | 49% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 46 | 46% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 42 | 42% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 41 | 41% | `coord_base_12` | base/estouro | coord_base | importante |
| 39 | 33% | `transferencia_sobe` | base/estouro/travessia/auge/declinio/legado | empresario | importante |
| 37 | 37% | `parceiro_base_09` | base | parceiro | importante |
| 37 | 37% | `parceiro_base_01` | base | parceiro | importante |
| 36 | 36% | `valdir_base_03` | base | empresario | padrao |
| 35 | 35% | `coord_base_06` | base | coord_base | padrao |
| 33 | 33% | `roupeiro_base_05` | base | roupeiro | padrao |
| 33 | 33% | `parceiro_base_04` | base | parceiro | padrao |
| 33 | 33% | `coord_base_05` | base | coord_base | padrao |

### Viciado — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 281 | 91% | `transferencia_sobe` | base/estouro/travessia/auge/declinio/legado | empresario | importante |
| 92 | 92% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 88 | 64% | `valdir_estouro_03` | estouro/travessia/auge | empresario | padrao |
| 85 | 85% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 76 | 76% | `valdir_estouro_04` | estouro/travessia | empresario | legado |
| 75 | 75% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 74 | 74% | `coord_base_12` | base/estouro | coord_base | importante |
| 74 | 59% | `organizada_estouro_02` | estouro/travessia/auge | organizada | importante |
| 73 | 57% | `capitao_estouro_03` | estouro/travessia/auge | capitao | padrao |
| 72 | 72% | `capitao_estouro_02` | estouro/travessia | capitao | padrao |
| 70 | 70% | `fisio_estouro_02` | estouro/travessia | fisio | importante |
| 69 | 54% | `mae_estouro_03` | estouro/travessia/auge | mae | padrao |

### Elon Musk — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 58 | 58% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 51 | 51% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 48 | 48% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 47 | 47% | `mae_base_05` | base/estouro | mae | padrao |
| 45 | 45% | `coord_base_09` | base | coord_base | padrao |
| 42 | 42% | `coord_base_12` | base/estouro | coord_base | importante |
| 40 | 40% | `valdir_base_01` | base | empresario | importante |
| 40 | 35% | `transferencia_sobe` | base/estouro/travessia/auge/declinio/legado | empresario | importante |
| 38 | 38% | `parceiro_base_04` | base | parceiro | padrao |
| 37 | 37% | `valdir_base_02` | base/estouro | empresario | importante |
| 37 | 37% | `parceiro_base_05` | base | parceiro | padrao |
| 35 | 35% | `roupeiro_base_02` | base | roupeiro | padrao |

### Gabigol — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 26 | 26% | `coord_base_05` | base | coord_base | padrao |
| 25 | 25% | `parceiro_base_01` | base | parceiro | importante |
| 25 | 25% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 23 | 23% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 23 | 23% | `mae_base_04` | base | mae | padrao |
| 23 | 23% | `roupeiro_base_04` | base | roupeiro | padrao |
| 22 | 22% | `coord_base_08` | base | coord_base | padrao |
| 21 | 21% | `mae_base_03` | base | mae | padrao |
| 21 | 21% | `parceiro_base_02` | base | parceiro | padrao |
| 20 | 20% | `roupeiro_base_05` | base | roupeiro | padrao |
| 20 | 20% | `fisio_base_04` | base | fisio | padrao |
| 20 | 20% | `roupeiro_base_02` | base | roupeiro | padrao |

### CR7 — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 26 | 26% | `roupeiro_base_05` | base | roupeiro | padrao |
| 25 | 25% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 25 | 25% | `parceiro_base_01` | base | parceiro | importante |
| 25 | 25% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 25 | 25% | `coord_base_03` | base | coord_base | padrao |
| 24 | 24% | `coord_base_12` | base/estouro | coord_base | importante |
| 23 | 23% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 22 | 22% | `roupeiro_base_04` | base | roupeiro | padrao |
| 21 | 21% | `coord_base_09` | base | coord_base | padrao |
| 20 | 20% | `coord_base_10` | base | coord_base | padrao |
| 20 | 20% | `parceiro_base_09` | base | parceiro | importante |
| 20 | 20% | `parceiro_base_06` | base | parceiro | padrao |

### Diego Ribas — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 56 | 56% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 41 | 41% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 40 | 40% | `coord_base_12` | base/estouro | coord_base | importante |
| 37 | 37% | `roupeiro_base_05` | base | roupeiro | padrao |
| 37 | 37% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 36 | 36% | `valdir_base_01` | base | empresario | importante |
| 36 | 36% | `parceiro_base_09` | base | parceiro | importante |
| 35 | 35% | `parceiro_base_08` | base | parceiro | padrao |
| 35 | 35% | `coord_base_06` | base | coord_base | padrao |
| 33 | 33% | `coord_base_10` | base | coord_base | padrao |
| 32 | 32% | `parceiro_base_04` | base | parceiro | padrao |
| 31 | 31% | `roupeiro_base_02` | base | roupeiro | padrao |

### Bruno — as 12 cartas que mais apareceram

| Vezes em 100 carreiras | % das carreiras que viram | Carta | Era | Cargo | Peso dram. |
|---:|---:|---|---|---|---|
| 155 | 76% | `transferencia_sobe` | base/estouro/travessia/auge/declinio/legado | empresario | importante |
| 83 | 83% | `roupeiro_vida4_01` | base/estouro/travessia/auge | roupeiro | importante |
| 79 | 79% | `roupeiro_vida3_01` | base/estouro/travessia | roupeiro | importante |
| 72 | 57% | `organizada_estouro_02` | estouro/travessia/auge | organizada | importante |
| 70 | 70% | `roupeiro_vida2_01` | base/estouro | roupeiro | padrao |
| 61 | 61% | `valdir_estouro_04` | estouro/travessia | empresario | legado |
| 60 | 60% | `mae_estouro_02` | estouro/travessia | mae | importante |
| 59 | 59% | `coord_base_12` | base/estouro | coord_base | importante |
| 58 | 58% | `capitao_estouro_02` | estouro/travessia | capitao | padrao |
| 57 | 48% | `valdir_estouro_03` | estouro/travessia/auge | empresario | padrao |
| 55 | 55% | `fisio_estouro_02` | estouro/travessia | fisio | importante |
| 54 | 54% | `mae_base_05` | base/estouro | mae | padrao |

---

## 7. Conteúdo que ninguém viu — o achado mais útil para balanceamento

**43 de 433 cartas (10%) não apareceram em nenhuma das 1000 carreiras.**

| Era(s) | Quantas | Cartas |
|---|---:|---|
| declinio | 13 | `companheira_declinio_01` · `diretor_declinio_04` · `filho_declinio_02` · `filho_declinio_03` · `filho_declinio_04` · `filho_declinio_05` · `filho_declinio_06` · `fio_aniversario_b3aa` … +5 |
| declinio/legado | 12 | `filho_declinio_01` · `fio_aniversario_b2a` · `fio_aniversario_b2b` · `fio_aniversario_b3ab` · `fio_aniversario_b3ba` · `fio_aniversario_b3bb` · `fio_duzentos_b3a` · `fio_duzentos_b3b` … +4 |
| legado | 8 | `filho_legado_01` · `filho_legado_02` · `filho_legado_03` · `filho_legado_04` · `fio_heranca_b3bb` · `fio_licenca_b3aa` · `fio_licenca_b3ba` · `fio_licenca_b3bb` |
| travessia | 2 | `companheira_carreira_01` · `companheira_pedagio` |
| travessia/auge | 2 | `companheira_carreira_02` · `companheira_distancia_01` |
| auge | 2 | `companheira_distancia_02` · `companheira_ruptura` |
| estouro/travessia/auge | 1 | `capitao_partida` |
| estouro/travessia | 1 | `valdir_estouro_02` |
| auge/declinio/legado | 1 | `fio_cicatriz_b3bb` |
| auge/declinio | 1 | `fio_valdir_b3bb` |

Além dessas, **23 cartas apareceram 3 vezes ou menos** em 1.000 carreiras.

---

## 8. O que estes números dizem — minha leitura

### 8.1 Consertado durante o teste: as fatais estavam todas do mesmo lado

**Todas as 24 opções fatais e todas as 6 saídas do futebol estavam na ESQUERDA.** O Destro e o Canhoto expuseram isso na primeira rodada, e nenhuma simulação anterior tinha pegado, porque todos os meus agentes decidiam por conteúdo:

| | Destro (só direita) | Canhoto (só esquerda) |
|---|---:|---:|
| Morte súbita **antes** | **0%** | 33% |
| Morte súbita **depois** | **37%** | 21% |

Um jogador que aprendesse "esquerda é perigo" ficava **imortal a morte súbita** e nunca podia sair do futebol. Espelhei metade das cartas (12 fatais de cada lado, 3 saídas de cada lado) e o validador ganhou uma regra: opção que encerra concentrada em mais de 70% de um lado passa a ser **erro**.

Os números do relatório acima já são os de depois do conserto.

### 8.2 O problema aberto, e é o maior: monomania mata em sete decisões

**Gabigol e CR7 morrem em 7 decisões, 100% das vezes, na era Base, com o mesmo final de contexto** — *"O que não passou da base"*. Um único final, em cem carreiras. Nenhum dos dois chega ao Estouro.

A causa é aritmética: os medidores começam em 50, uma carta de legado move até ~40 num medidor, e três escolhas alinhadas na mesma direção fecham os 50 pontos que faltam para o teto. **Qualquer estratégia consistente morre antes de entender o jogo** — e "escolher o que a torcida quer" é a estratégia mais natural que um jogador novo tem.

Que o excesso mate é a regra central e não deve ser suavizada. Que ele mate em 50 segundos, na primeira era, é outra coisa: essa morte não ensina nada, porque o jogador não teve tempo de ver o mundo. Para comparar: o Bruno faz 54 decisões e vê 43 finais; o Vitinho, que só intercala mecanicamente, já faz 12 e vê 20.

Três caminhos, na ordem em que eu recomendaria:

1. **Teto de magnitude na era Base.** Nenhuma carta da base move mais de ~20 num medidor. A base é onde se aprende a ler as barras, e hoje ela tem cartas de 40. Custa pouco, é local, não toca no resto do baralho.
2. **Rendimento decrescente perto do teto, só no ganho.** Um `+40` em TORCIDA com ela em 85 entra como `+15`; a perda continua inteira. Preserva a morte por excesso e tira a morte por três cliques. É diferente do amortecimento que já testamos e descartamos — aquele valia nos dois sentidos e nos dois extremos, e apagou 40 finais.
3. **Não mexer.** Aceitar que o jogo pune monomania desde o primeiro minuto, e que a lição se aprende na segunda carreira — que dura 50 segundos.

Não implementei nenhum: é decisão sua, e mexeria no balanceamento que você acabou de aprovar.

### 8.3 Conteúdo morto: 43 cartas e 11 títulos

**43 de 433 cartas (10%) não apareceram em nenhuma das mil carreiras**, e a lista tem padrão: quase tudo é batida 2 ou 3 de fio no declínio e no legado, mais **o arco inteiro da companheira** (`companheira_carreira_01/02`, `companheira_distancia_01/02`, `companheira_ruptura`, `companheira_pedagio`).

Não é bug: é consequência de a carreira mediana morrer aos 23 anos. Só o Viciado (31%) e o Bruno (27%) chegam ao Legado com alguma frequência. Os **11 títulos que ninguém conquistou** contam a mesma história — O Padrinho, O Pai, O Professor, O Campeão e O Sobrevivente são todos de declínio ou legado.

A pergunta que isso levanta é de projeto, não de número: **um terço do baralho existe para os 27% de carreiras que chegam lá.** Ou o conteúdo tardio ganha portas mais cedo, ou a carreira dura mais, ou a reencarnação precisa ser mais insistente em levar o jogador até o fim.

### 8.4 O Viciado valida a coleção

O agente que joga para colecionar faz **88 decisões (11,8 min)**, vê **41 finais e 16 títulos** e é o único que chega ao Legado com frequência. É exatamente o que se quer de um jogo de coleção: **jogar para ver tudo é uma estratégia distinta de jogar para sobreviver, e ela rende mais.** O Bruno, jogando realista, vê 43 finais em 54 decisões — mais finais em menos cartas, porque morre de jeitos mais variados.

### 8.5 Duas ressalvas de método

- **Elon Musk e Diego Ribas com 0% de morte súbita é artefato do meu agente, não propriedade do jogo:** programei os maximizadores para nunca escolher uma opção fatal. O número que vale deles é o de morte por medidor — 71% e 49%.
- Nos agentes que **intercalam** (Vitinho e Dembele), a alternância conta só as decisões: as cartas de eco não viram o lado, porque não decidem nada.
