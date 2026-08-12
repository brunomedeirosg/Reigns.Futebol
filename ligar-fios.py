#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Liga as batidas 1 (cartas de legado que já existem) às batidas 2 dos fios.

A batida 1 não é reescrita: ela só ganha um bloco 'fio' em cada opção. A opção
esquerda abre um caminho, a direita abre o outro — e é isso que faz a batida 3
ter quatro variantes em vez de uma.

Uso: python3 ferramentas/ligar-fios.py [--aplicar]
"""
import glob, json, os, sys

RAIZ = os.path.join(os.path.dirname(__file__), "..")

# batida 1  ->  (fio da esquerda, fio da direita)
LIGACOES = {
    "fisio_base_01":        ("fio_joelho_b2a",       "fio_joelho_b2b"),
    "apostas_estouro_01":   ("fio_apostas_b2a",      "fio_apostas_b2b"),
    "valdir_estouro_04":    ("fio_fundo_b2a",        "fio_fundo_b2b"),
    "capitao_duda_02":      ("fio_cicatriz_b2b",     "fio_cicatriz_b2a"),
    "imprensa_auge_01":     ("fio_microfone_b2a",    "fio_microfone_b2b"),
    "valdir_auge_02":       ("fio_laranja_b2a",      "fio_laranja_b2b"),
    "sucessor_declinio_01": ("fio_sucessor_b2a",     "fio_sucessor_b2b"),
    "filho_declinio_01":    ("fio_aniversario_b2a",  "fio_aniversario_b2b"),
    "treinador_declinio_04":("fio_licenca_b2a",      "fio_licenca_b2b"),
}

# a consequência chega entre 20 e 30 cartas depois — longe o bastante para você
# ter esquecido o número e perto o bastante para lembrar a cena
JANELA = {"em": [20, 30]}
JANELA_TARDE = {"em": [14, 22]}   # eras finais: a carreira pode não ter 30 cartas sobrando
ERAS_TARDIAS = {"declinio", "legado"}


def main():
    aplicar = "--aplicar" in sys.argv
    arquivos = sorted(glob.glob(os.path.join(RAIZ, "cartas", "*.json")))
    dados = {a: json.load(open(a, encoding="utf-8")) for a in arquivos}
    todas = {c["id"]: c for d in dados.values() for c in d["cartas"]}

    faltando = [x for par in LIGACOES.values() for x in par if x not in todas]
    if faltando:
        print("batidas 2 inexistentes:", faltando); sys.exit(1)

    n = 0
    for b1, (esq, dir_) in LIGACOES.items():
        c = todas.get(b1)
        if c is None:
            print(f"batida 1 '{b1}' não existe"); sys.exit(1)
        tardia = bool(set(c["era"]) & ERAS_TARDIAS) and "auge" not in c["era"]
        janela = JANELA_TARDE if tardia else JANELA
        c["esquerda"]["fio"] = {"id": esq, **janela}
        c["direita"]["fio"] = {"id": dir_, **janela}
        n += 1
        print(f"{b1:24} esq->{esq:22} dir->{dir_:22} janela {janela['em']}")

    print(f"\n{n} fios ligados · {n*6} cartas novas de consequência")

    if aplicar:
        for a, d in dados.items():
            json.dump(d, open(a, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("aplicado nos JSON.")
    else:
        print("(simulação — use --aplicar para gravar)")


main()
