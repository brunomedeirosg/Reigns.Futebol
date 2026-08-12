#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corrige a deriva do baralho merged com ajustes de ±1, só onde não quebra nada.

Alvo: |deriva| <= ALVO em todos os medidores, calculado exatamente como o
validador calcula (peso da carta x probabilidade do ramo x valor / 2).

Regras que o ajuste NUNCA pode violar:
  - a carta continua na faixa de magnitude do peso_dramatico dela;
  - a simetria continua valendo (hi <= lo*1.35 + 2);
  - só mexe em cartas REPETÍVEIS (as únicas que contam na deriva);
  - nunca zera um efeito (um +1 virando 0 apaga a intenção da carta);
  - nunca inverte sinal.

Uso: python3 ferramentas/balancear-deriva.py [--aplicar] [--fios]

Com --fios, opera sobre as cartas de FIO (peso 0), que ficam fora da conta do
baralho justamente por não serem sorteadas. Elas têm alvo mais folgado (±0,25 por
carta): são poucas e todas de alto impacto, e zerar a deriva delas apagaria a
intenção — um fio de apostas *deve* puxar dinheiro.
"""
import glob, json, os, sys
from collections import defaultdict

RAIZ = os.path.join(os.path.dirname(__file__), "..")
P_SUCESSO = 0.40
ALVO = 0.06                     # margem abaixo do limite de 0.08 do validador
MEDIDORES = ("forma", "torcida", "diretoria", "dinheiro")
# faixas.json é a fonte única: duplicar isso aqui já causou um bug silencioso
_FX = json.load(open(os.path.join(os.path.dirname(__file__), "faixas.json"), encoding="utf-8"))
FAIXAS = {k: tuple(v) for k, v in _FX["faixas"].items()}
FAIXA_MORTE = tuple(_FX["morte"])


def repetivel(c):
    return not c.get("unico") and c.get("tipo") != "catastrofica"


def ramos(c):
    """(caminho_para_o_dict_de_efeitos, peso_de_probabilidade) por lado."""
    for lado in ("esquerda", "direita"):
        o = c[lado]
        if "sucesso" in o:
            yield (lado, "sucesso"), o["sucesso"].setdefault("efeitos", {}), P_SUCESSO
            yield (lado, "falha"), o["falha"].setdefault("efeitos", {}), 1 - P_SUCESSO
        elif "morte" in o:
            p_vive = 1.0 - o["morte"].get("chance", 1.0)
            if p_vive > 0:
                yield (lado, "sobrevive"), o.setdefault("sobrevive", {}).setdefault("efeitos", {}), p_vive
        else:
            yield (lado,), o.setdefault("efeitos", {}), 1.0


def magnitude(c, lado):
    o = c[lado]
    if "morte" in o:
        return 0.0
    if "sucesso" in o:
        return (P_SUCESSO * sum(abs(v) for v in o["sucesso"].get("efeitos", {}).values())
                + (1 - P_SUCESSO) * sum(abs(v) for v in o["falha"].get("efeitos", {}).values()))
    return sum(abs(v) for v in o.get("efeitos", {}).values())


def faixa_ok(c):
    lo_f, hi_f = FAIXA_MORTE if c.get("tipo") == "morte_subita" else FAIXAS[c["peso_dramatico"]]
    for lado in ("esquerda", "direita"):
        if "morte" in c[lado]:
            continue
        m = magnitude(c, lado)
        if not (lo_f <= m <= hi_f):
            return False
    return True


def simetria_ok(c):
    a, b = magnitude(c, "esquerda"), magnitude(c, "direita")
    if not (a and b):
        return True
    lo, hi = min(a, b), max(a, b)
    return hi <= lo * 1.35 + 2


def calcular_deriva(cartas):
    soma, peso_total = defaultdict(float), 0.0
    for c in cartas:
        if not repetivel(c):
            continue
        w = c.get("peso", 8)
        if w == 0:
            continue
        peso_total += w
        for _, efeitos, p in ramos(c):
            for k, v in efeitos.items():
                soma[k] += w * p * v / 2
    return soma, peso_total


ALVO_FIOS = 0.25


def balancear_fios(dados, todas, aplicar):
    # capitao_partida e companheira_pedagio também são peso 0, mas são cartas do
    # motor e já estavam balanceadas: o ajuste é só das batidas de fio
    fios = [c for c in todas if c.get("peso", 8) == 0 and c["id"].startswith("fio_")]
    soma, n = calcular_deriva_fios(todas)
    print(f"{len(fios)} cartas de fio")
    print("deriva inicial: " + "  ".join(f"{k}={soma[k]/n:+.3f}" for k in MEDIDORES))

    # deltas de fio são grandes (20 a 33): até 5 pontos de ajuste é ~15% e não
    # muda o que a carta diz. No baralho comum, 1 já é o limite.
    ajustes, usados = [], defaultdict(int)
    for medidor in MEDIDORES:
        while abs(soma[medidor] / n) > ALVO_FIOS:
            sinal = -1 if soma[medidor] > 0 else +1
            escolhida = None
            for c in fios:
                if usados[(c["id"], medidor)] >= 5:
                    continue
                for caminho, efeitos, p in ramos(c):
                    v = efeitos.get(medidor)
                    if v is None:
                        continue
                    novo = v + sinal
                    if novo == 0 or (novo > 0) != (v > 0):
                        continue
                    efeitos[medidor] = novo
                    ok = faixa_ok(c) and simetria_ok(c)
                    efeitos[medidor] = v
                    if ok:
                        escolhida = (c, caminho, efeitos, v, p)
                        break
                if escolhida:
                    break
            if escolhida is None:
                print(f"  {medidor}: sem candidato seguro — parando em {soma[medidor]/n:+.3f}")
                break
            c, caminho, efeitos, v, p = escolhida
            efeitos[medidor] = v + sinal
            soma[medidor] += p * sinal / 2
            usados[(c["id"], medidor)] += 1
            ajustes.append((c["id"], caminho, medidor, v, v + sinal))

    print("deriva final:   " + "  ".join(f"{k}={soma[k]/n:+.3f}" for k in MEDIDORES))
    print(f"{len(ajustes)} ajuste(s) de ±1 em {len({a[0] for a in ajustes})} cartas")
    for cid, caminho, medidor, antes, depois in ajustes:
        print(f"  {cid} {'/'.join(caminho)} {medidor}: {antes:+d} -> {depois:+d}")

    if aplicar:
        for a, d in dados.items():
            json.dump(d, open(a, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("\naplicado nos JSON.")
    else:
        print("\n(simulação — use --aplicar para gravar)")


def calcular_deriva_fios(cartas):
    """Cartas de peso 0: não são sorteadas, então valem 1 cada, não 'peso' cada."""
    soma = defaultdict(float)
    fios = [c for c in cartas if c.get("peso", 8) == 0]
    for c in fios:
        for _, efeitos, p in ramos(c):
            for k, v in efeitos.items():
                soma[k] += p * v / 2
    return soma, float(len(fios))


def main():
    aplicar = "--aplicar" in sys.argv
    modo_fios = "--fios" in sys.argv
    arquivos = sorted(glob.glob(os.path.join(RAIZ, "cartas", "*.json")))
    dados = {a: json.load(open(a, encoding="utf-8")) for a in arquivos}
    todas = [c for d in dados.values() for c in d["cartas"]]

    if modo_fios:
        return balancear_fios(dados, todas, aplicar)

    soma, peso_total = calcular_deriva(todas)
    print("deriva inicial: " + "  ".join(f"{k}={soma[k]/peso_total:+.3f}" for k in MEDIDORES))

    ajustes = []
    usados = set()   # (id da carta, medidor) — no máximo um ±1 por carta por medidor,
                     # senão o conserto do baralho vira deformação de uma carta só
    for medidor in MEDIDORES:
        # sentido do conserto: se deriva > 0, precisamos tirar pontos
        while abs(soma[medidor] / peso_total) > ALVO:
            alvo_sinal = -1 if soma[medidor] > 0 else +1
            melhor = None
            for c in todas:
                if not repetivel(c) or c.get("peso", 8) == 0:
                    continue
                if (c["id"], medidor) in usados:
                    continue
                w = c.get("peso", 8)
                for caminho, efeitos, p in ramos(c):
                    v = efeitos.get(medidor)
                    if v is None:
                        continue
                    novo = v + alvo_sinal
                    if novo == 0 or (novo > 0) != (v > 0):
                        continue        # não zera nem inverte
                    efeitos[medidor] = novo
                    ok = faixa_ok(c) and simetria_ok(c)
                    efeitos[medidor] = v
                    if not ok:
                        continue
                    ganho = abs(w * p / 2)
                    if melhor is None or ganho > melhor[0]:
                        melhor = (ganho, c, caminho, efeitos, v, p, w)
            if melhor is None:
                print(f"  {medidor}: sem candidato seguro — parando em "
                      f"{soma[medidor]/peso_total:+.3f}")
                break
            _, c, caminho, efeitos, v, p, w = melhor
            efeitos[medidor] = v + alvo_sinal
            soma[medidor] += w * p * alvo_sinal / 2
            usados.add((c["id"], medidor))
            ajustes.append((c["id"], caminho, medidor, alvo_sinal, v, v + alvo_sinal))

    print("deriva final:   " + "  ".join(f"{k}={soma[k]/peso_total:+.3f}" for k in MEDIDORES))
    print(f"{len(ajustes)} ajuste(s) de ±1:")
    for cid, caminho, medidor, sinal, antes, depois in ajustes:
        print(f"  {cid} {'/'.join(caminho)} {medidor}: {antes:+d} -> {depois:+d}")

    if aplicar:
        for a, d in dados.items():
            json.dump(d, open(a, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("\naplicado nos JSON.")
    else:
        print("\n(simulação — use --aplicar para gravar)")


main()
