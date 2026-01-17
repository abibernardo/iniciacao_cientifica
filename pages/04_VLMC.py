import streamlit as st

st.set_page_config(
    page_title="VLMC – Context Algorithm",
    layout="centered"
)

# =====================================================
# TÍTULO
# =====================================================
st.title("Variable Length Markov Chains (VLMC)")

st.markdown(
    "Descrição conceitual e estatística dos **VLMCs** "
    "e do **Context Algorithm** para seleção da árvore de contextos."
)

st.divider()

# =====================================================
# O QUE É UM VLMC
# =====================================================
st.header("1. O que é um VLMC")

st.markdown(
    "Um **Variable Length Markov Chain (VLMC)** é um processo estocástico "
    "no qual o comprimento da memória relevante depende do passado observado."
)

st.markdown("Em uma cadeia de Markov de ordem fixa:")

st.latex(
    r"P(X_t \mid X_{t-1}, X_{t-2}, \dots) = "
    r"P(X_t \mid X_{t-1}, \dots, X_{t-k})"
)

st.markdown("No VLMC, a dependência é dada por um **contexto**:")

st.latex(
    r"P(X_t \mid X_{t-1}, X_{t-2}, \dots) = "
    r"P(X_t \mid c(X_{t-1}, X_{t-2}, \dots))"
)

st.markdown(
    "onde \(c(\cdot)\) é o **menor sufixo do passado** "
    "necessário para determinar a distribuição de \(X_t\)."
)

st.info(
    "A memória não é fixa: alguns padrões exigem passado longo, "
    "outros apenas passado curto."
)

st.divider()

# =====================================================
# ÁRVORE DE CONTEXTOS
# =====================================================
st.header("2. Árvore de Contextos")

st.markdown(
    "Os contextos formam uma **árvore de contextos** \\(\\tau\\), "
    "que satisfaz a **propriedade do sufixo**:"
)

st.markdown(
    "- Nenhum contexto é sufixo de outro  \n"
    "- Cada passado infinito admite exatamente um contexto"
)

st.markdown(
    "A árvore de contextos, junto com as probabilidades de transição, "
    "define completamente o VLMC."
)

st.divider()

# =====================================================
# DADOS E ESTIMAÇÃO
# =====================================================
st.header("3. Dados e estimação empírica")

st.markdown("Considere uma amostra observada:")

st.latex(r"X_1, X_2, \dots, X_n \in \mathcal{X}")

st.markdown("Para um contexto \(w\), define-se a contagem:")

st.latex(
    r"N(w) = \sum_{t=1}^n \mathbf{1}\{X_{t-|w|+1}^t = w\}"
)

st.markdown("A estimativa empírica da transição é:")

st.latex(
    r"\hat P(a \mid w) = \frac{N(wa)}{N(w)}"
)

st.markdown(
    "Essa é a **estimativa de máxima verossimilhança local** "
    "associada a cada contexto."
)

st.divider()

# =====================================================
# IDEIA DO ALGORITMO
# =====================================================
st.header("4. Ideia do Context Algorithm")

st.markdown(
    "O **Context Algorithm** estima simultaneamente:\n\n"
    "- a árvore de contextos\n"
    "- as probabilidades de transição\n\n"
    "A estratégia é simples:"
)

st.success(
    "Começar com uma árvore de memória máxima e **podar contextos longos** "
    "que não produzem ganho estatístico relevante."
)

st.divider()

# =====================================================
# CRITÉRIO DE PODA
# =====================================================
st.header("5. Critério estatístico de poda")

st.markdown(
    "Para um contexto candidato \(w\) e seu sufixo imediato \(v\), define-se:"
)

st.latex(
    r"\Delta_w = "
    r"N(w)\sum_{a\in\mathcal{X}} "
    r"\hat P(a\mid w)\log\frac{\hat P(a\mid w)}{\hat P(a\mid v)}"
)

st.markdown("Equivalentemente:")

st.latex(
    r"\Delta_w = N(w)\cdot "
    r"\mathrm{KL}\big(\hat P(\cdot\mid w)\,\|\,\hat P(\cdot\mid v)\big)"
)

st.markdown("**Regra de decisão:**")

st.markdown(
    "- Se \\(\\Delta_w \\ge K_n\\): manter o contexto  \n"
    "- Se \\(\\Delta_w < K_n\\): podar o contexto"
)

st.markdown("O cutoff cresce lentamente com a amostra:")

st.latex(r"K_n = C\log n")

st.warning(
    "Memória longa só é aceita quando melhora "
    "significativamente a verossimilhança."
)

st.divider()

# =====================================================
# PASSO A PASSO
# =====================================================
st.header("6. Passo a passo do algoritmo")

st.markdown("**Step 1 — Árvore máxima**")
st.markdown(
    "- Escolher profundidade máxima \(m\)\n"
    "- Incluir todos os contextos observados com \\(|w| \\le m\\)\n"
    "- Exigir \\(N(w) \\ge 2\\)"
)

st.markdown("**Step 2 — Poda bottom-up**")
st.markdown(
    "- Para cada nó terminal:\n"
    "  - Comparar \(w\) com seu sufixo\n"
    "  - Calcular \\(\\Delta_w\\)\n"
    "  - Podar se \\(\\Delta_w < K_n\\)"
)

st.markdown("**Step 3 — Iterar**")
st.markdown(
    "Repetir a poda até que nenhuma remoção adicional seja possível."
)

st.markdown("**Step 4 — Estimação final**")

st.latex(
    r"\hat P(a\mid c) = \frac{N(ca)}{N(c)}"
)

st.markdown(
    "O resultado final é a **árvore de contextos estimada** "
    "e o **VLMC ajustado por máxima verossimilhança**."
)

st.divider()

# =====================================================
# INTERPRETAÇÃO
# =====================================================
st.header("7. Interpretação estatística")

st.markdown(
    "- Cada poda corresponde a um **teste de razão de verossimilhança**\n"
    "- O método equivale a uma seleção hierárquica tipo **BIC / MDL**\n"
    "- O estimador é **consistente** sob hipóteses regulares"
)

st.caption("Rissanen (1983) • Bühlmann & Wyner (1999)")
