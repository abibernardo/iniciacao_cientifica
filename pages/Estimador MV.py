from pathlib import Path
import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd
import math
from scipy.stats import chi2

np.random.seed(42)

estados = ["A", "B", "C"]
n = 2000

sequencia = list(np.random.choice(estados, size=n))

k = 3

contagens_transicao = {}   # dict: contexto -> dict de contagens de estados seguintes
total_contexto = {}        # dict: contexto -> número total de vezes que o contexto ocorreu



"""
# exemplo pra ver a probabilidade de transição:
contexto = ("A", "A", "B")

for estado in estados:
    print(
        f"P({estado} | {contexto}) =",
        contagens_transicao[contexto].get(estado, 0) / total_contexto[contexto]
    )
"""



def log_verossimilhanca_markov(sequencia, estados, k):
    contagens_transicao = {}
    total_contexto = {}

    for t in range(k, len(sequencia)):
        contexto = tuple(sequencia[t-k:t])
        proximo_estado = sequencia[t]

        if contexto not in contagens_transicao:
            contagens_transicao[contexto] = {}
            total_contexto[contexto] = 0

        contagens_transicao[contexto][proximo_estado] = \
            contagens_transicao[contexto].get(proximo_estado, 0) + 1
        total_contexto[contexto] += 1

    ell = 0.0
    for contexto, contagens in contagens_transicao.items():
        Nk_c = total_contexto[contexto]
        for Nk_ca in contagens.values():
            ell += Nk_ca * math.log(Nk_ca / Nk_c)

    return ell

ell_k   = log_verossimilhanca_markov(sequencia, estados, k)
ell_k1  = log_verossimilhanca_markov(sequencia, estados, k+1)

LR = 2 * (ell_k1 - ell_k)



p_value = 1 - chi2.cdf(LR, df=(len(estados)-1)*(len(estados)**k))

print(p_value)
