#!/usr/bin/env python3
"""
Validador de contraste da paleta do CRAQUE.

Uso:  python3 ferramentas/validar-paleta.py [arte/paleta.json]

Checa WCAG AA (4.5:1) para todo par cor-de-texto × superfície onde texto cai,
e 3:1 para elementos gráficos (barras dos medidores, silhuetas de personagem).
Sai com código 1 se algum par reprovar.
"""
import json, sys

AA_TEXTO = 4.5
AA_GRAFICO = 3.0
# a carta se separa do fundo por contorno, não por contraste de área.
# 1.5 só garante que dá para perceber a borda da carta; o contorno é obrigatório.
SEPARACAO_CARTA = 1.5


def _lin(c):
    c /= 255
    return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4


def luminancia(hexcor):
    h = hexcor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _lin(r) + 0.7152 * _lin(g) + 0.0722 * _lin(b)


def contraste(a, b):
    l1, l2 = sorted((luminancia(a), luminancia(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else "arte/paleta.json"
    p = json.load(open(caminho, encoding="utf-8"))
    falhas = []

    print(f"=== {caminho} ===\n")
    print(f"{'era':12} {'txt/sup':>8} {'txt2/sup':>9} {'txt/fundo':>10} {'destaque/fundo':>15}")
    for era, v in p["eras"].items():
        pares = {
            "texto/superficie":        (contraste(v["texto"], v["superficie"]), AA_TEXTO),
            "texto_sec/superficie":    (contraste(v["texto_secundario"], v["superficie"]), AA_TEXTO),
            "texto/fundo":             (contraste(v["texto"], v["fundo"]), AA_TEXTO),
            "destaque/fundo":          (contraste(v["destaque"], v["fundo"]), AA_GRAFICO),
            "superficie/fundo":        (contraste(v["superficie"], v["fundo"]), SEPARACAO_CARTA),
        }
        vals = list(pares.values())
        print(f"{era:12} {vals[0][0]:8.2f} {vals[1][0]:9.2f} {vals[2][0]:10.2f} {vals[3][0]:15.2f}")
        for nome, (r, alvo) in pares.items():
            if r < alvo:
                falhas.append(f"{era}: {nome} = {r:.2f} (mínimo {alvo})")

    print("\nmedidores sobre o fundo de cada era (mínimo 3.0):")
    for med, mv in p["medidores"].items():
        piores = [(era, contraste(mv["cor"], v["fundo"])) for era, v in p["eras"].items()]
        era, r = min(piores, key=lambda x: x[1])
        print(f"  {med:10} pior caso: {era} = {r:.2f}")
        if r < AA_GRAFICO:
            falhas.append(f"medidor {med} sobre fundo de {era} = {r:.2f} (mínimo {AA_GRAFICO})")

    print("\ncor de assinatura de cargo que exige contorno claro (< 3.0 em alguma era):")
    for pers, cor in p.get("cargos", p.get("personagens", {})).items():
        eras_ruins = [e for e, v in p["eras"].items() if contraste(cor, v["fundo"]) < AA_GRAFICO]
        if eras_ruins:
            print(f"  {pers:15} {', '.join(eras_ruins)}")

    print()
    for f in falhas:
        print(f"REPROVA  {f}")
    print(f"\n{len(falhas)} reprovação(ões).")
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
