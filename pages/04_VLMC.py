import streamlit as st
import numpy as np
import itertools
import numpy as np
from scipy.stats import chi2
import plotly.express as px
import pandas as pd

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
X = simular_vlmc(arvore, estados, T=50000, pi=pi, ordem_max=3)


def contagem_contextos(historico, ordem_max):

    contagens_transicao = {}

    # Para cada posição no histórico:
    for t in range(1, len(historico)):

        # Registrando contextos de tamanho 1 até a ordem máxima da cadeia:
        for k in range(1, min(ordem_max, t) + 1):

            # contexto mais recente primeiro; últimos k estados:
            contexto = tuple(reversed(historico[t-k:t]))

            proximo_estado = historico[t] #estado seguinte após contexto

            if contexto not in contagens_transicao:
                contagens_transicao[contexto] = {}

            # adiciona 1 na contagem de vezes que 'proximo_estado' aparece após 'contexto'
            contagens_transicao[contexto][proximo_estado] = (
                contagens_transicao[contexto].get(proximo_estado, 0) + 1
            )


    return contagens_transicao

contagens_transicao = contagem_contextos(X, 3)


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


from scipy.stats import chi2
import numpy as np

def teste_poda_contexto(historico, contexto_longo, alpha, m):

    # sufixo imediato (remove o estado mais antigo)
    contexto_curto = contexto_longo[:-1]
    df = estimar_probabilidades(historico)
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


df1 = teste_poda_contexto(X, ("B", "C",), 0.05, 3)
print(df1)



# Dúvida: os graus de liberdade da qui-quadrado estão certos?

