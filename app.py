import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Gestão Rubi&Gabi",
    page_icon="💰",
    layout="wide"
)

# =========================
# ESTILO (MOBILE + ANIMAÇÕES)
# =========================
st.markdown("""
<style>

/* fundo */
body, .stApp {
    background-color: #2b3441;
    color: white;
    font-family: 'Arial';
}

/* títulos */
h1, h2, h3 {
    text-align: center;
    color: #38bdf8;
}

/* cartões métricas estilo app */
div[data-testid="metric-container"] {
    background-color: #3a4656;
    border-radius: 16px;
    padding: 16px;
    transition: all 0.3s ease-in-out;
}

/* hover suave */
div[data-testid="metric-container"]:hover {
    transform: scale(1.02);
    background-color: #44536a;
}

/* animação de entrada */
.stApp {
    animation: fadeIn 0.6s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* botões */
button {
    border-radius: 10px !important;
    transition: 0.2s;
}

button:hover {
    transform: scale(1.03);
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
st.subheader("➕ Novo movimento")

pessoa = st.selectbox("Pessoa", ["Ruben", "Gabi"])
tipo = st.selectbox("Tipo", ["Salário", "Subsídio Alimentação", "Despesa"])

categoria = ""
descricao = ""

if tipo == "Despesa":
    categoria = st.selectbox(
        "Categoria da Despesa",
        ["Renda", "Água", "Luz", "Vodafone", "Alimentação", "Gasolina", "Outros"]
    )

    if categoria == "Outros":
        descricao = st.text_input("📝 Descrição")

valor = st.number_input("Valor (€)", min_value=0.0, step=10.0)
data = st.date_input("Data", datetime.today())

# =========================
# ADICIONAR
# =========================
if st.button("Adicionar"):
    st.session_state.data.append({
        "Pessoa": pessoa,
        "Tipo": tipo,
        "Categoria": categoria,
        "Descrição": descricao,
        "Valor": valor,
        "Data": data,
        "Ano": data.year,
        "Mês": data.month
    })
    st.success("Adicionado 👍")

# =========================
# DATAFRAME
# =========================
df = pd.DataFrame(st.session_state.data)

# =========================
# RESUMO
# =========================
st.subheader("📊 Resumo Financeiro")

if not df.empty:

    rend = df[df["Tipo"].isin(["Salário", "Subsídio Alimentação"])]["Valor"].sum()
    desp = df[df["Tipo"] == "Despesa"]["Valor"].sum()
    saldo = rend - desp

    col1, col2, col3 = st.columns(3)

    col1.metric("💵 Rendimentos", f"€ {rend:.2f}")
    col2.metric("🧾 Despesas", f"€ {desp:.2f}")
    col3.metric("📈 Saldo", f"€ {saldo:.2f}")

    # =========================
    # ALERTAS INTELIGENTES
    # =========================
    if rend > 0:

        percent = desp / rend

        if percent >= 1:
            st.error("🚨 Despesas ultrapassaram os rendimentos!")
        elif percent >= 0.8:
            st.warning("⚠️ Estás perto de ultrapassar o orçamento (80%)")
        else:
            st.success("✅ Gestão financeira saudável")

# =========================
# FILTRO
# =========================
if not df.empty:
    pessoa_sel = st.selectbox("Ver dados de:", ["Todos", "Ruben", "Gabi"])
    if pessoa_sel != "Todos":
        df = df[df["Pessoa"] == pessoa_sel]

# =========================
# GRÁFICO MENSAL
# =========================
if not df.empty:

    st.subheader("📊 Evolução Mensal")

    mensal = df.groupby("Mês")["Valor"].sum().reset_index()

    fig = px.bar(mensal, x="Mês", y="Valor", text="Valor")
    st.plotly_chart(fig, use_container_width=True)

# =========================
# DESPESAS
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
st.subheader("📅 Histórico")

if not df.empty:
    st.dataframe(df, use_container_width=True)
else:
    st.info("Sem dados ainda.")
