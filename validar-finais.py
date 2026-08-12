#!/usr/bin/env python3
"""
Validador dos finais do CRAQUE.

Uso:  python3 ferramentas/validar-finais.py [finais.json] ["cartas/*.json"]

Checa:
  1. simetria — toda família tem exatamente N finais (regras.finais_por_familia)
  2. todo família tem exatamente 1 dourado e 1 genérico, e o genérico é o ÚLTIMO
  3. o dourado combina pelo menos K fatores distintos (regras.fatores_minimos_no_dourado)
  4. nenhum final é inalcançável por ordem (um final sem condição antes do fim mata os seguintes)
  5. toda flag exigida por um final é produzida por alguma carta, pelo motor, ou é derivada
  6. ids únicos, molduras válidas, todo final tem texto

Sai com código 1 se houver erro.
"""
import glob
import json
import sys

MOLDURAS = {"dourada", "prata", "cinza", "preta"}

erros, avisos = [], []


def fatores(cond):
    """Quantos eixos distintos uma condição combina."""
    n = 0
    n += len(cond.get("flags", []))
    n += len(cond.get("flags_qualquer", [])) and 1
    n += len(cond.get("sem_flags", []))
    n += len(cond.get("medidores", {}))
    n += len(cond.get("estatisticas", {}))
    n += 1 if "era" in cond else 0
    n += 1 if "idade" in cond else 0
    n += 1 if "marca_de_alma" in cond else 0
    n += 1 if "medidores_entre" in cond else 0
    return n


def flags_exigidas(cond):
    return (set(cond.get("flags", []))
            | set(cond.get("flags_qualquer", []))
            | set(cond.get("sem_flags", [])))


def main():
    args = sys.argv[1:]
    caminho_finais = args[0] if args else "finais.json"
    padroes = args[1:] or ["cartas/*.json"]

    dados = json.load(open(caminho_finais, encoding="utf-8"))
    regras = dados["regras"]
    derivadas = set(dados.get("flags_derivadas", {}))
    do_motor = set(dados.get("flags_do_motor", {}))
    pendentes = dados.get("flags_pendentes", {})

    # --- flags que o conteúdo realmente produz, e onde ---
    produzidas = set()
    origem = {}          # flag -> [(id_da_carta, eras)]
    arquivos = [f for p in padroes for f in glob.glob(p)]
    for arq in arquivos:
        for c in json.load(open(arq, encoding="utf-8"))["cartas"]:
            for lado in ("esquerda", "direita"):
                o = c[lado]
                for bloco in (o, o.get("sucesso", {}), o.get("falha", {})):
                    if isinstance(bloco, dict):
                        for fl in bloco.get("flags", []):
                            produzidas.add(fl)
                            origem.setdefault(fl, []).append((c["id"], c["era"]))
    disponiveis = produzidas | do_motor | derivadas | set(pendentes)

    # uma flag declarada como pendente que já ganhou carta deve sair da lista
    for fl in sorted(set(pendentes) & produzidas):
        avisos.append(f"flag '{fl}' está em flags_pendentes mas já é produzida por carta — "
                      f"remover de flags_pendentes")

    ids = set()
    bloqueados = {}   # final -> flags pendentes que o tornam inalcançável hoje
    print(f"=== {caminho_finais} ===")
    print(f"flags disponíveis: {len(produzidas)} de cartas ({len(arquivos)} arquivos) "
          f"+ {len(do_motor)} do motor + {len(derivadas)} derivadas "
          f"+ {len(pendentes)} pendentes\n")

    total = 0
    for chave, fam in dados["familias"].items():
        finais = fam["finais"]
        total += len(finais)
        dourados = [f for f in finais if f["moldura"] == "dourada"]
        genericos = [f for f in finais if not f["condicoes"]]

        n_alvo = regras["finais_por_familia"]
        marca = "ok" if len(finais) == n_alvo else f"ESPERADO {n_alvo}"
        print(f"{chave:16} {len(finais)} finais  {len(dourados)} dourado(s)  "
              f"{len(genericos)} genérico(s)   {marca}")

        if len(finais) != n_alvo:
            erros.append(f"{chave}: {len(finais)} finais (regra: {n_alvo}) — quebra a simetria")
        if len(dourados) != regras["dourados_por_familia"]:
            erros.append(f"{chave}: {len(dourados)} dourados (regra: {regras['dourados_por_familia']})")
        if len(genericos) != regras["genericos_por_familia"]:
            erros.append(f"{chave}: {len(genericos)} genéricos (regra: {regras['genericos_por_familia']})")
        if genericos and finais[-1] is not genericos[0]:
            erros.append(f"{chave}: o genérico não é o último da lista — ele engole os finais seguintes")

        for d in dourados:
            n = fatores(d["condicoes"])
            if n < regras["fatores_minimos_no_dourado"]:
                erros.append(f"{chave}/{d['id']}: dourado combina só {n} fator(es) "
                             f"(mínimo {regras['fatores_minimos_no_dourado']}) — fácil demais")

        for i, f in enumerate(finais):
            if f["id"] in ids:
                erros.append(f"id de final duplicado: {f['id']}")
            ids.add(f["id"])
            if f["moldura"] not in MOLDURAS:
                erros.append(f"{f['id']}: moldura '{f['moldura']}' inválida")
            if not f.get("texto", "").strip():
                erros.append(f"{f['id']}: sem texto")
            if not f["condicoes"] and i < len(finais) - 1:
                erros.append(f"{f['id']}: sem condição na posição {i} — "
                             f"torna inalcançáveis os {len(finais) - i - 1} finais seguintes")
            exigidas = flags_exigidas(f["condicoes"])
            for fl in sorted(exigidas - disponiveis):
                erros.append(f"{f['id']}: exige a flag '{fl}', que nenhuma carta produz "
                             f"e que não está declarada como pendente")
            travando = sorted(exigidas & set(pendentes))
            if travando:
                bloqueados[f["id"]] = travando

    print(f"\ncontexto: {len(dados['contexto'])} finais · "
          f"fim natural: {len(dados.get('fim_natural',[]))} · "
          f"morte súbita: {len(dados.get('mortes_subitas',[]))}")
    for f in dados["contexto"] + dados.get("fim_natural", []) + dados.get("mortes_subitas", []):
        if f["id"] in ids:
            erros.append(f"id de final duplicado: {f['id']}")
        ids.add(f["id"])
        faltando = flags_exigidas(f.get("condicoes", {})) - disponiveis
        for fl in sorted(faltando):
            erros.append(f"{f['id']}: exige a flag '{fl}', que nenhuma carta produz")

    total += len(dados["contexto"]) + len(dados.get("fim_natural", [])) + len(dados.get("mortes_subitas", []))
    dourados_total = sum(1 for fam in dados["familias"].values()
                         for f in fam["finais"] if f["moldura"] == "dourada")
    dourados_total += sum(1 for f in dados["contexto"] if f["moldura"] == "dourada")
    artes = len(dados["familias"]) + len(dados["contexto"])
    print(f"\nTOTAL: {total} finais · {dourados_total} dourados · {artes} ilustrações")

    if bloqueados:
        print(f"\n--- BACKLOG: {len(bloqueados)} final(is) inalcançável(is) até a carta existir ---")
        for fid, fls in sorted(bloqueados.items()):
            for fl in fls:
                print(f"  {fid:24} espera '{fl}'")
                print(f"  {'':24}   → {pendentes[fl]}")

    # --- alcançabilidade dos dourados ---
    ORDEM = ["base", "estouro", "travessia", "auge", "declinio", "legado"]
    print("\n--- ALCANÇABILIDADE DOS DOURADOS ---")
    todos_dourados = [(k, f) for k, fam in dados["familias"].items()
                      for f in fam["finais"] if f["moldura"] == "dourada"]
    todos_dourados += [("contexto", f) for f in dados["contexto"] if f["moldura"] == "dourada"]

    for fam, f in todos_dourados:
        cond = f["condicoes"]
        eras_ok = cond.get("era")
        limite = max(ORDEM.index(e) for e in eras_ok) if eras_ok else len(ORDEM) - 1
        linhas, problema = [], False

        # grupo OR: robusto se a SOMA das fontes do grupo for > 1
        grupo = cond.get("flags_qualquer", [])
        if grupo:
            fontes_grupo = sum(len(origem.get(fl, [])) for fl in grupo)
            cedo_g = min((min(ORDEM.index(e) for e in eras)
                          for fl in grupo for _, eras in origem.get(fl, [])), default=None)
            if fontes_grupo == 0:
                linhas.append(f"      qualquer de {len(grupo)}          SEM FONTE")
                problema = True
            else:
                extra = "  ← FONTE ÚNICA" if fontes_grupo == 1 else ""
                if extra:
                    avisos.append(f"{f['id']}: o grupo OR {grupo} tem uma fonte só — o dourado depende dela")
                linhas.append(f"      qualquer de {len(grupo):<2} flags      "
                              f"{fontes_grupo} carta(s), 1ª em {ORDEM[cedo_g]}{extra}")

        for fl in sorted(flags_exigidas(cond) - set(grupo)):
            if fl in derivadas:
                linhas.append(f"      {fl:26} derivada pelo motor")
                continue
            if fl in do_motor:
                linhas.append(f"      {fl:26} escrita pelo motor")
                continue
            fontes = origem.get(fl, [])
            if not fontes:
                linhas.append(f"      {fl:26} SEM FONTE")
                problema = True
                continue
            cedo = min(min(ORDEM.index(e) for e in eras) for _, eras in fontes)
            aviso_era = ""
            if cedo > limite:
                aviso_era = f"  ← só nasce em {ORDEM[cedo]}, DEPOIS do final"
                problema = True
            if len(fontes) == 1 and not aviso_era:
                aviso_era = "  ← FONTE ÚNICA"
                avisos.append(f"{f['id']}: depende de '{fl}', produzida por uma carta só "
                              f"({fontes[0][0]}) — se ela não sair, o dourado morre")
            linhas.append(f"      {fl:26} {len(fontes)} carta(s), 1ª em {ORDEM[cedo]}{aviso_era}")
        n = fatores(cond)
        print(f"  [{'!' if problema else 'ok'}] {f['nome']:34} ({fam}, {n} fatores)")
        for ln in linhas:
            print(ln)
        if problema:
            avisos.append(f"{f['id']}: dourado com flag sem fonte ou tardia demais — pode ser inalcançável")

    print()
    for a in avisos:
        print(f"AVISO  {a}")
    for e in erros:
        print(f"ERRO   {e}")
    print(f"\n{len(erros)} erro(s), {len(avisos)} aviso(s).")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
