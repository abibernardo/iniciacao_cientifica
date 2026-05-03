import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

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

if sec == "Target: Normal":
    st.title("Metropolis-Hastings para Normal Padrão")
    st.write("Distribuição alvo: N(0,1)")
    st.write("Distribuição proposta: Uniforme(x atual ± passo)")

    # ----------------------------
    # Parâmetros interativos
    # ----------------------------
    n_iter = st.slider("Número de iterações", 1000, 100000, 50000, step=1000)
    passo = st.slider("Passo da proposta", 0.01, 2.0, 0.1, step=0.01)
    burn_in = st.slider("Burn-in", 0, 10000, 1000, step=100)

    # ----------------------------
    # Distribuição target
    # ----------------------------
    def target(x):
        return np.exp(-x**2 / 2)

    # ----------------------------
    # Algoritmo Metropolis-Hastings
    # ----------------------------
    x_atual = 0.0
    amostras = []
    aceitos = 0

    for _ in range(n_iter):
        # proposta uniforme
        x_prop = np.random.uniform(x_atual - passo, x_atual + passo)

        # probabilidade de aceitação
        alpha = min(1, target(x_prop) / target(x_atual))

        # aceita ou rejeita
        if np.random.rand() < alpha:
            x_atual = x_prop
            aceitos += 1

        amostras.append(x_atual)

    amostras = np.array(amostras)

    # ----------------------------
    # Burn-in
    # ----------------------------
    amostras_final = amostras[burn_in:]

    # ----------------------------
    # Métricas
    # ----------------------------
    taxa_aceitacao = aceitos / n_iter

    col1, col2, col3 = st.columns(3)

    col1.metric("Taxa de aceitação", f"{taxa_aceitacao:.2%}")
    col2.metric("Média amostral", f"{np.mean(amostras_final):.4f}")
    col3.metric("Variância amostral", f"{np.var(amostras_final):.4f}")

    # ----------------------------
    # Histograma + curva teórica
    # ----------------------------
    fig1, ax1 = plt.subplots(figsize=(8, 5))

    ax1.hist(amostras_final, bins=50, density=True)

    x = np.linspace(-4, 4, 1000)
    normal = (1 / np.sqrt(2 * np.pi)) * np.exp(-x**2 / 2)

    ax1.plot(x, normal)
    ax1.set_title("Histograma das Amostras")
    ax1.set_xlabel("x")
    ax1.set_ylabel("Densidade")

    st.pyplot(fig1)

    # ----------------------------
    # Trace plot
    # ----------------------------
    fig2, ax2 = plt.subplots(figsize=(8, 4))

    ax2.plot(amostras[:1000])
    ax2.set_title("Trace Plot (primeiras 1000 iterações)")
    ax2.set_xlabel("Iteração")
    ax2.set_ylabel("Valor")

    st.pyplot(fig2)

    # ----------------------------
    # Explicação
    # ----------------------------
    st.subheader("Interpretação")

    st.write("""
    Com o passo muito curto (~0.1) a cadeia não converge bem. Fica com a taxa de aceitação altíssima.
    """)

    st.code("""
    def target(x):
        return np.exp(-x**2 / 2)

    # ----------------------------
    # Algoritmo Metropolis-Hastings
    # ----------------------------

    # valor inicial da cadeia
    x_atual = 3.0

    # lista que armazenará as amostras geradas
    amostras = []

    # contador de quantas propostas foram aceitas
    aceitos = 0

    # loop principal do algoritmo
    for _ in range(n_iter):

        # ----------------------------
        # 1) Geração da proposta
        # ----------------------------

        # propõe um novo valor ao redor do estado atual
        # usando uma uniforme no intervalo
        # [x_atual - passo, x_atual + passo]
        x_prop = np.random.uniform(x_atual - passo, x_atual + passo)

        # ----------------------------
        # 2) Probabilidade de aceitação
        # ----------------------------

        # calcula a razão entre a densidade no ponto proposto
        # e a densidade no ponto atual
        alpha = min(1, target(x_prop) / target(x_atual))

        # ----------------------------
        # 3) Aceita ou rejeita
        # ----------------------------

        # gera um número aleatório entre 0 e 1
        # se for menor que alpha, aceita a proposta
        if np.random.rand() < alpha:
            x_atual = x_prop
            aceitos += 1

        # guarda o valor atual da cadeia
        # (se rejeitou, repete o valor anterior)
        amostras.append(x_atual)

    # converte para array numpy
    amostras = np.array(amostras)

    # ----------------------------
    # Burn-in
    # ----------------------------

    # remove as primeiras iterações,
    # pois ainda podem estar influenciadas
    # pelo valor inicial
    amostras_final = amostras[burn_in:]
    """, language="python")

else:
    import streamlit as st
    import numpy as np
    import matplotlib.pyplot as plt

    st.set_page_config(page_title="MH Uniforme", layout="wide")

    st.title("Metropolis-Hastings para Uniforme U(0,1)")
    st.write("Distribuição alvo: U(0,1)")
    st.write("Distribuição proposta: Normal centrada no valor atual")

    # ----------------------------
    # Parâmetros interativos
    # ----------------------------
    n_iter = st.slider("Número de iterações", 1000, 100000, 50000, step=1000)
    sigma = st.slider("Desvio padrão da proposta", 0.01, 1.0, 0.1, step=0.01)
    burn_in = st.slider("Burn-in", 0, 10000, 1000, step=100)


    # ----------------------------
    # Distribuição target uniforme
    # ----------------------------
    def target_uniform(x):
        return 1 if 0 <= x <= 1 else 0


    # ----------------------------
    # Algoritmo MH
    # ----------------------------
    x_atual = 0.5
    amostras = []
    aceitos = 0

    for _ in range(n_iter):
        # proposta normal centrada no estado atual
        x_prop = np.random.normal(x_atual, sigma)

        # como a proposta é simétrica,
        # alpha = pi(x') / pi(x_t)
        # para uniforme: 1 dentro do suporte, 0 fora
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

    # ----------------------------
    # Métricas
    # ----------------------------
    taxa_aceitacao = aceitos / n_iter

    col1, col2, col3 = st.columns(3)

    col1.metric("Taxa de aceitação", f"{taxa_aceitacao:.2%}")
    col2.metric("Média amostral", f"{np.mean(amostras_final):.4f}")
    col3.metric("Variância amostral", f"{np.var(amostras_final):.4f}")

    # ----------------------------
    # Histograma
    # ----------------------------
    fig1, ax1 = plt.subplots(figsize=(8, 5))

    ax1.hist(amostras_final, bins=50, density=True)

    # curva teórica da uniforme
    x = np.linspace(0, 1, 1000)
    uniforme = np.ones_like(x)

    ax1.plot(x, uniforme)
    ax1.set_title("Histograma das Amostras")
    ax1.set_xlabel("x")
    ax1.set_ylabel("Densidade")
    ax1.set_xlim(-0.2, 1.2)

    st.pyplot(fig1)

    # ----------------------------
    # Trace plot
    # ----------------------------
    fig2, ax2 = plt.subplots(figsize=(8, 4))

    ax2.plot(amostras[:1000])
    ax2.set_title("Trace Plot (primeiras 1000 iterações)")
    ax2.set_xlabel("Iteração")
    ax2.set_ylabel("Valor")
    ax2.set_ylim(-0.2, 1.2)

    st.pyplot(fig2)

    # ----------------------------
    # Valores teóricos
    # ----------------------------
    st.subheader("Valores teóricos para U(0,1)")
    st.write(r"Média teórica = 0.5")
    st.write(r"Variância teórica = 1/12 ≈ 0.0833")

    st.subheader("Interpretação")
    st.write("""
    - Gerar novo valor com dist proposta
    - Valor de aceitação = prob da dist target ter gerado o novo valor observado/ prob da dist target ter gerado o valor anterior
    - Se prob de ter gerado valor atual for MAIOR que de ter gerado valor antigo, aceita direto (razão maor que 1)
    - Se for menor, vira uma prob [0, 1]. Gera uniforme[0, 1]. Se valor de aceitação > uniforme, aceita novo valor. Caso contrário, nega.
    - Se aceitar novo valor, usa a dist proposta pra gerar valor candidato a partir do novo valor aceito (com o tamanho do passo ditando o 'alcance' do sorteio
    (no caso da Normal, e 'tamanho do passo' é a variancia)
    """)

    st.code("""
    def target_uniform(x):
        return 1 if 0 <= x <= 1 else 0

    # ----------------------------
    # Algoritmo Metropolis-Hastings
    # ----------------------------

    # valor inicial dentro do suporte da uniforme
    x_atual = 0.5

    # lista para armazenar as amostras
    amostras = []

    # contador de aceitações
    aceitos = 0

    # loop principal
    for _ in range(n_iter):

        # ----------------------------
        # 1) Geração da proposta
        # ----------------------------

        # proposta normal centrada no estado atual
        x_prop = np.random.normal(x_atual, sigma)

        # ----------------------------
        # 2) Probabilidade de aceitação
        # ----------------------------

        # como a proposta é simétrica,
        # a razão de Hastings simplifica para:
        # alpha = pi(x') / pi(x_t)
        #
        # na uniforme:
        # - dentro do intervalo [0,1], densidade = 1
        # - fora do intervalo, densidade = 0

        if 0 <= x_prop <= 1:
            alpha = 1
        else:
            alpha = 0

        # ----------------------------
        # 3) Aceita ou rejeita
        # ----------------------------

        # se a proposta estiver dentro do suporte,
        # ela é sempre aceita
        if np.random.rand() < alpha:
            x_atual = x_prop
            aceitos += 1

        # armazena o estado atual
        # (repete se houve rejeição)
        amostras.append(x_atual)

    # converte para array
    amostras = np.array(amostras)

    # ----------------------------
    # Burn-in
    # ----------------------------

    # remove as primeiras iterações
    amostras_final = amostras[burn_in:]
    """, language="python")
