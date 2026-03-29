import streamlit as st
from datetime import datetime
from typing import Any, Optional
import pandas as pd

from components.charts import create_premium_area
from utils.theme_manager import ThemeManager

def render_forecast_view(
    financial_svc: Any,
    export_svc: Any,
    df_active: pd.DataFrame,
    months_to_forecast: int = 6,
    delinquency_rate: float = 0.10,
    theme_manager: Optional[ThemeManager] = None
) -> None:
    if theme_manager is None:
        theme_manager = ThemeManager()

    theme = theme_manager.get_current_theme()
    colors = theme_manager.get_theme_colors(theme)

    st.markdown(
        f"""
        <h2 style="color: {colors['text_primary']}; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">
        🔮 Projeção Financeira</h2>
        <p style="color: {colors['text_secondary']}; font-size: 0.875rem; margin-bottom: 2rem;">
        Projeção de fluxo de caixa para os próximos {months_to_forecast} meses</p>
        """,
        unsafe_allow_html=True
    )

    # Note: Usando os novos serviços desmembrados (Fase 2)
    df_forecast = financial_svc.get_financial_forecasting(
        df_active=df_active,
        months=months_to_forecast,
        delinquency_rate=delinquency_rate
    )

    if df_forecast.empty:
        st.warning("Sem dados para projeção.")
        return

    st.markdown(
        f"""<h4 style="color: {colors['text_primary']}; font-size: 1.125rem; margin-bottom: 1rem;">
        📈 Projeção de Receita vs Risco</h4>""", unsafe_allow_html=True
    )

    fig_forecast = create_premium_area(
        data=df_forecast,
        x_col='Mês',
        y_cols=['Receita Projetada (Líquida)', 'Risco de Inadimplência'],
        theme=theme
    )
    st.plotly_chart(fig_forecast, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""<h4 style="color: {colors['text_primary']}; font-size: 1.125rem; margin-bottom: 1rem;">
        📋 Planilha de Projeção</h4>""", unsafe_allow_html=True
    )

    st.dataframe(
        df_forecast.style.format({
            "Receita Bruta": "R$ {:,.2f}",
            "Receita Projetada (Líquida)": "R$ {:,.2f}",
            "Risco de Inadimplência": "R$ {:,.2f}"
        }),
        use_container_width=True, hide_index=True
    )

    col_btn, _ = st.columns([1, 3])
    with col_btn:
        # Note: ExportService independente cuidando do Excel
        if st.download_button(
            label="📥 Baixar Projeção em Excel",
            data=export_svc.to_excel(df_forecast, sheet_name='Projecao'),
            file_name=f"projecao_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        ):
            st.success("Download iniciado com sucesso!")