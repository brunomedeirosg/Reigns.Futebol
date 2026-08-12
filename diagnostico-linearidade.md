# CRAQUE — diagnóstico: linearidade, repetição e o teto do Estouro

Medido em 12/08. **Nada foi aplicado.** Este documento é só o diagnóstico e o cardápio de conserto.

---

## 0. O ponto cego que invalidava parte das medições anteriores

Todas as medições anteriores rodavam **100 carreiras seguidas na mesma página**. `VIDAS` só sobe, nunca zera — então da carreira ~5 em diante eu estava medindo **veterano**, com o bônus de reencarnação (folga maior) ligado. Você jogou 3 campanhas: vidas 1, 2 e 3.

Refiz tudo com **página nova a cada 4 carreiras** (280 carreiras, 70 sessões limpas) e com um agente novo, o **"humano"**: lê a frase e só olha os medidores quando algum está visivelmente perto da borda (<30 ou >70). O agente antigo ("equilibrista") somava `|valor−50|^1.6` dos quatro medidores a cada carta — ninguém joga assim, e era ele que produzia os números otimistas.

| | equilibrista (o de antes) | humano (o novo) |
|---|---:|---:|
| decisões, vida 1 | 73 | 65 |
| chega ao Legado, vida 1 | 25% | 24% |

Os dois concordam. **Sua experiência não é desvio de agente** — é variância mais um problema de leitura, e os dois são explicáveis.

---

## 1. Onde a carreira termina — o número que explica quase tudo

280 carreiras, vidas 1 a 4:

| termina em | Base | Estouro | Travessia | Auge | Declínio | Legado |
|---|---:|---:|---:|---:|---:|---:|
| | 1% | **31%** | 17% | 16% | 9% | **25%** |

A distribuição é **bimodal**: ou você morre no Estouro (dos 19 aos 21 anos, entre a decisão ~15 e a ~35), ou você atravessa e vai até o teto de idade. Quase não existe carreira "média".

E o Legado é a **segunda** faixa mais provável — 25% na vida 1. Em 3 campanhas, a chance de não ver o Legado nenhuma vez é de **43%**. Você não teve azar excepcional; você teve azar normal. Mas 25% ainda é baixo para uma etapa que carrega os finais dourados.

---

## 2. Linearidade: ela existe nos dados e é invisível na tela

Este é o achado principal, e não é um problema de balanceamento.

Por carreira (mediana / média):

- fios **abertos** por decisões suas: **9,7**
- batidas de **retorno** que você chegou a viver: **6,0**
- carreiras que não viram **nenhuma** batida de retorno: **25%**
- decisão em que a **primeira** batida de retorno aparece: **26** (mediana)

Ou seja: em 75% das carreiras o fio *funciona* — a segunda batida chega. **Mas nada na tela diz que aquilo é uma segunda batida.** O eco prometeu "ficou", e 20 a 30 cartas depois chega uma carta que se lê exatamente como qualquer outra: mesmo cargo, mesmo formato, sem nenhuma marca de "isto é a conta daquilo". O jogador precisaria lembrar de uma decisão tomada 26 cartas atrás **e** adivinhar que esta carta é a resposta.

Some-se a isso que **31% das carreiras acabam no Estouro**, ou seja, perto ou antes da decisão 26: um terço dos jogadores morre sem receber conta nenhuma.

**A linearidade não está faltando. Está sem legenda, e chegando tarde demais para um terço das carreiras.**

Sobre os fios curtos (os que vivem e morrem dentro de uma era): média de **2,0 cartas de fio curto por carreira**. Foram escritos 12 fios curtos, 3–4 por era; na prática o jogador encosta em dois. Eles eram justamente a resposta para "o jogador demora demais a perceber que decide" — e estão sub-entregues.

---

## 3. Repetição dentro da mesma campanha: existe, e não é escassez

Você disse que isso nunca deveria acontecer. Concordo. Acontece:

- **40% das carreiras repetem pelo menos uma carta do baralho** (média 0,9 por carreira)
- mais **1,4 repetições de cartas do motor** por carreira (`transferencia_sobe`, `capitao_partida`)

**A causa é a regra, não a falta de carta.** Em `cumpre()`:

```js
if(c.unico && E.historico.includes(c.id)) return false;
const cd=c.cooldown||25, ultimo=E.historico.lastIndexOf(c.id);
if(!c.unico && ultimo>=0 && E.historico.length-ultimo<cd) return false;
```

54 cartas não são `unico`, com cooldown de 25 ou 30. A carreira mediana tem **55 decisões**. Um cooldown de 25 numa carreira de 55 não é uma trava: é uma **licença para repetir uma vez**. E as repetidas se concentram no Estouro e na Travessia, porque são justamente as cartas marcadas com três eras (`estouro/travessia/auge`) — as que ficam elegíveis por mais tempo:

`capitao_estouro_03` · `valdir_estouro_03` · `mae_estouro_03` · `organizada_estouro_02` · `valdir_travessia_04` · `treinador_travessia_03`

**E não há escassez que justifique.** Pool elegível no momento do sorteio:

| era | p10 | p50 |
|---|---:|---:|
| base | 35 | 41 |
| estouro | 40 | 48 |
| travessia | 47 | 55 |
| auge | 72 | 80 |
| declínio | 54 | 60 |
| **legado** | **13** | **25** |

Só o Legado é apertado — e é a era em que você nunca entrou. Em todas as outras há 35 a 80 cartas disponíveis para consumir 7 por temporada. **Proibir repetição na mesma campanha não custa nada.**

---

## 4. Repetição entre campanhas: 29%, e isso é aritmética, não bug

- a Base consome **14 cartas** (2 temporadas × 7)
- a Base tem ~47 cartas utilizáveis
- sobreposição medida entre campanhas consecutivas: **29%**

14 sorteadas de 47, duas vezes, dá 30% de sobreposição esperada. O medido é 29%. **O baralho está se comportando exatamente como sorteio sem memória.**

Isso significa uma coisa importante: **escrever mais cartas de Base é o remédio mais caro e menos eficiente que existe aqui.** Para cair de 29% para 15% seriam necessárias ~100 cartas novas de Base. Para cair para 15% com memória entre carreiras: ~15 linhas de motor.

---

## 5. Encurtar a fase inicial

Concordo em parte, e com uma correção de alvo.

A **Base já é curta**: 14 cartas, dos 17 aos 18. Não é ela que cansa. O que cansa é **Base + Estouro = 35 cartas**, e como 31% das carreiras terminam no Estouro, **a maioria do seu tempo de jogo total foi passada nessas duas eras** — em três campanhas você viu a Base três vezes e o Estouro três vezes, e quase nada além. A sensação de repetição vem daí muito mais do que da taxa real.

Encurtar a Base para **1 temporada (7 cartas)** é barato e eu apoio, mas sozinho resolve pouco: economiza 7 cartas e joga o problema para o Estouro. O que realmente muda a sensação é **atravessar o Estouro com mais frequência**.

---

## 6. Cardápio de conserto

Ordenado por (efeito na sua queixa) ÷ (custo). Nenhum foi aplicado.

### A. Proibir repetição na mesma campanha — *fazer*
`unico` passa a ser o padrão: nenhuma carta aparece duas vezes numa carreira. `cooldown` some. As cartas do motor (`transferencia_sobe`/`desce`, `capitao_partida`) ganham variantes por patamar/era em vez de reaparecerem idênticas.
**Custo:** ~10 linhas de motor + 6 a 8 variantes de carta do motor. **Risco:** só o Legado tem pool apertado (p10 = 13); precisa de um fallback quando o pool secar — hoje o fallback *é* a repetição.

### B. Marcar a batida de retorno na tela — *fazer, é o conserto da linearidade*
Quando a carta que chega é a segunda ou terceira batida de um fio que **você** abriu, ela precisa dizer isso. Três níveis, do mais barato ao mais caro:
1. uma **tarja discreta** no alto da carta com uma frase curta que cita a decisão antiga ("*você prometeu que ia estudar*") — sem número, sem ícone de sistema;
2. a mesma tarja + **moldura diferente** da carta (como a carta de eco já tem);
3. um **eco de abertura** antes da batida de retorno, no formato de carta-texto que já existe, dizendo o que voltou.
**Custo:** (1) é uma linha por fio — 122 fios, mas só ~40 têm segunda batida escrita. **Risco:** baixo; o formato já existe.

### C. Antecipar a primeira batida — *fazer*
Hoje a janela padrão é `em:[20,30]`. Para o **primeiro** fio aberto numa carreira, usar `[6,10]`. O jogador recebe uma conta antes da decisão 15, dentro da Base ou no começo do Estouro, e aprende cedo que o jogo lembra.
**Custo:** 3 linhas em `agendar()`. **Risco:** nenhum; a janela já é parametrizada por fio.

### D. Entregar os fios curtos — *fazer*
Média de 2,0 por carreira contra 12 escritos. Provavelmente é o mesmo tipo de bug de ordenação que matou o arco da companheira: gatilhos que exigem flag que chega depois, ou portas de entrada concentradas em cartas raras. **Precisa de investigação antes de virar tarefa** — não sei ainda se é conteúdo ou motor.
**Custo:** desconhecido até investigar. **Risco:** é o candidato mais provável a "achei um bug de meses".

### E. Memória entre carreiras (o "saco") — *fazer, é barato*
As cartas vistas na carreira anterior entram no sorteio com **peso reduzido** (não zerado — zerar cria previsibilidade inversa). Sobreposição da Base cai de ~29% para ~15% sem escrever uma carta.
**Custo:** ~15 linhas. **Risco:** baixo, desde que seja peso e não proibição.

### F. Baixar a mortalidade do Estouro — *discutir antes*
31% das carreiras morrem lá. Reduzir isso levaria mais gente ao Legado (hoje 25%) e resolveria a queixa "nunca cheguei ao Legado" pela raiz. **Mas foi você que pediu para aumentar a dificuldade**, e o resultado (80 decisões / 10,6 min para o agente realista) ficou dentro da faixa de 8–12 min que você escolheu. Mexer aqui desfaz a rodada anterior.
**Alternativa que não desfaz:** manter a mortalidade e tornar a morte no Estouro **mais informativa** — hoje existem 8 famílias precoces só para a Base; o Estouro não tem equivalente e cai no genérico. Oito finais de Estouro custam pouco e transformam 31% de "morri sem entender" em "morri por causa disso".

### G. Encurtar a Base para 1 temporada — *fazer junto com C, não sozinho*
7 cartas em vez de 14. Só faz sentido combinado com a antecipação da primeira batida (C), senão o jogador só chega mais rápido ao mesmo Estouro.

### H. Escrever mais cartas de Base — *não fazer*
É o instinto natural e é o pior negócio da lista: ~100 cartas novas para o mesmo efeito que E entrega com 15 linhas. Fica para quando A, B, C, D, E estiverem feitos e a repetição *ainda* incomodar.

---

## 7. O que eu faria, na ordem

1. **D** — investigar os fios curtos primeiro, porque pode ser bug e bug muda o resto do diagnóstico
2. **A** — proibir repetição na mesma campanha (com fallback para o Legado)
3. **B** + **C** — marcar a batida de retorno e antecipar a primeira
4. **E** — o saco entre carreiras
5. **G** — Base de 1 temporada
6. **F** — decidir juntos: finais próprios do Estouro (sim) ou baixar a mortalidade (a discutir)

Os itens 2 a 5 são todos motor, medíveis em uma bateria, e nenhum exige escrever carta nova. O item 1 pode virar qualquer coisa.
