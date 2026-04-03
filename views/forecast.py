import streamlit as st
import pandas as pd
from components.charts import create_premium_area
from components.typography import render_page_header, render_section_title

def render_forecast_view(financial_svc, export_svc, df_active: pd.DataFrame, months_to_forecast: int = 6, delinquency_rate: float = 0.10) -> None:
    render_page_header("forecast", "Projeções Financeiras", f"Simulação para os próximos {months_to_forecast} meses")

    df_forecast = financial_svc.get_financial_forecasting(df_active=df_active, months=months_to_forecast, delinquency_rate=delinquency_rate)

    if df_forecast.empty:
        st.warning("Sem dados para projeção.")
        return

    render_section_title("Evolução de Receita vs Risco")
    fig = create_premium_area(df_forecast, 'Mês', ['Receita Projetada (Líquida)', 'Risco de Inadimplência'])
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Tabela de Projeção")
    st.dataframe(df_forecast.style.format({"Receita Bruta": "R$ {:,.2f}", "Receita Projetada (Líquida)": "R$ {:,.2f}", "Risco de Inadimplência": "R$ {:,.2f}"}), use_container_width=True, hide_index=True)