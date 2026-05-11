library(bacontrees)

alfabeto <- c("a", "b", "c")

lista_contextos <- c("*.a", "*.b", "*.c.a", "*.c.b", "*.c.c")

probabilidades_contextos <- list(
  c(0.1, 0.2, 0.7),
  c(0.3, 0.3, 0.4),
  c(0.2, 0.1, 0.7),
  c(0.01, 0.98, 0.01),
  c(0.4, 0.4, 0.2)
)

set.seed(123)
sequencia <- rvlmc(500, alfabeto, lista_contextos, probabilidades_contextos)

ajuste <- fit_vlmc(sequencia, cutoff = 10, max_length = 3)

ajuste$getActiveNodes()

plot(ajuste)

bt <- baConTree$new(
  data = sequencia,
  maximalDepth = 3,
  alpha = 0.5,
  priorWeights = function(node) {
    exp(-100*node$getDepth())
  }
)

bt$getMarginalLikelihood(log = TRUE)

bt$activateMap()

bt$getActiveNodes()

plot(bt)

library(bacontrees)
alfabeto1 <- c("a", "b")

contexto1 <- c(
  "*.a",
  "*.b"
)

probs1 <- list(
  c(0.9, 0.1),  # após "a"
  c(0.1, 0.9)   # após "b"
)

##########

alfabeto4 <- c("a", "b")

contexts4 <- c(
  "*.a",
  "*.b"
)

probs4 <- list(
  c(0.51, 0.49),
  c(0.49, 0.51)
)

##############

alfabeto2 <- c("a", "b")

contexto2 <- c(
  "*.a",
  "*.b.a",
  "*.b.b"
)

probs2 <- list(
  c(0.8, 0.2),  # após "a"
  c(0.1, 0.9),  # após "ab"
  c(0.7, 0.3)   # após "bb"
)

#########################

alfabeto3 <- c("a", "b", "c")

contexto3 <- c(
  "*.a",
  "*.b",
  "*.c.a",
  "*.c.b",
  "*.c.c"
)

probs3 <- list(
  c(0.1, 0.2, 0.7),   # após "a"
  c(0.3, 0.3, 0.4),   # após "b"
  c(0.2, 0.1, 0.7),   # após "ac"
  c(0.01, 0.98, 0.01),# após "bc"
  c(0.4, 0.4, 0.2)    # após "cc"
)

############

alfabeto5 <- c("a", "b", "c")

contexto5 <- c(
  "*.a",
  "*.b",
  "*.c.a",
  "*.c.b",
  "*.c.c.a",
  "*.c.c.b",
  "*.c.c.c"
)

probs5 <- list(
  c(0.7, 0.2, 0.1),   # após "a"
  c(0.2, 0.7, 0.1),   # após "b"
  c(0.1, 0.1, 0.8),   # após "ac"
  c(0.05, 0.9, 0.05), # após "bc"
  c(0.8, 0.1, 0.1),   # após "acc"
  c(0.1, 0.8, 0.1),   # após "bcc"
  c(0.33, 0.33, 0.34) # após "ccc"
)

#############

alfabeto6 <- c("a", "b", "c", "d")

contexto6 <- c(
  "*.a",
  "*.b",
  "*.c",
  "*.d.a",
  "*.d.b",
  "*.d.c",
  "*.d.d"
)

probs6 <- list(
  c(0.7, 0.1, 0.1, 0.1),
  c(0.1, 0.7, 0.1, 0.1),
  c(0.1, 0.1, 0.7, 0.1),
  c(0.25, 0.25, 0.25, 0.25),
  c(0.05, 0.8, 0.1, 0.05),
  c(0.1, 0.1, 0.7, 0.1),
  c(0.4, 0.2, 0.2, 0.2)
)

################################
set.seed(123)

seq <- rvlmc(
  1000,
  alfabeto5,
  contexto5,
  probs5
)

plot(
  fit_vlmc(seq, cutoff = 10, max_length = 4)
)

# Comparação de prioris:
# QUanto de probabilidade a posteriori está sendo atribuída para a árvore certa
# Medida de distância entre árvores; qual árvore está 'mais próxima' da árvore correta?

# Diferença simétrica - contexto 5 - 'crescer um galho extra em c.a, é diferença simétrica = 4
# (ganho contextos c.a.a, c.a.b, c.a.c que não existem, e perco contexto c.a que existe)
# Diferença simétrica = (tamanho do alfabeto+1) * operação que se distancia da árvore  
# -- pode ser métrica de distância: qtd de operações que se distancia da árvore real
# Distância esperada das árvores sugeridas pelo algoritmo de acordo com as probabilidades atribuídas

# Atv: explorar as posteriores das árvores de exemplo
# Usar função metropolis_vlmc

