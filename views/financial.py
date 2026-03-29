"""
View Financeiro - Performance e Custos Refatorado (Design System)
"""

import streamlit as st
import pandas as pd
from typing import Any, Optional
from components.cards import render_kpi_grid
from components.charts import create_premium_pie, create_premium_bar
from components.typography import render_page_header, render_section_title
from utils.theme_manager import ThemeManager

def render_financial_view(
    analytics: Any,
    df_filtered: pd.DataFrame,
    expenses_summary: dict,
    theme_manager: Optional[ThemeManager] = None
) -> None:
    
    if theme_manager is None:
        theme_manager = ThemeManager()
    
    theme = theme_manager.get_current_theme()
    
    # 1. Uso do Design System
    render_page_header(
        title="💰 Performance Financeira",
        subtitle="Análise detalhada de receitas e custos por segmento educacional",
        theme_manager=theme_manager
    )
    
    if df_filtered is None or df_filtered.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return

    if "net_tuition" not in df_filtered.columns:
        st.warning("Dados insuficientes: coluna 'net_tuition' não encontrada.")
        return

    receita_filtrada = float(df_filtered["net_tuition"].sum())
    ticket_medio = float(df_filtered["net_tuition"].mean())
    qtd_alunos = int(len(df_filtered))

    cols = st.columns(3)
    metrics =[
        {"label": "Alunos na Seleção", "value": f"{qtd_alunos:,}", "icon": "users", "variant": "info"},
        {
            "label": "Ticket Médio",
            "value": f"R$ {ticket_medio:,.2f}",
            "delta": f"R$ {ticket_medio - 800:+.2f} vs meta",
            "delta_color": "success" if ticket_medio > 800 else "warning",
            "icon": "coins",
            "variant": "success",
        },
        {
            "label": "Receita Líquida",
            "value": f"R$ {receita_filtrada:,.2f}",
            "icon": "revenue",
            "variant": "success",
            "help_text": "Soma das mensalidades líquidas do recorte selecionado",
        },
    ]
    render_kpi_grid(metrics, cols, theme_manager=theme_manager)

    st.markdown("<br>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        # 2. Uso do Design System
        render_section_title("📊 Composição de Custos", theme_manager=theme_manager)
        
        details = expenses_summary.get("details")
        if isinstance(details, pd.DataFrame) and not details.empty:
            fig_costs = create_premium_pie(
                data=details,
                values_col="valor",
                names_col="categoria",
                hole=0.4,
                theme=theme,
            )
            st.plotly_chart(fig_costs, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sem dados de custos para exibir.")

    with col_g2:
        # 3. Uso do Design System
        render_section_title("📈 Receita por Série", theme_manager=theme_manager)
        
        if "grade" in df_filtered.columns:
            df_grade = df_filtered.groupby("grade")["net_tuition"].sum().reset_index()
            fig_grade = create_premium_bar(
                data=df_grade,
                x_col="grade",
                y_col="net_tuition",
                theme=theme,
                color_discrete_sequence=True,
            )
            st.plotly_chart(fig_grade, use_container_width=True, config={"displayModeBar": False})
        else:
            st.info("Sem coluna 'grade' para agrupar receita por série.")