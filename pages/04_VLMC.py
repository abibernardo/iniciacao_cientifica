import streamlit as st
import numpy as np

st.title("Variable Length Markov Chains (VLMC)")


if "sec" not in st.session_state:
    st.session_state.sec = "VLMC"

col1, col2, col3 = st.columns(3)

with col1:
    st.button("VLMC", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="VLMC"))
with col2:
    st.button("Simulação", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Simulação"))
with col3:
    st.button("Estimação", use_container_width=True,
              on_click=lambda: st.session_state.update(sec="Estimação"))

sec = st.session_state.sec
st.divider()
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
elif sec == "Simulação":

    st.header("Representação da Estrutura")

    st.markdown("A representação de árvore para a cadeia de ordem variável é a mesma que para cadeias de ordem fixa, com exceção que a profundidade da árvore varia com o contexto (galhos de tamanhos diferentes):")

    st.code(
        """
    
        arvore = {
            "A": [0.5, 0.3, 0.2],   # Contexto curto: apenas "A"
    
            "B": {
                "A": {
                    "A": [0.7, 0.2, 0.1],  # Contexto longo: "BAA"
                    "B": [0.4, 0.4, 0.2]   # Contexto longo: "BAB"
                },
                "C": [0.2, 0.5, 0.3]       # Contexto médio: "BC"
            }
        }
        """,
        language="python"
    )

    st.divider()
    st.header("Encontrando probabilidades de transição")
    st.markdown("Para simular uma sequência gerada por uma vlmc, a função auxiliar abaixo encontra as probabilidades de transição, dada a árvore e o histórico.")
    st.markdown("1. Parte do maior contexto possível de comprimento K,")
    st.markdown("2. Verifica se os últimos K estados do histórico correspondem ao contexto, caminhando pela árvore do estado mais antigo até o mais novo,")
    st.markdown("3. Se caminhar por todo contexto e chegar até as folhas (lista), a função retorna as probabilidades. Caso contrário, ela encurta o contexto analisado no histórico (desconsidera o estado mais antigo) e repete o processo.")

    st.code(
        """
        def achar_contexto(arvore, historico):
            # Percorremos do MAIOR sufixo para o menor
            for k in range(len(historico), 0, -1):
    
                sufixo = historico[-k:]  # últimos k símbolos
                contexto = arvore        # começamos na raiz
                ok = True
    
                # Descemos na árvore símbolo por símbolo
                for s in sufixo:
    
                    # Se já estamos numa folha, já achamos o contexto
                    if isinstance(contexto, list):
                        return contexto
    
                    # Se o símbolo existe como filho, seguimos descendo
                    if s in contexto:
                        contexto = contexto[s]
                    # Caso não haja correspondência, voltamos para o loop externo
                    else:
                        ok = False
                        break
    
                # Se o caminho existe e terminamos numa folha → contexto válido
                if ok and isinstance(contexto, list):
                    return contexto
    
            # Se nada foi encontrado, há erro no modelo
            raise ValueError("Nenhum contexto encontrado.")
        """,
        language="python"
    )

    st.markdown(
        """
        - Parte do passado completo do histórico (maior sufixo possível)
        - Tenta caminhar na árvore com os estados do sufixo **(loop interno)**
        - Se não existir na árvore → encurta a memória **(loop externo)**
        - Para quando encontra uma folha (um contexto válido)
        - Retorna a folha (probabilidades de transição)
        """
    )

    st.divider()
    st.header("Simulação da VLMC")

    st.markdown("Para simular uma sequência:")
    st.markdown("1. Gera os primeiros k_max estados a partir de uma dist inicial")
    st.markdown("2. Usa todo o histórico (lista X)")
    st.markdown("3. Usa a função auxiliar para encontrar probabilidades de transição dado o histórico")
    st.markdown("4. Gera próximo estado de acordo com essas probabilidades, e adiciona no histórico X.")

    st.code(
        """
        def simular_vlmc(arvore, estados, T, pi, K_max):
    
            # Passado inicial gerado da distribuição inicial
            X = [np.random.choice(estados, p=pi) for _ in range(K_max)]
    
            # Evolução da cadeia
            for t in range(K_max, T):
    
                historico = X[:]  # todo o passado observado
    
                # Encontramos as probs de transição com a função auxiliar
                probs = achar_contexto(arvore, historico)
    
                # Sorteamos o próximo estado segundo essa distribuição
                proximo = np.random.choice(estados, p=probs)
    
                # Acrescentamos à sequência
                X.append(proximo)
    
            return X
            
        estados = ["A", "B", "C"]
        pi = np.array([0.5, 0.3, 0.2])
        seq = simular_vlmc(arvore, estados, T=20, pi=pi, K_max=4)
        """,
        language="python"
    )

