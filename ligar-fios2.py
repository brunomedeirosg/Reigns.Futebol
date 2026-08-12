#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Segunda rodada de ligações: as 27 cartas de legado que ainda não abriam fio.

Decisão de design tomada aqui, e o motivo:

  27 cartas de legado NÃO precisam de 27 fios privados. Cinco cartas do arco das
  apostas não merecem cinco acertos de contas separados pelo mesmo pecado — elas
  merecem entrar no MESMO fio, por portas diferentes. O motor descarta a marcação
  quando a batida já foi vivida, então a primeira porta é a que vale.

  Isso troca 162 cartas por 54, e o jogo fica melhor: o arco das apostas passa a
  ter uma espinha longa com cinco entradas, em vez de cinco espinhas curtas.

Regra de mapeamento: a opção que AFUNDA vai para o ramo 'a', a que AFASTA vai
para o ramo 'b'. Não é o lado da tela, é o sentido da escolha.

Uso: python3 ferramentas/ligar-fios2.py [--aplicar]
"""
import glob, json, os, sys

RAIZ = os.path.join(os.path.dirname(__file__), "..")

# carta de legado -> (fio da esquerda, fio da direita, janela)
# janela None = usa o padrão da era
LIGACOES = {
    # arco das apostas: 5 portas para o mesmo fio tardio
    "apostas_travessia_01":  ("fio_aptarde_b2a", "fio_aptarde_b2b", [20, 30]),
    "apostas_auge_01":       ("fio_aptarde_b2b", "fio_aptarde_b2a", [18, 28]),
    "apostas_auge_02":       ("fio_aptarde_b2a", "fio_aptarde_b2b", [18, 28]),
    "apostas_declinio_01":   ("fio_aptarde_b2b", "fio_aptarde_b2a", [14, 22]),
    "apostas_declinio_02":   ("fio_aptarde_b2a", "fio_aptarde_b2b", [14, 22]),

    # o empresário: 2 portas
    "valdir_estouro_02":     ("fio_valdir_b2a", "fio_valdir_b2b", [20, 30]),
    "valdir_auge_03":        ("fio_valdir_b2a", "fio_valdir_b2b", [18, 28]),

    # a voz: 4 portas
    "imprensa_auge_02":      ("fio_voz_b2a", "fio_voz_b2b", [18, 28]),
    "imprensa_declinio_01":  ("fio_voz_b2a", "fio_voz_b2b", [14, 22]),
    "treinador_iracema_02":  ("fio_voz_b2a", "fio_voz_b2b", [18, 28]),
    "treinador_iracema_04":  ("fio_voz_b2a", "fio_voz_b2b", [18, 28]),

    # a herança: 3 portas
    "sucessor_legado_01":    ("fio_heranca_b2a", "fio_heranca_b2b", [6, 12]),
    "treinador_declinio_02": ("fio_heranca_b2a", "fio_heranca_b2b", [14, 22]),
    "coord_base_legado_01":  ("fio_heranca_b2a", "fio_heranca_b2b", [6, 12]),

    # cartas que entram em fios que já existem, sem carta nova nenhuma
    "fisio_estouro_01":      ("fio_joelho_b2b", "fio_joelho_b2a", [20, 30]),
    "diretor_auge_02":       ("fio_fundo_b2b", "fio_fundo_b2a", [18, 28]),
    "filho_legado_02":       ("fio_aniversario_b2b", "fio_aniversario_b2a", [6, 12]),
}

# mortes súbitas: só a opção que sobrevive abre fio — a que matou tem final, não
# consequência. Em todas as dez, a opção segura é a da direita.
MORTES = {
    "morte_base_peneira":        "fio_peneira_b2",
    "morte_base_apito":          "fio_apito_b2",
    "morte_estouro_tatuagem":    "fio_tatuagem_b2",
    "morte_estouro_carro":       "fio_carro_b2",
    "morte_travessia_procuracao":"fio_procuracao_b2",
    "morte_travessia_live":      "fio_live_b2",
    "morte_auge_var":            "fio_var_b2",
    "morte_auge_helicoptero":    "fio_helicoptero_b2",
    "morte_auge_selecao":        "fio_selecao_b2",
    "morte_declinio_aposta":     "fio_duzentos_b2",
}
JANELA_MORTE = [16, 26]


def main():
    aplicar = "--aplicar" in sys.argv
    arquivos = sorted(glob.glob(os.path.join(RAIZ, "cartas", "*.json")))
    dados = {a: json.load(open(a, encoding="utf-8")) for a in arquivos}
    todas = {c["id"]: c for d in dados.values() for c in d["cartas"]}

    faltando = [x for par in LIGACOES.values() for x in par[:2] if x not in todas]
    faltando += [x for x in MORTES.values() if x not in todas]
    faltando += [x for x in list(LIGACOES) + list(MORTES) if x not in todas]
    if faltando:
        print("ids inexistentes:", sorted(set(faltando))); sys.exit(1)

    for b1, (esq, dir_, janela) in LIGACOES.items():
        c = todas[b1]
        c["esquerda"]["fio"] = {"id": esq, "em": janela}
        c["direita"]["fio"] = {"id": dir_, "em": janela}
        print(f"{b1:24} esq->{esq:22} dir->{dir_:22} {janela}")

    print()
    for b1, alvo in MORTES.items():
        c = todas[b1]
        segura = "esquerda" if "morte" in c["direita"] else "direita"
        c[segura]["fio"] = {"id": alvo, "em": JANELA_MORTE}
        print(f"{b1:28} {segura:8} -> {alvo:22} {JANELA_MORTE}")

    leg = [c for c in todas.values() if c.get("peso_dramatico") == "legado"
           and not c["id"].startswith("fio_")]
    com_fio = [c for c in leg if any(c[l].get("fio") for l in ("esquerda", "direita"))]
    print(f"\n{len(LIGACOES)} + {len(MORTES)} cartas ligadas nesta rodada")
    print(f"cartas de legado com fio: {len(com_fio)} de {len(leg)}")
    sem = sorted(c["id"] for c in leg if c not in com_fio)
    if sem:
        print("ainda sem fio:", sem)

    if aplicar:
        for a, d in dados.items():
            json.dump(d, open(a, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("aplicado nos JSON.")
    else:
        print("(simulação — use --aplicar para gravar)")


main()
