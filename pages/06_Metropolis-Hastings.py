import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Metropolis-Hastings para Normal Padrão")
st.divider()

col1, col2 = st.columns(2)

if "sec" not in st.session_state:
    st.session_state.sec = "Target: Normal"

with col1:
    st.button("Metrópolis-Hastings", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="MH Explicação"))
with col2:
    st.button("Target: Normal", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Target: Normal"))

sec = st.session_state.sec

# =========================================================
# CASO NORMAL (SIMULAÇÃO)
# =========================================================
if sec == "Target: Normal":
    st.header("Metropolis-Hastings para Normal Padrão")
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

    # Histograma
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

    # Trace plot
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
    Com o passo muito curto (~0.1), a cadeia anda pouco.
    Isso gera alta taxa de aceitação, mas má exploração do espaço.
    """)



else:
    st.header("Algoritmo de Metropolis–Hastings")



    st.write("""
    Construímos uma cadeia de Markov que, ao longo do tempo, passa a visitar os estados
    com frequência proporcional à distribuição alvo π(x).
    """)

    st.latex(r"\text{Distribuição estacionária da cadeia} = \pi(x)")

    st.write("""
    Ou seja: não precisamos amostrar diretamente de π(x),
    basta simular a cadeia.
    """)

    st.markdown("---")

    st.markdown("## Componentes do algoritmo")

    st.markdown("### 1. Distribuição alvo π(x)")
    st.write("""
    É a distribuição que queremos amostrar.

    Importante: não precisamos da constante de normalização.
    Basta algo proporcional:
    """)

    st.latex(r"\pi(x) \propto f(x)")

    st.markdown("### 2. Distribuição proposta q(x' | x)")
    st.write("""
    É a regra usada para gerar candidatos.

    Exemplos:
    - Normal centrada no estado atual
    - Uniforme ao redor do estado atual
    - Qualquer distribuição que permita explorar o espaço
    """)

    st.latex(r"x' \sim q(x' \mid x_t)")

    st.markdown("### 3. Estado atual")
    st.latex(r"x_t")

    st.markdown("---")

    st.markdown("## Passo a passo do algoritmo")

    st.markdown("### Passo 1: inicialização")
    st.write("Escolha um valor inicial arbitrário:")
    st.latex(r"x_0")

    st.markdown("### Passo 2: propor novo estado")
    st.latex(r"x' \sim q(x' \mid x_t)")

    st.markdown("### Passo 3: calcular probabilidade de aceitação")

    st.latex(r"\alpha = \min\left(1, \frac{\pi(x') \, q(x_t \mid x')}{\pi(x_t)\, q(x' \mid x_t)} \right)")

    st.markdown("### Passo 4: aceitar ou rejeitar")
    st.write("""
    - Gere u ~ Uniforme(0,1)
    - Se u < α → aceita x'
    - Caso contrário → mantém x_t
    """)

    st.latex(r"x_{t+1} = \begin{cases} x' & \text{com probabilidade } \alpha \\ x_t & \text{caso contrário} \end{cases}")

    st.markdown("### Passo 5: repetir")
    st.write("Repita muitas vezes para gerar a cadeia:")

    st.latex(r"x_0, x_1, x_2, ..., x_n")

    st.markdown("---")

    st.markdown("## Caso especial: proposta simétrica")

    st.write("""
    Se a proposta for simétrica (ex: Normal centrada no estado atual),
    então:
    """)

    st.latex(r"q(x'|x_t) = q(x_t|x')")

    st.write("A fórmula simplifica para:")

    st.latex(r"\alpha = \min\left(1, \frac{\pi(x')}{\pi(x_t)} \right)")

    st.markdown("---")


    st.write("""
    O algoritmo faz uma caminhada aleatória com preferência por regiões mais prováveis.

    - Regiões de alta densidade → visitadas com mais frequência
    - Regiões de baixa densidade → menos visitadas

    """)



    st.markdown("---")


    st.write("A regra de aceitação garante:")

    st.latex(r"\pi(x) P(x \to y) = \pi(y) P(y \to x)")

    st.write("""
    **balanço detalhado**. Consequência:
    """)

    st.latex(r"\pi(x) \text{ é distribuição estacionária}")

    st.markdown("---")

    st.markdown("## Problemas comuns")

    st.write("""
    **Passo muito pequeno:**
    - Alta aceitação
    - Movimento lento
    - Alta autocorrelação

    **Passo muito grande:**
    - Muitas rejeições
    - Cadeia não anda

    **Poucas iterações:**
    - Não converge

    **Burn-in insuficiente:**
    - Viés do valor inicial
    """)

    st.code("x_atual = 0.0", language="python")
    st.code("x_prop = np.random.uniform(x_atual - passo, x_atual + passo)", language="python")
    st.code("target(x) = np.exp(-x**2 / 2)", language="python")
    st.code("alpha = min(1, target(x_prop) / target(x_atual))", language="python")
    st.code("""
    if np.random.rand() < alpha:
        x_atual = x_prop
    """, language="python")

    st.markdown("---")

    st.markdown("### propor → calcular aceitação → aceitar/rejeitar → repetir")

