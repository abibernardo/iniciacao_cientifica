import streamlit as st
import numpy as np
import plotly.express as px

# -----------------------------
# TÍTULO E INTRODUÇÃO
# -----------------------------
st.title("Simulação de Cadeia de Markov de Primeira Ordem")
st.markdown("""
Esta aplicação demonstra passo a passo como uma **Cadeia de Markov de primeira ordem** funciona.

A dinâmica segue:
- Escolher o primeiro estado usando a **distribuição inicial**.
- Utilizar a **matriz de transição** para gerar os próximos estados.
- Visualizar a trajetória gerada.
""")

# -----------------------------
# PARÂMETROS
# -----------------------------
st.header("1. Parâmetros da Cadeia")

estados = ["A", "B", "C"]
m = len(estados)

st.write("**Estados:**", estados)

pi = np.array([0.5, 0.3, 0.2])
st.write("**Distribuição inicial (π):**", pi)

P = np.array([
    [0.7, 0.2, 0.1],
    [0.3, 0.4, 0.3],
    [0.2, 0.3, 0.5]
])

st.write("**Matriz de transição (P):**")
st.dataframe(P)

T = st.slider("Número de passos (T)", 5, 200, 20)

# -----------------------------
# SIMULAÇÃO
# -----------------------------
st.header("2. Simulação da Cadeia")

X = []
X.append(np.random.choice(estados, p=pi))  # primeiro estado

for t in range(1, T):
    estado_atual = X[-1]
    i = estados.index(estado_atual)
    proximo = np.random.choice(estados, p=P[i])
    X.append(proximo)

st.write("Trajetória gerada:")
st.write(X)

# -----------------------------
# EXPLICAÇÃO PASSO-A-PASSO
# -----------------------------
st.header("3. Explicação passo-a-passo")
st.markdown("""
- O primeiro estado é sorteado segundo a distribuição inicial.
- Cada próximo estado é sorteado com base na linha correspondente da matriz de transição.
- Isso garante a **propriedade de Markov de ordem 1**: apenas o estado atual importa.
""")

# -----------------------------
# GRÁFICO (PLOTLY)
# -----------------------------
st.header("4. Visualização da Trajetória (Plotly)")

indices = list(range(T))
fig = px.scatter(x=indices, y=X, text=X, title="Trajetória da Cadeia de Markov",
                 labels={"x": "Tempo (t)", "y": "Estado"})
fig.update_traces(mode="lines+markers+text", textposition="top center")

st.plotly_chart(fig)

st.success("Simulação concluída!")
