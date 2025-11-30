import streamlit as st
import numpy as np
import itertools
import plotly.express as px

st.title("Simulação de Cadeia de Markov de Segunda Ordem")
st.markdown("""
Passo a passo de como funciona uma **Cadeia de Markov de ordem 2**, onde  
o próximo estado depende dos **dois últimos estados**.
""")

st.markdown("### Seção")

# Inicializa o estado
if "sec" not in st.session_state:
    st.session_state.sec = "Simulação"

# Layout horizontal
col1, col2 = st.columns(2)

# Funções de callback
def set_simul():
    st.session_state.sec = "Simulação"

def set_inter():
    st.session_state.sec = "Simulação interativa"

# Botões
with col1:
    st.button("📄 Simulação", use_container_width=True, on_click=set_simul)
with col2:
    st.button("🎛️ Interativa", use_container_width=True, on_click=set_inter)

# Valor final
sec = st.session_state.sec

st.divider()

# --------------------------------------------------------------------
# SEÇÃO DE SIMULAÇÃO
# --------------------------------------------------------------------
if sec == 'Simulação':

    st.header("Passo a Passo")
    st.markdown("""
    **Abaixo definimos os estados, os contextos de ordem 2, a árvore de transição e o número de passos T.**
    """)

    st.code(
        """
        estados = ["A", "B", "C"]

        # Todas as combinações possíveis de 2 estados (contextos)
        contextos = list(itertools.product(estados, repeat=2))

        # Árvore: prob do próximo estado dado (estado_{t-2}, estado_{t-1})
        arvore = {
            ("A","A"): np.array([0.7, 0.2, 0.1]),
            ("A","B"): np.array([0.3, 0.5, 0.2]),
            ("A","C"): np.array([0.1, 0.3, 0.6]),
            ("B","A"): np.array([0.4, 0.4, 0.2]),
            ("B","B"): np.array([0.2, 0.5, 0.3]),
            ("B","C"): np.array([0.25, 0.25, 0.5]),
            ("C","A"): np.array([0.6, 0.3, 0.1]),
            ("C","B"): np.array([0.2, 0.2, 0.6]),
            ("C","C"): np.array([0.1, 0.4, 0.5])
        }

        T = 20
        """
    )

    st.markdown("""
    **Sorteamos os dois primeiros estados de forma independente  
    e criamos a lista X contendo esses valores iniciais:**
    """)

    st.code(
        """
        pi = np.array([0.5, 0.3, 0.2])

        s1 = np.random.choice(estados, p=pi)
        s2 = np.random.choice(estados, p=pi)

        X = [s1, s2]
        """
    )

    st.markdown("""
    **O loop abaixo (do passo 2 ao passo T):**
    - Define o contexto atual = últimos dois estados da lista X  
    - Busca o vetor de probabilidades na árvore  
    - Sorteia o próximo estado  
    - Adiciona o novo estado à lista  
    """)

    st.code(
        """
        for t in range(2, T):
            contexto = (X[-2], X[-1])  # últimos dois estados
            probs = arvore[contexto]  # distribuição do próximo estado
            proximo = np.random.choice(estados, p=probs)
            X.append(proximo)
        """
    )

    # --------------------------------------------------------------------
    # PARÂMETROS DA SIMULAÇÃO (rodando de fato)
    # --------------------------------------------------------------------
    st.header("Simulação da Cadeia")

    estados = ["A", "B", "C"]
    pi = np.array([0.5, 0.3, 0.2])

    # Definição da árvore (ordem 2)
    arvore = {
        ("A","A"): np.array([0.7, 0.2, 0.1]),
        ("A","B"): np.array([0.3, 0.5, 0.2]),
        ("A","C"): np.array([0.1, 0.3, 0.6]),
        ("B","A"): np.array([0.4, 0.4, 0.2]),
        ("B","B"): np.array([0.2, 0.5, 0.3]),
        ("B","C"): np.array([0.25, 0.25, 0.5]),
        ("C","A"): np.array([0.6, 0.3, 0.1]),
        ("C","B"): np.array([0.2, 0.2, 0.6]),
        ("C","C"): np.array([0.1, 0.4, 0.5])
    }

    # Slider igual ao da simulação de ordem 1
    T = st.slider("Número de passos (T)", 5, 200, 20)

    # Simulação real agora:
    s1 = np.random.choice(estados, p=pi)
    s2 = np.random.choice(estados, p=pi)

    X = [s1, s2]

    for t in range(2, T):
        contexto = (X[-2], X[-1])
        probs = arvore[contexto]
        proximo = np.random.choice(estados, p=probs)
        X.append(proximo)

    # -----------------------------
    # GRÁFICO
    # -----------------------------
    indices = list(range(T))
    fig = px.scatter(x=indices, y=X, text=X, title="Trajetória da Cadeia de Ordem 2",
                     labels={"x": "Tempo (t)", "y": "Estado"})
    fig.update_traces(mode="lines+markers+text", textposition="top center")

    st.plotly_chart(fig)

