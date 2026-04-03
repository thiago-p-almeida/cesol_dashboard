import streamlit as st
import pandas as pd
from components.cards import render_kpi_grid
from components.charts import create_premium_pie, create_premium_bar
from components.typography import render_page_header, render_section_title

def render_financial_view(df_filtered: pd.DataFrame, expenses_summary: dict) -> None:
    
    # 1. Cabeçalho Principal (Sincronizado com Lucide Icons)
    render_page_header(
        page_id="financial",
        title="Performance Financeira",
        subtitle="Análise detalhada de receitas e custos por segmento"
    )
    
    if df_filtered is None or df_filtered.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return

    # 2. Cálculos de Negócio
    receita_total = float(df_filtered["net_tuition"].sum())
    ticket_medio = float(df_filtered["net_tuition"].mean())
    qtd_alunos = len(df_filtered)
    meta_ticket = 800.0

    # 3. Grade de Métricas Premium
    cols = st.columns(3)
    metrics = [
        {
            "label": "Alunos na Seleção", 
            "value": f"{qtd_alunos}", 
            "type": "info"
        },
        {
            "label": "Ticket Médio",
            "value": f"R$ {ticket_medio:,.2f}",
            "delta": f"{(ticket_medio - meta_ticket):+,.2f} vs meta",
            "trend": "up" if ticket_medio >= meta_ticket else "down",
            "type": "success" if ticket_medio >= meta_ticket else "warning"
        },
        {
            "label": "Receita Líquida",
            "value": f"R$ {receita_total:,.2f}",
            "delta": "Faturamento Total do Recorte",
            "type": "success"
        }
    ]
    render_kpi_grid(metrics, cols)

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Seção de Gráficos (Utilizando o novo motor v2.5)
    c1, c2 = st.columns(2)
    
    with c1:
        render_section_title("Composição de Custos")
        df_costs = expenses_summary.get("details")
        if isinstance(df_costs, pd.DataFrame) and not df_costs.empty:
            # O motor agora remove o 'undefined' e gerencia legendas maiores
            fig_costs = create_premium_pie(df_costs, "valor", "categoria")
            st.plotly_chart(fig_costs, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sem dados de custos para exibir.")

    with c2:
        render_section_title("Receita por Série")
        if "grade" in df_filtered.columns:
            df_grade = df_filtered.groupby("grade")["net_tuition"].sum().reset_index()
            # O motor agora traduz 'net_tuition' para 'Receita Líquida' e 'grade' para 'Série'
            fig_grade = create_premium_bar(df_grade, "grade", "net_tuition")
            st.plotly_chart(fig_grade, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Informação de série não encontrada nos dados.")