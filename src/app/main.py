# main.py refatorado - Arquitetura Nativa Streamlit (v2.3)
# Entry point otimizado sem dependências manuais de CSS/Theme

import os
import sys
from datetime import datetime
import streamlit as st
import pandas as pd

# =============================================================================
# CONFIGURAÇÃO INICIAL
# =============================================================================

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(
    page_title="CESOL Pro | Gestão Escolar",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# IMPORTS E LAZY LOADING
# =============================================================================

from components.navigation import render_sidebar_navigation
from components.alerts import show_alert_container

@st.cache_resource
def get_services():
    """Cache de serviços segmentados."""
    from src.services.academic import AcademicService
    from src.services.financial import FinancialService
    from src.services.exports import ExportService
    from src.services.ingestion import DataIngestionService
    return AcademicService(), FinancialService(), ExportService(), DataIngestionService()

@st.cache_resource
def get_views():
    """Cache de views."""
    from views.overview import render_overview_view
    from views.financial import render_financial_view
    from views.retention import render_retention_view
    from views.forecast import render_forecast_view
    from views.admin import render_admin_view
    return {
        "overview": render_overview_view,
        "financial": render_financial_view,
        "retention": render_retention_view,
        "forecast": render_forecast_view,
        "admin": render_admin_view,
    }

# =============================================================================
# SERVIÇOS E DADOS
# =============================================================================

academic_svc, financial_svc, export_svc, ingestor = get_services()

@st.cache_data(ttl=300)
def load_dashboard_data():
    df = academic_svc.get_active_students_df()
    churn = academic_svc.get_churn_analysis()
    expenses = financial_svc.get_expenses_summary()
    return df, churn, expenses

df_all_active, churn_data, expenses_summary = load_dashboard_data()

# =============================================================================
# NAVEGAÇÃO E FILTROS
# =============================================================================

selected_page = render_sidebar_navigation()

from src.schemas.student_schema import ACADEMIC_TAXONOMY

if df_all_active is not None and not df_all_active.empty:
    rename_map = {
        "Educação Infantil": "Ed. Infantil", "Infantil": "Ed. Infantil",
        "Ensino Fundamental I": "Fundamental I", "Ensino Fundamental": "Fundamental I",
        "Fundamental": "Fundamental I", "Ensino Fundamental II": "Fundamental II",
    }
    df_all_active["segment"] = df_all_active["segment"].replace(rename_map)
    all_segments = list(ACADEMIC_TAXONOMY.keys())

    with st.sidebar:
        st.markdown("---")
        st.header("🔍 Filtros")
        selected_segments = st.multiselect("Segmento:", options=all_segments, default=all_segments)
        allowed_grades = [grade for segment in selected_segments for grade in ACADEMIC_TAXONOMY.get(segment, [])]
        df_filtered_step1 = df_all_active[df_all_active["segment"].isin(selected_segments)]
        available_grades = sorted([grade for grade in df_filtered_step1["grade"].unique() if grade in allowed_grades])
        selected_grades = st.multiselect("Série:", options=available_grades, default=available_grades)
        df_final = df_filtered_step1[df_filtered_step1["grade"].isin(selected_grades)]
        st.markdown("---")
        st.header("🔮 Projeção")
        delinquency = st.slider("Inadimplência Estimada (%)", 0, 50, 10) / 100
        months_to_forecast = st.number_input("Meses de Projeção", 1, 24, 6)
else:
    df_final, delinquency, months_to_forecast = df_all_active, 0.10, 6

# =============================================================================
# ALERTAS GLOBAIS
# =============================================================================

alertas_ativos = []
total_receita = df_all_active["net_tuition"].sum() if df_all_active is not None and not df_all_active.empty else 0
total_despesas = expenses_summary.get("total_despesas", 0)
resultado_global = total_receita - total_despesas

if total_receita > 0:
    if (resultado_global / total_receita) < 0:
        alertas_ativos.append({"tipo": "error", "msg": f"Déficit operacional de R$ {abs(resultado_global):,.2f}"})
if churn_data.get("churn_rate", 0) > 10:
    alertas_ativos.append({"tipo": "error", "msg": f"Churn elevado: {churn_data['churn_rate']:.1f}%"})

if alertas_ativos:
    show_alert_container(alertas_ativos)

# =============================================================================
# RENDERIZAÇÃO
# =============================================================================

views = get_views()
view_params = {
    "overview": {"df_all_active": df_all_active, "churn_data": churn_data, "expenses_summary": expenses_summary},
    "financial": {"df_filtered": df_final, "expenses_summary": expenses_summary},
    "retention": {"churn_data": churn_data},
    "forecast": {"financial_svc": financial_svc, "export_svc": export_svc, "df_active": df_all_active, "months_to_forecast": months_to_forecast, "delinquency_rate": delinquency},
    "admin": {"ingestor": ingestor},
}

view_func = views.get(selected_page, views["overview"])
view_func(**view_params.get(selected_page, {}))

st.markdown("---")
st.caption(f"© {datetime.now().year} CESOL Pro - v2.3")