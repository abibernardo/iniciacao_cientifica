import streamlit as st
import numpy as np
import plotly.express as px

# -----------------------------
# TÍTULO E INTRODUÇÃO
# -----------------------------
st.title("Simulação de Cadeia de Markov de Primeira Ordem")
st.markdown("""
Passo a passo como uma **Cadeia de Markov de primeira ordem** funciona.

A dinâmica segue:
- Escolher o primeiro estado usando a **distribuição inicial**.
- Utilizar a **matriz de transição** para gerar os próximos estados.
- Visualizar a trajetória gerada.
""")

st.markdown("### Seção")

# Inicializa o estado
if "sec" not in st.session_state:
    st.session_state.sec = "Simulação"

# Cria as colunas para o layout horizontal
col1, col2 = st.columns(2)


# Funções de callback para manter o estado
def set_simul():
    st.session_state.sec = "Simulação"


def set_inter():
    st.session_state.sec = "Simulação interativa"


# Cria botões estilizados (agora persistentes)
with col1:
    st.button(
        "📄 Simulação",
        use_container_width=True,
        on_click=set_simul
    )

with col2:
    st.button(
        "🎛️ Interativa",
        use_container_width=True,
        on_click=set_inter
    )

# Valor final (persistente)
sec = st.session_state.sec

st.divider()
# -----------------------------
# PARÂMETROS
# -----------------------------
if sec == 'Simulação':
    st.header("Passo a Passo")
    st.markdown("""
    **Abaixo, define-se respectivamente os estados, as probabilidades iniciais, a matriz de transição e o número de passos da cadeia de markov:**
    """)

    st.code(
        """
        estados = ["A", "B", "C"] 

        pi = np.array([0.5, 0.3, 0.2]) 

        P = np.array([
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
        ])

        T = 20
        """
    )

    st.markdown("""
    **Cria-se a lista X. O primeiro estado é sorteado segundo a distribuição inicial, e adicionado à lista:**
    """)

    st.code(
        """
        X = []
        X.append(np.random.choice(estados, p=pi))
        """
    )

    st.markdown("""
    **O loop abaixo (do passo 1 ao passo T):**
    - Define o estado atual, que é o último estado adicionado à lista X
    - Define o index do estado atual (0, 1 ou 2 no nosso caso de 3 estados)
    - Sorteia o próximo estado, com as probabilidades da linha referente ao estado atual na matriz de transição
       * por exemplo, se o estado atual é B (segundo index), as probabilidades do próximo estado são referentes a segunda linha de P.
    - Adiciona o estado sorteado à lista X.

    """)

    st.code(
        """
        for t in range(1, T):
            estado_atual = X[-1]
            i = estados.index(estado_atual)
            proximo = np.random.choice(estados, p=P[i])
            X.append(proximo)
        """
    )

    estados = ["A", "B", "C"]

    m = len(estados)

    pi = np.array([0.5, 0.3, 0.2])

    P = np.array([
        [0.7, 0.2, 0.1],
        [0.3, 0.4, 0.3],
        [0.2, 0.3, 0.5]
    ])

    # -----------------------------
    # SIMULAÇÃO
    # -----------------------------
    st.header("Simulação da Cadeia")

    T = st.slider("Número de passos (T)", 5, 200, 20)

    X = []
    X.append(np.random.choice(estados, p=pi))  # primeiro estado

    for t in range(1, T):
        estado_atual = X[-1]  # Olhe onde a cadeia está (estado atual); último elemento de X
        i = estados.index(estado_atual)  # index do estado atual
        proximo = np.random.choice(estados, p=P[
            i])  # Escolhe o próximo estado com as probabilidades da LINHA da matriz de transição correspondente ao estado atual
        X.append(proximo)  # Adiciona o estado atual a lista

    indices = list(range(T))
    fig = px.scatter(x=indices, y=X, text=X, title=" ",
                     labels={"x": "Tempo (t)", "y": "Estado"})
    fig.update_traces(mode="lines+markers+text", textposition="top center")

    st.plotly_chart(fig)


elif sec == 'Simulação interativa':

    st.subheader("Número de estados")

    # Quantidade de estados
    m = st.number_input(" ", 2, 8, 3)

    # -----------------------------
    # NOME DOS ESTADOS
    # -----------------------------
    st.divider()
    st.subheader("Nomes dos estados")

    estados = []
    cols = st.columns(min(m, 4))  # até 4 colunas por linha

    for i in range(m):
        with cols[i % 4]:
            estados.append(
                st.text_input(f"Estado {i + 1}", value=f"E{i + 1}", key=f"estado_{i}")
            )

    # -----------------------------
    # DISTRIBUIÇÃO INICIAL π
    # -----------------------------
    st.divider()
    st.subheader("Distribuição Inicial (π)")

    pi_vals = []
    cols_pi = st.columns(min(m, 4))

    for i, est in enumerate(estados):
        with cols_pi[i % 4]:
            pi_vals.append(
                st.number_input(f"P({est})", 0.0, 1.0, 1.0 / m, key=f"pi_{i}")
            )

    pi = np.array(pi_vals)

    if pi.sum() == 0:
        st.error("A soma de π não pode ser zero.")
        st.stop()

    pi = pi / pi.sum()

    # -----------------------------
    # MATRIZ DE TRANSIÇÃO P
    # -----------------------------
    st.divider()
    st.subheader("Matriz de Transição (P)")

    P = np.zeros((m, m))

    for i in range(m):
        #st.markdown(f"**Linha: estado atual = {estados[i]}**")

        # criar colunas (até 4 por linha)
        cols_row = st.columns(min(m, 4))

        row_vals = []
        for j in range(m):
            with cols_row[j % 4]:
                row_vals.append(
                    st.number_input(
                        f"P({estados[i]} → {estados[j]})",
                        0.0, 1.0,
                        1.0 / m,
                        key=f"p_{i}_{j}"
                    )
                )

        row = np.array(row_vals)

        if row.sum() == 0:
            st.error(f"A linha do estado {estados[i]} não pode somar zero.")
            st.stop()

        P[i] = row / row.sum()
    # -----------------------------
    # VISUALIZAÇÃO DA MATRIZ DE TRANSIÇÃO
    # -----------------------------

    figP = px.imshow(
        P,
        text_auto=".2f",
        color_continuous_scale="Blues",
        labels=dict(x="Próximo estado", y="Estado atual", color="Probabilidade"),
        x=estados,
        y=estados,
        aspect="auto",
    )

    figP.update_layout(
        title=" ",
        xaxis_title="Próximo estado",
        yaxis_title="Estado atual",
        font=dict(size=14),
        coloraxis_colorbar=dict(
            thickness=20,
            len=0.75,
            title="Probabilidade",
            title_side="right"
        ),
    )

    figP.update_xaxes(side="top")
    st.divider()
    st.plotly_chart(figP, use_container_width=True)

    # Número de passos
    st.header("Simulação da Cadeia")
    T = st.slider("Número de passos (T)", 5, 300, 20)

    # ------------------------
    # SIMULAÇÃO
    # ------------------------
    X = []
    X.append(np.random.choice(estados, p=pi))

    for t in range(1, T):
        estado_atual = X[-1]
        idx = estados.index(estado_atual)
        proximo = np.random.choice(estados, p=P[idx])
        X.append(proximo)

    # Plot
    indices = list(range(T))
    fig = px.scatter(
        x=indices,
        y=X,
        text=X,
        title=" ",
        labels={"x": "Tempo (t)", "y": "Estado"},
    )
    fig.update_traces(mode="lines+markers+text", textposition="top center")
    st.plotly_chart(fig)

    # MATRIZ DE N PASSOS + VISUALIZAÇÃO
    # -----------------------------
    st.divider()
    st.header("Matriz de Transição de n Passos")

    n = st.slider("Escolha n para calcular Pⁿ", 1, 50, 5)
    P_n = np.linalg.matrix_power(P, n)

    # -----------------------------
    # HEATMAP DE Pⁿ
    # -----------------------------

    figPn = px.imshow(
        P_n,
        text_auto=".3f",
        color_continuous_scale="Viridis",
        labels=dict(
            x="Estado no futuro",
            y="Estado atual",
            color="Probabilidade"
        ),
        x=estados,
        y=estados,
        aspect="auto",
    )

    figPn.update_layout(
        title=f" ",
        xaxis_title="Próximo estado em n passos",
        yaxis_title="Estado atual",
        font=dict(size=14),
        coloraxis_colorbar=dict(
            thickness=18,
            len=0.75,
            title="Probabilidade",
            title_side="right",
        ),
    )

    # Coloca os nomes das colunas em cima
    figPn.update_xaxes(side="top")

    st.plotly_chart(figPn, use_container_width=True)

    st.info(
        "Interpretação: Pⁿ[i, j] é a probabilidade de estar no estado j depois de n passos, partindo do estado i. Com n alto, probabilidades convergem para distribuição estacionária.")
