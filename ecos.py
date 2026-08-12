#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Os ecos de legado — UM POR CAMINHO, não um por carta.

Correção do Bruno, 11/08: o eco aparecia igual para os dois lados, o que é o
oposto do que ele existe para fazer. Um eco que não muda com a escolha não
promete consequência nenhuma — só decora.

Regras (rodada-peso §5):
  - nunca dizem O QUE mudou; dizem que ficou;
  - são específicos DAQUELE caminho, não intercambiáveis entre os dois lados;
  - máximo 60 caracteres;
  - nenhum se repete no baralho inteiro.

Cartas de morte súbita só têm eco do lado que sobrevive: quem morreu tem final.

Uso: python3 ferramentas/ecos.py [--aplicar]
"""
import glob, json, os, sys

RAIZ = os.path.join(os.path.dirname(__file__), "..")

# id da carta -> (eco da esquerda, eco da direita).  None = lado fatal, sem eco.
ECOS = {
 # ---------- o arco das apostas ----------
 "apostas_estouro_01":  ("Agora eles têm o seu telefone.",
                         "Eles anotaram que você sabe dizer não."),
 "apostas_travessia_01":("Eles sabem esperar melhor do que você.",
                         "Duas recusas viram fama antes de virar hábito."),
 "apostas_auge_01":     ("Sair no meio custa mais do que entrar.",
                         "Ele já sabia a resposta antes de perguntar."),
 "apostas_auge_02":     ("Seu nome agora abre sozinho, sem você.",
                         "Alguém vai aparecer nessa tela. Não você."),
 "apostas_declinio_01": ("Romper com plateia tem outro preço.",
                         "O moleque vai repetir isso a vida inteira."),
 "apostas_declinio_02": ("O mercado descobriu quanto você vale hoje.",
                         "Você saiu antes de ser dispensado."),
 "fio_aptarde_b3aa":    ("As quatro datas viraram quatro perguntas.",
                         "Muro limpo, e todo mundo lembra do que tinha."),
 "fio_aptarde_b3ab":    ("Não assinar era o começo de outra coisa.",
                         "O advogado falou. Ninguém ouviu você."),
 "fio_aptarde_b3ba":    ("Você pagou para sair e disse quanto.",
                         "O moleque vai descobrir o valor sozinho."),
 "fio_aptarde_b3bb":    ("Você falou depois de abrir o documentário.",
                         "O vídeo elogiando ficou fixado no perfil."),
 "fio_apostas_b3aa":    ("Mudar de ideia na frente da câmera.",
                         "Aquele vídeo tem legenda em quatro idiomas."),
 "fio_apostas_b3ab":    ("Recusar duas vezes é posição, não susto.",
                         "Você está na foto oficial, com a marca."),
 "fio_apostas_b3ba":    ("A faixa levou três semanas para ser costurada.",
                         "Eles costuraram e você agradeceu por telefone."),
 "fio_apostas_b3bb":    ("Rasgar na frente dele foi para ele ver.",
                         "Perguntar o valor já era metade da resposta."),

 # ---------- o corpo ----------
 "capitao_duda_02":     ("Ele levantou o meião por um motivo.",
                         "Você escolheu a mesma cicatriz que ele."),
 "fisio_base_01":       ("O joelho tem memória melhor que a sua.",
                         "Três semanas paradas custaram a peneira."),
 "fisio_estouro_01":    ("Ela anotou a data no prontuário e sublinhou.",
                         "Cinco jogos passaram sem você e foram cinco."),
 "fio_peneira_b3a":     ("Você tirou a piada e tiraram o cachê junto.",
                         "A maionese daquele sábado virou piada paga."),
 "fio_peneira_b3b":     ("Dois dias sumidos e o clube contando.",
                         "Sete quilos abaixo por três temporadas."),
 "fio_joelho_b3aa":     ("O corpo aceitou o acordo. Você também.",
                         "Você foi atrás de uma coisa que não volta."),
 "fio_joelho_b3ab":     ("Sair no aquecimento de uma decisão.",
                         "Ela guardou o número daquele aquecimento."),
 "fio_joelho_b3ba":     ("O departamento médico ouviu a sua versão.",
                         "O médico soube quem disse o nome dele."),
 "fio_joelho_b3bb":     ("Chegar antes da notícia custa a notícia.",
                         "O laudo bom tinha uma segunda via."),
 "fio_cicatriz_b3aa":   ("Voltar a chegar antes aos trinta e dois.",
                         "Você parou de treinar dobrado e ninguém viu."),
 "fio_cicatriz_b3ab":   ("A diferença entre as duas coxas tinha número.",
                         "A cicatriz dele tinha vinte centímetros."),
 "fio_cicatriz_b3ba":   ("Alguém contou ao moleque como você treinava.",
                         "O moleque anotou e vai treinar igual."),
 "fio_cicatriz_b3bb":   ("Você entrou no gramado sem ter respondido.",
                         "Ele se aposentou e você não respondeu nada."),

 # ---------- dinheiro e quem cuida dele ----------
 "valdir_estouro_02":   ("A planilha zerou e ele guardou o arquivo.",
                         "Aquela interrogação era o contrato inteiro."),
 "valdir_estouro_04":   ("Ele disse sim antes de você. Isso não volta.",
                         "Você é a única pessoa que não te vendeu."),
 "valdir_auge_02":      ("Advogado abre gaveta que não fecha mais.",
                         "A assinatura era sua. O resto se descobre."),
 "valdir_auge_03":      ("Dez anos terminaram no terceiro toque.",
                         "Ele disse nós. Você ouviu bem."),
 "diretor_auge_02":     ("Assinaram na mesma página por um motivo.",
                         "Separar as duas coisas foi caro e foi seu."),
 "fio_fundo_b3aa":      ("Trinta meses fora e o país esqueceu o rosto.",
                         "A escada tinha um degrau que não subia."),
 "fio_fundo_b3ab":      ("Você negociou sozinho e eles anotaram isso.",
                         "Um fundo sai e outro entra pela mesma porta."),
 "fio_fundo_b3ba":      ("O celular parou de tocar e ficou parado.",
                         "Contrato curto vence sempre num mês ruim."),
 "fio_fundo_b3bb":      ("Cinco anos é muito tempo para os dois lados.",
                         "Metade do contrato virou um cargo depois."),
 "fio_valdir_b3aa":     ("Você levantou da mesa e ocupou o microfone.",
                         "Ele falou de ingratidão e ficou sem resposta."),
 "fio_valdir_b3ab":     ("Dez anos de linhas, uma por uma.",
                         "Ficar sentado tinha um preço por temporada."),
 "fio_valdir_b3ba":     ("Sua mãe deixou de receber o mercado dele.",
                         "Você parou de contar no terceiro item."),
 "fio_valdir_b3bb":     ("Ela quase assinou, e ligou depois.",
                         "Gentileza de dez anos vira dívida sozinha."),
 "fio_laranja_b3aa":    ("Papel para uma coisa que não tinha papel.",
                         "Os dois contratos que faltavam tinham motivo."),
 "fio_laranja_b3ab":    ("Quatro contratos eram quatro de seis.",
                         "Seu nome está no topo do organograma."),
 "fio_laranja_b3ba":    ("Ele te ouviu antes de ler no jornal. Contou.",
                         "Recusar palco sobre ética também é notícia."),
 "fio_laranja_b3bb":    ("O contador voltou de viagem com uma pasta.",
                         "Engano de nome funciona uma vez só."),
 "fio_procuracao_b3a":  ("Você não assinou em branco. Ele reparou.",
                         "Conversar primeiro foi o que ele pediu."),
 "fio_procuracao_b3b":  ("Ela guardou na gaveta e esperou você.",
                         "Ele conseguiu do mesmo jeito, sem você."),
 "fio_carro_b3a":       ("Ele numerou quinze anos e você só viu hoje.",
                         "Ele nunca falou do empréstimo outra vez."),
 "fio_carro_b3b":       ("Rasgar depois não desfaz ter pedido.",
                         "O recibo existe e alguém guardou cópia."),

 # ---------- o microfone ----------
 "imprensa_auge_01":    ("O garoto viu o que você fez com o microfone.",
                         "O garoto também viu o que você não fez."),
 "imprensa_auge_02":    ("O vestiário feminino assistiu inteiro.",
                         "Existe um vídeo curto dessa resposta."),
 "imprensa_declinio_01":("O clube soube o que você faz com a versão dele.",
                         "A lesão que não existiu está no boletim."),
 "treinador_iracema_02":("Ela ouviu você antes de ouvir o comentarista.",
                         "O microfone chegou em você primeiro. E passou."),
 "treinador_iracema_04":("A nota do clube fica no site. A sua também.",
                         "A nota do clube ficou sozinha no site."),
 "fio_microfone_b3aa":  ("Não assinar cláusula padrão vira caso.",
                         "Duas vezes no ar não é mais um deslize."),
 "fio_microfone_b3ab":  ("O garoto da arquibancada tem nome e idade.",
                         "A entrevista dele fica na internet."),
 "fio_microfone_b3ba":  ("Cinco minutos num estacionamento vazio.",
                         "Souberam exatamente para onde você apontou."),
 "fio_microfone_b3bb":  ("Ele viu você olhar para o chão naquele dia.",
                         "Ele foi sozinho e falou o que deu."),
 "fio_voz_b3aa":        ("Dizer que não sabe é raro o bastante.",
                         "Falar duas vezes te transformou em pauta fixa."),
 "fio_voz_b3ab":        ("Você falou uma vez e parou. Ele reparou.",
                         "Ele trouxe anotado e levou de volta."),
 "fio_voz_b3ba":        ("Concordar depois vale menos, e você sabia.",
                         "A faixa continua sem o seu nome."),
 "fio_voz_b3bb":        ("Uma década depois ainda é uma década depois.",
                         "Cada um falou o seu. O seu ficou em branco."),
 "fio_apito_b3a":       ("O vestiário te empurrou e ficou olhando.",
                         "Dois anos de boa conduta foram anotados."),
 "fio_apito_b3b":       ("A arquibancada percebeu antes da arbitragem.",
                         "Sua ficha na arbitragem tem seis anos."),
 "fio_live_b3a":        ("Você falou sóbrio e depois foi conversar.",
                         "A faixa tinha o seu nome e você honrou."),
 "fio_live_b3b":        ("Dois sem clube dão uma audiência só.",
                         "Seu colega está sem clube há dois anos."),
 "fio_var_b3a":         ("Vinte mil bandeirinhas já estavam impressas.",
                         "A figurinha do aplauso ainda circula."),
 "fio_var_b3b":         ("Sua desculpa formal virou modelo.",
                         "Ele copiou o gesto e não copiou o resto."),
 "fio_selecao_b3a":     ("A janela era de doze horas e você dormiu.",
                         "Existe gravação daquela ligação."),
 "fio_helicoptero_b3a": ("A previsão daquela noite estava certa.",
                         "Ela perguntou uma vez e você foi treinar."),
 "fio_helicoptero_b3b": ("Cortar quatro contratos aparece no extrato.",
                         "Quatro festas rendem quatro álbuns de fotos."),
 "fio_tatuagem_b3a":    ("Vinte e duas linhas com o seu apelido.",
                         "O bolão do vestiário tem quatro anos de arquivo."),
 "fio_tatuagem_b3b":    ("Você pagou em dinheiro e virou história boa.",
                         "Pedir para mudarem a música é mudar a letra."),

 # ---------- família ----------
 "filho_declinio_01":   ("Ele vai lembrar do sábado, não do gol.",
                         "O gol saiu. Ele estava dormindo."),
 "filho_legado_02":     ("Um ano inteiro em casa é muito tempo.",
                         "Ele perguntou uma vez. Não pergunta de novo."),
 "fio_aniversario_b3aa":("Dez dias fora custaram exatamente dez dias.",
                         "O documento existe e você prometeu por ele."),
 "fio_aniversario_b3ab":("Ele montou o álbum sozinho, no computador.",
                         "Ele parou de perguntar quando você volta."),
 "fio_aniversario_b3ba":("Ele jogou dois anos sem dizer o seu nome.",
                         "Você decidiu o que era melhor pelos dois."),
 "fio_aniversario_b3bb":("Alguém filmou você na beira do campinho.",
                         "Tirar o vídeo é mais visto que o vídeo."),
 "fio_selecao_b3b":     ("Você nunca vestiu aquela camisa. Ele reparou.",
                         "A camisa comprada tem o nome de outro."),

 # ---------- o que vem depois de você ----------
 "sucessor_declinio_01":("O vestiário inteiro ouviu a sua resposta.",
                         "Ele perguntou na frente de todo mundo. E ouviu."),
 "sucessor_legado_01":  ("A primeira foto da estreia dele já tem dono.",
                         "Da tribuna dá para ver tudo, menos ele."),
 "treinador_declinio_02":("Ele pediu sinceridade e anotou o que ouviu.",
                          "Os defeitos que você apontou foram corrigidos."),
 "treinador_declinio_04":("Março chega e a inscrição tem o seu nome.",
                          "Março chega todo ano. A vaga, não."),
 "coord_base_legado_01":("Dois anos de aula por um crachá.",
                         "A base inteira cresce com essa resposta."),
 "fio_sucessor_b3aa":   ("Ele pediu para jogar com você. Isso não se pede.",
                         "Vocês dois saíram na mesma semana."),
 "fio_sucessor_b3ab":   ("Você trocou de vestiário sem ninguém pedir.",
                         "Ele aprendeu a jogar sozinho e aprendeu bem."),
 "fio_sucessor_b3ba":   ("Você concordou em público e alguém guardou.",
                         "Disputar um campo de treino com um nome."),
 "fio_sucessor_b3bb":   ("Procurar primeiro é sempre mais caro.",
                         "Você corrigiu o moleque na frente do país."),
 "fio_duzentos_b3a":    ("Você apostou um café e ele viu.",
                         "Corrigir a frase na frente da base inteira."),
 "fio_duzentos_b3b":    ("Você é o nome mais velho daquela lista.",
                         "Duzentos reais por semana durante dois anos."),
 "fio_licenca_b3aa":    ("Você faltou a jogos por uma sala de aula.",
                         "A licença abriu porta e você pegou a grande."),
 "fio_licenca_b3ab":    ("Recomeçar aos trinta e cinco tem plateia.",
                         "A aula reposta nunca foi reposta."),
 "fio_licenca_b3ba":    ("Seu nome entrou numa lista e não saiu mais.",
                         "Ele explicou devagar para você entender bem."),
 "fio_licenca_b3bb":    ("Ele perguntou e você foi olhar o calendário.",
                         "Você disse que ainda era jogador. E era."),
 "fio_heranca_b3aa":    ("Duas tardes por semana durante três anos.",
                         "O programa tem o seu nome na porta."),
 "fio_heranca_b3ab":    ("Um garoto de quinze bateu e você abriu.",
                         "O crachá saiu. As duas tardes, não."),
 "fio_heranca_b3ba":    ("Sua frase virou o título da matéria.",
                         "Ele repete a frase achando que é dele."),
 "fio_heranca_b3bb":    ("Você levou a primeira e deixou a última.",
                         "A matéria fechou sem uma linha sua."),

 # ---------- mortes súbitas: só quem sobreviveu tem eco ----------
 "morte_base_peneira":        (None, "Sua mãe vai contar essa no Natal inteiro."),
 "morte_base_apito":          (None, "O apito daquele jogo ainda te encontra."),
 "morte_estouro_tatuagem":    (None, "Aquele vídeo já saiu do vestiário."),
 "morte_estouro_carro":       (None, "O marketing guardou o arquivo bruto."),
 "morte_travessia_procuracao":(None, "Aquele campo em branco tem dono agora."),
 "morte_travessia_live":      (None, "Catorze pessoas viram. Uma delas gravou."),
 "morte_auge_var":            (None, "A câmera do VAR também filma pra fora."),
 "morte_auge_helicoptero":    (None, "Aquela noite tinha duas versões possíveis."),
 "morte_auge_selecao":        (None, "Amanhã é depois do prazo que ele deu."),
 "morte_declinio_aposta":     (None, "Alguém no vestiário apostou os duzentos."),
}


def main():
    aplicar = "--aplicar" in sys.argv
    todos = [e for par in ECOS.values() for e in par if e]

    longos = [(e, len(e)) for e in todos if len(e) > 60]
    repetidos = {e for e in todos if todos.count(e) > 1}
    if longos:
        print("ECOS LONGOS:", longos); sys.exit(1)
    if repetidos:
        print("ECOS REPETIDOS:", repetidos); sys.exit(1)

    arquivos = sorted(glob.glob(os.path.join(RAIZ, "cartas", "*.json")))
    dados = {a: json.load(open(a, encoding="utf-8")) for a in arquivos}
    cartas = {c["id"]: c for d in dados.values() for c in d["cartas"]}

    legado = {cid for cid, c in cartas.items() if c.get("peso_dramatico") == "legado"}
    faltando = legado - set(ECOS)
    sobrando = set(ECOS) - legado
    if faltando:
        print("cartas de legado sem eco:", sorted(faltando)); sys.exit(1)
    if sobrando:
        print("ecos sem carta:", sorted(sobrando)); sys.exit(1)

    n = 0
    for cid, (esq, dir_) in ECOS.items():
        c = cartas[cid]
        c.pop("eco", None)   # o eco sai do nível da carta e vai para o da opção
        for lado, texto in (("esquerda", esq), ("direita", dir_)):
            c[lado].pop("eco", None)
            if texto is None:
                if "morte" not in c[lado]:
                    print(f"AVISO {cid}/{lado}: eco None num lado que não é fatal")
                continue
            if "morte" in c[lado]:
                print(f"ERRO {cid}/{lado}: eco num lado fatal — quem morre tem final"); sys.exit(1)
            c[lado]["eco"] = texto
            n += 1

    print(f"{n} ecos em {len(ECOS)} cartas de legado "
          f"· maior {max(len(e) for e in todos)} chars · média {sum(map(len, todos))/len(todos):.0f}")

    if aplicar:
        for a, d in dados.items():
            json.dump(d, open(a, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        print("aplicado nos JSON.")
    else:
        print("(simulação — use --aplicar para gravar)")


main()
