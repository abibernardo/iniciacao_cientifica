import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd
from scipy.stats import chi2

historico = ["B", "C", "B", "A", "C", "A", "B", "C", "C", "A", "A", "B", "B", "C", "B"]

arvore = {

    # Hoje é A
    "A": [0.5, 0.3, 0.2],

    # Hoje é B
    "B": {

        # Ontem foi C
        "C": [0.2, 0.5, 0.3],
        # Ontem foi B
        "B": [0.3, 0.4, 0.3],
        # Ontem foi A
        "A": {
            # Anteontem foi A:
            "A": [0.7, 0.2, 0.1],
            # Anteontem foi B:
            "B": [0.4, 0.4, 0.2],
            # Anteontem foi C:
            "C": [0.5, 0.3, 0.2]
        }
    },

    # Hoje é C
    "C": {
        # Ontem foi A
        "A": [0.3, 0.4, 0.3],
        # Ontem foi B
        "B": [0.2, 0.5, 0.3],
        # Ontem foi C
        "C": [0.4, 0.3, 0.3]
    }
}


def achar_contexto(arvore, historico):
    contexto = arvore

    # percorre do mais recente para o mais antigo.
    # Se historico = [anteontem, ontem, hoje], então partimos de 'hoje' até 'anteontem'
    for s in list(reversed(historico)):

        # se já estamos numa folha → contexto encontrado, retona folha com probabilidades
        if isinstance(contexto, list):
            return contexto

        # se existe ramo correspondente, desce a árvore (estado anterior) e retorna ao loop
        if s in contexto:
            contexto = contexto[s]
        # se não existe ramo correspondente, sai do loop
        else:
            break  # não há mais aprofundamento possível

    # se terminamos numa lista, retornamos a folha com as probabilidades
    if isinstance(contexto, list):
        return contexto
    # Caso contrário, o historico não existe na árvore
    raise ValueError("Nenhum contexto encontrado.")


def simular_vlmc(arvore, estados, T, pi, ordem_max):
    # Passado inicial gerado da distribuição inicial
    X = [np.random.choice(estados, p=pi) for _ in range(ordem_max)]

    # Evolução da cadeia
    for t in range(ordem_max, T):
        historico = X[-ordem_max:]

        # Encontramos as probs de transição com a função auxiliar
        probs = achar_contexto(arvore, historico)

        # Sorteamos o próximo estado segundo essa distribuição
        proximo = np.random.choice(estados, p=probs)

        # Acrescentamos à sequência
        X.append(proximo)

    return X


estados = ["A", "B", "C"]
pi = np.array([0.5, 0.3, 0.2])


def contagem_contextos(historico, ordem_max):
    contagens_transicao = {}

    # Para cada posição no histórico:
    for t in range(1, len(historico)):

        # Registrando contextos de tamanho 1 até a ordem máxima da cadeia:
        for k in range(1, min(ordem_max, t) + 1):

            # contexto mais recente primeiro; últimos k estados:
            contexto = tuple(reversed(historico[t - k:t]))

            proximo_estado = historico[t]  # estado seguinte após contexto

            if contexto not in contagens_transicao:
                contagens_transicao[contexto] = {}

            # adiciona 1 na contagem de vezes que 'proximo_estado' aparece após 'contexto'
            contagens_transicao[contexto][proximo_estado] = (
                    contagens_transicao[contexto].get(proximo_estado, 0) + 1
            )

    return contagens_transicao


historico = simular_vlmc(arvore, estados, T=50000, pi=pi, ordem_max=4)

st.title("Variable Length Markov Chains (VLMC)")

if "sec" not in st.session_state:
    st.session_state.sec = "VLMC"

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.button("VLMC", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="VLMC"))
with col2:
    st.button("Simulação", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Simulação"))
with col3:
    st.button("Estimação", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Estimação"))
with col4:
    st.button("Verossimilhança", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Verossimilhança"))

sec = st.session_state.sec
st.divider()
# =====================================================
# O QUE É UM VLMC
if sec == "VLMC":
    # =====================================================
    st.header("O que é um VLMC")

    st.markdown(
        "Um **Variable Length Markov Chain (VLMC)** é um processo estocástico "
        "no qual o comprimento da memória relevante depende do passado observado."
    )

    st.markdown("Em uma cadeia de Markov de ordem fixa:")

    st.latex(
        r"P(X_t \mid X_{t-1}, X_{t-2}, \dots) = "
        r"P(X_t \mid X_{t-1}, \dots, X_{t-k})"
    )

    st.markdown("No VLMC, a dependência é dada por um **contexto**:")

    st.markdown(
        "onde $c(\\cdot)$ é o menor sufixo do passado necessário "
        "para determinar a distribuição de $X_t$."
    )

    st.info(
        "A memória não é fixa: alguns padrões exigem passado longo, "
        "outros apenas passado curto."
    )

    st.divider()

    # =====================================================
    # ÁRVORE DE CONTEXTOS
    # =====================================================
    st.header("Árvore de Contextos")

    st.markdown(
        "Os contextos formam uma **árvore de contextos** \\(\\tau\\), "
        "que satisfaz a **propriedade do sufixo**:"
    )

    st.markdown(
        "- Nenhum contexto é sufixo de outro  \n"
        "- Cada passado infinito admite exatamente um contexto"
    )

    st.markdown(
        "A árvore de contextos, junto com as probabilidades de transição, "
        "define completamente o VLMC."
    )

    st.divider()

    # =====================================================
    # DADOS E ESTIMAÇÃO
    # =====================================================
    st.header("Estimação")

    st.markdown("Considere uma amostra observada:")

    st.latex(r"X_1, X_2, \dots, X_n \in \mathcal{X}")

    st.markdown("Para um contexto \(w\), define-se a contagem:")

    st.latex(
        r"N(w) = \sum_{t=1}^n \mathbf{1}\{X_{t-|w|+1}^t = w\}"
    )

    st.markdown("A estimativa da probabilidade de transição é:")

    st.latex(
        r"\hat P(a \mid w) = \frac{N(wa)}{N(w)}"
    )

    st.markdown(
        "Essa é a **estimativa de máxima verossimilhança** "
        "associada a cada contexto."
    )

    st.divider()

    # =====================================================
    # IDEIA DO ALGORITMO
    # =====================================================
    st.header("Ideia do Context Algorithm")

    st.markdown(
        "O **Context Algorithm** estima simultaneamente:\n\n"
        "- a árvore de contextos\n"
        "- as probabilidades de transição\n\n"
    )

    st.success(
        "Começar com uma árvore de memória máxima e **podar contextos longos** "
        "que não produzem ganho estatístico relevante."
    )

    st.divider()

    # =====================================================
    # CRITÉRIO DE PODA
    # =====================================================
    st.header("Critério de Poda")

    st.markdown(
        "Para um contexto \(w\) e seu sufixo imediato \(v\), define-se:"
    )

    st.latex(
        r"\Delta_w = "
        r"N(w)\sum_{a\in\mathcal{X}} "
        r"\hat P(a\mid w)\log\frac{\hat P(a\mid w)}{\hat P(a\mid v)}"
    )

    st.markdown("Equivalentemente:")

    st.latex(
        r"\Delta_w = N(w)\cdot "
        r"\mathrm{KL}\big(\hat P(\cdot\mid w)\,\|\,\hat P(\cdot\mid v)\big)"
    )

    st.markdown("**Regra de decisão:**")

    st.markdown("Se $\\Delta_w \\ge K_n$, manter o contexto.")
    st.markdown("Se $\\Delta_w < K_n$, podar o contexto.")

    st.markdown("O cutoff cresce lentamente com a amostra:")

    st.latex(r"K_n = C\log n")

    st.warning(
        "Memória longa só é aceita quando melhora "
        "significativamente a verossimilhança."
    )

    st.divider()

    # =====================================================
    # PASSO A PASSO
    # =====================================================
    st.header("Passo a passo do algoritmo")

    st.markdown("**Passo 1 — Árvore máxima**")

    st.markdown("- Escolher profundidade máxima $m$")
    st.markdown("- Incluir todos os contextos observados com $|w| \\le m$")
    st.markdown("- Exigir $N(w) \\ge 2$")

    st.markdown("**Passo 2 — Poda bottom-up**")

    st.markdown("- Para cada nó terminal:")
    st.markdown("- Comparar o contexto $w$ com seu sufixo")
    st.markdown("- Calcular $\\Delta_w$")
    st.markdown("- Podar se $\\Delta_w < K_n$")

    st.markdown("**Passo 3 — Iterar**")
    st.markdown(
        "Repetir a poda até que nenhuma remoção adicional seja possível."
    )

    st.markdown("**Passo 4 — Estimação final**")

    st.latex(
        r"\hat P(a\mid c) = \frac{N(ca)}{N(c)}"
    )

    st.markdown(
        "O resultado final é a **árvore de contextos estimada** "
        "e o **VLMC ajustado por máxima verossimilhança**."
    )

    st.divider()

    # =====================================================
    # INTERPRETAÇÃO
    # =====================================================
    st.header("Interpretação")

    st.markdown(
        "- Cada poda corresponde a um **teste de razão de verossimilhança**\n"
        "que testa cada contexto contra seu sufixo"

    )

    st.caption("Rissanen (1983) • Bühlmann & Wyner (1999)")
elif sec == "Simulação":

    st.header("Representação da Estrutura")

    st.markdown(
        "A representação de árvore para a cadeia de ordem variável é a mesma que para cadeias de ordem fixa, com exceção que a profundidade da árvore varia com o contexto (galhos de tamanhos diferentes):")

    st.code(
        """
    arvore = {

    # Hoje é A
    "A": [0.5, 0.3, 0.2],

    # Hoje é B
    "B": {

        # Ontem foi C
        "C": [0.2, 0.5, 0.3],
        # Ontem foi B
        "B": [0.3, 0.4, 0.3],
        # Ontem foi A
        "A": {
            # Anteontem foi A:
            "A": [0.7, 0.2, 0.1],  
            # Anteontem foi B:
            "B": [0.4, 0.4, 0.2],  
            # Anteontem foi C:  
            "C": [0.5, 0.3, 0.2]   
        }
    },

    # Hoje é C
    "C": {
        # Ontem foi A
        "A": [0.3, 0.4, 0.3],
        # Ontem foi B
        "B": [0.2, 0.5, 0.3],
        # Ontem foi C
        "C": [0.4, 0.3, 0.3]
    }
}


        """,
        language="python"
    )
    st.markdown(
        "A ideia é que a árvore seja acessada do estado mais recente até o mais antigo, da forma **contexto = arvore[hoje][ontem][anteontem]**, até a folha (probabilidades de transição)")

    st.divider()
    st.header("Encontrando probabilidades de transição")
    st.markdown(
        "Para simular uma sequência gerada por uma vlmc, a função auxiliar abaixo encontra as probabilidades de transição, dada a árvore e o histórico.")
    st.markdown("1. Acessa a árvore por esse estado mais recente do histórico,")
    st.markdown(
        "2. Caminha pela árvore do estado mais recente até o mais antigo, até que não haja mais correspondência")
    st.markdown(
        "3. Retorna a folha com as probabilidades correspondentes ao contexto")

    st.code(
        """
    def achar_contexto(arvore, historico):
        contexto = arvore

        # percorre do mais recente para o mais antigo. 
        # Se historico = [anteontem, ontem, hoje], então partimos de 'hoje' até 'anteontem'
        for s in list(reversed(historico)):

            # se já estamos numa folha → contexto encontrado, retona folha com probabilidades
            if isinstance(contexto, list):
                return contexto

            # se existe ramo correspondente, desce a árvore (estado anterior) e retorna ao loop
            if s in contexto:
                contexto = contexto[s]
            # se não existe ramo correspondente, sai do loop
            else:
                break  # não há mais aprofundamento possível

        # se terminamos numa lista, retornamos a folha com as probabilidades
        if isinstance(contexto, list):
            return contexto
        # Caso contrário, o historico não existe na árvore
        raise ValueError("Nenhum contexto encontrado.")
        """,
        language="python"
    )

    st.divider()
    st.header("Simulação da VLMC")

    st.markdown("Para simular uma sequência:")
    st.markdown("1. Gera os primeiros estados a partir de uma dist inicial")
    st.markdown("2. Usa o histórico (lista X)")
    st.markdown("3. Usa a função auxiliar para encontrar probabilidades de transição dado o histórico")
    st.markdown("4. Gera próximo estado de acordo com essas probabilidades, e adiciona no histórico X.")

    st.code(
        """
    def simular_vlmc(arvore, estados, T, pi, ordem_max):
        # Passado inicial gerado da distribuição inicial
        X = [np.random.choice(estados, p=pi) for _ in range(ordem_max)]

        # Evolução da cadeia
        for t in range(ordem_max, T):

            #Pega os últimos ordem_max estados do histórico, sem inverter a ordem (do mais antigo até o mais novo)
            historico = X[-ordem_max:] 

            # Encontramos as probs de transição com a função auxiliar
            probs = achar_contexto(arvore, historico)

            # Sorteamos o próximo estado segundo essa distribuição
            proximo = np.random.choice(estados, p=probs)

            # Acrescentamos à sequência
            X.append(proximo)

        return X


    estados = ["A", "B", "C"]
    pi = np.array([0.5, 0.3, 0.2])
    seq = simular_vlmc(arvore, estados, T=20, pi=pi, ordem_max=4)
        """,
        language="python"
    )

    X = simular_vlmc(arvore, estados, T=20, pi=pi, ordem_max=4)

    indices = list(range(20))

    fig = px.scatter(
        x=indices,
        y=X,
        text=X,
        title="Trajetória gerada pela VLMC",
        labels={"x": "Tempo (t)", "y": "Estado"},
    )

    fig.update_traces(
        mode="lines+markers+text",
        textposition="top center",
    )

    st.plotly_chart(fig, use_container_width=True)




elif sec == "Estimação":

    st.markdown(
        "**Agora, vamos assumir que temos um histórico/sequência de estados gerados por uma VLMC desconhecida, e que queremos estimar as probs de transição.**")
    st.header("Contagem de contextos e transições")
    st.markdown(
        "Definindo uma ordem máxima possível para a cadeia, a função **'contagem_contextos'** retorna quantas vezes cada contexto é seguido por cada estado no historico.")
    st.markdown(
        "Para cada posição no histórico (loop externo), de 1 até a ordem máxima (loop interno), a função registra o contexto observado, registra o estado observado após o contexto, e faz a contagem.")

    st.code(
        """
    def contagem_contextos(historico, ordem_max):

        contagens_transicao = {}

        # Para cada posição no histórico:
        for t in range(1, len(historico)):

            # Registrando contextos de tamanho 1 até a ordem máxima da cadeia:
            for k in range(1, min(ordem_max, t) + 1):

                # Contexto mais recente primeiro (últimos k estados)
                contexto = tuple(reversed(historico[t - k:t]))

                # Estado seguinte após o contexto
                proximo_estado = historico[t]

                if contexto not in contagens_transicao:
                    contagens_transicao[contexto] = {}

                # Adiciona 1 na contagem de vezes que 'proximo_estado' aparece após 'contexto'
                contagens_transicao[contexto][proximo_estado] = (
                    contagens_transicao[contexto].get(proximo_estado, 0) + 1
                )

        return contagens_transicao


    # Lista X com um histórico de estados gerados por uma VLMC:
    contagens_transicao = contagem_contextos(X, 3)
        """,
        language="python"
    )

    st.header("Probabilidades de transição")

    st.markdown("""Agora, usando da função auxiliar **'contagem_contextos'** definida acima, vamos estimar as probabilidades de transição com 
    $$
    \\hat p(a \\mid c) = \\frac{N_{c,a}}{N_c}.
    $$
    """)

    st.markdown(
        "A baixo, a função **'estimar_probabilidades'** conta quantas vezes um contexto foi observado (loop externo), e quantas vezes cada estado foi observado após o contexto (loop interno)")
    st.markdown(
        "e retorna um dataframe com a contagem de quantas vezes ocorreu a transição de cada contexto para cada estado; o total de vezes que o contexto foi observado, e as probs de transição")

    st.code(
        """
    def estimar_probabilidades(historico):

        linhas = []
        contagens_transicao = contagem_contextos(historico, 3)

        for contexto, transicoes in contagens_transicao.items():

            total = sum(transicoes.values())

            for estado, contagem in transicoes.items():
                linhas.append({
                    "contexto": contexto,
                    "estado_seguinte": estado,
                    "cont_estado_seguinte": contagem,
                    "cont_total_contexto": total
                })

        df = pd.DataFrame(linhas)
        df['prob_transicao'] = df['cont_estado_seguinte'] / df['cont_total_contexto']

        return df

df = estimar_probabilidades(historico)
        """,
        language="python"
    )

    st.warning(
        "A função retorna todos os contextos existentes no histórico de tamanho até a ordem máxima definida, sem fazer nenhuma inferência sobre a árvore (se o contexto existe na árvore ou não).")

    st.divider()
    st.markdown(
        "Dada uma sequência de 60.000 estados ('historico') gerados pela árvore construída na parte de simulação, esse é o retorno da função **'estimar_probabilidades'** ")


    def estimar_probabilidades(historico):

        linhas = []
        contagens_transicao = contagem_contextos(historico, 3)

        for contexto, transicoes in contagens_transicao.items():

            total = sum(transicoes.values())

            for estado, contagem in transicoes.items():
                linhas.append({
                    "contexto": contexto,
                    "estado_seguinte": estado,
                    "cont_estado_seguinte": contagem,
                    "cont_total_contexto": total
                })

        df = pd.DataFrame(linhas)
        df['prob_transicao'] = df['cont_estado_seguinte'] / df['cont_total_contexto']

        return df


    df = estimar_probabilidades(historico)
    st.dataframe(df)

    st.success(
        "Para os contextos existentes na árvore usada para a simulação, as estimativas das probs de transição foram aproximadamente iguais as probabilidades reais."
    )


elif sec == "Verossimilhança":

    def estimar_probabilidades(historico):
        linhas = []
        contagens_transicao = contagem_contextos(historico, 3)

        for contexto, transicoes in contagens_transicao.items():

            total = sum(transicoes.values())

            for estado, contagem in transicoes.items():
                linhas.append({
                    "contexto": contexto,
                    "estado_seguinte": estado,
                    "cont_estado_seguinte": contagem,
                    "cont_total_contexto": total
                })

        df = pd.DataFrame(linhas)
        df['prob_transicao'] = df['cont_estado_seguinte'] / df['cont_total_contexto']

        return df


    def teste_poda_contexto(df, contexto_longo, alpha, m):

        # sufixo imediato (remove o estado mais antigo)
        contexto_curto = contexto_longo[:-1]

        # filtra dataframe
        df_w = df[df["contexto"] == contexto_longo]
        df_v = df[df["contexto"] == contexto_curto]

        if df_w.empty or df_v.empty:
            raise ValueError("Contexto ou sufixo não encontrado no dataframe.")

        # ----------------------------
        # 1) Log-verossimilhança do modelo completo (w)
        # ℓ_w = Σ_a N_{w,a} log(N_{w,a}/N_w)
        # ----------------------------

        Nw = df_w["cont_total_contexto"].iloc[0]
        ell_w = 0.0

        for _, linha in df_w.iterrows():
            Nwa = linha["cont_estado_seguinte"]
            if Nwa > 0:
                ell_w += Nwa * np.log(Nwa / Nw)

        # ----------------------------
        # 2) Log-verossimilhança do modelo reduzido (v)
        # ℓ_v = Σ_a N_{w,a} log(N_{v,a}/N_v)
        # ----------------------------

        Nv = df_v["cont_total_contexto"].iloc[0]
        ell_v = 0.0

        for _, linha in df_w.iterrows():

            estado = linha["estado_seguinte"]
            Nwa = linha["cont_estado_seguinte"]

            linha_v = df_v[df_v["estado_seguinte"] == estado]

            if linha_v.empty:
                continue

            Nva = linha_v["cont_estado_seguinte"].iloc[0]

            if Nva > 0:
                ell_v += Nwa * np.log(Nva / Nv)

        # ----------------------------
        # 3) Estatística LR
        # LR = 2(ℓ_w − ℓ_v)
        # ----------------------------

        LR = 2 * (ell_w - ell_v)

        # graus de liberdade
        df_graus = m - 1

        p_value = 1 - chi2.cdf(LR, df=df_graus)

        decisao = "manter contexto" if p_value < alpha else "podar contexto"

        return {
            "contexto_testado": contexto_longo,
            "sufixo": contexto_curto,
            "ell_w": ell_w,
            "ell_v": ell_v,
            "LR": LR,
            "df": df_graus,
            "p_value": p_value,
            "decisao": decisao
        }


    df = estimar_probabilidades(historico)
    poda_galho = teste_poda_contexto(df, ("B", "C", "A"), 0.05, 3)

    st.markdown(
        "**Agora, partindo das contagens dos contextos, queremos podar os galhos e definir quais contextos existem na árvore real.**")
    st.header("Cálculo da Verossimilhança")
    st.markdown("Podemos calcular a verossimilhança de cada contexto usando a função **estimar_probabilidades**,")
    st.markdown("e realizar o teste de razão de verossimilhança para testar a significância de um contexto longo, com relação ao seu 'pai' (eliminando estado mais antigo)")
    st.markdown("""Lembrando que a log-verossimilhança de uma cadeia (que será calculada para o contexto fornecido e para seu sufixo) é
    $$
    \\ell(\\theta)
    =
    \\sum_{c \\in \\mathcal{A}^k}
    \\sum_{a \\in \\mathcal{A}}
    N_{c,a} \\, \\log \\frac{N_{c,a}}{N_c}
    $$
    """)
    st.code(
        """
def teste_poda_contexto(df, contexto_longo, alpha, m):

    # sufixo imediato (remove o estado mais antigo)
    contexto_curto = contexto_longo[:-1]

    # filtra dataframe
    df_w = df[df["contexto"] == contexto_longo]
    df_v = df[df["contexto"] == contexto_curto]

    if df_w.empty or df_v.empty:
        raise ValueError("Contexto ou sufixo não encontrado no dataframe.")

    # ----------------------------
    # 1) Log-verossimilhança do modelo completo (w)
    # ℓ_w = Σ_a N_{w,a} log(N_{w,a}/N_w)
    # ----------------------------

    Nw = df_w["cont_total_contexto"].iloc[0]
    ell_w = 0.0

    for _, linha in df_w.iterrows():
        Nwa = linha["cont_estado_seguinte"]
        if Nwa > 0:
            ell_w += Nwa * np.log(Nwa / Nw)

    # ----------------------------
    # 2) Log-verossimilhança do modelo reduzido (v)
    # ℓ_v = Σ_a N_{w,a} log(N_{v,a}/N_v)
    # ----------------------------

    Nv = df_v["cont_total_contexto"].iloc[0]
    ell_v = 0.0

    for _, linha in df_w.iterrows():

        estado = linha["estado_seguinte"]
        Nwa = linha["cont_estado_seguinte"]

        linha_v = df_v[df_v["estado_seguinte"] == estado]

        if linha_v.empty:
            continue

        Nva = linha_v["cont_estado_seguinte"].iloc[0]

        if Nva > 0:
            ell_v += Nwa * np.log(Nva / Nv)

    # ----------------------------
    # 3) Estatística LR
    # LR = 2(ℓ_w − ℓ_v)
    # ----------------------------

    LR = 2 * (ell_w - ell_v)

    # graus de liberdade
    df_graus = m - 1

    p_value = 1 - chi2.cdf(LR, df=df_graus)

    decisao = "manter contexto" if p_value < alpha else "podar contexto"

    return {
        "contexto_testado": contexto_longo,
        "sufixo": contexto_curto,
        "ell_w": ell_w,
        "ell_v": ell_v,
        "LR": LR,
        "df": df_graus,
        "p_value": p_value,
        "decisao": decisao
    }

df = estimar_probabilidades(X)
poda_galho = teste_poda_contexto(df, ("B", "C", "A"), 0.05, 3)
        """,
        language="python"
    )
    st.divider()
    st.header("Resultado")
    st.write(poda_galho)
    st.success(
        "Função poda galhos de acordo com os contextos existentes na árvore usada para simulação"
    )
