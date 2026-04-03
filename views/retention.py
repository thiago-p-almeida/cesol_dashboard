import streamlit as st
import pandas as pd
from components.charts import create_premium_pie # Importação garantida
from components.cards import render_kpi_grid
from components.typography import render_page_header, render_section_title

def render_retention_view(churn_data: dict) -> None:
    render_page_header(
        page_id="retention",
        title="Retenção e Churn",
        subtitle="Análise de evasão e saúde da base de alunos"
    )

    churn_rate = churn_data.get('churn_rate', 0)
    total_ativos = churn_data.get('total_ativos', 0)
    total_inativos = churn_data.get('total_inativos', 0)
    reasons_df = churn_data.get('reasons_df', pd.DataFrame())

    cols = st.columns(3)
    metrics = [
        {"label": "Retenção Global", "value": f"{100 - churn_rate:.1f}%", "type": "success" if churn_rate < 10 else "warning", "trend": "up" if churn_rate < 10 else "down"},
        {"label": "Alunos Inativos", "value": f"{total_inativos}", "delta": "Total de saídas", "type": "danger" if total_inativos > 0 else "info", "trend": "up" if total_inativos > 0 else None},
        {"label": "Taxa de Churn", "value": f"{churn_rate:.1f}%", "delta": "Meta < 10%", "type": "danger" if churn_rate > 10 else "success", "trend": "up" if churn_rate > 10 else "down"}
    ]
    render_kpi_grid(metrics, cols)

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)

    with c1:
        render_section_title("Motivos de Saída")
        if not reasons_df.empty:
            fig = create_premium_pie(reasons_df, "Quantidade", "Motivo")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Nenhuma evasão registrada.")

    with c2:
        render_section_title("Insights")
        principal = reasons_df.iloc[0]['Motivo'] if not reasons_df.empty else 'N/A'
        st.info(f"**Resumo:**\n- Ativos: {total_ativos}\n- Inativos: {total_inativos}\n- Churn: {churn_rate:.1f}%\n\nFoco: **{principal}**")