import streamlit as st
import pandas as pd
import plotly.express as px
from components.cards import render_kpi_grid
from components.typography import render_page_header, render_section_title

def render_retention_view(churn_data: dict) -> None:
    
    render_page_header(
        page_id="retention",
        title="Retenção e Churn",
        subtitle="Análise de evasão e saúde da base"
    )

    churn_rate = churn_data.get('churn_rate', 0)
    total_ativos = churn_data.get('total_ativos', 0)
    total_inativos = churn_data.get('total_inativos', 0)
    reasons_df = churn_data.get('reasons_df', pd.DataFrame())

    cols = st.columns(3)
    metrics =[
        {"label": "Retenção Global", "value": f"{100 - churn_rate:.1f}%", "type": "success" if churn_rate < 10 else "warning", "trend": "up" if churn_rate < 10 else "down"},
        {"label": "Alunos Inativos", "value": f"{total_inativos}", "delta": f"De um total de {total_ativos + total_inativos}", "type": "danger" if total_inativos > 0 else "info", "trend": "up" if total_inativos > 0 else None},
        {"label": "Taxa de Churn", "value": f"{churn_rate:.1f}%", "delta": "Meta < 10%", "type": "danger" if churn_rate > 10 else "success", "trend": "up" if churn_rate > 10 else "down"}
    ]
    render_kpi_grid(metrics, cols)

    st.markdown("<br>", unsafe_allow_html=True)
    col_churn1, col_churn2 = st.columns(2)

    with col_churn1:
        render_section_title("Motivos de Saída")
        if not reasons_df.empty:
            fig = px.pie(reasons_df, values='Quantidade', names='Motivo', template="plotly_dark", hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=30, b=60, l=20, r=20), legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Nenhuma evasão registrada.")

    with col_churn2:
        render_section_title("Insights de Retenção")
        principal_motivo = reasons_df.iloc[0]['Motivo'] if not reasons_df.empty else 'N/A'
        st.info(f"**Resumo da Base:**\n- Alunos Ativos: {total_ativos}\n- Alunos Inativos: {total_inativos}\n- Taxa de Churn: {churn_rate:.1f}%\n\n---\n**Ponto de Atenção:** O principal motivo de evasão é: **{principal_motivo}**.")