library(bacontrees)

n_replicas <- 3

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

contexto4 <- c(
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


# =========================================================
# PRIORIS
# =========================================================

# Priori que favorece árvores rasas
prior_raso <- function(node) {
  exp(-2 * node$getDepth())
}

# Priori neutro
prior_uniforme <- function(node) {
  1
}

# Priori que favorece árvores profundas
prior_profundo <- function(node) {
  exp(-1 * node$getDepth())
}
#################################################
#################################################

gerar_sequencia <- function(
    amostras,
    alfabeto,
    contexto,
    probs,
    seed = 321
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




# Lista de prioris, lista de alfas, e a sequência para cada modelo




# Gerar duas sequências diferentes para o mesmo modelo para validar ranking das distancias posterioris
# Para cada sequência gerada por modelo, para cada combinação alfa-priori, comparar a distância (tarefa!)
# Usar  500 amostras com 100 de Burn-in 

##################################################
# LISTA DE PRIORIS
##################################################

lista_prioris <- list(
  prior_penalizacao_forte = prior_raso,
  priori_penalizacao_fraca = prior_profundo,
  prior_uniforme = prior_uniforme
)

##################################################
# LISTA DE ALPHAS
##################################################

lista_alphas <- c(
  0.1,
  0.5,
  1
)

##################################################
# TAMANHOS DE AMOSTRA
##################################################

lista_amostras <- c(
  500,
  1000,
  3000,
  5000,
  10000,
  20000
)

##################################################
# MODELOS GERADORES
##################################################

modelos <- list(
  
  modelo_1 = list(
    alfabeto = alfabeto4,
    contexto = contexto4,
    probs = probs4
  ),
  modelo_2 = list(
    alfabeto = alfabeto5,
    contexto = contexto5,
    probs = probs5
  ),
  modelo_3 = list(
    alfabeto = alfabeto6,
    contexto = contexto6,
    probs = probs6
  )
)

##################################################
# GERAR UMA SEQUÊNCIA DE CADA MODELO
##################################################

resultado <- data.frame()

for (nome_modelo in names(modelos)) {
  
  cat("Modelo:", nome_modelo, "\n")
  
  arvore_verdadeira <- modelos[[nome_modelo]]$contexto
  
  max_depth <- max(
    sapply(arvore_verdadeira, function(x) {
      length(strsplit(sub("^\\*\\.", "", x), "\\.")[[1]])
    })
  )
  
  ##################################################
  # GERA UMA ÚNICA SEQUÊNCIA PARA O MODELO
  ##################################################
  
  seq_completa <- gerar_sequencia(
    amostras = max(lista_amostras),
    alfabeto = modelos[[nome_modelo]]$alfabeto,
    contexto = modelos[[nome_modelo]]$contexto,
    probs = modelos[[nome_modelo]]$probs,
    seed = 321
  )
  
  cat("  Sequência completa gerada\n")
  
  ##################################################
  # TAMANHOS DE AMOSTRA
  ##################################################
  
  for (amostras in lista_amostras) {
    
    cat("  Amostras:", amostras, "\n")
    
    # Usa apenas o prefixo da sequência
    seq <- seq_completa[1:amostras]
    
    for (nome_priori in names(lista_prioris)) {
      
      cat("    Priori:", nome_priori, "\n")
      
      priori <- lista_prioris[[nome_priori]]
      
      for (alpha in lista_alphas) {
        
        cat("      alpha =", alpha, "\n")
        
        for (replica in 1:n_replicas) {
          
          cat("        Replica:", replica, "\n")
          
          # Seed apenas para o MCMC
          set.seed(1000 + replica)
          
          distancia <- calcular_distancia_posterior(
            seq = seq,
            arvore_verdadeira = arvore_verdadeira,
            alpha = alpha,
            max_depth = max_depth,
            priori = priori,
            n_steps = 5000,
            burnin = 100
          )
          
          resultado <- rbind(
            resultado,
            data.frame(
              modelo = nome_modelo,
              amostras = amostras,
              replica = replica,
              priori = nome_priori,
              alpha = alpha,
              distancia = distancia
            )
          )
          
          cat("        Linha adicionada\n")
        }
      }
    }
  }
}

resultado


#################

# Visualizações
library(ggplot2)



ggplot(
  resultado,
  aes(
    x = factor(amostras),
    y = distancia,
    fill = factor(alpha)
  )
) +
  geom_boxplot(
    position = position_dodge(0.8)
  ) +
  facet_grid(
    modelo ~ priori
  ) +
  theme_minimal() +
  labs(
    fill = expression(alpha),
    x = "Número de amostras",
    y = "Distância posterior esperada"
  )



# Gerar as probabilidades por um vetor uniforme dividido pela soma

# n_steps: aumentar para 5.000 e ver se resultados mudam muito; se ficarem iguais, nem precisa do boxplot
# Se mudar: Gerar múltiplas vezes (2-3 réplicas); gerar dataframe
# Gerar boxplot ao invés dos graficos de linha

##################################################
# SALVAR RESULTADOS EM ARQUIVO RDS
##################################################

# Cria a pasta "resultados" caso ela não exista
if (!dir.exists("resultados")) {
  dir.create("resultados")
}

# Nome do arquivo com data e hora
nome_arquivo <- paste0(
  "resultado_",
  format(Sys.time(), "%Y%m%d_%H%M%S"),
  ".rds"
)

# Caminho completo
caminho_arquivo <- file.path("resultados", nome_arquivo)

# Salva o data.frame
saveRDS(resultado, file = caminho_arquivo)

# Mensagem de confirmação
cat("\n=========================================\n")
cat("Resultado salvo com sucesso em:\n")
cat(normalizePath(caminho_arquivo), "\n")
cat("=========================================\n")

#resultado <- readRDS("resultados/resultado_20260712_221530.rds")


ggplot(
  resultado,
  aes(
    x = factor(amostras),
    y = distancia,
    colour = factor(alpha)
  )
) +
  geom_point(
    position = position_jitterdodge(
      jitter.width = 0.05,
      dodge.width = 0.8
    ),
    size = 2
  ) +
  facet_grid(modelo ~ priori)




#################################################
#  PROBABILIDADES EXATAS COMPARAÇÃO

##################################################
# COMPARAÇÃO MCMC x POSTERIORI EXATA
##################################################

resultado_posteriori <- data.frame()

# Priori que penaliza mais árvores profundas
priori <- prior_raso

for(nome_modelo in names(modelos)) {
  
  cat("Modelo:", nome_modelo, "\n")
  
  mod <- modelos[[nome_modelo]]
  
  arvore_verdadeira <- mod$contexto
  
  max_depth <- max(
    sapply(
      arvore_verdadeira,
      function(x) {
        length(
          strsplit(
            sub("^\\*\\.", "", x),
            "\\."
          )[[1]]
        )
      }
    )
  )
  
  for(amostras in lista_amostras) {
    
    cat("  Amostras:", amostras, "\n")
    
    # Gerar sequência
    seq <- gerar_sequencia(
      amostras = amostras,
      alfabeto = mod$alfabeto,
      contexto = mod$contexto,
      probs = mod$probs
    )
    
    for(alpha in lista_alphas) {
      
      cat("    Alpha:", alpha, "\n")
      
      # ----------------------------------------------
      # 1. Posteriori via MCMC
      # ----------------------------------------------
      
      posteriori_mcmc <- analisar_sequencia(
        seq = seq,
        alpha = alpha,
        max_depth = max_depth,
        priori = priori,
        n_steps = 5000,
        burnin = 1000
      )
      
      # Probabilidade MCMC da árvore verdadeira
      prob_mcmc <- posteriori_mcmc$df$prob[
        sapply(
          posteriori_mcmc$df$tree_contexts,
          function(x) {
            setequal(
              distancia_arvores(
                x,
                arvore_verdadeira
              ),
              0
            )
          }
        )
      ]
      
      # Se a árvore verdadeira não apareceu
      if(length(prob_mcmc) == 0) {
        prob_mcmc <- 0
      } else {
        prob_mcmc <- sum(prob_mcmc)
      }
      
      
      # ----------------------------------------------
      # 2. Posteriori exata
      # ----------------------------------------------
      
      # Aqui entra a função do pacote
      probabilidades <- activeTreeProbabilities(
        seq,
        alpha = alpha,
        max_depth = max_depth,
        context_weights = priori
      )
      
      # Probabilidade da árvore verdadeira
      prob_exata <- probabilidades[
        names(probabilidades) %in%
          paste(arvore_verdadeira, collapse = ",")
      ]
      
      if(length(prob_exata) == 0) {
        prob_exata <- 0
      }
      
      
      # ----------------------------------------------
      # 3. Armazenar
      # ----------------------------------------------
      
      resultado_posteriori <- rbind(
        resultado_posteriori,
        data.frame(
          modelo = nome_modelo,
          amostras = amostras,
          alpha = alpha,
          posteriori_mcmc = prob_mcmc,
          posteriori_exata = prob_exata
        )
      )
    }
  }
}

resultado_posteriori
