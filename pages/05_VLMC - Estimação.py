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
    sufixo = contexto_longo[:-1]

    # filtra dataframe do sufixo
    df_v = df[df["contexto"] == sufixo]

    # encontra TODOS os contextos filhos do sufixo
    contextos_filhos = [
        c for c in df["contexto"].unique()
        if len(c) == len(sufixo) + 1 and c[:-1] == sufixo
    ]

    # ----------------------------
    # 1) Log-verossimilhança do modelo completo (SOMA DOS FILHOS)
    # ----------------------------

    ell_w = 0.0

    for contexto in contextos_filhos:

        df_w = df[df["contexto"] == contexto]
        Nw = df_w["cont_total_contexto"].iloc[0]

        for _, linha in df_w.iterrows():
            Nwa = linha["cont_estado_seguinte"]
            ell_w += Nwa * np.log(Nwa / Nw)

    # ----------------------------
    # 2) Log-verossimilhança do modelo reduzido
    # ----------------------------

    Nv = df_v["cont_total_contexto"].iloc[0]
    ell_v = 0.0

    for _, linha in df_v.iterrows():
        Nva = linha["cont_estado_seguinte"]

        ell_v += Nva * np.log(Nva / Nv)

    # ----------------------------
    # 3) Estatística LR
    # ----------------------------

    LR = 2 * (ell_w - ell_v)

    # graus de liberdade (mantido igual ao seu)
    df_graus = (m * (m - 1)) - (m - 1)

    p_value = 1 - chi2.cdf(LR, df=df_graus)

    decisao = "manter contexto" if p_value < alpha else "podar contexto"

    return {
        "sufixo_testado": sufixo,
        "filhos": contextos_filhos,
        "ell_w": ell_w,
        "ell_v": ell_v,
        "LR": LR,
        "df": df_graus,
        "p_value": p_value,
        "decisao": decisao
    }

def podar_arvore(df, alpha, m):
    contextos = set(df["contexto"].unique())

    # todos os sufixos possíveis
    sufixos = {c[:-1] for c in contextos if len(c) > 1}

    # testar primeiro os mais longos; substituir pra testar do mais curto ao mais longo?
    sufixos_ordenados = sorted(sufixos, key=len, reverse=True)

    contextos_restantes = set(contextos)
    resultados = []

    for sufixo in sufixos_ordenados:

        filhos = [c for c in contextos_restantes if c[:-1] == sufixo]

        if len(filhos) == 0:
            continue

        # pegar qualquer filho para chamar sua função
        contexto_longo = filhos[
            0]  # ideia de simplificação: mudar função "Teste poda contexto" para ter o sufixo como argumento

        resultado = teste_poda_contexto(df, contexto_longo, alpha, m)
        resultados.append(resultado)

        if resultado["decisao"] == "podar contexto":

            for f in filhos:
                contextos_restantes.discard(f)  # se podar, descarta todos os filhos

        else:
            if sufixo in contextos_restantes:
                contextos_restantes.discard(sufixo)  # Se não podar, descarta o sufixo como 'contexto mínimo'

    return contextos_restantes, resultados


historico = simular_vlmc(arvore, estados, T=50000, pi=pi, ordem_max=3)

X = historico

st.title("Variable Length Markov Chains (VLMC)")
st.write("Estimação das probabilidades de transição e teste de razão de verossimilhança do sufixo contra seus contextos filhos (poda da árvore)")

if "sec" not in st.session_state:
    st.session_state.sec = "VLMC"

col3, col4 = st.columns(2)

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




if sec == "Estimação":

    st.write("Dado que simulamos uma sequência gerada por essa árvore de contextos:")

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
        "**Vamos assumir que tal sequência foi gerada por uma VLMC desconhecida, e que queremos estimar as probs de transição.**")
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





    df = estimar_probabilidades(historico)
    st.dataframe(df)

    st.success(
        "Para os contextos existentes na árvore usada para a simulação, as estimativas das probs de transição foram aproximadamente iguais as probabilidades reais."
    )


elif sec == "Verossimilhança":

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

    st.markdown("Abaixo, testo a verossimilhança do sufixo (B, A ) contra a soma das log-verossimilhanças de (B, C, A), (B, C, B) e (B, C, C)")

    st.code(
        """
df = estimar_probabilidades(historico)

def teste_poda_contexto(df, contexto_longo, alpha, m):
    # sufixo imediato (remove o estado mais antigo)
    sufixo = contexto_longo[:-1]

    # filtra dataframe do sufixo
    df_v = df[df["contexto"] == sufixo]

    # encontra TODOS os contextos filhos do sufixo
    contextos_filhos = [
        c for c in df["contexto"].unique()
        if len(c) == len(sufixo) + 1 and c[:-1] == sufixo
    ]

    # ----------------------------
    # 1) Log-verossimilhança do modelo completo (SOMA DOS FILHOS)
    # ----------------------------

    ell_w = 0.0

    for contexto in contextos_filhos:

        df_w = df[df["contexto"] == contexto]
        Nw = df_w["cont_total_contexto"].iloc[0]

        for _, linha in df_w.iterrows():
            Nwa = linha["cont_estado_seguinte"]
            ell_w += Nwa * np.log(Nwa / Nw)

    # ----------------------------
    # 2) Log-verossimilhança do modelo reduzido
    # ----------------------------

    Nv = df_v["cont_total_contexto"].iloc[0]
    ell_v = 0.0

    for _, linha in df_v.iterrows():

        Nva = linha["cont_estado_seguinte"]

        ell_v += Nva * np.log(Nva / Nv)

    # ----------------------------
    # 3) Estatística LR
    # ----------------------------

    LR = 2 * (ell_w - ell_v)

    # graus de liberdade (mantido igual ao seu)
    df_graus = (m*(m-1))-(m - 1)

    p_value = 1 - chi2.cdf(LR, df=df_graus)

    decisao = "manter contexto" if p_value < alpha else "podar contexto"

    return {
        "sufixo_testado": sufixo,
        "filhos": contextos_filhos,
        "ell_w": ell_w,
        "ell_v": ell_v,
        "LR": LR,
        "df": df_graus,
        "p_value": p_value,
        "decisao": decisao
    }


poda = teste_poda_contexto(df, ("B", "C", "A"), 0.05, 3)
print(poda)
        """,
        language="python"
    )
    st.divider()
    st.header("Resultado")
    df = estimar_probabilidades(historico)
    poda_galho = teste_poda_contexto(df, ("B","C", "A"), 0.05, 3)
    st.write(poda_galho)
    st.success(
        "Função poda galhos de acordo com os contextos existentes na árvore usada para simulação"
    )
    st.write("Agora, aplicamos essa função para testarmos todos os sufixos possíveis dentro da profundidade 3:")

    st.code(
        """
def podar_arvore(df, alpha, m):
    contextos = set(df["contexto"].unique())

    # todos os sufixos possíveis
    sufixos = {c[:-1] for c in contextos if len(c) > 1}

    # testar primeiro os mais longos; substituir pra testar do mais curto ao mais longo?
    sufixos_ordenados = sorted(sufixos, key=len, reverse=True)

    contextos_restantes = set(contextos)
    resultados = []

    for sufixo in sufixos_ordenados:

        filhos = [c for c in contextos_restantes if c[:-1] == sufixo]

        if len(filhos) == 0:
            continue

        # pegar qualquer filho para chamar sua função
        contexto_longo = filhos[0]  # ideia de simplificação: mudar função "Teste poda contexto" para ter o sufixo como argumento

        resultado = teste_poda_contexto(df, contexto_longo, alpha, m)
        resultados.append(resultado)

        if resultado["decisao"] == "podar contexto":

            for f in filhos:
                contextos_restantes.discard(f) # se podar, descarta todos os filhos

        else:
            if sufixo in contextos_restantes:
                contextos_restantes.discard(sufixo)  # Se não podar, descarta o sufixo como 'contexto mínimo'

    return contextos_restantes, resultados


contextos_finais, historico_podas = podar_arvore(df, 0.03, 3)
        """,
        language="python"
    )

    st.markdown("""'historico_podas' armazena o retorno da função **'teste_poda_contexto'** para cada sufixo, e o dicionário **'contextos_finais'** armazena os contextos mínimos significativos""")
    st.write("No caso de nossa simulação, esses foram os contextos mínimos considerados significativos após a poda:")


    contextos_finais, historico_podas = podar_arvore(df, 0.03, 3)

    contextos_legiveis = sorted(["".join(c) for c in contextos_finais])

    df_contextos = pd.DataFrame({"Contexto": contextos_legiveis})

    st.dataframe(df_contextos)

    st.success(
        "Os contextos mínimos são os mesmos contextos " 
        "existentes na nossa árvore usada para simulação"
    )
