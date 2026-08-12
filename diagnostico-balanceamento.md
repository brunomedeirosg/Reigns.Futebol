# CRAQUE — diagnóstico de balanceamento e manual de soluções

**Base de evidência:** 2.000 carreiras (10 personalidades × 100 × 2 baterias independentes), baralho de 433 cartas, 77 finais, 25 títulos. Nada aqui foi aplicado — é diagnóstico e catálogo de opções.

---

## Sumário: seis problemas, em ordem de impacto

| # | Problema | Evidência de uma linha | Custo de consertar |
|---|---|---|---|
| **P1** | **44,5% das carreiras terminam no mesmo final** | 891 de 2.000 caíram em *"O que não passou da base"* | Baixo — 8 finais escritos |
| **P2** | **O teto mata 5× mais que o piso** | 83% das mortes por medidor são em 100, 17% em 0 | Médio — mecânica nova |
| **P3** | **Monomania mata em 7 decisões** | Gabigol e CR7: 7 decisões, 98–100% na era Base | Baixo — teto local de magnitude |
| **P4** | **Um terço do baralho para um quarto das carreiras** | 31 cartas, 15 finais e 9 títulos nunca vistos | Médio — depende de escolha de projeto |
| **P5** | **15 finais respondem por 80% das carreiras** | de 77 disponíveis | É consequência de P1, P2 e P4 |
| **P6** | **O teto de idade cria um pico artificial** | 40 das 200 carreiras do agente realista pararam exatamente no limite | Baixo |

**P1 é o mais barato e o mais grave ao mesmo tempo.** Se eu pudesse mexer em uma coisa só, seria essa.

---

# Parte I — Diagnóstico

## P1. Quase metade das carreiras vê a mesma tela final

### Sintoma
Em 2.000 carreiras, **891 (44,5%) terminaram em *"O que não passou da base"***. O segundo final mais comum aparece em 5,5%. Para oito dos dez agentes, esse é o final mais frequente; para o Gabigol e o CR7 é o **único** final em cem carreiras.

### Causa
Uma linha em `resolverFinal`:

```js
for(const f of DADOS.finais.contexto) if(bate(f.condicoes)) return f;   // ← contexto vem primeiro
if(medidor===null){ ...fim natural... }
const fam=DADOS.finais.familias[medidor+"_"+extremo];                   // ← família só depois
```

E a condição desse final de contexto é:

```json
{ "era": ["base"] }
```

**Toda morte na era Base devolve esse final, seja por qual medidor for e com quais flags for.** As oito famílias de medidor — 40 finais escritos — só entram em cena para quem sobrevive à primeira era.

A ordem *contexto antes de família* existe por um bom motivo: um garoto de 17 anos morrendo não pode receber *"Santo de gesso"*, que é final de ídolo veterano. O erro não é a ordem, é **a era Base ter um final só**.

### Consequência em cadeia
É a causa raiz de metade de P5 e de parte de P3: quando a morte precoce sempre mostra a mesma tela, ela **não ensina nada e não recompensa nada** — o jogador perde e não ganha informação nem coleção.

---

## P2. O teto mata cinco vezes mais que o piso

### Sintoma
Das 638 mortes por medidor nas 2.000 carreiras:

| | Fatia |
|---|---:|
| Morte por **excesso** (medidor em 100) | **87,6%** |
| Morte por **falta** (medidor em 0) | 12,4% |

E não é artefato dos agentes maximizadores. Isolando só os dois que jogam de verdade:

| Agente | Excesso | Falta |
|---|---:|---:|
| Bruno (realista) | 83,3% | 16,7% |
| Viciado (colecionador) | 83,3% | 16,7% |

Detalhe por família, no total:

```
dinheiro_100   30,7%      diretoria_0    4,9%
diretoria_100  29,6%      forma_0        3,1%
torcida_100    17,1%      dinheiro_0     2,4%
forma_100      10,2%      torcida_0      2,0%
```

### Causa
Não é deriva do baralho — ela está medida e neutra (±0,05/carta). É **comportamento de jogador**, e é estrutural:

> Quando um medidor está baixo, existem muitas opções que o levantam, e o jogador as escolhe de bom grado. Quando um medidor está alto, as opções que o baixariam também cobram de outro medidor — e "ter demais" não parece perigo. **O piso é defendido pelo interesse próprio; o teto não é defendido por ninguém.**

### Consequência
Metade do sistema de finais é conteúdo quase morto. **As quatro famílias de piso somam 12,4% das mortes por medidor**, que são 32% das carreiras — ou seja, ~4% de todas as carreiras se dividem entre 20 finais escritos. E os dourados atrás delas (*Deu tudo o que tinha* em FORMA=0, *Quebrado e limpo* em DINHEIRO=0, *O vilão necessário* em TORCIDA=0, *Saiu pela porta da frente* em DIRETORIA=0) ficam praticamente inalcançáveis por consequência aritmética, não por dificuldade de escolha.

O pilar do jogo é *"chegar a zero mata, chegar a cem também"*. Hoje a segunda metade da frase é 5× mais verdadeira que a primeira.

---

## P3. Uma estratégia consistente morre antes de entender o jogo

### Sintoma
| Agente | Decisões | Tempo | Finais distintos em 200 carreiras |
|---|---:|---:|---:|
| Gabigol (só torcida) | 7 | 0,8 min | **2** |
| CR7 (só forma) | 7 | 0,8 min | **1** |
| Diego Ribas (só diretoria) | 14 | 1,8 min | 7 |
| Elon Musk (só dinheiro) | 18 | 2,3 min | 9 |

98% a 100% dessas carreiras acabam na era Base, nas duas baterias. **É regra, não variância.**

### Causa
Aritmética simples: o medidor começa em **50**, a faixa de legado move até **~40** num único medidor, e a de importante até ~25. **Três escolhas alinhadas fecham os 50 pontos que faltam para o teto.** Como o jogo não tem nenhuma resistência perto das bordas — testamos e removemos, por bons motivos —, qualquer coerência de estratégia é letal.

E "escolher o que a torcida quer" é o instinto mais natural que um jogador novo tem.

### O que isso não é
Não é "o jogo está difícil demais". O agente realista faz 73 decisões e vê 52 finais. O problema é específico: **o jogo pune coerência mais do que pune erro**, e pune antes de ensinar.

---

## P4. Um terço do baralho existe para um quarto das carreiras

### Sintoma
- **31 de 433 cartas (7%) não apareceram uma única vez** em 2.000 carreiras — e são **as mesmas 31 nas duas baterias**, o que descarta azar de amostra.
- **15 de 77 finais** nunca alcançados.
- **9 de 25 títulos** nunca conquistados.

Quem chega em cada era, pelo agente realista: base 100% · estouro 90% · travessia 63% · auge 44% · **declínio 35% · legado 27%**.

O conteúdo morto tem endereço: batidas 2 e 3 de fio no declínio e no legado, o **arco inteiro da companheira** (`companheira_carreira_01/02`, `companheira_distancia_01/02`, `companheira_ruptura`, `companheira_pedagio`) e os títulos tardios (O Padrinho, O Pai, O Professor, O Sobrevivente, O de Casa).

### Causa
Não é bug: é a consequência direta e esperada da rodada de dificuldade. A carreira mediana morre aos 23 anos. Isso foi uma **escolha sua** — 8 a 12 minutos, várias carreiras por sessão — e o preço dela é este.

### A pergunta que isso levanta
Não é "como consertar", é **"o conteúdo tardio é recompensa de quem joga bem, ou é conteúdo desperdiçado?"** As duas respostas são defensáveis e levam a soluções opostas.

---

## P5. Concentração de finais

**15 finais respondem por 80% de todas as carreiras**, de 77 disponíveis. Retirando o efeito de P1, a distribuição do resto é razoavelmente saudável: 26 finais de família distintos apareceram. Este problema é **derivado** — não tem solução própria, e deve ser re-medido depois de P1, P2 e P4, não antes.

---

## P6. O teto de idade cria um pico artificial

Distribuição das 200 carreiras do agente realista:

```
  0- 15 decisões   17  ########
 15- 30            34  #################
 30- 50            31  ###############
 50- 80            26  #############
 80-110            26  #############
110-132            26  #############
132+               40  ####################   ← o teto de idade
```

**Correção de uma coisa que eu disse errado na entrega anterior:** chamei essa distribuição de "quase bimodal". Olhando o histograma, ela não é — é razoavelmente plana com **um pico no limite de idade**. O que balançava a mediana entre baterias era esse pico somado à massa plana no meio, não dois montes. A distribuição está melhor do que eu descrevi; o pico é que é artificial.

20% das carreiras param no mesmo lugar porque o calendário diz, não porque algo aconteceu.

---

# Parte II — Manual de soluções

Cada solução tem: o que fazer, o que custa, **o que medir para saber se funcionou**, e o risco.

## Para P1 — o final único da era Base

### S1.1 · Uma família de finais precoces ⭐ recomendada
Criar um bloco `familias_precoces` com **8 finais** (um por medidor × extremo), válido nas eras Base e Estouro, consultado **antes** do contexto quando a morte é por medidor e a era é inicial.

- **Custo:** 8 finais escritos + ~15 linhas em `resolverFinal`.
- **Efeito esperado:** os 44,5% de hoje se espalham por 8 finais; nenhum passa de ~10%.
- **Medir:** `finais mais frequentes` — nenhum acima de 12%; finais distintos vistos sobe de 62 para ~70.
- **Risco:** baixo. Os textos precisam ser de morte precoce (17–21 anos), não de veterano — é exatamente por isso que o contexto vinha primeiro.

### S1.2 · Estreitar a condição do final de contexto
Trocar `{"era": ["base"]}` por algo como `{"era": ["base"], "rodada": {"max": 8}}`, para que só as mortes **muito** precoces peguem esse final e o resto caia na família.

- **Custo:** uma linha de JSON + suporte a `rodada` em `bate()`.
- **Efeito:** derruba os 44,5% para talvez 15%, mas o resto vai para famílias com texto de veterano — **cria o problema que o contexto existia para evitar**.
- **Veredito:** só serve **combinada** com S1.1. Sozinha, troca um defeito por outro.

### S1.3 · Inverter a ordem de resolução
Família primeiro, contexto como fallback. **Não recomendo:** devolve *"Santo de gesso"* para um garoto de 17 anos. A ordem atual está certa.

---

## Para P2 — o teto matando 5× mais que o piso

Estas soluções mexem no coração do jogo. Recomendo aplicar **uma por vez** e medir entre elas.

### S2.1 · Sangria de fim de temporada no medidor mais alto ⭐ recomendada
Toda virada de temporada, o medidor mais alto perde `X` pontos (sugestão: 4 a 6, ou 8% do valor). Justificativa temática: fama esfria, dinheiro se gasta, diretoria troca, corpo cansa.

- **Custo:** 3 linhas em `viraTemporada`.
- **Efeito esperado:** teto puxado para baixo continuamente → mortes por excesso caem, e o piso passa a ser alcançável porque o jogador gasta cartas defendendo o topo.
- **Medir:** proporção excesso/falta — alvo entre **60/40 e 70/30**. E a duração mediana, que vai **subir** (menos mortes por teto) — provavelmente precisa de compensação na escala.
- **Risco:** médio. Pode achatar tudo em direção ao meio e alongar carreira. É por isso que se mede a proporção *e* a duração.

### S2.2 · O mundo para de ajudar quem está no chão ⭐ recomendada junto com S2.1
Quando um medidor está abaixo de ~20, **reduzir o peso de sorteio das cartas que o levantam**. Hoje o jogador sempre acha resgate; é isso que defende o piso.

- **Custo:** um modificador de peso em `proxima()`, ~8 linhas.
- **Efeito:** o piso passa a ser um risco real. É a metade que falta de S2.1 — S2.1 empurra o topo para baixo, S2.2 impede o resgate embaixo.
- **Medir:** mesma proporção excesso/falta. As duas juntas devem chegar mais perto de 55/45 do que qualquer uma sozinha.
- **Risco:** médio-alto. Pode virar espiral da morte: caiu, não levanta, morre. Mitigação: aplicar o desconto de peso só até 50%, nunca zerar.

### S2.3 · Cartas de pressão de topo
Quando um medidor passa de 85, entram cartas específicas cujas duas opções mexem naquele medidor — uma sobe mais, a outra derruba com custo alto. O `refém do ídolo` que já existe como conceito de final passa a existir como pressão de jogo.

- **Custo:** alto — 8 a 16 cartas novas (uma ou duas por medidor × extremo).
- **Efeito:** transforma "estar no topo" de estado passivo em situação jogável. É a solução mais interessante e a mais cara.
- **Medir:** quantas carreiras passam de 85 e sobrevivem; hoje passar de 85 é quase sentença.

### S2.4 · Não mexer, e aceitar que o jogo é sobre excesso
Reescrever o pilar: *"o excesso mata; a falta te deixa jogar mal"*. Aposentar as 4 famílias de piso ou reduzi-las a 2 finais cada.

- **Custo:** zero de código, alto de conteúdo jogado fora (20 finais escritos).
- **Quando faz sentido:** se você achar que "morrer de excesso" é o tema do jogo e "morrer de falta" nunca foi interessante. É uma escolha legítima, e é honesto colocá-la na mesa.

---

## Para P3 — monomania matando em 7 decisões

### S3.1 · Teto de magnitude na era Base ⭐ recomendada
Nenhuma carta elegível na Base move mais de ~20 num único medidor. Hoje a Base tem cartas de 40 (`fisio_base_01` move FORMA em 40).

- **Custo:** baixo. Uma regra no validador + reescalar as ~10 cartas de legado da Base.
- **Efeito:** dobra o número de decisões necessárias para estourar um medidor na primeira era — de 3 para 6 ou 7.
- **Medir:** Gabigol e CR7 saindo de 7 decisões para 15–20, e passando a ver mais de 1 final.
- **Risco:** baixo, e localizado. Não toca em nada depois da Base.

### S3.2 · Rendimento decrescente perto do teto, só no ganho
Um `+40` em TORCIDA com ela em 85 entra como `+15`; a perda continua inteira. Fórmula sugerida: `ganho × (1 − (valor−70)/45)` acima de 70.

- **Custo:** 4 linhas em `aplicar()`.
- **Efeito:** mata a morte-por-três-cliques e **ajuda P2 de graça**, porque reduz justamente as mortes por excesso, que são 83%.
- **Medir:** proporção excesso/falta e duração mediana.
- **Diferença importante do que já testamos e descartamos:** o amortecimento anterior valia **nos dois sentidos e nos dois extremos** — apagou as mortes por medidor inteiras e com elas 40 finais. Este vale **só no ganho e só perto do teto**. É outra coisa.
- **Risco:** médio. Se combinado com S2.1, pode zerar as mortes por excesso. **Não aplicar as duas na mesma rodada.**

### S3.3 · Pool de abertura
As primeiras 6 a 8 cartas de toda carreira saem de um subconjunto de magnitude `padrao` apenas.

- **Custo:** baixo, ~10 linhas.
- **Efeito:** garante que ninguém morra antes da oitava carta.
- **Risco:** é onboarding disfarçado; pode tirar a tensão da primeira era, que hoje é boa.

---

## Para P4 — conteúdo tardio inalcançável

A escolha de projeto vem primeiro. As soluções mudam conforme a resposta.

### Se o conteúdo tardio é **recompensa**:

**S4.1 · A reencarnação leva mais longe** ⭐ a mais interessante
Cada vida completada dá um bônus estrutural: vida 2 começa aos 19, vida 3 começa com um medidor em 60, vida 4 abre uma era. Hoje a reencarnação só dá a marca de alma.
- **Custo:** médio. Mexe em `novoJogo` e nas marcas.
- **Efeito:** o jogador chega ao Legado *porque persistiu*, não *porque teve sorte*. Dá função ao meta-jogo, que hoje é decorativo.
- **Medir:** % de carreiras da vida 3+ que chegam ao Legado — alvo acima de 50%.

### Se é **conteúdo desperdiçado**:

**S4.2 · Portas mais cedo**
Adicionar `auge` à lista de eras das batidas de fio que hoje são só `declinio`/`legado`, e adiantar 2 ou 3 títulos tardios.
- **Custo:** baixo, é edição de JSON.
- **Efeito:** as 31 cartas mortas viram ~10.
- **Risco:** algumas cartas não fazem sentido no auge (o sucessor de 18 anos, o filho de 9). Cerca de metade não é realocável.

**S4.3 · Encurtar as eras iniciais**
Base de 3 para 2 temporadas, estouro de 4 para 3. Chega-se à travessia mais cedo com a mesma duração total.
- **Custo:** baixo.
- **Efeito:** era reach sobe em todas as eras tardias.
- **Risco:** a Base fica apertada — hoje ela tem 46 cartas elegíveis para 16–20 de consumo.

**S4.4 · Aceitar e arquivar**
Mover as 31 cartas e os 9 títulos para um arquivo `v2/`, parar de pagar manutenção e validação por eles.
- **Custo:** zero. É a única opção que *reduz* trabalho.
- **Quando faz sentido:** se você preferir 400 cartas que todo mundo vê a 433 em que 31 são decoração.

---

## Para P6 — o pico no teto de idade

### S6.1 · Aposentadoria distribuída ⭐ recomendada
Em vez de encerrar em `idade >= 36`, dar a partir dos 33 uma chance crescente de a temporada ser a última: 15% aos 33, 35% aos 34, 60% aos 35, 100% aos 36.

- **Custo:** 4 linhas em `viraTemporada`.
- **Efeito:** o pico de 20% se espalha em quatro anos.
- **Medir:** o histograma de duração — nenhuma faixa acima de ~15%.
- **Bônus:** a aposentadoria passa a ser surpresa em vez de calendário, o que combina com o tom do jogo.

---

# Parte III — Como usar este manual

## Ordem recomendada

| Rodada | O que | Por que nesta ordem |
|---|---|---|
| **1** | S1.1 (família de finais precoces) | Barata, isolada, resolve o problema mais grave sem tocar em mecânica |
| **2** | S3.1 (teto de magnitude na Base) | Barata e local; muda o número de decisões da monomania sem mexer no resto |
| **3** | **Decidir P4** — recompensa ou desperdício | É escolha de projeto, não de número; tudo depois depende dela |
| **4** | S2.1 **ou** S3.2, nunca as duas juntas | Ambas puxam o teto; juntas podem zerar as mortes por excesso |
| **5** | S2.2, se a proporção ainda não chegou perto de 60/40 | Só faz sentido depois de medir o efeito de 4 |
| **6** | S6.1 (aposentadoria distribuída) | Cosmética de distribuição; deixar para o fim |

**Regra que valeu para tudo até agora e deve continuar valendo: uma alavanca por rodada, medida antes da seguinte.** Metade das descobertas deste projeto veio de uma mudança ter feito o contrário do esperado.

## O que NÃO fazer — já testado e descartado

| Ideia | O que aconteceu quando testamos |
|---|---|
| **Amortecimento simétrico** perto dos dois extremos | Com fator 0,72, as mortes por medidor foram a **0%** e 40 dos 57 finais ficaram inalcançáveis. Não comprou duração nenhuma. |
| **Antecipar o decaimento por idade** (30 → 28 anos) | **Alongou** a carreira: 84 → 91 decisões, e o teto de idade subiu de 26,6% para 31%. Pressão que o jogador consegue responder vira gradiente e o faz corrigir para o meio. |
| **Mexer no fator de escala global** | Já calibrado em cinco medições (1,00 → 133 decisões · 1,45 → 84 · 1,67 → 46 · 1,49 → 68 · **1,344 → 60**). Mexer nele reabre todo o balanceamento; use como último recurso, para compensar, nunca como conserto. |
| **Baixar o peso das cartas de morte abaixo de 4** | Com peso 9 elas causavam 43% das carreiras; abaixo de 4, as 24 desaparecem da experiência. 4 é o ponto onde todas aparecem em 500 carreiras e a fatia fica em 32%. |
| **Teto de idade mais cedo** (37 → 34) | Desloca o pico em vez de espalhá-lo. É S6.1 que resolve. |

## Como medir qualquer uma delas

As ferramentas estão prontas e versionadas:

```
node /tmp/personas.js <semente> <saida.json>    # 10 personalidades × 100 carreiras
python3 /tmp/relatorio.py                       # relatório completo
python3 /tmp/comparar.py                        # replicação entre duas baterias
```

O RNG do jogo é semeado; `window.__craque.semente(n)` troca a semente. **Rodar duas baterias com sementes diferentes é obrigatório** — a mediana do agente realista variou 54 → 82 entre duas amostras de 100.

### Os seis números que dizem se o jogo está balanceado

| Medida | Hoje | Alvo |
|---|---:|---|
| Duração mediana (agente realista) | 73 decisões · 9,6 min | 8 a 12 min |
| Final mais frequente | **44,5%** | abaixo de 12% |
| Mortes por medidor: excesso / falta | **83 / 17** | entre 70/30 e 55/45 |
| Decisões até a morte por monomania | **7** | acima de 15 |
| Cartas nunca vistas em 2.000 carreiras | **31 de 433** | abaixo de 10 |
| Faixa mais cheia do histograma de duração | **20%** (o teto de idade) | abaixo de 15% |
