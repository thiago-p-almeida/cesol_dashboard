# View Retenção - Análise de Churn e Evasão
# Autogerado com validação automática

import streamlit as st
import plotly.express as px
from components.cards import render_kpi_grid
from components.typography import render_page_header, render_section_title



def render_retention_view(
    churn_data: dict,
) -> None:
    """
    Renderiza view de análise de retenção e churn.

    Args:
        churn_data: Dicionário com dados de churn
    """
    render_page_header(
        title="📉 Retenção e Churn",
        subtitle="Saúde da base e análise de evasão de alunos",
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
    render_kpi_grid(metrics, cols)

    # Espaçamento
    st.write("")

    # Gráficos e insights
    col_churn1, col_churn2 = st.columns(2)

    with col_churn1:
        render_section_title("🎯 Motivos de Saída")

        if not churn_data['reasons_df'].empty:
            fig_reasons = px.pie(
                churn_data['reasons_df'],
                values='Quantidade',
                names='Motivo',
                color_discrete_sequence=px.colors.sequential.RdBu_r,
                template="plotly",
            )
            fig_reasons.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
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
        render_section_title("💡 Insights de Retenção")

        principal_motivo = (
            churn_data['reasons_df'].iloc[0]['Motivo']
            if not churn_data['reasons_df'].empty
            else 'N/A'
        )

        with st.container(border=True):
            st.markdown("#### Resumo da Base")
            st.write(f"**Alunos Ativos:** {churn_data['total_ativos']}")
            st.write(f"**Alunos Inativos:** {churn_data['total_inativos']}")
            st.write(f"**Taxa de Churn:** {churn_data['churn_rate']:.1f}%")
            st.divider()
            st.info(f"Ponto focal: principal motivo de evasão '{principal_motivo}'.")