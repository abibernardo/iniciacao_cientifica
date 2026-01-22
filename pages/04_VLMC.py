import streamlit as st

st.title("Variable Length Markov Chains (VLMC)")
st.divider()

if "sec" not in st.session_state:
    st.session_state.sec = "VLMC"

col1, col2 = st.columns(2)

with col1:
    st.button("VLMC", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="VLMC"))
with col2:
    st.button("Implementação", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Implementação"))

sec = st.session_state.sec


# =====================================================
# O QUE É UM VLMC
if sec == "VLMC":
    # =====================================================
    st.header("O que é um VLMC")

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

    st.markdown(
        "onde $c(\\cdot)$ é o menor sufixo do passado necessário "
        "para determinar a distribuição de $X_t$."
    )



    st.info(
        "A memória não é fixa: alguns padrões exigem passado longo, "
        "outros apenas passado curto."
    )

    st.divider()

    # =====================================================
    # ÁRVORE DE CONTEXTOS
    # =====================================================
    st.header("Árvore de Contextos")

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
    st.header("Estimação")

    st.markdown("Considere uma amostra observada:")

    st.latex(r"X_1, X_2, \dots, X_n \in \mathcal{X}")

    st.markdown("Para um contexto \(w\), define-se a contagem:")

    st.latex(
        r"N(w) = \sum_{t=1}^n \mathbf{1}\{X_{t-|w|+1}^t = w\}"
    )

    st.markdown("A estimativa da probabilidade de transição é:")

    st.latex(
        r"\hat P(a \mid w) = \frac{N(wa)}{N(w)}"
    )

    st.markdown(
        "Essa é a **estimativa de máxima verossimilhança** "
        "associada a cada contexto."
    )

    st.divider()

    # =====================================================
    # IDEIA DO ALGORITMO
    # =====================================================
    st.header("Ideia do Context Algorithm")

    st.markdown(
        "O **Context Algorithm** estima simultaneamente:\n\n"
        "- a árvore de contextos\n"
        "- as probabilidades de transição\n\n"
    )

    st.success(
        "Começar com uma árvore de memória máxima e **podar contextos longos** "
        "que não produzem ganho estatístico relevante."
    )

    st.divider()

    # =====================================================
    # CRITÉRIO DE PODA
    # =====================================================
    st.header("Critério de Poda")

    st.markdown(
        "Para um contexto \(w\) e seu sufixo imediato \(v\), define-se:"
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

    st.markdown("Se $\\Delta_w \\ge K_n$, manter o contexto.")
    st.markdown("Se $\\Delta_w < K_n$, podar o contexto.")


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
    st.header("Passo a passo do algoritmo")

    st.markdown("**Passo 1 — Árvore máxima**")

    st.markdown("- Escolher profundidade máxima $m$")
    st.markdown("- Incluir todos os contextos observados com $|w| \\le m$")
    st.markdown("- Exigir $N(w) \\ge 2$")


    st.markdown("**Passo 2 — Poda bottom-up**")

    st.markdown("- Para cada nó terminal:")
    st.markdown("- Comparar o contexto $w$ com seu sufixo")
    st.markdown("- Calcular $\\Delta_w$")
    st.markdown("- Podar se $\\Delta_w < K_n$")

    st.markdown("**Passo 3 — Iterar**")
    st.markdown(
        "Repetir a poda até que nenhuma remoção adicional seja possível."
    )

    st.markdown("**Passo 4 — Estimação final**")

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
    st.header("Interpretação")

    st.markdown(
        "- Cada poda corresponde a um **teste de razão de verossimilhança**\n"
        "que testa cada contexto contra seu sufixo"

    )

    st.caption("Rissanen (1983) • Bühlmann & Wyner (1999)")
else:
    st.code(
        """vlmc = {
        "A": [0.5, 0.3, 0.2],          # contexto curto
        "B": {
            "C": [0.1, 0.6, 0.3],      # contexto médio
            "A": {
                "B": [0.2, 0.3, 0.5]   # contexto longo
            }
        }
    }""",
        language="python"
    )
