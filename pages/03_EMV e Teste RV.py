import streamlit as st
import numpy as np
import itertools
import plotly.express as px
import pandas as pd

st.title("Verossimilhança de uma Cadeia de Markov")

st.markdown("""
Passo a passo de como calcular o EMV de uma Cadeia de Markov, e do teste RMV para testar sua ordem
""")

# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------


if "sec" not in st.session_state:
    st.session_state.sec = "Estimador de Máxima Verossimilhança"

col1, col2 = st.columns(2)

with col1:
    st.button("Estimador de Máxima Verossimilhança", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Estimador de Máxima Verossimilhança"))
with col2:
    st.button("Teste de Razão de Verossimilhança", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Teste de Razão de Verossimilhança"))


sec = st.session_state.sec

st.divider()

# ---------------------------------------------------------
# SIMULAÇÃO
# ---------------------------------------------------------
if sec == 'Estimador de Máxima Verossimilhança':
    st.markdown("""
    ## Estimador de Máxima Verossimilhança em Cadeias de Markov

    Considere uma cadeia de Markov homogênea de ordem $k$ com espaço de estados finito
    $\\mathcal{A} = \\{a_1, \\dots, a_m\\}$.
    O modelo assume que

    $$
    P(X_t \\mid X_{t-1}, \\dots, X_0)
    =
    P(X_t \\mid X_{t-k}, \\dots, X_{t-1}).
    $$

    Ou seja, a distribuição do próximo estado depende apenas dos últimos $k$ estados
    observados, chamados de **contexto**.

    ---

    ### Parâmetros do modelo

    Para cada contexto $c = (X_{t-k}, \\dots, X_{t-1})$, o modelo possui uma distribuição
    de probabilidade condicional:

    $$
    p(a \\mid c), \\quad a \\in \\mathcal{A},
    $$

    com a restrição:

    $$
    \\sum_{a \\in \\mathcal{A}} p(a \\mid c) = 1.
    $$

    ---

    ### Estimador de Máxima Verossimilhança (EMV)

    Dada uma sequência observada $x_0, \\dots, x_n$, definimos:

    - $N_{c,a}$: número de vezes que o estado $a$ ocorre logo após o contexto $c$;
    - $N_c = \\sum_a N_{c,a}$: número total de vezes que o contexto $c$ aparece.

    O **estimador de máxima verossimilhança** das probabilidades de transição é:

    $$
    \\hat p(a \\mid c) = \\frac{N_{c,a}}{N_c}.
    $$

    Ou seja, a probabilidade estimada é simplesmente a **frequência relativa observada**
    do estado seguinte, dado o contexto.

    ---

    ### Computacional

    O primeiro passo para calcular o EMV é **contar** quantas vezes cada transição
    contexto → estado ocorre na sequência.  

    Essas contagens são armazenadas em dois dicionários:

    - `contagens_transicao`: guarda $N_{c,a}$;
    - `total_contexto`: guarda $N_c$.

    O código abaixo implementa exatamente essa contagem.
    """)

    st.code("""

    contagens_transicao = {}

    # Dicionário que armazena o total N_c de cada contexto
    total_contexto = {}

    # Percorre a sequência a partir do instante k
    for t in range(k, len(sequencia)):

        # Contexto = (X_{t-k}, ..., X_{t-1})
        contexto = tuple(sequencia[t-k:t])

        # Estado observado no tempo t (X_t)
        proximo_estado = sequencia[t]

        # Se o contexto ainda não apareceu, inicializa as estruturas
        if contexto not in contagens_transicao:
            contagens_transicao[contexto] = {}
            total_contexto[contexto] = 0

        # Incrementa a contagem da transição contexto -> proximo_estado
        # Se o estado ainda não apareceu após esse contexto, começa em zero
        
        contagens_transicao[contexto][proximo_estado] = (
            contagens_transicao[contexto].get(proximo_estado, 0) + 1
        )

        # Incrementa o número total de ocorrências do contexto
        total_contexto[contexto] += 1
    """, language="python")

    st.markdown("""
    Ao final desse processo:

    - `contagens_transicao[contexto][estado]` contém $N_{c,a}$;
    - `total_contexto[contexto]` contém $N_c$.

    Assim, o EMV das probabilidades de transição é obtido por:

    $$
    \\hat p(a \\mid c) = \\frac{N_{c,a}}{N_c}.
    $$

    Essas estimativas maximizam a função de verossimilhança da cadeia de Markov:
    """)

    st.markdown("""

    $$
    L(\\theta)
    =
    \\prod_{t=k}^{n}
    p\\bigl(x_t \\mid x_{t-k}, \\dots, x_{t-1}\\bigr),
    $$
    """)


    st.markdown("""
    Que pode ser escrita como a log-verossimilhança:
    
    $$
    \\ell(\\theta)
    =
    \\sum_{c \\in \\mathcal{A}^k}
    \\sum_{a \\in \\mathcal{A}}
    N_{c,a} \\, \\log \\frac{N_{c,a}}{N_c}
    $$

    onde:

    - $N_{c,a}$ é o número de vezes que o estado $a$ ocorre após o contexto $c$;
    - $N_c = \\sum_a N_{c,a}$ é o número total de ocorrências do contexto $c$.
    
    A função para calcular a log-verossimilhança de uma cadeia de ordem k foi definida como:
    """)

    st.code("""
        def log_verossimilhanca_markov(sequencia, k):

        # Calcula contagens:
        contagens_transicao = {}
        total_contexto = {}

        for t in range(k, len(sequencia)):
            contexto = tuple(sequencia[t-k:t])
            proximo_estado = sequencia[t]

            if contexto not in contagens_transicao:
                contagens_transicao[contexto] = {}
                total_contexto[contexto] = 0

            contagens_transicao[contexto][proximo_estado] = contagens_transicao[contexto].get(proximo_estado, 0) + 1
            total_contexto[contexto] += 1

        # calcula verossimilhança:
        ell = 0.0
        for contexto, contagens in contagens_transicao.items(): # elementos do .items "Desempacota" Dicionário; não é um loop duplo!!!
            Nk_c = total_contexto[contexto]
            for Nk_ca in contagens.values():  # .values pega apenas a contagem
                ell += Nk_ca * math.log(Nk_ca / Nk_c)

        return ell
            """, language="python")







elif sec == "Teste de Razão de Verossimilhança":
    st.markdown(r"""
    ## Teste de Razão de Verossimilhança (TRV)

    Uma vez calculada a log-verossimilhança de uma cadeia de Markov de ordem $k$,
    podemos utilizá-la para **comparar modelos de ordens diferentes**.

    O objetivo do teste de razão de verossimilhança é verificar se aumentar a ordem
    do modelo (de $k$ para $k+1$) traz um ganho estatisticamente significativo
    na capacidade de explicar os dados.

    ---

    ### Hipóteses do teste

    Considere dois modelos aninhados:

    - **Hipótese nula** $H_0$:  
      A sequência segue uma cadeia de Markov de ordem $k$.

    - **Hipótese alternativa** $H_1$:  
      A sequência segue uma cadeia de Markov de ordem $k+1$.

    O modelo de ordem $k$ é um caso particular do modelo de ordem $k+1$.


    Sejam:

    - $\ell_k$ a log-verossimilhança maximizada do modelo de ordem $k$;
    - $\ell_{k+1}$ a log-verossimilhança maximizada do modelo de ordem $k+1$.

    A estatística do teste de razão de verossimilhança é definida como:

    $$
    \mathrm{LR}
    =
    2\bigl(\ell_{k+1} - \ell_k\bigr).
    $$
    
    E segue uma distribuição qui-quadrado com $$ (m - 1)\, m^{k}$$ graus de liberdade.""")

    st.markdown(r"""
        ## Computacional
        
    Usando a função log_verossimilhanca_markov, o teste de Razão de Verossimilhança para as cadeias de ordem k e de ordem k+1 são montados assim:
    """)

    st.code("""
ell_k   = log_verossimilhanca_markov(sequencia, k)
ell_k1  = log_verossimilhanca_markov(sequencia, k+1)

LR = 2 * (ell_k1 - ell_k)

m = len(estados)
p_value = 1 - chi2.cdf(LR, df=((m-1)*(m**(k+1)) - ((m-1)*(m**k))))

print(p_value)
            """, language="python")

