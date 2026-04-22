import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Financeiro Família",
    page_icon="💰",
    layout="wide"
)

# =========================
# ESTILO (MOBILE MODERNO)
# =========================
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}

.stApp {
    background-color: #0f172a;
    color: white;
}

h1, h2, h3 {
    color: #38bdf8;
    text-align: center;
}

div[data-testid="metric-container"] {
    background-color: #1e293b;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

.stButton button {
    background-color: #38bdf8;
    color: black;
    border-radius: 8px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# =========================
# TÍTULO
# =========================
st.title("💰 Financeiro da Família")
st.write("Gestão simples de Ruben & Gabi 📱")

# =========================
# DADOS
# =========================
if "data" not in st.session_state:
    st.session_state.data = []

# =========================
# INPUT
# =========================
st.subheader("➕ Novo movimento")

col1, col2 = st.columns(2)

with col1:
    pessoa = st.selectbox("Pessoa", ["Ruben", "Gabi"])

with col2:
    tipo = st.selectbox("Tipo", ["Rendimento", "Despesa"])

descricao = st.text_input("Descrição")
valor = st.number_input("Valor (€)", min_value=0.0, step=10.0)

if st.button("Adicionar"):
    st.session_state.data.append({
        "Pessoa": pessoa,
        "Tipo": tipo,
        "Descrição": descricao,
        "Valor": valor
    })
    st.success("Adicionado 👍")

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(st.session_state.data)

# =========================
# RESUMO
# =========================
st.subheader("📊 Resumo")

if not df.empty:

    ruben = df[df["Pessoa"] == "Ruben"]
    gabi = df[df["Pessoa"] == "Gabi"]

    saldo_ruben = ruben[ruben["Tipo"] == "Rendimento"]["Valor"].sum() - \
                  ruben[ruben["Tipo"] == "Despesa"]["Valor"].sum()

    saldo_gabi = gabi[gabi["Tipo"] == "Rendimento"]["Valor"].sum() - \
                 gabi[gabi["Tipo"] == "Despesa"]["Valor"].sum()

    total = saldo_ruben + saldo_gabi

    col1, col2, col3 = st.columns(3)

    col1.metric("Ruben", f"€ {saldo_ruben:.2f}")
    col2.metric("Gabi", f"€ {saldo_gabi:.2f}")
    col3.metric("Total", f"€ {total:.2f}")

# =========================
# TABELA
# =========================
st.subheader("📋 Movimentos")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Sem dados ainda.")

# =========================
# GRÁFICO
# =========================
if not df.empty:
    st.subheader("📊 Análise")

    fig = px.bar(
        df,
        x="Pessoa",
        y="Valor",
        color="Tipo",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# LIMPAR
# =========================
if st.button("🗑 Limpar tudo"):
    st.session_state.data = []
    st.rerun()