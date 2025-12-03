import streamlit as st

# Configurações gerais do app
st.set_page_config(
    page_title="Iniciação Científica",
    page_icon="📊",
    layout="wide"
)

# ---- Estilo CSS leve e profissional ----
st.markdown("""
<style>
/* Caixa central */
.presentation-box {
    background-color: rgba(255, 255, 255, 0.85);
    padding: 2.5rem;
    border-radius: 18px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    backdrop-filter: blur(4px);
}

/* Título principal */
h1 {
    font-weight: 700 !important;
    font-size: 2.3rem !important;
}

/* Subtítulo */
.subtitle {
    font-size: 1.1rem;
    color: #4A4A4A;
    margin-top: -10px;
}

/* Nome do autor */
.author {
    font-size: 1.2rem;
    font-style: italic;
    margin-top: 25px;
    color: #333;
}
</style>
""", unsafe_allow_html=True)


# ---- Conteúdo da apresentação ----
st.markdown("<div class='presentation-box'>", unsafe_allow_html=True)

st.markdown("<h1>Avaliação do Impacto da Prior na Inferência para Árvores de Contexto Bayesianas</h1>", unsafe_allow_html=True)



# Espaço reservado para você colocar seu nome
st.markdown("""
<div class="author">
<b>Autor:</b> Bernardo Abib 
<b>Orientador:</b> Victor Freguglia
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
