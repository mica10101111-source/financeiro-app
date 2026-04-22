import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="Gestão Rubi&Gabi",
    page_icon="💰",
    layout="wide"
)

# =========================
# ESTILO (CINZA MODERNO)
# =========================
st.markdown("""
<style>
body {
    background-color: #2b3441;
    color: white;
}

.stApp {
    background-color: #2b3441;
    color: white;
}

h1, h2, h3 {
    text-align: center;
    color: #38bdf8;
}

div[data-testid="metric-container"] {
    background-color: #3a4656;
    border-radius: 12px;
    padding: 15px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# DADOS
# =========================
if "data" not in st.session_state:
    st.session_state.data = []

# =========================
# TÍTULO
# =========================
st.title("💰 Gestão Rubi&Gabi")

# =========================
# INPUT
# =========================
st.subheader("➕ Adicionar movimento")

col1, col2 = st.columns(2)

with col1:
    pessoa = st.selectbox("Pessoa", ["Ruben", "Gabi"])

with col2:
    tipo = st.selectbox("Tipo", ["Salário", "Subsídio Alimentação", "Despesa"])

categoria = st.selectbox(
    "Categoria",
    ["Renda", "Água", "Luz", "Vodafone", "Alimentação", "Gasolina", "Outros"]
)

# 🧠 DESCRIÇÃO SÓ SE FOR "OUTROS"
descricao = ""

if categoria == "Outros":
    descricao = st.text_input("📝 Descrição (obrigatório para 'Outros')")

valor = st.number_input("Valor (€)", min_value=0.0, step=10.0)

data = st.date_input("Data", datetime.today())

if st.button("Adicionar"):
    st.session_state.data.append({
        "Pessoa": pessoa,
        "Tipo": tipo,
        "Categoria": categoria,
        "Descrição": descricao,
        "Valor": valor,
        "Data": data
    })
    st.success("Adicionado 👍")

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(st.session_state.data)

# =========================
# RESUMO
# =========================
st.subheader("📊 Resumo Mensal")

if not df.empty:

    rend = df[df["Tipo"].isin(["Salário", "Subsídio Alimentação"])]["Valor"].sum()
    desp = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    saldo = rend - desp

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Rendimentos", f"€ {rend:.2f}")
    col2.metric("🧾 Despesas", f"€ {desp:.2f}")
    col3.metric("📈 Saldo", f"€ {saldo:.2f}")

# =========================
# GRÁFICO 1
# =========================
if not df.empty:
    st.subheader("📊 Rendimentos vs Despesas")

    fig = px.bar(
        df,
        x="Tipo",
        y="Valor",
        color="Tipo",
        barmode="group"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# GRÁFICO 2
# =========================
if not df.empty:
    st.subheader("📊 Despesas por Categoria")

    despesas = df[df["Tipo"] == "Despesa"]

    fig2 = px.pie(
        despesas,
        values="Valor",
        names="Categoria"
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# HISTÓRICO
# =========================
st.subheader("📋 Histórico Completo")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.markdown("""
    <div style="
        background-color: #ab91ed;
        color: white;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
    ">
    Sem dados ainda
    </div>
    """, unsafe_allow_html=True)

# =========================
# RESET
# =========================
if st.button("🗑 Limpar tudo"):
    st.session_state.data = []
    st.rerun()
