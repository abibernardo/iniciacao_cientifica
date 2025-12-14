from pathlib import Path
import plotly.express as px
import streamlit as st
import numpy as np
import pandas as pd

sequencia = [
    "A", "A", "B", "C", "A", "A", "B", "A",
    "C", "B", "A", "C", "C", "A", "B"
]

estados = ["A", "B", "C"]
k = 3

contagens_transicao = {}   # dict: contexto -> dict de contagens de estados seguintes
total_contexto = {}        # dict: contexto -> número total de vezes que o contexto ocorreu

for t in range(k, len(sequencia)):
    contexto = tuple(sequencia[t-k:t])     # contexto (X_{t-k}, ..., X_{t-1})
    proximo_estado = sequencia[t]           # estado observado no tempo t (X_t)

    if contexto not in contagens_transicao:
        contagens_transicao[contexto] = {}
        total_contexto[contexto] = 0

    if proximo_estado not in contagens_transicao[contexto]:
        contagens_transicao[contexto][proximo_estado] = 0

    # Incrementa N_{contexto, j}
    contagens_transicao[contexto][proximo_estado] += 1

    # Incrementa N_{contexto}
    total_contexto[contexto] += 1


# Criando as estimações das probs de transição (em forma de árvore):

arvore_emv = {}

for contexto in contagens_transicao:
    no = arvore_emv  # Posição atual na árvore

    # desce na árvore seguindo o contexto
    for estado_contexto in contexto:
        if estado_contexto not in no:
            no[estado_contexto] = {}
        no = no[estado_contexto]   # 'aprofundando' a árvore

    # folha: probabilidades EMV
    for estado in estados:
        no[estado] = (
            contagens_transicao[contexto].get(estado, 0)  # Se o estado apareceu → usa a contagem, Se nunca apareceu → retorna 0
            / total_contexto[contexto]
        )
