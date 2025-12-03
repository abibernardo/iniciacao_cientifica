import streamlit as st

st.markdown("""
<style>
    /* MENU LATERAL (nav) */
    [data-testid="stSidebarNav"] {
        background-color: #1E2A38;
        padding-top: 20px;
    }

    /* Textos do menu */
    [data-testid="stSidebarNav"] a {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* Item selecionado */
    [data-testid="stSidebarNav"] a:hover {
        background-color: #2E4053 !important;
        color: #FFFFFF !important;
    }

    [data-testid="stSidebarNav"]::before {
        content: "📘 Minha IC – Unicamp";
        display: block;
        font-size: 18px;
        font-weight: 700;
        color: white;
        margin-left: 20px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="Iniciação Científica",
    page_icon="📊",
    layout="wide"
)

# --- Estilo CSS personalizado ---
st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-top: 40px;
}

.subtitle {
    font-size: 22px;
    font-weight: 400;
    text-align: center;
    color: #555;
    margin-top: -10px;
}

.author-box {
    text-align: center;
    font-size: 18px;
    margin-top: 25px;
    color: #444;
}

.divider {
    height: 2px;
    margin: 35px auto 25px auto;
    background: linear-gradient(90deg, rgba(0,0,0,0) 0%, rgba(90,90,90,0.4) 50%, rgba(0,0,0,0) 100%);
    width: 70%;
    border-radius: 2px;
}

.description {
    text-align: center;
    font-size: 19px;
    max-width: 850px;
    margin: 0 auto;
    line-height: 1.5;
    color: #333;
}

</style>
""", unsafe_allow_html=True)


# --- Conteúdo visual ---
st.markdown("<div class='main-title'>Iniciação Científica – IMECC/Unicamp</div>", unsafe_allow_html=True)

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div class='subtitle'>
Avaliação do Impacto da Priori na Inferência para Árvores de Contexto Bayesianas
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class='author-box'>
<strong>Autor:</strong> Bernardo Abib  
<br>
<strong>Orientador:</strong> Victor Freguglia
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

