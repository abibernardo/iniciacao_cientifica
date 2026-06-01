library(bacontrees)

# Arvores:

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

#################################################
#################################################

gerar_sequencia <- function(
    amostras,
    alfabeto,
    contexto,
    probs,
    seed = 123
) {
  
  set.seed(seed)
  
  rvlmc(
    amostras,
    alfabeto,
    contexto,
    probs
  )
  
}



analisar_sequencia <- function(
    seq,
    alpha,
    max_depth,
    priori,
    n_steps = 5000,
    burnin = 1000
) {
  

  
  posteriori <- metropolis_vlmc(
    seq,
    n_steps = n_steps,
    burnin = burnin,
    max_depth = max_depth,
    alpha = alpha,
    context_weights = priori
  )
  
  
  invisible(posteriori)
}

################
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
  
  simbolos <- unique(
    sub("^\\*\\.", "", arvore_verdadeira)
  )
  
  tamanho_alfabeto <- length(simbolos)
  
  distancia <- (length(apenas_estimada) +
    length(apenas_verdadeira)) / (tamanho_alfabeto + 1)
  
  
  return(distancia)
}

#############

distancia_posterior_esperada <- function(
    posteriori,
    arvore_verdadeira
) {
  
  df <- posteriori$df
  
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

calcular_distancia_posterior <- function(
    seq,
    arvore_verdadeira,
    alpha,
    max_depth,
    priori,
    n_steps = 5000,
    burnin = 1000
) {
  
  posteriori <- analisar_sequencia(
    seq = seq,
    alpha = alpha,
    max_depth = max_depth,
    priori = priori,
    n_steps = n_steps,
    burnin = burnin
  )
  
  distancia_posterior_esperada(
    posteriori,
    arvore_verdadeira
  )
  
}

############################################

seq <- gerar_sequencia(
  amostras = 10000,
  alfabeto = alfabeto1,
  contexto = contexto1,
  probs = probs1
)

calcular_distancia_posterior(
  seq = seq,
  arvore_verdadeira = contexto1,
  alpha = 0.5,
  max_depth = 2,
  priori = prior_raso
)


# Lista de prioris, lista de alfas, e a sequência para cada modelo

# Gerar duas sequências diferentes para o mesmo modelo para validar ranking das distancias posterioris
# Para cada sequência gerada por modelo, para cada combinação alfa-priori, comparar a distância (tarefa!)
# Usar  500 amostras com 100 de Burn-in 
