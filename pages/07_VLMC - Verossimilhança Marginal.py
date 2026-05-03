import numpy as np
from scipy.special import gammaln

arvore = {

    # Hoje é A
    "A": [0.5, 0.3, 0.2],

    # Hoje é B
    "B": {

        # Ontem foi C
        "C": [0.2, 0.5, 0.3],
        # Ontem foi B
        "B": [0.3, 0.4, 0.3],
        # Ontem foi A
        "A": {
            # Anteontem foi A:
            "A": [0.7, 0.2, 0.1],
            # Anteontem foi B:
            "B": [0.4, 0.4, 0.2],
            # Anteontem foi C:
            "C": [0.5, 0.3, 0.2]
        }
    },

    # Hoje é C
    "C": {
        # Ontem foi A
        "A": [0.3, 0.4, 0.3],
        # Ontem foi B
        "B": [0.2, 0.5, 0.3],
        # Ontem foi C
        "C": [0.4, 0.3, 0.3]
    }
}

def achar_contexto(arvore, historico):
    contexto = arvore

    # percorre do mais recente para o mais antigo.
    # Se historico = [anteontem, ontem, hoje], então partimos de 'hoje' até 'anteontem'
    for s in list(reversed(historico)):

        # se já estamos numa folha → contexto encontrado, retona folha com probabilidades
        if isinstance(contexto, list):
            return contexto

        # se existe ramo correspondente, desce a árvore (estado anterior) e retorna ao loop
        if s in contexto:
            contexto = contexto[s]
        # se não existe ramo correspondente, sai do loop
        else:
            break  # não há mais aprofundamento possível

    # se terminamos numa lista, retornamos a folha com as probabilidades
    if isinstance(contexto, list):
        return contexto
    # Caso contrário, o historico não existe na árvore
    raise ValueError("Nenhum contexto encontrado.")

def simular_vlmc(arvore, estados, T, pi, ordem_max):
    # Passado inicial gerado da distribuição inicial
    X = [np.random.choice(estados, p=pi) for _ in range(ordem_max)]

    # Evolução da cadeia
    for t in range(ordem_max, T):

        #Pega os últimos ordem_max estados do histórico, sem inverter a ordem (do mais antigo até o mais novo)
        historico = X[-ordem_max:]

        # Encontramos as probs de transição com a função auxiliar
        probs = achar_contexto(arvore, historico)

        # Sorteamos o próximo estado segundo essa distribuição
        proximo = np.random.choice(estados, p=probs)

        # Acrescentamos à sequência
        X.append(proximo)

    return X


estados = ["A", "B", "C"]
pi = np.array([0.5, 0.3, 0.2])
X = simular_vlmc(arvore, estados, T=2000, pi=pi, ordem_max=3)

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
            contextos.append(tuple(novo_prefixo)) # do mais recente ao mais antigo, igual a árvore

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
