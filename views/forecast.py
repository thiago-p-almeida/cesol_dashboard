import streamlit as st
from datetime import datetime
from typing import Any
import pandas as pd

from components.charts import create_premium_area
from components.typography import render_page_header, render_section_title


def render_forecast_view(
    financial_svc: Any,
    export_svc: Any,
    df_active: pd.DataFrame,
    months_to_forecast: int = 6,
    delinquency_rate: float = 0.10,
) -> None:
    render_page_header(
        title="🔮 Projeção Financeira",
        subtitle=f"Projeção de fluxo de caixa para os próximos {months_to_forecast} meses",
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

    render_section_title("📈 Projeção de Receita vs Risco")

    fig_forecast = create_premium_area(
        data=df_forecast,
        x_col='Mês',
        y_cols=['Receita Projetada (Líquida)', 'Risco de Inadimplência'],
    )
    st.plotly_chart(fig_forecast, use_container_width=True, config={'displayModeBar': False})

    st.write("")
    render_section_title("📋 Planilha de Projeção")

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