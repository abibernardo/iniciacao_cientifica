import numpy as np
from scipy.special import gammaln

# =========================
# SUA FUNÇÃO (mantida)
# =========================
def contagem_contextos(historico, ordem_max):
    contagens_transicao = {}

    for t in range(1, len(historico)):
        for k in range(1, min(ordem_max, t) + 1):
            contexto = tuple(reversed(historico[t - k:t]))
            proximo_estado = historico[t]

            if contexto not in contagens_transicao:
                contagens_transicao[contexto] = {}

            contagens_transicao[contexto][proximo_estado] = (
                contagens_transicao[contexto].get(proximo_estado, 0) + 1
            )

    return contagens_transicao


# =========================
# 1. EXTRAIR CONTEXTOS DA ÁRVORE
# =========================
def extrair_contextos(arvore, prefixo=()):
    contextos = []

    for chave, valor in arvore.items():
        novo_prefixo = prefixo + (chave,)

        if isinstance(valor, dict):
            contextos.extend(extrair_contextos(valor, novo_prefixo))
        else:
            # folha → contexto válido
            contextos.append(tuple(reversed(novo_prefixo)))

    return contextos


# =========================
# 2. PREPARAR COUNTS
# =========================
def preparar_counts(contagens_transicao, tau, alfabeto):
    counts = {}

    for s in tau:
        c_s_dict = contagens_transicao.get(s, {})
        counts[s] = [c_s_dict.get(k, 0) for k in alfabeto]

    return counts


# =========================
# 3. LOG Q_alpha
# =========================
def log_Q_alpha(counts, alpha):
    log_Q = 0.0

    for s, c_s in counts.items():
        c_s = np.array(c_s)
        m = len(c_s)

        log_const = gammaln(m * alpha) - m * gammaln(alpha)
        log_num = np.sum(gammaln(c_s + alpha))
        log_den = gammaln(np.sum(c_s) + m * alpha)

        log_Q += log_const + log_num - log_den

    return log_Q


# =========================
# EXEMPLO DE USO
# =========================

# Sua árvore
arvore = {
    "A": [0.5, 0.3, 0.2],
    "B": {
        "C": [0.2, 0.5, 0.3],
        "B": [0.3, 0.4, 0.3],
        "A": {
            "A": [0.7, 0.2, 0.1],
            "B": [0.4, 0.4, 0.2],
            "C": [0.5, 0.3, 0.2]
        }
    },
    "C": {
        "A": [0.3, 0.4, 0.3],
        "B": [0.2, 0.5, 0.3],
        "C": [0.4, 0.3, 0.3]
    }
}

# Histórico de estados (exemplo)
X = ["A","B","A","A","C","B","A","B","C","A","A"]

# Alfabeto
alfabeto = ["A", "B", "C"]

# Ordem máxima da árvore
ordem_max = 3

# 1. Contagens
contagens_transicao = contagem_contextos(X, ordem_max)

# 2. Extrair contextos da árvore
tau = extrair_contextos(arvore)

# 3. Preparar counts
counts = preparar_counts(contagens_transicao, tau, alfabeto)

# 4. Calcular log Q
logQ = log_Q_alpha(counts, alpha=0.5)

print("Contextos (tau):", tau)
print("Counts:", counts)
print("log Q:", logQ)
