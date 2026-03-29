"""
View Overview - Dashboard Principal Refatorado (Design System)
"""

import streamlit as st
import pandas as pd
from components.cards import render_kpi_grid
from components.typography import render_page_header, render_section_title


def render_overview_view(
    df_all_active: pd.DataFrame,
    churn_data: dict,
    expenses_summary: dict,
) -> None:

    render_page_header(
        title="📊 Dashboard Principal",
        subtitle=f"Visão geral da gestão escolar - {len(df_all_active)} alunos ativos no sistema",
    )
    
    # Calcular métricas globais
    total_receita = df_all_active['net_tuition'].sum() if not df_all_active.empty else 0
    total_despesas = expenses_summary.get('total_despesas', 0)
    resultado_global = total_receita - total_despesas
    margem_operacional = (resultado_global / total_receita) * 100 if total_receita > 0 else 0
    
    # KPIs principais
    cols = st.columns(4)
    metrics =[
        {"label": "Receita Total", "value": f"R$ {total_receita:,.2f}", "icon": "coins", "variant": "success"},
        {"label": "Despesas Operacionais", "value": f"R$ {total_despesas:,.2f}", "icon": "expense", "variant": "danger"},
        {
            "label": "Resultado Líquido", 
            "value": f"R$ {resultado_global:,.2f}", 
            "delta": f"{margem_operacional:.1f}% margem", 
            "delta_color": "success" if resultado_global > 0 else "danger",
            "icon": "chart", 
            "variant": "success" if resultado_global > 0 else "danger"
        },
        {
            "label": "Taxa de Retenção", 
            "value": f"{100 - churn_data.get('churn_rate', 0):.1f}%", 
            "delta": f"{churn_data.get('churn_rate', 0):.1f}% churn", 
            "delta_color": "success" if churn_data.get('churn_rate', 0) < 10 else "warning",
            "icon": "users", 
            "variant": "info"
        }
    ]
    render_kpi_grid(metrics, cols)

    st.write("")

    render_section_title("📈 Distribuição por Segmento")
    
    if not df_all_active.empty:
        segment_summary = df_all_active.groupby('segment').agg({
            'net_tuition': ['sum', 'mean', 'count']
        }).reset_index()
        segment_summary.columns = ['Segmento', 'Receita Total', 'Ticket Médio', 'Alunos']
        
        # Formatar valores monetários
        segment_summary['Receita Total'] = segment_summary['Receita Total'].apply(lambda x: f"R$ {x:,.2f}")
        segment_summary['Ticket Médio'] = segment_summary['Ticket Médio'].apply(lambda x: f"R$ {x:,.2f}")
        
        st.dataframe(segment_summary, use_container_width=True, hide_index=True)
    else:
        st.info("Nenhum dado disponível para análise.")