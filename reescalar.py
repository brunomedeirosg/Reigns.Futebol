#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Reescala todos os deltas do baralho por um fator, preservando simetria e deriva.

Multiplicação é a única transformação que mexe na DIFICULDADE sem mexer no
desenho: a razão entre as duas opções de uma carta fica igual, a razão entre os
pesos dramáticos fica igual, e a deriva escala junto (então continua neutra).
O que muda é a variância — e é a variância que decide o tamanho da carreira.

Uso: python3 ferramentas/reescalar.py 1.4 [--aplicar]
"""
import glob, json, os, sys

RAIZ = os.path.join(os.path.dirname(__file__), "..")
MEDIDORES = ("forma", "torcida", "diretoria", "dinheiro")


def blocos_de_efeitos(c):
    for lado in ("esquerda", "direita"):
        o = c[lado]
        for sub in ("sucesso", "falha", "sobrevive"):
            if sub in o and isinstance(o[sub], dict) and "efeitos" in o[sub]:
                yield o[sub]["efeitos"]
        if "efeitos" in o:
            yield o["efeitos"]


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        print(__doc__); sys.exit(1)
    fator = float(args[0])
    aplicar = "--aplicar" in sys.argv

    arquivos = sorted(glob.glob(os.path.join(RAIZ, "cartas", "*.json")))
    dados = {a: json.load(open(a, encoding="utf-8")) for a in arquivos}
    todas = [c for d in dados.values() for c in d["cartas"]]

    antes, depois, n = [], [], 0
    for c in todas:
        for ef in blocos_de_efeitos(c):
            for k in list(ef):
                if k not in MEDIDORES:
                    continue
                v = ef[k]
                antes.append(abs(v))
                # nunca deixa um delta virar 0: um efeito que existe tem que mover
                novo = int(round(v * fator)) or (1 if v > 0 else -1)
                ef[k] = novo
                depois.append(abs(novo))
                n += 1

    med = lambda a: sorted(a)[len(a) // 2]
    print(f"fator {fator} · {n} deltas")
    print(f"  antes : min {min(antes)} · mediana {med(antes)} · máx {max(antes)}")
    print(f"  depois: min {min(depois)} · mediana {med(depois)} · máx {max(depois)}")
    print("faixas novas sugeridas para o validador:")
    for nome, (lo, hi) in (("padrao", (6, 10)), ("importante", (18, 26)),
                           ("legado", (32, 44)), ("MORTE", (8, 26))):
        print(f"  {nome:11} ({int(round(lo*fator))}, {int(round(hi*fator))})")

    if aplicar:
        for a, d in dados.items():
            json.dump(d, open(a, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("aplicado nos JSON.")
    else:
        print("(simulação — use --aplicar para gravar)")


main()
