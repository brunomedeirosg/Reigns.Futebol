# CRAQUE — como chegar nos oito dourados

**Documento interno, só para o Bruno.** Isto é gabarito: derivado de `finais.json` e das 409 cartas, não de memória. Se você quiser descobrir jogando, pare de ler aqui.

---

## 0. As três coisas que todo dourado exige

### 0.1 Você precisa morrer no extremo — não de velhice

Cada dourado pertence a uma **família de morte por medidor**. Só existem oito famílias, uma por extremo:

| Família | Morte | Dourado |
|---|---|---|
| O corpo cobrou | FORMA = 0 | Deu tudo o que tinha |
| Passou do ponto | FORMA = 100 | O corpo que virou método |
| Viraram | TORCIDA = 0 | O vilão necessário |
| Não é mais seu | TORCIDA = 100 | O nome do estádio |
| Fora dos planos | DIRETORIA = 0 | Saiu pela porta da frente |
| Deixou de ser gente | DIRETORIA = 100 | De olhos abertos |
| Acabou | DINHEIRO = 0 | Quebrado e limpo |
| A ganância | DINHEIRO = 100 | O clube que você comprou |

Se você chegar aos **36 anos vivo**, a carreira encerra em `fim_natural` e nenhum dourado é possível. **Chegar inteiro ao fim é a derrota, do ponto de vista do dourado.**

**Atualização da rodada de dificuldade (11/08):** isto ficou muito melhor. Antes, só 19% das carreiras morriam por medidor — as famílias douradas eram quase inalcançáveis por construção, e eu tinha registrado isso como problema estrutural em aberto. Depois de escalar os deltas por 1,49 e reequilibrar as mortes súbitas, **47% das carreiras morrem por medidor** e apenas 14% batem o teto de idade. Medido: o jogador neutro chega a dourado em 1,0% das carreiras (3 dos 8 aparecem) e o jogador que persegue redenção em **5,3%**. Antes eram 0,8% e 3,8%, com 1 e 2 dos 8. A dificuldade maior **abriu** os dourados em vez de fechar.

O jeito prático: monte a carreira inteira acumulando as flags e o medidor de apoio, e **derrube o medidor-alvo de propósito nas últimas temporadas**, com as cartas de legado, que agora movem **46 a 67 pontos por escolha** — mais de metade de uma barra.

### 0.1b A carreira agora é curta — planeje desde a base

Mediana de **68 decisões (9 min)**, e as eras finais são raras: 61% das carreiras chegam à travessia, 47% ao auge, **32% ao declínio, 23% ao legado**. Todo dourado que exige flag de declínio ou legado (`padrinho_do_kaique`, `curso_de_treinador`, `escolheu_o_filho`) exige antes de tudo **sobreviver até lá**, e sobreviver é a parte difícil. Nenhuma corrida de dourado se decide na era 5: se decide se você chega na era 5.

### 0.2 Títulos são o gargalo real

Dois dourados exigem títulos (3 e 4). O motor dá título no fim de temporada com:

```
FORMA > 62  E  DIRETORIA > 48  →  26% de chance naquele ano
```

Ou seja: **cada título custa cerca de 4 temporadas segurando FORMA acima de 62 e DIRETORIA acima de 48 ao mesmo tempo.** Três títulos ≈ 11 temporadas nessas condições. É a parte mais longa de qualquer corrida de dourado, e tem que ser feita cedo, porque FORMA decai a partir dos 30.

### 0.3 As marcas de escândalo são orçamento, não tempero

Cinco marcas bloqueiam `sem_escandalo`, que um dourado exige diretamente:

`investigacao_apostas` · `laranja` · `deve_pro_valdir` · `fundo_comprou_direitos` · `patrocinio_apostas`

Todas têm como ser desfeitas — mas só na **terceira batida de um fio**, e sempre com um custo alto no medidor que você menos quer perder. Não conte com a limpeza: é mais barato nunca sujar.

---

## 1. Deu tudo o que tinha — FORMA = 0

> "Você cuidou do corpo a vida inteira e ele acabou mesmo assim."

**Exige:** `joelho_tratado` · 3+ títulos · era declínio ou legado · TORCIDA ≥ 65 no fim.

**Roteiro**

1. **Base, primeira carta do fisioterapeuta** (`fisio_base_01`): escolha **"Paro agora"**. Você perde a peneira e ganha `joelho_tratado`. É a escolha certa desta corrida e a errada de quase todas as outras.
2. Segure FORMA acima de 62 e DIRETORIA acima de 48 da era Estouro até o Auge. É aqui que os 3 títulos aparecem — precisa de ~11 temporadas nessas condições, então **não pode desperdiçar ano nenhum**.
3. Suba TORCIDA em paralelo e não deixe cair abaixo de 65 depois dos 30.
4. **A partir dos 30 anos, pare de defender a FORMA.** O decaimento por idade já tira 5, depois 8, depois 12 por temporada. Some a isso as opções de legado que trocam FORMA por TORCIDA — "Quero o que era" no `fio_joelho_b3aa`, "Jogo assim mesmo" no `fio_joelho_b3ab` — e a queda vira despenque.

**Não faça:** nunca aceite infiltração. `infiltracao_cronica` não bloqueia este dourado, mas as cartas que a dão costumam também dar `joelho_ignorado`, e aí o `joelho_tratado` está lá mas você vai cair numa das três variantes cinza da família.

**Onde `joelho_tratado` aparece** (15 opções, nenhuma desfaz): `fisio_base_01` "Paro agora" · `fisio_estouro_01` "Cumpro as três" · `capitao_duda_02` "Corto o treino extra" · `fio_peneira_b2` "Sigo o cardápio dela" · `fio_peneira_b3b` "Internação" · as quatro batidas 3 do fio do joelho · `fio_cicatriz_b2a` "Paro o treino extra" · `fio_cicatriz_b2b` "Ligo pra ele" · `fio_cicatriz_b3aa` "Aprendi a dosar" · `fio_cicatriz_b3ab` "Faço o que ela diz" · `fio_cicatriz_b3ba` "Digo que não" · `fio_cicatriz_b3bb` "Entro com ele".

---

## 2. O corpo que virou método — FORMA = 100

> Morrer de excesso de forma, virado professor.

**Exige:** `joelho_tratado` · `padrinho_do_kaique` · idade ≥ 32 · DIRETORIA entre 40 e 70 no fim.

Este é o **mais fácil dos oito**, e a razão é a janela de DIRETORIA: 40 a 70 é largura enorme. É o dourado para tentar primeiro.

**Roteiro**

1. `joelho_tratado` cedo, igual ao anterior — "Paro agora" na base.
2. **Chegue ao declínio vivo com 32 anos.** Não force nada até lá.
3. No declínio, pegue `padrinho_do_kaique`: `sucessor_declinio_01` **"Ensino tudo"** é a porta mais direta, e ela também abre o fio do sucessor, que dá mais quatro chances da mesma flag.
4. Agora empurre FORMA para cima e deixe DIRETORIA parada no meio. As opções de legado que dão FORMA alta com custo em TORCIDA são as suas: "Aprendi a dosar" (`fio_cicatriz_b3aa`), "Saio agora" (`fio_joelho_b3ab`), "Jogo de cabeça" (`fio_joelho_b3aa`).

**Cuidado com a DIRETORIA:** o teto de 70 é tão fatal quanto o piso de 40. Se você está com diretoria alta, escolha de propósito as opções que a derrubam — elas estão em todo canto, porque quase toda escolha de torcida cobra diretoria.

---

## 3. O vilão necessário — TORCIDA = 0

> A torcida virou e você tem duas taças e a diretoria na mão.

**Exige:** `tomou_posicao` · `rompeu_apostas` · 2+ títulos · DIRETORIA ≥ 60 no fim.

**A armadilha:** `rompeu_apostas` só existe se você **entrou** no patrocínio antes. Você precisa se sujar de propósito e sair depois.

**Roteiro**

1. **Estouro:** `apostas_estouro_01` → **"Fecho"**. Pega `patrocinio_apostas`.
2. Aguente os anos de dinheiro fácil segurando FORMA > 62 e DIRETORIA > 48 até sair com 2 títulos.
3. **Auge ou declínio, rompa:** `apostas_auge_01` "Saio do contrato" · `apostas_declinio_01` "Rompo hoje" · `fio_apostas_b3aa` "Mudei de ideia" · `fio_aptarde_b2b` "Pago a multa" · `fio_aptarde_b3aa` "Vou explicar no muro" · `fio_aptarde_b3bb` "Falo no documentário" · `fio_helicoptero_b3b` "Corto os patrocínios". As três últimas também limpam `investigacao_apostas`.
4. `tomou_posicao` é a flag mais abundante do jogo (34 opções). A mais precoce é `fio_apito_b2` **"Reclamo do errado"**, no estouro — que exige ter sobrevivido à carta do árbitro no sub-20 escolhendo "Xingo o chão".
5. **Derrube TORCIDA no fim mantendo DIRETORIA acima de 60.** É a combinação mais antinatural do jogo, porque quase toda carta troca uma pela outra — e é justamente por isso que este final é o mais coerente com o próprio nome.

---

## 4. O nome do estádio — TORCIDA = 100

> Ídolo absoluto de um clube só.

**Exige:** `escolheu_o_filho` · **4+ títulos** · **`transferencias` = 0** · FORMA ≥ 50 no fim.

**Este é o mais difícil dos oito, e agora ficou mais interessante:** com a janela de transferências no jogo, `transferencias = 0` significa **recusar todas as propostas da carreira**. Em média são 2,6 janelas por carreira; você tem que dizer "Fico onde estou" em todas.

E aí vem o problema real: recusar transferência te mantém no patamar baixo, e ficar no acesso ou na segunda divisão **não te impede de ganhar título** (o motor só olha FORMA e DIRETORIA), mas te dá menos margem. É um dourado de jogador de um clube só, e o jogo agora cobra literalmente isso.

**Roteiro**

1. **Recuse toda proposta.** "Fico onde estou" (subida) e "Cumpro contrato aqui" (descida). Qualquer aceite mata a corrida na hora.
2. Segure FORMA > 62 e DIRETORIA > 48 pelo maior número de temporadas possível — 4 títulos custa ~15 temporadas nessas condições. Comece a mirar isso na era Estouro.
3. **Declínio:** `filho_declinio_01` → **"Não jogo sábado"**. Ou qualquer uma das outras 8: `filho_legado_02` "Fico o ano inteiro" · `imprensa_declinio_01` "Digo a verdade" · `fio_aniversario_b2b` "Vou de perto" · as três batidas 3 do fio do aniversário · `fio_selecao_b3b` "Conto o que aconteceu" · `fio_heranca_b3ba` "Escrevi pra ele".
4. **Estoure a TORCIDA no fim, com FORMA ainda em 50 ou mais.** Não deixe a idade comer a forma antes: o alvo é morrer de amor por volta dos 33 ou 34, não aos 36.

---

## 5. Saiu pela porta da frente — DIRETORIA = 0

> Brigado com o clube, rico e amado.

**Exige:** `recusou_apostas` · **qualquer um de** `rompeu_valdir` / `processou_valdir` / `quitou_valdir` · DINHEIRO ≥ 60 · TORCIDA ≥ 60.

Sem exigência de título. **É o segundo mais fácil.**

**Roteiro**

1. **Estouro:** `apostas_estouro_01` → **"Não é pra mim"**. Pronto, `recusou_apostas`.
2. Escolha um caminho contra o empresário. O mais barato e mais cedo é `valdir_estouro_02` → **"Pago tudo hoje"** (`quitou_valdir`), que é a única fonte dessa flag no jogo inteiro. Alternativas mais tardias: `valdir_auge_03` "Acabou", `valdir_auge_02` "Vou ao advogado", ou qualquer batida do fio do empresário e do fio da procuração.
3. Suba DINHEIRO e TORCIDA juntos — o que é raro, porque as cartas costumam opô-los. Os fios ajudam: as batidas 3 que dão torcida alta com custo em diretoria são exatamente o que você quer.
4. **Afunde a DIRETORIA de propósito no fim.** Fácil: "Não assino isso" (`fio_microfone_b3aa`, −20), "Não entro na foto" (`fio_apostas_b3ab`, −20), "A ideia foi minha" (`fio_joelho_b3ba`, −18), "Anota essa também" (`fio_aniversario_b3aa`, −18).

---

## 6. De olhos abertos — DIRETORIA = 100

> Virou dirigente sem deixar de ser gente.

**Exige:** `curso_de_treinador` · `padrinho_do_kaique` · **era legado** · TORCIDA ≥ 55 no fim.

Sem exigência de título. Exige chegar vivo aos 33 anos, o que é a parte simples.

**Roteiro**

1. **Declínio:** `treinador_declinio_04` → **"Me inscrevo"** (`curso_de_treinador`). Isso abre o fio da licença, cujas quatro batidas 3 dão a flag de novo e mais `padrinho_do_kaique` de brinde.
2. **Declínio:** `sucessor_declinio_01` → **"Ensino tudo"** (`padrinho_do_kaique`).
3. **Legado:** `fio_licenca_b3aa` **"Fico na base"** dá as duas flags de uma vez. `fio_heranca_b3aa` "Aceito o programa" também.
4. Empurre DIRETORIA ao teto mantendo TORCIDA acima de 55. As opções de "aceito o cargo / assino / vou ao evento" são todas de diretoria alta.

---

## 7. Quebrado e limpo — DINHEIRO = 0

> Sem um centavo, sem uma mancha, com a torcida inteira do lado.

**Exige:** `recusou_apostas` · **qualquer um de** `processou_valdir` / `rompeu_valdir` / `quitou_valdir` / `recusou_fundo` · TORCIDA ≥ 70 · era auge, declínio ou legado.

Mesma espinha do nº 5, com o grupo "qualquer" mais largo (inclui `recusou_fundo`) e sem exigência de dinheiro alto — óbvio, você vai morrer com zero.

**Este é o que o agente de redenção mais alcança nas simulações (3,3% das carreiras).** É o dourado mais acessível na prática.

**Roteiro**

1. `apostas_estouro_01` → **"Não é pra mim"**.
2. `valdir_estouro_04` → **"Não vendo pedaço meu"** (`recusou_fundo`) — mais cedo e mais barato que processar. Ou `diretor_auge_02` "Só o clube, não eu".
3. Passe a carreira **gastando**: toda opção com dinheiro negativo é sua amiga. "Pago a multa", "Pago sem perguntar", "Eu banco", "Fico na base", "Rasgo na frente dele".
4. Suba TORCIDA acima de 70 e zere o DINHEIRO depois do auge.

---

## 8. O clube que você comprou — DINHEIRO = 100

> Ficou rico até morrer, e ficou limpo.

**Exige:** `recusou_apostas` · `padrinho_do_kaique` · **`sem_escandalo`** · TORCIDA ≥ 60.

`sem_escandalo` é derivada: significa **nenhuma** de `investigacao_apostas`, `laranja`, `deve_pro_valdir`, `fundo_comprou_direitos`, `patrocinio_apostas` ativa no fim.

**A tensão que faz este final:** enriquecer sem tocar em nada sujo. As cinco marcas proibidas estão exatamente em cima das opções que dão mais dinheiro no jogo.

**Roteiro**

1. `apostas_estouro_01` → **"Não é pra mim"**. E recuse de novo em `apostas_travessia_01`, `apostas_auge_02`, `apostas_declinio_02` — o arco insiste.
2. `valdir_estouro_04` → **"Não vendo pedaço meu"**, e nunca aceite fundo depois.
3. Declínio: `sucessor_declinio_01` → **"Ensino tudo"**.
4. Enriqueça com o que é limpo: prêmio de título, transferência para cima (a janela!), "Assino e viajo", "Deixo a piada", "Trabalho fora de campo" — cuidado que essa última dá `turne_de_patrocinio`, que é feio mas **não** está na lista das cinco.
5. Se sujar sem querer, ainda dá: as sete opções que desfazem `patrocinio_apostas` e as nove que desfazem `laranja` estão listadas no fim deste documento.

---

## 9. Tabela-resumo

| # | Dourado | Morte | Flags | Títulos | Dificuldade |
|---|---|---|---|---:|---|
| 2 | O corpo que virou método | FORMA 100 | joelho_tratado + padrinho | 0 | ★★ |
| 5 | Saiu pela porta da frente | DIRETORIA 0 | recusou_apostas + 1 de 3 | 0 | ★★ |
| 7 | Quebrado e limpo | DINHEIRO 0 | recusou_apostas + 1 de 4 | 0 | ★★ |
| 6 | De olhos abertos | DIRETORIA 100 | curso + padrinho | 0 | ★★★ |
| 8 | O clube que você comprou | DINHEIRO 100 | recusou + padrinho + limpo | 0 | ★★★★ |
| 1 | Deu tudo o que tinha | FORMA 0 | joelho_tratado | 3 | ★★★★ |
| 3 | O vilão necessário | TORCIDA 0 | tomou_posicao + rompeu_apostas | 2 | ★★★★ |
| 4 | O nome do estádio | TORCIDA 100 | escolheu_o_filho + zero transferências | 4 | ★★★★★ |

---

## 10. As duas escolhas que decidem mais coisa que qualquer outra

**`fisio_base_01`, primeira era, "Paro agora".** Custa a peneira e abre dois dos oito dourados. Nenhuma carta no jogo desfaz `joelho_tratado`, então é uma decisão que você toma aos 17 anos e cobra aos 33.

**`apostas_estouro_01`, "Não é pra mim".** Abre três dos oito. Recusar é a escolha mais lucrativa do jogo a longo prazo e a mais pobre a curto — que é exatamente a piada do arco.

---

## 10b. As 24 mortes súbitas, por era

Nenhuma delas dá dourado — todas dão moldura preta. Estão aqui porque **32% das carreiras acabam numa delas**, e conhecê-las é metade de sobreviver até o declínio. O padrão é sempre o mesmo: a opção fatal é a que soa mais divertida, e o aviso está no texto.

| Era | Cartas | O que te mata ali |
|---|---|---|
| Base | van, pelada, peneira, apito | ser moleque |
| Estouro | moto, bicicleta no estúdio, tatuagem, carro novo | ser novo-rico |
| Travessia | frio, visto vencido, procuração, live de 3h | ser estrangeiro |
| Auge | jet ski, helicóptero, VAR, áudio da seleção, live | ser importante |
| Declínio | terceira infiltração, cápsula, despedida marcada, aposta de duzentos | ser teimoso |
| Legado | jogo de veterano, últimos quinze minutos, carregado no colo, chuteira da estreia | ser saudoso |

Seis delas têm `chance` menor que 1 — dá para sobreviver, e sobreviver abre um fio de três peças. As outras dezoito são certas.

---

## 11. Anexo: onde desfazer cada marca de escândalo

| Marca | Opções que desfazem |
|---|---|
| `patrocinio_apostas` | "Corto os patrocínios" · "Mudei de ideia" · "Não entro na foto" · "Vou explicar no muro" · "Não assino silêncio" · "Digo o valor exato" · "Falo no documentário" |
| `laranja` | "Levo ao delegado" · "Chamo o advogado dela" · "Quero com papel" · "Entrego o que sei" · "Vou ao evento" · "Não sou exemplo" · "Falo com o contador" · "Ocupo o espaço" · "Contesto linha a linha" |
| `deve_pro_valdir` | "Levo ao delegado" · "Quero com papel" · "Vou ao evento" · "Ocupo o espaço" · "Contesto linha a linha" · "Termino a lista" |
| `investigacao_apostas` | "Assumo as vinte e duas" · "Corto os patrocínios" · "Assumo que sabia" · "Vou explicar no muro" · "Não assino silêncio" · "Falo no documentário" |
| `fundo_comprou_direitos` | "Volto pra casa" · "Deixo tocar" · "Rescindo pela metade" |

Todas são **terceiras batidas de fio**: você só recebe a chance de se limpar se tiver aberto o fio dezenas de cartas antes. A redenção existe, mas tem que ter sido contratada com antecedência.
