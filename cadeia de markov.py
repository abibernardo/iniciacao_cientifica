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

sec = st.radio(
        "Seção",
        options=["Código", "Simulação"]
    )

# -----------------------------
# PARÂMETROS
# -----------------------------
if sec == 'Código':
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

elif sec == 'Simulação':
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
        estado_atual = X[-1] # Olhe onde a cadeia está (estado atual); último elemento de X
        i = estados.index(estado_atual) # index do estado atual
        proximo = np.random.choice(estados, p=P[i]) # Escolhe o próximo estado com as probabilidades da LINHA da matriz de transição correspondente ao estado atual
        X.append(proximo) # Adiciona o estado atual a lista



    indices = list(range(T))
    fig = px.scatter(x=indices, y=X, text=X, title="Trajetória da Cadeia de Markov",
                     labels={"x": "Tempo (t)", "y": "Estado"})
    fig.update_traces(mode="lines+markers+text", textposition="top center")

    st.plotly_chart(fig)

    # -----------------------------
    # MATRIZ DE N PASSOS
    # -----------------------------
    #st.header("Matriz de Transição de n Passos")

    #n = st.slider("Escolha n para calcular P^n", 1, 50, 5)
    #P_n = np.linalg.matrix_power(P, n)

    #st.write(f"Matriz de transição de {n} passos (P^{n}):")
    #st.dataframe(P_n)
    #st.write("Interpretação: Se você partir do estado i, essas são as probabilidades de estar em cada estado depois de n passos!")
    #st.success("Simulação concluída!")
