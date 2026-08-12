# CRAQUE — Sistema de Finais

**Versão 0.5.** A fonte de dados é `finais.json`; este documento é a versão legível dele. Rodar `python3 ferramentas/validar-finais.py` depois de qualquer mudança.

---

## 1. As duas decisões que moldaram o sistema

**Decisão 1 (Bruno):** morte por dinheiro demais não pode terminar em "ficou rico e parou de jogar", que soa a vitória. As mortes por ganância têm que ser trágicas.

**Decisão 2 (Bruno):** simetria — em vez de a ganância ter sete finais e as outras três, **toda família tem um final dourado de alta dificuldade**, exigindo vários fatores combinados.

O resultado é uma estrutura fixa: **8 famílias × 5 finais**, cada família com

```
1 dourado (3+ fatores combinados)  +  3 condicionais  +  1 genérico sem condição
```

O genérico é obrigatório e é sempre o último — é a rede de segurança. Nunca pode existir uma morte sem final. Somando os 4 finais de contexto, são **44 finais sobre 12 ilustrações**.

### O que isso significa mecanicamente

Um dourado não é "você venceu". É **você chegou ao extremo pelo caminho difícil**. Morrer de FORMA 0 tendo cuidado do corpo a vida inteira e ganhado três títulos é uma morte diferente de morrer de FORMA 0 por ter ignorado uma dor aos dezoito. O medidor é o mesmo; a história não.

Isso transforma cada medidor num eixo com duas mortes ruins e uma boa, e dá ao jogador um alvo em toda direção — não só na do equilíbrio.

---

## 2. Como o motor resolve

```
morte(medidor, extremo)
  → finais de contexto têm prioridade absoluta (era 1, era 6 com equilíbrio, etc.)
  → família = FAMILIAS[medidor][extremo]
  → percorre a família na ordem; o primeiro cujas condições batem é o escolhido
  → o último não tem condição, então sempre bate
```

---

## 3. Os finais dourados, lado a lado

Esta é a tabela que importa. São os onze alvos do jogo.

| Família | Dourado | O que exige |
|---|---|---|
| ⚡ FORMA 0 | **Deu tudo o que tinha** | `joelho_tratado` + 3 títulos + era 5–6 + TORCIDA ≥ 65 |
| ⚡ FORMA 100 | **O corpo que virou método** | `joelho_tratado` + `padrinho_do_kaique` + idade ≥ 32 + DIRETORIA entre 40 e 70 |
| 📣 TORCIDA 0 | **O vilão necessário** | `tomou_posicao` + `rompeu_apostas` + 2 títulos + DIRETORIA ≥ 60 |
| 📣 TORCIDA 100 | **O nome do estádio** | `escolheu_o_filho` + 4 títulos + zero transferências + FORMA ≥ 50 |
| 👔 DIRETORIA 0 | **Saiu pela porta da frente** | `recusou_apostas` + *qualquer* enfrentamento ao empresário + DINHEIRO ≥ 60 + TORCIDA ≥ 60 |
| 👔 DIRETORIA 100 | **De olhos abertos** | `curso_de_treinador` + `padrinho_do_kaique` + era 6 + TORCIDA ≥ 55 |
| 💰 DINHEIRO 0 | **Quebrado e limpo** | `recusou_apostas` + *qualquer* enfrentamento ao empresário + TORCIDA ≥ 70 + era 4–6 |
| 💰 DINHEIRO 100 | **O clube que você comprou** | `recusou_apostas` + `padrinho_do_kaique` + `sem_escandalo` + TORCIDA ≥ 60 |
| *(contexto)* | **Aposentadoria no dia certo** | era 6 + os quatro medidores entre 40 e 70 |
| *(contexto)* | **Camisa 10 de um clube só** | era 6 + zero transferências |
| *(contexto)* | **Estátua** | era 6 + 3 títulos + TORCIDA ≥ 80 |

**O par que eu mais gosto:** *Quebrado e limpo* (DINHEIRO 0) e *O clube que você comprou* (DINHEIRO 100) são espelhos exatos. Um recusou todos os atalhos e ficou sem nada. O outro recusou todos os atalhos e ficou com tudo. A diferença entre os dois é sorte, não caráter — e o jogo diz isso sem falar.

---

## 4. As oito famílias, completas

### ⚡ FORMA 0 — *O corpo cobrou*

| Final | Moldura | Condição |
|---|---|---|
| **Deu tudo o que tinha** | dourada | `joelho_tratado` + 3 títulos + era 5–6 + TORCIDA ≥ 65 |
| Juros do joelho | cinza | `joelho_ignorado` |
| A infiltração número quarenta | preta | `infiltracao_cronica` |
| Aos vinte e quatro | cinza | era 2–3 |
| Sucata | cinza | *(genérico)* |

### ⚡ FORMA 100 — *Passou do ponto*

| Final | Moldura | Condição |
|---|---|---|
| **O corpo que virou método** | dourada | `joelho_tratado` + `padrinho_do_kaique` + idade ≥ 32 + DIRETORIA 40–70 |
| Estourado | preta | `treino_dobrado` |
| A máquina | cinza | DIRETORIA ≥ 70 |
| Insaciável | preta | marca de alma `fome_antiga` |
| À disposição de ninguém | cinza | *(genérico)* |

### 📣 TORCIDA 0 — *Viraram*

| Final | Moldura | Condição |
|---|---|---|
| **O vilão necessário** | dourada | `tomou_posicao` + `rompeu_apostas` + 2 títulos + DIRETORIA ≥ 60 |
| O carro cercado | preta | `encarou_organizada` |
| Mercenário | cinza | 4+ transferências |
| Estrangeiro em casa | cinza | `foi_pro_golfo` |
| Persona non grata | cinza | *(genérico)* |

### 📣 TORCIDA 100 — *Não é mais seu*

| Final | Moldura | Condição |
|---|---|---|
| **O nome do estádio** | dourada | `escolheu_o_filho` + 4 títulos + 0 transferências + FORMA ≥ 50 |
| Refém do ídolo | cinza | `gol_da_final` |
| Santo de gesso | cinza | `tomou_posicao` |
| A estátua antes da hora | cinza | idade ≤ 29 |
| Bandeira | cinza | *(genérico)* |

### 👔 DIRETORIA 0 — *Fora dos planos*

| Final | Moldura | Condição |
|---|---|---|
| **Saiu pela porta da frente** | dourada | `recusou_apostas` + grupo OR + DINHEIRO ≥ 60 + TORCIDA ≥ 60 |
| Encostado | cinza | `atrito_tecnico` |
| A rescisão que você pediu | prata | `escolheu_o_filho` |
| Queimado no mercado | preta | `forcou_saida` |
| Sem clube | cinza | *(genérico)* |

### 👔 DIRETORIA 100 — *Deixou de ser gente*

| Final | Moldura | Condição |
|---|---|---|
| **De olhos abertos** | dourada | `curso_de_treinador` + `padrinho_do_kaique` + era 6 + TORCIDA ≥ 55 |
| Patrimônio do clube | cinza | `contrato_longo` |
| O garoto-propaganda | cinza | `calou` |
| Filho do clube | cinza | marca de alma `filho_do_clube` |
| Institucional | cinza | *(genérico)* |

### 💰 DINHEIRO 0 — *Acabou*

| Final | Moldura | Condição |
|---|---|---|
| **Quebrado e limpo** | dourada | `recusou_apostas` + grupo OR + TORCIDA ≥ 70 + era 4–6 |
| O posto do primo | preta | `deve_pro_valdir` |
| Penhora | preta | `familia_perto` |
| A dívida que não era sua | preta | `laranja` |
| Quebrado | cinza | *(genérico)* |

### 💰 DINHEIRO 100 — *A ganância*

| Final | Moldura | Condição |
|---|---|---|
| **O clube que você comprou** | dourada | `recusou_apostas` + `padrinho_do_kaique` + `sem_escandalo` + TORCIDA ≥ 60 |
| O nome no processo | preta | `investigacao_apostas` |
| Laranja | preta | `laranja` **ou** `fundo_comprou_direitos` |
| A casa caiu | preta | `patrocinio_apostas` **e não** `rompeu_apostas` |
| Rico e aposentado aos trinta | cinza | *(genérico)* |

**O que foi cortado para caber em cinco.** A ganância tinha sete. Para a simetria valer, dois saíram:

- **Ativo controlado** (o fundo que detém 100% de você) — foi **fundido** com *Laranja*, que agora aceita `laranja` **ou** `fundo_comprou_direitos`. Nada se perdeu, só um nome.
- **Nove quartos** (a casa gigante e vazia) — foi **cortado de verdade**. Era o mais fraco dos sete, e a solidão já está coberta por *Refém do ídolo* e *À disposição de ninguém*. Se você quiser de volta, ele entra no lugar de *Rico e aposentado aos trinta* como genérico, com a condição negativa virando o texto padrão.

---

## 5. Flags derivadas

Não vêm de carta nenhuma — o motor calcula na hora da morte:

| Flag | Cálculo |
|---|---|
| `sem_escandalo` | nenhuma de `investigacao_apostas`, `laranja`, `deve_pro_valdir`, `fundo_comprou_direitos`, `patrocinio_apostas` |
| `carreira_limpa` | `sem_escandalo` **e** nenhuma de `forcou_saida`, `calou` |

`sem_escandalo` é a espinha do dourado da ganância: você precisa ter acumulado muito dinheiro **e** ter recusado todos os atalhos que fazem dinheiro acumular rápido.

---

## 6. Grupo OR e robustez dos dourados

**Nenhum final está inalcançável.** Toda flag exigida por um final tem carta produtora — o backlog que o validador imprimia zerou.

O problema seguinte, mais sutil, era de **robustez**: um dourado que depende de uma flag produzida por uma única carta vira loteria, porque basta aquela carta não sair no sorteio para o final morrer naquela vida. Eram 13 dependências assim; hoje resta uma (`curso_de_treinador`), que resolve no bloco `treinador`.

Dois dourados foram resolvidos por uma extensão do schema, o **grupo OR** (`flags_qualquer`): em vez de exigir uma flag específica, aceitam qualquer uma de um conjunto que significa a mesma coisa dramaticamente.

```json
"condicoes": {
  "flags": ["recusou_apostas"],
  "flags_qualquer": ["processou_valdir", "rompeu_valdir", "quitou_valdir", "recusou_fundo"],
  "medidores": { "torcida": { "min": 70 } },
  "era": ["auge", "declinio", "legado"]
}
```

Lido em português: *você recusou o dinheiro das apostas **e** em algum momento enfrentou quem te sugava, de algum jeito.* Continua exigindo quatro fatores. Deixou de exigir sorte.

O grupo OR conta como **um** fator na regra dos três mínimos, e o validador só acusa fonte única quando a soma das fontes do grupo inteiro é 1.

---

## 6b. Morte súbita — dez finais fora das famílias

Cerca de dez cartas do baralho podem encerrar a carreira na hora, independente dos medidores (GDD §3.1b). Cada uma tem seu final nomeado, listado em `finais.json` sob `mortes_subitas`. Todos usam moldura preta e compartilham duas ilustrações — `final_morte_burra` e `final_morte_banido`.

| Final | O que aconteceu |
|---|---|
| **A intoxicação mais cara do futebol brasileiro** | A maionese ficou fora da geladeira. A peneira era às sete da manhã. |
| **O empurrão** | Sua mão no peito do árbitro na final do sub-20. Cento e oitenta dias, e ninguém espera cento e oitenta dias por um garoto. |
| **A tatuagem** | Aposta perdida no vestiário, escudo do rival na canela, foto na internet em duas horas. |
| **Vinte por hora** | Você bateu o carro novo num poste no estacionamento do próprio clube, na frente do marketing inteiro. |
| **A procuração** | Assinada em branco porque você estava com pressa. Deixou de ser dono de tudo seu, inclusive do nome. |
| **A live que ficou salva** | Três da manhã, quarenta minutos de sinceridade sobre o presidente do clube, e a gravação circulando antes do café. |
| **Trezentos e sessenta dias** | O monitor do VAR quebrado com a mão fechada, em rede nacional. Você tinha trinta e um anos. |
| **O helicóptero** | Festa a quatrocentos quilômetros na véspera da final. O pouso de emergência rendeu quarenta milhões de views e três fraturas. |
| **O áudio de trinta e sete segundos** | Você recusou a convocação por áudio, às pressas, com uma franqueza que nenhuma assessoria conseguiu explicar. |
| **Duzentos reais** | Uma aposta, no próprio jogo, para ganhar uma discussão de vestiário. Banimento vitalício custa exatamente duzentos reais. |

**Total geral de finais: 54** — 40 nas oito famílias, 4 de contexto e 10 de morte súbita, sobre 14 ilustrações.

---

## 6c. Fim natural — três finais que não são morte

Chegar aos 39 anos vivo não é uma morte de medidor, e por um tempo o jogo tratava como se fosse: o fim natural caía no genérico da família FORMA 0, e **42% de todas as carreiras terminavam em "Sucata"**. A simulação pegou isso.

O bloco `fim_natural` resolve o fim por idade, depois dos finais de contexto e antes de qualquer família:

| Final | Moldura | Condição |
|---|---|---|
| **O último jogo** | prata | 1+ título |
| **Uma carreira inteira** | cinza | zero títulos e zero convocações |
| **Fim de linha** | cinza | *(genérico)* |

*Uma carreira inteira* é o final mais importante dos três: vinte e dois anos de profissão, nenhum título, nenhuma convocação e uma casa quitada. É o que acontece com a esmagadora maioria dos jogadores, e ninguém escreve sobre isso.

**Total geral: 57 finais** — 40 nas famílias, 4 de contexto, 3 de fim natural e 10 de morte súbita.

---

## 7. Ficha de carreira

Toda morte gera uma figurinha de álbum com nome, apelido, posição, período, clubes na ordem, gols, jogos, títulos, convocações, e o nome do final em destaque. A moldura conta a história em uma cor:

| Moldura | Significado | Quantos |
|---|---|---|
| **Dourada** | chegou ao extremo pelo caminho difícil | 11 |
| **Prata** | escolha digna que custou a carreira | 1 |
| **Cinza** | a maioria | 20 |
| **Preta** | escândalo, negligência, dívida | 12 |

Exportável como imagem em um toque. É o objeto compartilhável do jogo.

---

## 8. O que testar

Bruno pediu testes para calibrar a dificuldade dos dourados. O que a simulação precisa medir, assim que o motor existir:

1. **Taxa de cada dourado.** Alvo: entre 0,5% e 3% das carreiras. Abaixo de 0,5% é frustrante; acima de 3% deixa de ser conquista.
2. **Compatibilidade de flags.** Algumas condições podem ser logicamente impossíveis de combinar — por exemplo, se `padrinho_do_kaique` só aparece na era 5 e o dourado exige DINHEIRO em 100, que costuma matar antes. É o risco maior dos dourados de DINHEIRO 100 e FORMA 100.
3. **Distribuição de molduras.** Se 80% das partidas saem cinza, os condicionais estão exigindo demais.

Enquanto o motor não existe, o validador já garante o que dá para garantir sem simular: simetria, presença de dourado e genérico, ordem correta e existência das flags.
