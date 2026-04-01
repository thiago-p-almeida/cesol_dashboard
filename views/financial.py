import streamlit as st
import pandas as pd
from components.cards import render_kpi_grid
from components.charts import create_premium_pie, create_premium_bar
from components.typography import render_page_header, render_section_title

def render_financial_view(df_filtered: pd.DataFrame, expenses_summary: dict) -> None:
    
    render_page_header(
        page_id="financial",
        title="Performance Financeira",
        subtitle="Análise detalhada de receitas e custos por segmento"
    )
    
    if df_filtered is None or df_filtered.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return

    receita_total = float(df_filtered["net_tuition"].sum())
    ticket_medio = float(df_filtered["net_tuition"].mean())
    qtd_alunos = len(df_filtered)
    meta_ticket = 800.0

    cols = st.columns(3)
    metrics =[
        {"label": "Alunos na Seleção", "value": f"{qtd_alunos}", "type": "info"},
        {"label": "Ticket Médio", "value": f"R$ {ticket_medio:,.2f}", "delta": f"{(ticket_medio - meta_ticket):+,.2f} vs meta", "trend": "up" if ticket_medio >= meta_ticket else "down", "type": "success" if ticket_medio >= meta_ticket else "warning"},
        {"label": "Receita Líquida", "value": f"R$ {receita_total:,.2f}", "delta": "Faturamento Total do Recorte", "type": "success"}
    ]
    render_kpi_grid(metrics, cols)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        render_section_title("Composição de Custos")
        details = expenses_summary.get("details")
        if isinstance(details, pd.DataFrame) and not details.empty:
            st.plotly_chart(create_premium_pie(details, "valor", "categoria"), use_container_width=True)
        else:
            st.info("Sem dados de custos para exibir.")
    with c2:
        render_section_title("Receita por Série")
        df_grade = df_filtered.groupby("grade")["net_tuition"].sum().reset_index()
        st.plotly_chart(create_premium_bar(df_grade, "grade", "net_tuition"), use_container_width=True)