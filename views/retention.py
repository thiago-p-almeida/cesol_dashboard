# View Retenção - Análise de Churn e Evasão
# Autogerado com validação automática

import streamlit as st
import plotly.express as px
from typing import Any, Optional
from components.cards import render_metric_card, render_kpi_grid
from utils.theme_manager import ThemeManager


def render_retention_view(
    analytics: Any,
    churn_data: dict,
    theme_manager: Optional[ThemeManager] = None
) -> None:
    """
    Renderiza view de análise de retenção e churn.

    Args:
        analytics: Instância SchoolAnalytics
        churn_data: Dicionário com dados de churn
        theme_manager: Instância ThemeManager (auto-cria se None)
    """
    if theme_manager is None:
        theme_manager = ThemeManager()

    theme = theme_manager.get_current_theme()
    colors = theme_manager.get_theme_colors(theme)

    # Header
    st.markdown(
        f"""
        <h2 style="
            color: {colors['text_primary']};
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">📉 Retenção e Churn</h2>
        <p style="
            color: {colors['text_secondary']};
            font-size: 0.875rem;
            margin-bottom: 2rem;
        ">Saúde da base e análise de evasão de alunos</p>
        """,
        unsafe_allow_html=True
    )

    # KPIs
    cols = st.columns(3)
    metrics = [
        {
            "label": "Taxa de Retenção Global",
            "value": f"{100 - churn_data['churn_rate']:.1f}%",
            "icon": "users",
            "variant": "success"
        },
        {
            "label": "Alunos Inativos",
            "value": f"{churn_data['total_inativos']}",
            "delta": f"de {churn_data['total_ativos'] + churn_data['total_inativos']} total",
            "delta_color": "warning",
            "icon": "warning",
            "variant": "warning"
        },
        {
            "label": "Taxa de Churn",
            "value": f"{churn_data['churn_rate']:.1f}%",
            "delta": "Meta: < 10%",
            "delta_color": "success" if churn_data['churn_rate'] < 10 else "danger",
            "icon": "chart",
            "variant": "danger" if churn_data['churn_rate'] > 10 else "info"
        }
    ]
    render_kpi_grid(metrics, cols, theme_manager)

    # Espaçamento
    st.markdown("<br>", unsafe_allow_html=True)

    # Gráficos e insights
    col_churn1, col_churn2 = st.columns(2)

    with col_churn1:
        st.markdown(
            f"""
            <h4 style="color: {colors['text_primary']}; font-size: 1.125rem; margin-bottom: 1rem;">
                🎯 Motivos de Saída
            </h4>
            """,
            unsafe_allow_html=True
        )

        if not churn_data['reasons_df'].empty:
            fig_reasons = px.pie(
                churn_data['reasons_df'],
                values='Quantidade',
                names='Motivo',
                color_discrete_sequence=px.colors.sequential.RdBu_r,
                template=colors['plotly_template']
            )
            fig_reasons.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Inter", color=colors['text_primary']),
                margin=dict(t=30, b=60, l=20, r=20),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.1,
                    xanchor="center",
                    x=0.5
                )
            )
            st.plotly_chart(
                fig_reasons,
                use_container_width=True,
                config={'displayModeBar': False}
            )
        else:
            st.info("Nenhuma evasão registrada.")

    with col_churn2:
        st.markdown(
            f"""
            <h4 style="color: {colors['text_primary']}; font-size: 1.125rem; margin-bottom: 1rem;">
                💡 Insights de Retenção
            </h4>
            """,
            unsafe_allow_html=True
        )

        principal_motivo = (
            churn_data['reasons_df'].iloc[0]['Motivo']
            if not churn_data['reasons_df'].empty
            else 'N/A'
        )

        st.markdown(
            f"""
            <div style="
                background-color: {colors['bg_surface']};
                border-radius: 12px;
                padding: 1.5rem;
                border-left: 4px solid {colors['accent_info']};
                box-shadow: {colors['shadow_md']};
            ">
                <h5 style="color: {colors['text_primary']}; margin-bottom: 1rem;">Resumo da Base</h5>
                <ul style="color: {colors['text_secondary']}; line-height: 1.8;">
                    <li><strong>Alunos Ativos:</strong> {churn_data['total_ativos']}</li>
                    <li><strong>Alunos Inativos:</strong> {churn_data['total_inativos']}</li>
                    <li><strong>Taxa de Churn:</strong> {churn_data['churn_rate']:.1f}%</li>
                </ul>
                <hr style="border-color: {colors['border_subtle']}; margin: 1rem 0;">
                <p style="color: {colors['text_secondary']};">
                    <strong>Ponto Focal:</strong> O principal motivo de evasão é
                    <span style="color: {colors['accent_warning']}; font-weight: 600;">'{principal_motivo}'</span>
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )