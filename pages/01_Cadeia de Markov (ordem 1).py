import streamlit as st
import numpy as np
import itertools
import plotly.express as px
import pandas as pd


st.title("Cadeia de Markov de Ordem K")

st.markdown("""
Passo a passo de como funciona uma **Cadeia de Markov de ordem K**, onde  
o próximo estado depende dos **K últimos estados**.
""")

# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------


if "sec" not in st.session_state:
    st.session_state.sec = "Simulação"

col1, col2 = st.columns(2)

with col1:
    st.button("📄 Simulação", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Simulação"))
with col2:
    st.button("🎛️ Interativa", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Simulação interativa"))

sec = st.session_state.sec

st.divider()


# ---------------------------------------------------------
# SIMULAÇÃO
# ---------------------------------------------------------
if sec == 'Simulação':

    st.header("Passo a Passo")
    st.markdown("""
    **Definimos:**
    - os estados  
    - a ordem K  
    - o número de passos T  
    """)

    st.code(
        """
        estados = ["A", "B", "C"]

        K = 3  

        T = 20
        """
    )

    st.markdown("""
    Agora, criamos uma lista com todas as combinações possíveis de K estados consecutivos —  
    chamadas de **contextos**.

    O número total de combinações é $$\t{Estados}^K$$
    """)

    st.code(
        """
        contextos = list(itertools.product(estados, repeat=K))
        # Exemplo para K=2: [("A","A"), ("A","B"), ("A","C"), ("B","A"), ("B","B")..., ("C","C")]
        """
    )

    st.markdown("""
    Em seguida, **construímos a *árvore* de contexto**, que é um dicionário onde:

   - **Chaves** → Combinações dos últimos K estados (contextos)  
   - **Valores** → Vetor de probabilidade do próximo estado dado o contexto
    """)

    st.code(
        """
        arvore = {}

        for ctx in contextos:
            p = np.random.rand(len(estados))  # Gera vetor de probabilidade p para estados
            p = p / p.sum()  # normaliza p
            arvore[ctx] = p  # adiciona contexto à árvore e atribúi probabilidade p

        """
    )

    st.markdown("""
    Agora:
    - Definimos probabilidades iniciais pi  
    - Criamos a lista X  
    - Sorteamos os primeiros K estados de forma independente  
    - Adicionamos esses K estados iniciais à lista X  
    """)

    st.code(
        """
        pi = np.array([0.5, 0.3, 0.2])

        X = []
        for _ in range(K):
            X.append(np.random.choice(estados, p=pi))
        """
    )

    st.markdown("""
    **O loop abaixo (do passo K ao passo T):**

    - Define o contexto atual (últimos K estados na lista X)  
    - Busca na árvore o vetor de probabilidade correspondente ao contexto 
    - Sorteia o próximo estado baseado no vetor acima
    - Adiciona à lista X  
    - Repete  
    """)

    st.code(
        """
        for t in range(K, T):
            contexto = tuple(X[-K:]) 
            probs = arvore[contexto] 
            proximo = np.random.choice(estados, p=probs) 
            X.append(proximo)
        """
    )

    estados = ["A", "B", "C"]
    K = 3
    T = 20

    contextos = list(itertools.product(estados, repeat=K))

    arvore = {}
    for ctx in contextos:
        p = np.random.rand(len(estados))
        p = p / p.sum()
        arvore[ctx] = p

    pi = np.array([0.5, 0.3, 0.2])

    # Gerar estados iniciais
    X = [np.random.choice(estados, p=pi) for _ in range(K)]

    caminho = []  # para registrar passo a passo

    # Loop da simulação
    for t in range(K, T):
        contexto = tuple(X[-K:])
        probs = arvore[contexto]
        proximo = np.random.choice(estados, p=probs)
        X.append(proximo)

        caminho.append({
            "Passo": t,
            "Contexto usado": contexto,
            "Probabilidades": np.round(probs, 3),
            "Próximo estado": proximo
        })

    # -------------------------------------------
    # GRÁFICO DA TRAJETÓRIA (Cadeia de ordem K)
    # -------------------------------------------

    st.header("Trajetória Gerada pela Cadeia")

    indices = list(range(T))

    fig = px.scatter(
        x=indices,
        y=X,
        text=X,
        title=" ",
        labels={"x": "Tempo (t)", "y": "Estado"},
    )

    fig.update_traces(
        mode="lines+markers+text",
        textposition="top center",
    )

    st.plotly_chart(fig, use_container_width=True)


elif sec == "Simulação interativa":

    # -----------------------------------------------------
    # NÚMERO DE ESTADOS
    # -----------------------------------------------------
    st.subheader("Número de estados")
    m = st.number_input(" ", 2, 8, 3)

    # -----------------------------------------------------
    # NOME DOS ESTADOS
    # -----------------------------------------------------
    st.divider()
    st.subheader("Nomes dos estados")

    estados = []
    cols = st.columns(min(m, 4))

    for i in range(m):
        with cols[i % 4]:
            estados.append(
                st.text_input(f"Estado {i+1}", value=f"E{i+1}", key=f"estado_{i}")
            )

    # -----------------------------------------------------
    # DISTRIBUIÇÃO INICIAL π
    # -----------------------------------------------------
    st.divider()
    st.subheader("Distribuição Inicial (π)")

    pi_vals = []
    cols_pi = st.columns(min(m, 4))

    for i, est in enumerate(estados):
        with cols_pi[i % 4]:
            pi_vals.append(
                st.number_input(f"P({est})", 0.0, 1.0, 1.0/m, key=f"pi_{i}")
            )

    pi = np.array(pi_vals)
    if pi.sum() == 0:
        st.error("A soma de π não pode ser zero.")
        st.stop()

    pi = pi / pi.sum()

    # -----------------------------------------------------
    # ORDEM K DA CADEIA
    # -----------------------------------------------------
    st.divider()
    st.subheader("Ordem da Cadeia (K)")

    K = st.number_input("Escolha a ordem K", 1, 5, 2)

    # -----------------------------------------------------
    # ÁRVORE (TRANSIÇÕES DE ORDEM K)
    # -----------------------------------------------------
    st.divider()
    st.subheader("Árvore de Probabilidades")

    contextos = list(itertools.product(estados, repeat=K))
    arvore = {}

    for ctx in contextos:
        cols_row = st.columns(min(m, 4))

        probs = []
        for j in range(m):
            with cols_row[j % 4]:
                probs.append(
                    st.number_input(
                        f"P({ctx} → {estados[j]})",
                        0.0, 1.0,
                        1.0/m,
                        key=f"ctx_{'_'.join(ctx)}_{j}"
                    )
                )

        probs = np.array(probs)
        if probs.sum() == 0:
            st.error(f"As probabilidades do contexto {ctx} não podem somar zero.")
            st.stop()

        probs = probs / probs.sum()
        arvore[ctx] = probs

    # -----------------------------------------------------

    # -----------------------------------------------------
    # SIMULAÇÃO DA CADEIA
    # -----------------------------------------------------
    st.divider()
    st.header("Simulação da Cadeia")

    T = st.slider("Número de passos (T)", 5, 300, 20)

    # SORTEIO DOS K PRIMEIROS ESTADOS
    X = []
    for _ in range(K):
        X.append(np.random.choice(estados, p=pi))

    # SIMULAÇÃO
    caminho_contextos = []

    for t in range(K, T):
        contexto = tuple(X[-K:])
        probs = arvore[contexto]
        proximo = np.random.choice(estados, p=probs)
        caminho_contextos.append(str(contexto))
        X.append(proximo)

    # -----------------------------------------------------
    # PLOT DA TRAJETÓRIA
    # -----------------------------------------------------
    indices = list(range(T))
    fig = px.scatter(
        x=indices,
        y=X,
        text=X,
        title="Trajetória da Cadeia de Ordem K",
        labels={"x": "Tempo (t)", "y": "Estado"},
    )
    fig.update_traces(mode="lines+markers+text", textposition="top center")
    st.plotly_chart(fig)

    # -----------------------------------------------------
