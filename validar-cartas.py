#!/usr/bin/env python3
"""
Validador de cartas do CRAQUE.

Uso:  python3 validar-cartas.py cartas/*.json

Checa as regras do GDD §4.2 e §4.5:
  1. simetria de magnitude entre as duas opções   (nenhuma escolha óbvia)
  2. no máximo 3 medidores por opção
  3. texto <= 220 chars, rótulo <= 22 chars
  4. deltas dentro das faixas por tipo de carta
  5. grafo de flags: órfãs produzidas / consumidas sem produtor
  6. encadeamentos apontando para ids existentes
  7. deriva do baralho por medidor (a regra que só aparece na simulação)

Sai com código 1 se houver erro. Avisos não quebram o build.
"""
import glob, json, os, re, sys
from collections import defaultdict

TOKENS_VALIDOS = {"{nome}", "{apelido}", "{clube}", "{clube_novo}", "{patamar_novo}"}

# {clube_novo} e {patamar_novo} só existem quando o motor abriu uma proposta:
# usá-los fora das cartas da janela imprime string vazia na tela do jogador
TOKENS_DE_PROPOSTA = {"{clube_novo}", "{patamar_novo}"}
CARTAS_DA_JANELA = {"transferencia_sobe", "transferencia_desce"}

# cargos.json é a fonte do elenco; sem ele, as checagens de cargo são puladas
CARGOS, ERAS_ALVO = {}, {}
for _p in ("cargos.json", os.path.join(os.path.dirname(__file__), "..", "cargos.json")):
    if os.path.exists(_p):
        _d = json.load(open(_p, encoding="utf-8"))
        CARGOS = _d["cargos"]
        ERAS_ALVO = {k: v for k, v in _d.get("eras_alvo", {}).items() if isinstance(v, dict)}
        break

FOLGA_MINIMA = 2.0   # elegíveis por era >= 2x o consumo máximo, senão a repetição aparece

# flags criadas pelo motor, não por cartas
FLAGS_DO_MOTOR = {
    "jogou_na_europa", "capitao", "aposentado_selecao",
    "contrato_vencido", "lesionado", "viveu_arco_capitao",
    "trocou_de_clube",   # motor: aceitou uma proposta da janela
}

P_SUCESSO = 0.40          # probabilidade média assumida em cartas de risco
LIMITE_DERIVA = 0.08      # pontos por carta jogada, por medidor (escala meia)
PESO_MINIMO_DERIVA = 150  # abaixo disso a deriva é ruído, não sinal
MEDIDORES = ("forma", "torcida", "diretoria", "dinheiro")

# Escala de dificuldade: fator acumulado 1,49 sobre a escala original, medido em
# três passos (1,45 -> mediana 84 · 1,67 -> 46 · 1,49 -> 79 decisões). É a variância
# que controla o tamanho da carreira, não o decaimento por idade nem o calendário.
#
# A faixa de magnitude agora vem do PESO DRAMÁTICO, não do tipo narrativo.
# Uma carta é de legado porque muda o seu final, não porque move um número grande —
# o tamanho do delta é consequência da classificação.
_FX = json.load(open(os.path.join(os.path.dirname(__file__), "faixas.json"), encoding="utf-8"))
FAIXAS = {k: tuple(v) for k, v in _FX["faixas"].items()}
FAIXA_MORTE = tuple(_FX["morte"])

# finais de morte súbita declarados em finais.json
FINAIS_DE_ESCOLHA = set()
FINAIS_DE_MORTE = set()
for _p in ("finais.json", os.path.join(os.path.dirname(__file__), "..", "finais.json")):
    if os.path.exists(_p):
        _fj = json.load(open(_p, encoding="utf-8"))
        FINAIS_DE_MORTE = {f["id"] for f in _fj.get("mortes_subitas", [])}
        FINAIS_DE_ESCOLHA = {f["id"] for f in _fj.get("escolhas_de_vida", [])}
        break

erros, avisos = [], []

def REPETIVEL(c):
    return not c.get("unico") and c.get("tipo") != "catastrofica"


def opcoes(c):
    """Gera (rótulo_do_lado, dict_de_efeitos, peso_de_probabilidade)."""
    for lado in ("esquerda", "direita"):
        o = c[lado]
        if "sucesso" in o:
            yield f"{lado}/sucesso", o["sucesso"].get("efeitos", {}), P_SUCESSO
            yield f"{lado}/falha",   o["falha"].get("efeitos", {}),   1 - P_SUCESSO
        elif "morte" in o:
            # a morte não mexe medidor: encerra. Só o ramo de sobrevivência conta na deriva.
            p_vive = 1.0 - o["morte"].get("chance", 1.0)
            if p_vive > 0:
                yield f"{lado}/sobrevive", o.get("sobrevive", {}).get("efeitos", {}), p_vive
        else:
            yield lado, o.get("efeitos", {}), 1.0


def magnitude(c, lado):
    o = c[lado]
    if o.get("encerra"):
        return 0.0   # encerra a carreira: categórica, como a morte
    if "morte" in o:
        return 0.0   # categórica: não entra na regra de simetria
    if "sucesso" in o:
        return (P_SUCESSO * sum(abs(v) for v in o["sucesso"].get("efeitos", {}).values())
                + (1 - P_SUCESSO) * sum(abs(v) for v in o["falha"].get("efeitos", {}).values()))
    return sum(abs(v) for v in o.get("efeitos", {}).values())


TODAS_AS_CARTAS = []   # acumulador para a deriva do baralho inteiro
PRODUZIDAS, CONSUMIDAS = set(), set()   # grafo de flags é global, não por arquivo
FIOS_APONTADOS = set()   # ids alcançáveis por 'fio' — cartas de peso 0 dependem disso
ENCADEADOS = set()       # ids alcançáveis por 'encadeia'
REMOVIDAS = set()        # flags que algum 'tiraFlags' desfaz

ORDEM_ERAS = ["base", "estouro", "travessia", "auge", "declinio", "legado"]

# expressões que só fazem sentido se o motor já colocou o jogador naquele estado
PRESSUPOSTOS = [
    ("clube novo",            {"trocou_de_clube", "jogou_na_europa"}),
    ("novo clube",            {"trocou_de_clube", "jogou_na_europa"}),
    ("clube que te comprou",  {"trocou_de_clube", "assinou_com_valdir"}),
    ("clube anterior",        {"trocou_de_clube"}),
    ("fuso",                  {"jogou_na_europa"}),
    ("no exterior",           {"jogou_na_europa"}),
    ("lá fora",               {"jogou_na_europa"}),
]

# cartas que o motor empurra na fila direto (build-html.py), não outra carta.
# Os abridores de fio curto entraram aqui em 12/08: saíram do sorteio (peso 0) e
# passaram a ser agendados pelo motor, um por era — peso 3 entregava 1,42 carta de
# fio curto por carreira contra 12 fios escritos, e peso 9 dominava a era.
CHAMADAS_PELO_MOTOR = {"capitao_partida", "companheira_pedagio",
                       "transferencia_sobe", "transferencia_desce"}
# o motor agenda um destes por era (agendarCurto), então eles são alcançáveis
# mesmo com peso 0 e sem ninguém apontar um 'fio' para eles
ABRIDOR_DE_FIO_CURTO = re.compile(r"^curto_[a-z]+_b1$")


def deriva(cartas, filtro):
    soma, peso_total = defaultdict(float), 0.0
    for c in cartas:
        if not filtro(c):
            continue
        w = c["peso"] if "peso" in c else 8
        if w == 0:
            continue
        peso_total += w
        for _, efeitos, p in opcoes(c):
            for k, v in efeitos.items():
                soma[k] += w * p * v / 2
    return soma, peso_total


def validar(caminho):
    dados = json.load(open(caminho, encoding="utf-8"))
    cartas = dados["cartas"]
    TODAS_AS_CARTAS.extend(cartas)
    ids = {c["id"] for c in cartas}
    produzidas, consumidas = PRODUZIDAS, CONSUMIDAS

    for c in cartas:
        cid = c["id"]
        tipo = c.get("tipo", "arco" if c.get("unico") else "rotina")

        # --- cargo, eras e arquétipo ---
        cargo = c.get("cargo")
        if not cargo:
            erros.append(f"{cid}: sem campo 'cargo'")
        elif CARGOS:
            if cargo not in CARGOS:
                erros.append(f"{cid}: cargo '{cargo}' não existe em cargos.json")
            else:
                cfg = CARGOS[cargo]
                fora = set(c["era"]) - set(cfg["eras"])
                if fora:
                    erros.append(f"{cid}: cargo '{cargo}' não atua na(s) era(s) {sorted(fora)}")
                arq = c.get("arquetipo")
                if arq:
                    if not cfg.get("com_arquetipo"):
                        erros.append(f"{cid}: cargo '{cargo}' não tem arquétipos, mas a carta define '{arq}'")
                    elif arq not in {e["id"] for e in cfg["elenco"]}:
                        erros.append(f"{cid}: arquétipo '{arq}' não está no elenco de '{cargo}'")

        # --- morte súbita ---
        fatais = [l for l in ("esquerda", "direita") if "morte" in c[l]]
        if c.get("tipo") == "morte_subita":
            if len(fatais) != 1:
                erros.append(f"{cid}: carta morte_subita com {len(fatais)} opção(ões) fatal(is) — tem que ser exatamente 1")
            for lado in fatais:
                mo = c[lado]["morte"]
                if FINAIS_DE_MORTE and mo.get("final") not in FINAIS_DE_MORTE:
                    erros.append(f"{cid}/{lado}: final de morte '{mo.get('final')}' não existe em finais.json")
                ch = mo.get("chance", 1.0)
                if not (0 < ch <= 1):
                    erros.append(f"{cid}/{lado}: chance de morte {ch} fora de (0, 1]")
                if ch < 1.0 and not c[lado].get("sobrevive", {}).get("efeitos"):
                    erros.append(f"{cid}/{lado}: chance {ch} < 1 exige bloco 'sobrevive' com efeitos")
                if ch == 1.0 and c[lado].get("sobrevive"):
                    avisos.append(f"{cid}/{lado}: morte certa não deveria ter bloco 'sobrevive'")
            # a opção segura precisa ter efeito real, senão a escolha é falsa
            for lado in ("esquerda", "direita"):
                if lado not in fatais and not c[lado].get("efeitos"):
                    erros.append(f"{cid}/{lado}: opção segura sem efeitos — a escolha fica falsa")
        elif fatais:
            erros.append(f"{cid}: tem opção fatal mas não é do tipo morte_subita")

        # --- pressuposto de estado: o texto não pode afirmar o que o jogo não garante ---
        # Foi assim que apareceu a carta do roupeiro agradecendo a camisa do clube
        # novo numa carreira em que o jogador nunca saiu do primeiro clube.
        gates = set((c.get("requer") or {}).get("flags") or [])
        baixo = " ".join(c["texto"].lower().split())
        for expr, precisa in PRESSUPOSTOS:
            if expr in baixo and not (precisa & gates):
                avisos.append(f"{cid}: o texto diz \"{expr}\" mas a carta não exige "
                              f"{' ou '.join(sorted(precisa))} — pode aparecer sem fazer sentido")

        # --- tokens de texto ---
        for tok in set(re.findall(r"\{[a-z_]+\}", c["texto"])):
            if tok not in TOKENS_VALIDOS:
                erros.append(f"{cid}: token '{tok}' inválido (só {', '.join(sorted(TOKENS_VALIDOS))})")
            elif tok in TOKENS_DE_PROPOSTA and cid not in CARTAS_DA_JANELA \
                    and not any(c[l].get("aceitaProposta") for l in ("esquerda", "direita")):
                erros.append(f"{cid}: usa '{tok}', que só existe nas cartas da janela "
                             f"— fora delas imprime vazio na tela")

        if len(c["texto"]) > 220:
            erros.append(f"{cid}: texto com {len(c['texto'])} chars (máx 220)")

        for lado in ("esquerda", "direita"):
            o = c[lado]
            if len(o["rotulo"]) > 22:
                erros.append(f"{cid}/{lado}: rótulo com {len(o['rotulo'])} chars — \"{o['rotulo']}\"")
            if o.get("encadeia") and o["encadeia"] not in ids:
                erros.append(f"{cid}/{lado}: encadeia '{o['encadeia']}', que não existe")
            if o.get("encadeia"):
                ENCADEADOS.add(o["encadeia"])
            # --- fio de três batidas ---
            if o.get("encerra"):
                if FINAIS_DE_ESCOLHA and o["encerra"] not in FINAIS_DE_ESCOLHA:
                    erros.append(f"{cid}/{lado}: encerra em '{o['encerra']}', "
                                 f"que não existe em finais.json/escolhas_de_vida")
                if o.get("efeitos"):
                    avisos.append(f"{cid}/{lado}: encerra a carreira e ainda mexe medidor — "
                                  f"o delta não vai ser visto")
            # carta que promete clube novo mas não troca clube nenhum: foi assim que
            # valdir_base_04 contava transferência e deixava o rodapé mentindo
            if o.get("estatisticas", {}).get("transferencias") and not o.get("aceitaProposta"):
                erros.append(f"{cid}/{lado}: conta transferência sem 'aceitaProposta' — "
                             f"o clube do rodapé não vai mudar")
            fio = o.get("fio")
            if fio:
                FIOS_APONTADOS.add(fio["id"])
                em = fio.get("em")
                if em and (len(em) != 2 or em[0] > em[1] or em[0] < 3):
                    erros.append(f"{cid}/{lado}: janela de fio {em} inválida "
                                 f"(mínimo 3 cartas, senão a consequência cola na decisão)")
            REMOVIDAS.update(o.get("tiraFlags", []))

        for nome, efeitos, _ in opcoes(c):
            if len(efeitos) > 3:
                erros.append(f"{cid}/{nome}: mexe em {len(efeitos)} medidores (máx 3)")
            for k in efeitos:
                if k not in MEDIDORES:
                    erros.append(f"{cid}/{nome}: medidor desconhecido '{k}'")

        # regra 1 — simetria
        a, b = magnitude(c, "esquerda"), magnitude(c, "direita")
        if a and b:
            lo, hi = min(a, b), max(a, b)
            if hi > lo * 1.35 + 2:
                avisos.append(f"{cid}: opções assimétricas ({a:.0f} vs {b:.0f}) — pode virar escolha óbvia")

        # regra 4 — magnitude compatível com o peso dramático
        pd = c.get("peso_dramatico")
        if not pd:
            erros.append(f"{cid}: sem 'peso_dramatico'")
        else:
            lo, hi = FAIXA_MORTE if c.get("tipo") == "morte_subita" else FAIXAS[pd]
            for v, lado in ((a, "esquerda"), (b, "direita")):
                if v and not (lo <= v <= hi):
                    avisos.append(f"{cid}/{lado}: magnitude {v:.0f} fora da faixa de "
                                  f"'{pd}' ({lo}–{hi}) — peso e tamanho desalinhados")
            # o eco vive na OPÇÃO, não na carta: um eco igual para os dois lados
            # não promete consequência, só decora
            if pd == "legado":
                if c.get("eco"):
                    erros.append(f"{cid}: 'eco' no nível da carta — tem que ser por opção, "
                                 f"senão os dois caminhos recebem a mesma frase")
                for lado in ("esquerda", "direita"):
                    # lado que ENCERRA a carreira (morte ou escolha de vida) não tem eco:
                    # o final é a consequência, e ele já está na tela inteira
                    if "morte" in c[lado] or c[lado].get("encerra"):
                        if c[lado].get("eco"):
                            erros.append(f"{cid}/{lado}: eco num lado que encerra — o final é a consequência")
                        continue
                    if not c[lado].get("eco"):
                        avisos.append(f"{cid}/{lado}: opção de legado sem 'eco'")
                    elif len(c[lado]["eco"]) > 60:
                        erros.append(f"{cid}/{lado}: eco com {len(c[lado]['eco'])} chars (máx 60)")

        # regra 5 — flags
        for lado in ("esquerda", "direita"):
            o = c[lado]
            for bloco in (o, o.get("sucesso", {}), o.get("falha", {})):
                produzidas.update(bloco.get("flags", []) if isinstance(bloco, dict) else [])
        r = c.get("requer", {})
        consumidas.update(r.get("flags", []))
        consumidas.update(x.lstrip("!") for x in r.get("semFlags", []))

    # regra 7 — deriva (informativa por arquivo; a regra vale só no baralho merged)
    print(f"\n=== {caminho} — {len(cartas)} cartas ===")
    for rotulo, filtro in (("baralho inteiro", lambda c: True),
                           ("só repetíveis", REPETIVEL)):
        soma, peso_total = deriva(cartas, filtro)
        if peso_total == 0:
            continue
        linha = "  ".join(f"{k}={soma[k]/peso_total:+.2f}" for k in MEDIDORES)
        print(f"deriva ({rotulo}): {linha}")
    print("  (deriva de um arquivo só é informativa — personagem tem viés de propósito)")


def checar_globais():
    """Checagens que só fazem sentido sobre o baralho inteiro, rodadas uma vez."""
    vistos = set()
    por_texto = defaultdict(list)
    for c in TODAS_AS_CARTAS:
        if c["id"] in vistos:
            erros.append(f"id duplicado entre arquivos: '{c['id']}'")
        vistos.add(c["id"])
        # duplicata de CONTEÚDO: carta migrada para um bloco e esquecida no arquivo original
        por_texto[" ".join(c["texto"].lower().split())].append(c["id"])
    for cids in por_texto.values():
        if len(cids) > 1:
            erros.append(f"texto idêntico em {len(cids)} cartas de ids diferentes: "
                         f"{', '.join(cids)} — provável migração incompleta")

    # nenhum eco se repete no baralho: eco repetido é eco genérico disfarçado
    vistos_eco = defaultdict(list)
    for c in TODAS_AS_CARTAS:
        for lado in ("esquerda", "direita"):
            e = c[lado].get("eco")
            if e:
                vistos_eco[e].append(f"{c['id']}/{lado}")
    for e, onde in vistos_eco.items():
        if len(onde) > 1:
            erros.append(f"eco repetido em {len(onde)} opções: \"{e}\" — {', '.join(onde)}")

    for f in sorted(CONSUMIDAS - PRODUZIDAS - FLAGS_DO_MOTOR):
        erros.append(f"flag '{f}' é exigida por alguma carta mas nenhuma carta a produz")
    for f in sorted(PRODUZIDAS - CONSUMIDAS - REMOVIDAS):
        avisos.append(f"flag '{f}' é produzida e nunca lida — conteúdo futuro ou lixo")

    # --- fios: alcance e integridade ---
    por_id = {c["id"]: c for c in TODAS_AS_CARTAS}
    for alvo in sorted(FIOS_APONTADOS):
        if alvo not in por_id:
            erros.append(f"fio aponta para '{alvo}', que não existe")
    for f in sorted(REMOVIDAS - PRODUZIDAS - FLAGS_DO_MOTOR):
        erros.append(f"'tiraFlags' desfaz a flag '{f}', que nenhuma carta produz — provável erro de digitação")

    # uma carta de peso 0 só existe se alguém a chamar: ou é batida de fio, ou é encadeada
    orfas = [c["id"] for c in TODAS_AS_CARTAS
             if c.get("peso", 8) == 0
             and c["id"] not in FIOS_APONTADOS and c["id"] not in ENCADEADOS
             and c["id"] not in CHAMADAS_PELO_MOTOR
             and not ABRIDOR_DE_FIO_CURTO.match(c["id"])]
    for o in orfas:
        erros.append(f"{o}: peso 0 e ninguém a chama — carta inalcançável")

    # a batida seguinte tem que poder atuar em alguma era igual ou posterior à da batida atual
    for c in TODAS_AS_CARTAS:
        for lado in ("esquerda", "direita"):
            fio = c[lado].get("fio")
            if not fio or fio["id"] not in por_id:
                continue
            alvo = por_id[fio["id"]]
            piso = min(ORDEM_ERAS.index(e) for e in c["era"])
            if fio.get("proximaEra"):
                piso += 1
            possiveis = [e for e in alvo["era"] if ORDEM_ERAS.index(e) >= piso]
            if not possiveis:
                erros.append(f"{c['id']}/{lado}: fio para '{alvo['id']}', que não atua em nenhuma era "
                             f"a partir de '{ORDEM_ERAS[min(piso, 5)]}' — o fio nunca fecha")
            elif len(possiveis) == 1 and possiveis[0] == "legado":
                avisos.append(f"{c['id']}/{lado}: fio para '{alvo['id']}' só fecha na era Legado — "
                              f"quem parar antes nunca vê o acerto de contas")

    # Lado das opções que encerram: se todas caírem do mesmo lado, quem aprende
    # "esquerda é perigo" fica imortal. Medido com agentes de personalidade fixa:
    # com 24/24 na esquerda, o agente que só arrasta para a direita tinha 0% de
    # morte súbita e o que só arrasta para a esquerda tinha 33%.
    for rotulo, teste in (("morte súbita", lambda o: "morte" in o),
                          ("saída por escolha", lambda o: bool(o.get("encerra")))):
        e = sum(1 for c in TODAS_AS_CARTAS if teste(c["esquerda"]))
        dd = sum(1 for c in TODAS_AS_CARTAS if teste(c["direita"]))
        tot = e + dd
        if tot >= 4 and (max(e, dd) / tot) > 0.70:
            erros.append(f"opções de {rotulo} concentradas num lado: {e} na esquerda, {dd} na direita "
                         f"— quem decorar o lado fica imune")

    # deriva das cartas de fio: peso 0 as tira da conta do baralho, então elas
    # precisam de uma checagem própria, senão empurram um medidor sem ninguém ver
    fios = [c for c in TODAS_AS_CARTAS if c.get("peso", 8) == 0]
    if fios:
        soma_f = defaultdict(float)
        for c in fios:
            for _, efeitos, p in opcoes(c):
                for k, v in efeitos.items():
                    soma_f[k] += p * v / 2
        print(f"\n=== CARTAS DE FIO — {len(fios)} cartas (peso 0, fora do sorteio) ===")
        print("deriva própria: " + "  ".join(f"{k}={soma_f[k]/len(fios):+.2f}" for k in MEDIDORES))
        for k in MEDIDORES:
            d = soma_f[k] / len(fios)
            if abs(d) > 0.6:   # faixa mais larga: são poucas cartas e todas de alto impacto
                avisos.append(f"deriva de {k.upper()} = {d:+.2f}/carta nas cartas de fio "
                              f"— o conjunto dos fios empurra esse medidor")

    # cobertura por era: o baralho elegível tem que ser folgado em relação ao consumo
    if ERAS_ALVO:
        # só conta o que o sorteio pode tirar: carta de peso 0 chega por agenda,
        # não cobre era nenhuma
        por_era = defaultdict(int)
        for c in TODAS_AS_CARTAS:
            if c.get("peso", 8) == 0:
                continue
            for e in c["era"]:
                por_era[e] += 1
        print("\n=== COBERTURA POR ERA ===")
        print(f"{'era':12} {'elegíveis':>9} {'consumo':>9} {'folga':>7}")
        for era, alvo in ERAS_ALVO.items():
            n, consumo = por_era.get(era, 0), alvo["max"]
            folga = n / consumo if consumo else 0
            estado = "ok" if folga >= FOLGA_MINIMA else ("MAGRO" if folga >= 1.0 else "CRÍTICO")
            print(f"{era:12} {n:9} {alvo['min']}–{consumo:<5} {folga:6.1f}x  {estado}")
            if folga < 1.0:
                erros.append(f"era '{era}': {n} cartas elegíveis para consumo de até {consumo} "
                             f"— a carreira não fecha a era sem repetir")
            elif folga < FOLGA_MINIMA:
                avisos.append(f"era '{era}': folga de apenas {folga:.1f}x "
                              f"({n} elegíveis / {consumo} consumidas) — repetição vai ficar visível")


def main():
    caminhos = sys.argv[1:] or sorted(glob.glob("cartas/*.json"))
    for c in caminhos:
        validar(c)
    checar_globais()

    # A regra de deriva só vale sobre o baralho MERGED. Um personagem tem viés
    # de propósito: o Valdir empurra DINHEIRO, a Dra. Kênia empurra FORMA para
    # baixo. Balancear cada arquivo isoladamente destruiria a identidade deles.
    if len(caminhos) > 1 or True:
        soma, peso_total = deriva(TODAS_AS_CARTAS, REPETIVEL)
        print(f"\n=== BARALHO MERGED — {len(TODAS_AS_CARTAS)} cartas, "
              f"{len([c for c in TODAS_AS_CARTAS if REPETIVEL(c)])} repetíveis ===")
        if peso_total == 0:
            print("nenhuma carta repetível.")
        else:
            linha = "  ".join(f"{k}={soma[k]/peso_total:+.2f}" for k in MEDIDORES)
            suficiente = peso_total >= PESO_MINIMO_DERIVA
            print(f"deriva: {linha}"
                  f"{'' if suficiente else '   [peso ' + str(int(peso_total)) + ' < ' + str(PESO_MINIMO_DERIVA) + ' — informativo]'}")
            if suficiente:
                for k in MEDIDORES:
                    d = soma[k] / peso_total
                    if abs(d) > LIMITE_DERIVA:
                        avisos.append(f"deriva de {k.upper()} = {d:+.2f}/carta no baralho merged "
                                      f"(limite ±{LIMITE_DERIVA}) — o baralho empurra esse medidor sozinho")

        # ---------------------------------------------------------------------
        # PONTO CEGO ENCONTRADO EM 12/08, e ele é grande.
        # A regra de deriva sempre mediu só as cartas REPETÍVEIS — 57 de 433, 12% do
        # baralho — com o argumento de que carta única aparece uma vez e não forma
        # tendência. O argumento não fecha: uma carreira sorteia ~47 cartas DISTINTAS,
        # e a soma delas é exatamente a tendência que o jogador vive. Medido sobre
        # tudo o que o sorteio pode tirar, TORCIDA deriva quase +1 ponto por carta,
        # doze vezes o limite. Boa parte é absorvida pelo rendimento decrescente
        # (medido: mortes por excesso 70% contra 30% por falta no agente aleatório),
        # e é por isso que nunca apareceu — mas absorver não é o mesmo que não existir.
        # Fica como AVISO e como rodada própria: corrigir isto junto com outra
        # alavanca tornaria as duas medições inúteis.
        soma_t, peso_t = deriva(TODAS_AS_CARTAS, lambda c: True)
        if peso_t:
            linha = "  ".join(f"{k}={soma_t[k]/peso_t:+.2f}" for k in MEDIDORES)
            print(f"\n=== BARALHO SORTEÁVEL INTEIRO — o que o jogador realmente vive ===")
            print(f"deriva: {linha}   [informativo: a regra cobra só as repetíveis]")
            for k in MEDIDORES:
                d = soma_t[k] / peso_t
                if abs(d) > LIMITE_DERIVA * 3:
                    avisos.append(f"deriva de {k.upper()} = {d:+.2f}/carta no baralho SORTEÁVEL "
                                  f"inteiro (não só nas repetíveis) — o jogador sorteia ~47 cartas "
                                  f"distintas por carreira e a soma delas é a tendência que ele vive")
    print()
    for a in avisos:
        print(f"AVISO  {a}")
    for e in erros:
        print(f"ERRO   {e}")
    print(f"\n{len(erros)} erro(s), {len(avisos)} aviso(s).")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
