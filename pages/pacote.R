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

# - Priori costuma penalizar profundidade/complexidade; sempre penalizar profundidade
# Mudar prioris: penalizar mais e penalizar menos;




# =========================================================
# PRIORIS
# =========================================================

# Priori que favorece árvores rasas
prior_raso <- function(node) {
  exp(-2 * node$getDepth())
}

# Priori neutro
prior_neutro <- function(node) {
  1
}

# Priori que favorece árvores profundas
prior_profundo <- function(node) {
  exp(-1 * node$getDepth())
}

# =========================================================
# FUNÇÃO AUXILIAR
# =========================================================

# Esta função:
# 1. gera uma sequência
# 2. roda o Metropolis-Hastings
# 3. imprime as árvores mais prováveis

analisar_arvore <- function(
    nome,
    alfabeto,
    contexto,
    probs,
    amostras,
    max_depth
) {
  
  cat("\n")
  cat("=================================================\n")
  cat("MODELO:", nome, "\n")
  cat("=================================================\n")
  
  # ------------------------------------------------
  # Gerando sequência
  # ------------------------------------------------
  
  set.seed(123)
  
  seq <- rvlmc(
    amostras,
    alfabeto,
    contexto,
    probs
  )
  
  # =================================================
  # PRIORI RASA
  # =================================================
  
  cat("\n")
  cat("---------- PRIORI RASO ----------\n")
  
  mh_raso <- metropolis_vlmc(
    seq,
    
    n_steps = 5000,
    burnin = 1000,
    
    max_depth = max_depth,
    
    alpha = 0.5,
    
    context_weights = prior_raso
  )
  
  print(head(mh_raso$df, 5))
  
  # =================================================
  # PRIORI NEUTRO
  # =================================================
  
  cat("\n")
  cat("---------- PRIOR NEUTRO ----------\n")
  
  mh_neutro <- metropolis_vlmc(
    seq,
    
    n_steps = 5000,
    burnin = 1000,
    
    max_depth = max_depth,
    
    alpha = 0.5,
    
    context_weights = prior_neutro
  )
  
  print(head(mh_neutro$df, 5))
  
  # =================================================
  # PRIOR PROFUNDO
  # =================================================
  
  cat("\n")
  cat("---------- PRIOR PROFUNDO ----------\n")
  
  mh_profundo <- metropolis_vlmc(
    seq,
    
    n_steps = 5000,
    burnin = 1000,
    
    max_depth = max_depth,
    
    alpha = 0.5,
    
    context_weights = prior_profundo
  )
  
  print(head(mh_profundo$df, 5))
}



# =========================================================
# MODELO 1 
# =========================================================

analisar_arvore(
  nome = "MODELO 1 — BINÁRIO FÁCIL",
  
  alfabeto = alfabeto1,
  
  contexto = contexto1,
  
  probs = probs1,
  
  amostras = 10000,
  
  max_depth = 2
)



# =========================================================
# MODELO 2 
# =========================================================

analisar_arvore(
  nome = "MODELO 2 — BINÁRIO DIFÍCIL",
  
  alfabeto = alfabeto4,
  
  contexto = contexts4,
  
  probs = probs4,
  
  max_depth = 2
)



# =========================================================
# MODELO 3 
# =========================================================

analisar_arvore(
  nome = "MODELO 3 — PROFUNDIDADE VARIÁVEL",
  
  alfabeto = alfabeto2,
  
  contexto = contexto2,
  
  probs = probs2,
  
  max_depth = 3
)



# =========================================================
# MODELO 4 
# =========================================================

analisar_arvore(
  nome = "MODELO 4 — TRÊS SÍMBOLOS",
  
  alfabeto = alfabeto3,
  
  contexto = contexto3,
  
  probs = probs3,
  
  max_depth = 3
)



# =========================================================
# MODELO 5 
# =========================================================

analisar_arvore(
  nome = "MODELO 5 — ÁRVORE PROFUNDA",
  
  alfabeto = alfabeto5,
  
  contexto = contexto5,
  
  probs = probs5,
  
  max_depth = 4
)



# =========================================================
# MODELO 6 — ALFABETO GRANDE
# =========================================================

analisar_arvore(
  nome = "MODELO 6 — ALFABETO GRANDE",
  
  alfabeto = alfabeto6,
  
  contexto = contexto6,
  
  probs = probs6,
  
  amostras = 1000,
  
  max_depth = 3
)


#############################################

# =========================================================
# FUNÇÃO DE DISTÂNCIA ENTRE ÁRVORES
# =========================================================

# Ideia:
#
# Cada árvore é representada pelo conjunto de contextos.
#
# A distância será baseada na diferença simétrica:
#
# A Δ B
#
# Ou seja:
#
# - contextos que existem em A mas não em B
# - contextos que existem em B mas não em A
#
# ---------------------------------------------------------
# Exemplo:
#
# árvore verdadeira:
# "*.a" "*.b"
#
# árvore estimada:
# "*.a.a" "*.a.b" "*.b"
#
# diferença:
#
# perde "*.a"
# ganha "*.a.a"
# ganha "*.a.b"
#
# distância = 3
#
# =========================================================


distancia_arvores <- function(
    arvore_estimada,
    arvore_verdadeira
) {
  
  # ------------------------------------------------------
  # Transformar string em vetor de contextos
  # ------------------------------------------------------
  
  parse_contextos <- function(x) {
    
    # remove chaves
    x <- gsub("\\{", "", x)
    x <- gsub("\\}", "", x)
    
    # separa por vírgula
    x <- strsplit(x, ",")[[1]]
    
    # remove espaços
    x <- trimws(x)
    
    x
  }
  
  # ------------------------------------------------------
  # Se vier string:
  # "{*.a,*.b}"
  # transformar em vetor
  # ------------------------------------------------------
  
  if (length(arvore_estimada) == 1) {
    arvore_estimada <- parse_contextos(arvore_estimada)
  }
  
  if (length(arvore_verdadeira) == 1) {
    arvore_verdadeira <- parse_contextos(arvore_verdadeira)
  }
  
  # ------------------------------------------------------
  # Diferença simétrica
  # ------------------------------------------------------
  
  apenas_estimada <- setdiff(
    arvore_estimada,
    arvore_verdadeira
  )
  
  apenas_verdadeira <- setdiff(
    arvore_verdadeira,
    arvore_estimada
  )
  
  distancia <- length(apenas_estimada) +
    length(apenas_verdadeira)
  
  
  return(distancia)
}



# exemplos

distancia_arvores(
  "{*.a,*.b}",
  "{*.a,*.b}"
)


distancia_arvores(
  "{*.a.a,*.a.b,*.b}",
  "{*.a,*.b}"
)

distancia_arvores(
  "{*.a,*.b,*.c.a,*.c.b}",
  "{*.a,*.b}"
)


############## Distância esperada




# POSTERIORIS
posterioris <- function(
    alfabeto,
    contexto,
    probs,
    amostras,
    max_depth,
    prior
) {
  
  # ------------------------------------------------------
  # Gerando sequência
  # ------------------------------------------------------
  
  set.seed(123)
  
  seq <- rvlmc(
    amostras,
    alfabeto,
    contexto,
    probs
  )
  
  # ------------------------------------------------------
  # Rodando Metropolis-Hastings
  # ------------------------------------------------------
  
  mh <- metropolis_vlmc(
    
    seq,
    
    n_steps = 5000,
    
    burnin = 1000,
    
    max_depth = max_depth,
    
    alpha = 0.5,
    
    context_weights = prior
  )
  
  return(mh)
}

mh_raso <- posterioris(
  
  alfabeto = alfabeto1,
  
  contexto = contexto1,
  
  probs = probs1,
  
  amostras = 10000,
  
  max_depth = 2,
  
  prior = prior_raso
)

# --------------------------------------------------------
# Rodando algoritmo com prior neutro
# --------------------------------------------------------

mh_neutro <- analisar_arvore(
  
  alfabeto = alfabeto1,
  
  contexto = contexto1,
  
  probs = probs1,
  
  amostras = 10000,
  
  max_depth = 2,
  
  prior = prior_neutro
)

# --------------------------------------------------------
# Rodando algoritmo com prior profundo
# --------------------------------------------------------

mh_profundo <- analisar_arvore(
  
  alfabeto = alfabeto1,
  
  contexto = contexto1,
  
  probs = probs1,
  
  amostras = 10000,
  
  max_depth = 2,
  
  prior = prior_profundo
)

##### distancia poteriori esperada

distancia_posterior_esperada <- function(
    mh_result,
    arvore_verdadeira
) {
  
  df <- mh_result$df
  
  distancias <- sapply(
    df$tree_contexts,
    function(x) {
      distancia_arvores(
        x,
        arvore_verdadeira
      )
    }
  )
  
  soma <- sum(
    distancias * df$prob
  )
  
  return(soma)
}


distancia_posterior_esperada(
  mh_raso,
  "{*.a,*.b}"
)
