import streamlit as st



# =========================================================
# TÍTULO
# =========================================================
st.title("Cadeias de Markov de Comprimento Variável (VLMC)")


# =========================================================
# O QUE É UM VLMC
# =========================================================
st.header("O que é um VLMC?")

st.markdown(r"""
Um **Variable Length Markov Chain (VLMC)** é um processo estocástico no qual o **comprimento da memória relevante depende do passado observado**.

Em uma cadeia de Markov de ordem fixa \(k\):
\[
P(X_t \mid X_{t-1}, X_{t-2}, \dots)
=
P(X_t \mid X_{t-1}, \dots, X_{t-k})
\]

No VLMC, a dependência é dada por um **contexto**:
\[
P(X_t \mid X_{t-1}, X_{t-2}, \dots)
=
P(X_t \mid c(X_{t-1}, X_{t-2}, \dots))
\]

onde \(c(\cdot)\) é o **menor sufixo do passado** suficiente para determinar
a distribuição condicional de \(X_t\).
""")

st.info("""
A memória **não é fixa**: alguns padrões exigem passado longo,
outros apenas passado curto.
""")

# =========================================================
# ÁRVORE DE CONTEXTOS
# =========================================================
st.header("Árvore de Contextos")

st.markdown(r"""
O conjunto de todos os contextos forma uma **árvore de contextos** \(\tau\),
que satisfaz a **propriedade do sufixo**:

- Nenhum contexto é sufixo de outro
- Cada passado infinito possui exatamente um contexto associado

A árvore define completamente o modelo VLMC.
""")

# =========================================================
# DADOS E ESTIMAÇÃO
# =========================================================
st.header("Estimação")

st.markdown(r"""
Considere uma amostra observada:
\[
X_1, X_2, \dots, X_n \in \mathcal{X}
\]

Para uma palavra (contexto) \(w\), define-se a contagem:
\[
N(w) = \sum_{t=1}^n \mathbf{1}\{X_{t-|w|+1}^t = w\}
\]

A estimativa de máxima verossimilhança da probabilidade de transição é:
\[
\hat P(a \mid w) = \frac{N(wa)}{N(w)}
\]

""")

# =========================================================
# IDEIA DO CONTEXT ALGORITHM
# =========================================================
st.header("Ideia do Context Algorithm")

st.markdown("""
O **Context Algorithm**:

1. Estima a **árvore de contextos**
2. Estima as **probabilidades de transição**

A estratégia é:

> Começar com uma árvore de memória máxima  
> e **podar contextos longos** sempre que eles **não trazem ganho estatístico suficiente**.
""")

# =========================================================
# CRITÉRIO DE PODA
# =========================================================
st.header("Critério estatístico de poda")

st.markdown(r"""
Para um contexto candidato \(w\) e seu sufixo imediato \(v\),
define-se:

\[
\Delta_w
=
N(w)
\sum_{a \in \mathcal{X}}
\hat P(a \mid w)
\log
\frac{\hat P(a \mid w)}{\hat P(a \mid v)}
\]

Equivalentemente:
\[
\Delta_w
=
N(w) \cdot
\mathrm{KL}\big(\hat P(\cdot \mid w)\;\|\;\hat P(\cdot \mid v)\big)
\]

Esse valor mede **quanto a distribuição muda** ao usar
um contexto mais longo.
""")

st.markdown("""
### Regra de decisão

- Se \(\Delta_w \ge K_n\): **mantém o contexto**
- Se \(\Delta_w < K_n\): **poda o contexto**

onde o cutoff cresce lentamente com a amostra, tipicamente:
\[
K_n = C \log n
\]
""")

st.warning("""
O algoritmo só aceita memória longa quando ela é
estatisticamente justificável.
""")

# =========================================================
# PASSO A PASSO DO ALGORITMO
# =========================================================
st.header("Passo a passo do Context Algorithm")

st.markdown("""
### **Step 1 — Construção da árvore máxima**
- Escolha uma profundidade máxima \(m\)
- Construa todos os contextos observados com \(|w| \le m\)
- Exija \(N(w) \ge 2\) (todo contexto deve aparecer pelo menos duas vezes)

---

### **Step 2 — Poda bottom-up**
- Para cada **nó terminal** (folha) da árvore:
  - Compare o contexto \(w\) com seu sufixo imediato ("pai")
  - Calcule \(\Delta_w\)
  - Pode o nó se \(\Delta_w < K_n\)

---

### **Step 3 — Iteração**
- Repita o Step 2 até que nenhuma poda adicional seja possível

---

### **Step 4 — Estimação final**
- Para cada contexto final \(c\):
\[
\hat P(a \mid c) = \frac{N(ca)}{N(c)}
\]

O resultado é o **VLMC ajustado por máxima verossimilhança**.
""")

# =========================================================
# INTERPRETAÇÃO FINAL
# =========================================================
st.header("Interpretação")

st.markdown("""
- Cada decisão de poda é um **teste de razão de verossimilhança** que testa cada contexto contra seu sufixo (contexto imediatamente anterior)

""")

st.markdown("---")
st.caption("VLMC • Context Algorithm • Rissanen (1983), Bühlmann & Wyner (1999)")

