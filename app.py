import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px

st.set_page_config(
    page_title="Dashboard – Varejo Moda",
    layout="wide"
)

st.title("Dashboard – Varejo de Moda por Datas Comemorativas")

# --------------------------------------------------------------------------------
# GERAÇÃO DE DADOS MOCKADOS
# --------------------------------------------------------------------------------
np.random.seed(42)

meses = pd.date_range(start="2025-01-01", periods=12, freq="M")

def make_share_df(index, categories, col_index="Período", col_cat="Categoria", col_val="Percentual"):
    rows = []
    for t in index:
        vals = np.random.rand(len(categories))
        vals = vals / vals.sum()  # normaliza para somar 1 (100%)
        for cat, v in zip(categories, vals):
            rows.append({col_index: t, col_cat: cat, col_val: v})
    return pd.DataFrame(rows)

# 1) Tendências de comportamento
canais_compra_df = make_share_df(
    meses,
    ["Online - Site", "Online - App", "Loja física"],
    col_index="Mês",
    col_cat="Canal",
    col_val="Percentual"
)

motivadores_compra_df = make_share_df(
    meses,
    ["Influenciadores", "Mídia paga", "Promoções/Descontos", "Tendência/Novidade"],
    col_index="Mês",
    col_cat="Motivador",
    col_val="Percentual"
)

habitos_midia_df = make_share_df(
    meses,
    ["Redes sociais", "TV/Streaming", "Lojas físicas/Vitrines", "Boca a boca/Influencers"],
    col_index="Mês",
    col_cat="Hábito de mídia",
    col_val="Percentual"
)

# 2) Tendências de consumo – próprio vs presente
consumo_finalidade_df = make_share_df(
    meses,
    ["Consumo próprio", "Presentear"],
    col_index="Mês",
    col_cat="Finalidade",
    col_val="Percentual"
)

# Ticket médio por região
regioes = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]
rows_ticket = []
for mes in meses:
    base = np.random.randint(120, 260)
    ajustes = np.random.randint(-40, 40, size=len(regioes))
    for r, aj in zip(regioes, ajustes):
        rows_ticket.append({
            "Mês": mes,
            "Região": r,
            "Ticket médio (R$)": max(60, base + aj)
        })
ticket_regiao_df = pd.DataFrame(rows_ticket)

# 3) Intenção e disposição – quanto pretende gastar + share-roupas
faixas_gasto = ["Até R$ 150", "R$ 151-300", "R$ 301-500", "Acima de R$ 500"]
gasto_vals = np.random.rand(len(faixas_gasto))
gasto_vals = gasto_vals / gasto_vals.sum()
pretende_gastar_df = pd.DataFrame({
    "Faixa de gasto no próximo mês": faixas_gasto,
    "Percentual": gasto_vals
})

categorias_nao_essenciais = ["Roupas", "Beleza", "Lazer", "Eletrônicos"]
share_vals = np.array([0.4, 0.25, 0.2, 0.15])  # já normalizado
share_roupas_df = pd.DataFrame({
    "Categoria": categorias_nao_essenciais,
    "Share do gasto em não essenciais": share_vals
})

# 4) Cenário competitivo – consideração ao longo do tempo
marcas = ["Riachuelo", "Renner", "C&A", "Zara"]
rows_marcas = []
for mes in meses:
    base = np.random.randint(40, 70)
    ajustes = np.random.randint(-15, 15, size=len(marcas))
    for m, aj in zip(marcas, ajustes):
        val = np.clip(base + aj, 10, 90) / 100  # converte para 0-1
        rows_marcas.append({
            "Mês": mes,
            "Marca": m,
            "Consideração": val
        })
consideracao_df = pd.DataFrame(rows_marcas)

# 5) Zoom em datas – territórios (radar) e drivers (barras)
datas_especiais = ["Dia das Mães", "Natal", "Black Friday"]

territorios_por_data = {
    "Dia das Mães": {
        "Nostalgia": 0.8,
        "Conexão": 0.95,
        "Celebração": 0.75,
        "Cuidado": 0.9,
        "Autoexpressão": 0.6
    },
    "Natal": {
        "Nostalgia": 0.9,
        "Conexão": 0.85,
        "Celebração": 0.95,
        "Cuidado": 0.7,
        "Autoexpressão": 0.5
    },
    "Black Friday": {
        "Nostalgia": 0.3,
        "Conexão": 0.5,
        "Celebração": 0.6,
        "Cuidado": 0.4,
        "Autoexpressão": 0.7
    }
}

drivers_por_data = {
    "Dia das Mães": {
        "Emoção da mensagem": 0.9,
        "Curadoria de presentes": 0.85,
        "Preço / promoções": 0.7,
        "Facilidade de troca": 0.8,
        "Experiência loja/app": 0.78
    },
    "Natal": {
        "Campanhas inspiracionais": 0.92,
        "Sortimento temático": 0.88,
        "Preço / promoções": 0.83,
        "Experiência loja/app": 0.75,
        "Disponibilidade de tamanhos": 0.68
    },
    "Black Friday": {
        "Descontos agressivos": 0.95,
        "Comunicação de urgência": 0.85,
        "Facilidade de compra online": 0.9,
        "Confiança em trocas/entregas": 0.78,
        "Experiência no app/site": 0.82
    }
}

# --------------------------------------------------------------------------------
# LAYOUT – ABAS
# --------------------------------------------------------------------------------
tabs = st.tabs([
    "Tendências de comportamento (Quem são)",
    "Tendências de consumo (O que consomem)",
    "Intenção & disposição para gastar",
    "Cenário competitivo (Marca & concorrentes)",
    "Zoom em datas (Mood & drivers)"
])

# --------------------------------------------------------------------------------
# 1) TENDÊNCIAS DE COMPORTAMENTO
# --------------------------------------------------------------------------------
with tabs[0]:
    st.subheader("Tendências de comportamento – Quem são")

    tipo_visao = st.radio(
        "Selecione o tipo de visão:",
        [
            "Canais de compra ao longo do tempo",
            "Motivadores de compra ao longo do tempo",
            "Hábitos de mídia ao longo do tempo"
        ],
        horizontal=True
    )

    if tipo_visao == "Canais de compra ao longo do tempo":
        df = canais_compra_df.rename(columns={"Percentual": "Share"})
        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Mês:T", title="Mês"),
                y=alt.Y("Share:Q", axis=alt.Axis(format="%"), title="Participação (%)"),
                color=alt.Color("Canal:N", title="Canal"),
                tooltip=["Mês:T", "Canal:N", alt.Tooltip("Share:Q", format=".0%")]
            )
            .properties(height=400)
        )
        st.altair_chart(chart, use_container_width=True)

    elif tipo_visao == "Motivadores de compra ao longo do tempo":
        df = motivadores_compra_df.rename(columns={"Percentual": "Share"})
        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Mês:T", title="Mês"),
                y=alt.Y("Share:Q", axis=alt.Axis(format="%"), title="Participação (%)"),
                color=alt.Color("Motivador:N", title="Motivador"),
                tooltip=["Mês:T", "Motivador:N", alt.Tooltip("Share:Q", format=".0%")]
            )
            .properties(height=400)
        )
        st.altair_chart(chart, use_container_width=True)

    else:  # Hábitos de mídia
        df = habitos_midia_df.rename(columns={"Percentual": "Share"})
        chart = (
            alt.Chart(df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Mês:T", title="Mês"),
                y=alt.Y("Share:Q", axis=alt.Axis(format="%"), title="Participação (%)"),
                color=alt.Color("Hábito de mídia:N", title="Hábito de mídia"),
                tooltip=["Mês:T", "Hábito de mídia:N", alt.Tooltip("Share:Q", format=".0%")]
            )
            .properties(height=400)
        )
        st.altair_chart(chart, use_container_width=True)

# --------------------------------------------------------------------------------
# 2) TENDÊNCIAS DE CONSUMO
# --------------------------------------------------------------------------------
with tabs[1]:
    st.subheader("Tendências de consumo – O que consomem")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Consumo próprio vs presentear (ao longo do tempo)")
        df = consumo_finalidade_df.rename(columns={"Percentual": "Share"})
        chart = (
            alt.Chart(df)
            .mark_area()
            .encode(
                x=alt.X("Mês:T", title="Mês"),
                y=alt.Y("Share:Q", stack="normalize", axis=alt.Axis(format="%"), title="Participação (%)"),
                color=alt.Color("Finalidade:N", title="Finalidade"),
                tooltip=["Mês:T", "Finalidade:N", alt.Tooltip("Share:Q", format=".0%")]
            )
            .properties(height=380)
        )
        st.altair_chart(chart, use_container_width=True)

    with col2:
        st.markdown("#### Ticket médio por região (R$/mês)")
        chart_ticket = (
            alt.Chart(ticket_regiao_df)
            .mark_line(point=True)
            .encode(
                x=alt.X("Mês:T", title="Mês"),
                y=alt.Y("Ticket médio (R$):Q", title="Ticket médio (R$)"),
                color=alt.Color("Região:N", title="Região"),
                tooltip=["Mês:T", "Região:N", "Ticket médio (R$):Q"]
            )
            .properties(height=380)
        )
        st.altair_chart(chart_ticket, use_container_width=True)

# --------------------------------------------------------------------------------
# 3) INTENÇÃO & DISPOSIÇÃO PARA GASTAR
# --------------------------------------------------------------------------------
with tabs[2]:
    st.subheader("Intenção de compra e disposição para gastar")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Quanto pretende gastar em roupas no próximo mês")
        chart_gasto = (
            alt.Chart(pretende_gastar_df)
            .mark_bar()
            .encode(
                x=alt.X("Faixa de gasto no próximo mês:N", title="Faixa de gasto"),
                y=alt.Y("Percentual:Q", axis=alt.Axis(format="%"), title="Participação (%)"),
                tooltip=["Faixa de gasto no próximo mês:N", alt.Tooltip("Percentual:Q", format=".0%")]
            )
            .properties(height=380)
        )
        st.altair_chart(chart_gasto, use_container_width=True)

    with col2:
        st.markdown("#### Share-roupas dentro do gasto em não essenciais")
        chart_share = (
            alt.Chart(share_roupas_df)
            .mark_bar()
            .encode(
                x=alt.X("Categoria:N", title="Categoria não essencial"),
                y=alt.Y("Share do gasto em não essenciais:Q", axis=alt.Axis(format="%"), title="Share (%)"),
                tooltip=["Categoria:N", alt.Tooltip("Share do gasto em não essenciais:Q", format=".0%")]
            )
            .properties(height=380)
        )
        st.altair_chart(chart_share, use_container_width=True)

# --------------------------------------------------------------------------------
# 4) CENÁRIO COMPETITIVO
# --------------------------------------------------------------------------------
with tabs[3]:
    st.subheader("Cenário competitivo – Marca & concorrentes")

    st.markdown("#### Nível de consideração ao longo do tempo")

    chart_consideracao = (
        alt.Chart(consideracao_df)
        .mark_line(point=True)
        .encode(
            x=alt.X("Mês:T", title="Mês"),
            y=alt.Y("Consideração:Q", axis=alt.Axis(format="%"), title="Consideração (%)"),
            color=alt.Color("Marca:N", title="Marca"),
            tooltip=["Mês:T", "Marca:N", alt.Tooltip("Consideração:Q", format=".0%")]
        )
        .properties(height=420)
    )
    st.altair_chart(chart_consideracao, use_container_width=True)

# --------------------------------------------------------------------------------
# 5) ZOOM EM DATAS – MOOD & DRIVERS
# --------------------------------------------------------------------------------
with tabs[4]:
    st.subheader("Zoom em datas – Mood da data & drivers de consumo")

    data_selecionada = st.selectbox(
        "Selecione uma data comemorativa:",
        datas_especiais
    )

    col1, col2 = st.columns(2)

    # Radar de territórios
    with col1:
        st.markdown(f"#### Territórios de marca – {data_selecionada}")
        territ_dict = territórios = territorios_por_data[data_selecionada]
        territ_df = pd.DataFrame({
            "Território": list(territ_dict.keys()),
            "Score": list(territ_dict.values())
        })

        # Radar com Plotly
        radar_fig = px.line_polar(
            territ_df,
            r="Score",
            theta="Território",
            line_close=True,
            range_r=[0, 1]
        )
        radar_fig.update_traces(fill="toself")
        st.plotly_chart(radar_fig, use_container_width=True)

    # Drivers de consumo
    with col2:
        st.markdown(f"#### Drivers de consumo – {data_selecionada}")
        drivers_dict = drivers_por_data[data_selecionada]
        drivers_df = pd.DataFrame({
            "Driver": list(drivers_dict.keys()),
            "Peso": list(drivers_dict.values())
        })

        drivers_chart = (
            alt.Chart(drivers_df)
            .mark_bar()
            .encode(
                x=alt.X("Peso:Q", title="Força do driver", scale=alt.Scale(domain=[0, 1])),
                y=alt.Y("Driver:N", sort="-x", title="Driver"),
                tooltip=["Driver:N", alt.Tooltip("Peso:Q", format=".0%")]
            )
            .properties(height=380)
        )
        st.altair_chart(drivers_chart, use_container_width=True)
