import streamlit as st
import numpy as np
import plotly.graph_objects as go

col1, col2 = st.columns(2)

if "sec" not in st.session_state:
    st.session_state.sec = "Target: Normal"

with col1:
    st.button("Target: Normal", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Target: Normal"))
with col2:
    st.button("Target: Uniforme", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Target: Uniforme"))

sec = st.session_state.sec

# =========================================================
# CASO NORMAL
# =========================================================
if sec == "Target: Normal":
    st.title("Metropolis-Hastings para Normal Padrão")
    st.write("Distribuição alvo: N(0,1)")
    st.write("Distribuição proposta: Uniforme(x atual ± passo)")

    n_iter = st.slider("Número de iterações", 1000, 100000, 50000, step=1000)
    passo = st.slider("Passo da proposta", 0.01, 2.0, 0.1, step=0.01)
    burn_in = st.slider("Burn-in", 0, 10000, 1000, step=100)

    def target(x):
        return np.exp(-x**2 / 2)

    x_atual = 0.0
    amostras = []
    aceitos = 0

    for _ in range(n_iter):
        x_prop = np.random.uniform(x_atual - passo, x_atual + passo)
        alpha = min(1, target(x_prop) / target(x_atual))

        if np.random.rand() < alpha:
            x_atual = x_prop
            aceitos += 1

        amostras.append(x_atual)

    amostras = np.array(amostras)
    amostras_final = amostras[burn_in:]

    taxa_aceitacao = aceitos / n_iter

    col1, col2, col3 = st.columns(3)
    col1.metric("Taxa de aceitação", f"{taxa_aceitacao:.2%}")
    col2.metric("Média amostral", f"{np.mean(amostras_final):.4f}")
    col3.metric("Variância amostral", f"{np.var(amostras_final):.4f}")

    # ----------------------------
    # HISTOGRAMA (PLOTLY)
    # ----------------------------
    x = np.linspace(-4, 4, 1000)
    normal = (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)

    fig1 = go.Figure()

    fig1.add_trace(go.Histogram(
        x=amostras_final,
        nbinsx=50,
        histnorm='probability density',
        name="Amostras"
    ))

    fig1.add_trace(go.Scatter(
        x=x,
        y=normal,
        mode='lines',
        name='Normal teórica'
    ))

    fig1.update_layout(
        title="Histograma das Amostras",
        xaxis_title="x",
        yaxis_title="Densidade",
        template="plotly_white"
    )

    st.plotly_chart(fig1, use_container_width=True)

    # ----------------------------
    # TRACE PLOT (PLOTLY)
    # ----------------------------
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        y=amostras[:1000],
        mode='lines',
        name='Trace'
    ))

    fig2.update_layout(
        title="Trace Plot (primeiras 1000 iterações)",
        xaxis_title="Iteração",
        yaxis_title="Valor",
        template="plotly_white"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Interpretação")

    st.write("""
    Com o passo muito curto (~0.1) a cadeia não converge bem. Fica com a taxa de aceitação altíssima.
    """)

# =========================================================
# CASO UNIFORME
# =========================================================
else:
    st.title("Metropolis-Hastings para Uniforme U(0,1)")
    st.write("Distribuição alvo: U(0,1)")
    st.write("Distribuição proposta: Normal centrada no valor atual")

    n_iter = st.slider("Número de iterações", 1000, 100000, 50000, step=1000)
    sigma = st.slider("Desvio padrão da proposta", 0.01, 1.0, 0.1, step=0.01)
    burn_in = st.slider("Burn-in", 0, 10000, 1000, step=100)

    def target_uniform(x):
        return 1 if 0 <= x <= 1 else 0

    x_atual = 0.5
    amostras = []
    aceitos = 0

    for _ in range(n_iter):
        x_prop = np.random.normal(x_atual, sigma)

        if 0 <= x_prop <= 1:
            alpha = 1
        else:
            alpha = 0

        if np.random.rand() < alpha:
            x_atual = x_prop
            aceitos += 1

        amostras.append(x_atual)

    amostras = np.array(amostras)
    amostras_final = amostras[burn_in:]

    taxa_aceitacao = aceitos / n_iter

    col1, col2, col3 = st.columns(3)
    col1.metric("Taxa de aceitação", f"{taxa_aceitacao:.2%}")
    col2.metric("Média amostral", f"{np.mean(amostras_final):.4f}")
    col3.metric("Variância amostral", f"{np.var(amostras_final):.4f}")

    # ----------------------------
    # HISTOGRAMA (PLOTLY)
    # ----------------------------
    x = np.linspace(0, 1, 1000)
    uniforme = np.ones_like(x)

    fig1 = go.Figure()

    fig1.add_trace(go.Histogram(
        x=amostras_final,
        nbinsx=50,
        histnorm='probability density',
        name="Amostras"
    ))

    fig1.add_trace(go.Scatter(
        x=x,
        y=uniforme,
        mode='lines',
        name='Uniforme teórica'
    ))

    fig1.update_layout(
        title="Histograma das Amostras",
        xaxis_title="x",
        yaxis_title="Densidade",
        template="plotly_white"
    )

    fig1.update_xaxes(range=[-0.2, 1.2])

    st.plotly_chart(fig1, use_container_width=True)

    # ----------------------------
    # TRACE PLOT
    # ----------------------------
    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(
        y=amostras[:1000],
        mode='lines'
    ))

    fig2.update_layout(
        title="Trace Plot (primeiras 1000 iterações)",
        xaxis_title="Iteração",
        yaxis_title="Valor",
        template="plotly_white"
    )

    fig2.update_yaxes(range=[-0.2, 1.2])

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Valores teóricos para U(0,1)")
    st.write("Média teórica = 0.5")
    st.write("Variância teórica = 1/12 ≈ 0.0833")
