# main.py refatorado - injeção única de CSS + lazy loading
# CESOL Pro v2.2 - Dashboard de Gestão Escolar

import os
import sys
from datetime import datetime
from pathlib import Path

import streamlit as st
import pandas as pd

# =============================================================================
# CONFIGURAÇÃO INICIAL CRÍTICA
# =============================================================================

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

# Configuração da página DEVE vir antes de qualquer outro elemento visual
st.set_page_config(
    page_title="CESOL Pro | Gestão Escolar",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# FORÇAR TEMA ESCURO COMO PADRÃO (prevenir flash de tema claro)
if "cesol_theme" not in st.session_state:
    st.session_state["cesol_theme"] = "dark"

# FLAG CRÍTICA: Controle de injeção única de CSS
if "_cesol_css_injected" not in st.session_state:
    st.session_state["_cesol_css_injected"] = False

# =============================================================================
# IMPORTS MODULARES (após set_page_config)
# =============================================================================

from utils.theme_manager import theme_manager
from components.navigation import render_sidebar_navigation
from components.alerts import show_alert_container

# =============================================================================
# LAZY IMPORTS: Services e Views 
# =============================================================================

@st.cache_resource
def get_services():
    """Cache de serviços divididos arquiteturalmente (Fase 2)."""
    from src.services.academic import AcademicService
    from src.services.financial import FinancialService
    from src.services.exports import ExportService
    from src.services.ingestion import DataIngestionService

    return AcademicService(), FinancialService(), ExportService(), DataIngestionService()

@st.cache_resource
def get_views():
    """Cache de views para performance."""
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
# INJEÇÃO DE CSS OTIMIZADA (apenas uma vez por sessão)
# =============================================================================

if not st.session_state.get("_cesol_css_injected", False):
    theme_manager.inject_css()
    st.session_state["_cesol_css_injected"] = True

# =============================================================================
# SERVIÇOS E DADOS (CORREÇÃO DO DESEMPACOTAMENTO)
# =============================================================================

# Aqui está a correção: agora recebemos as 4 variáveis corretamente!
academic_svc, financial_svc, export_svc, ingestor = get_services()

@st.cache_data(ttl=300)  # Cache 5 minutos
def load_dashboard_data():
    """Carrega dados usando os novos serviços segmentados."""
    df = academic_svc.get_active_students_df()
    churn = academic_svc.get_churn_analysis()
    expenses = financial_svc.get_expenses_summary()
    return df, churn, expenses

df_all_active, churn_data, expenses_summary = load_dashboard_data()

# Cópia defensiva para evitar mutação acidental de objeto cacheado
if df_all_active is not None and not df_all_active.empty:
    df_all_active = df_all_active.copy()

# =============================================================================
# NAVEGAÇÃO
# =============================================================================

selected_page = render_sidebar_navigation(theme_manager=theme_manager)

# =============================================================================
# FILTROS (Sidebar)
# =============================================================================

from src.schemas.student_schema import ACADEMIC_TAXONOMY

if df_all_active is not None and not df_all_active.empty:
    # Normalização de segmentos
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

        selected_segments = st.multiselect("Segmento:", options=all_segments, default=all_segments, key="filter_segments")
        allowed_grades =[grade for segment in selected_segments for grade in ACADEMIC_TAXONOMY.get(segment, [])]

        df_filtered_step1 = df_all_active[df_all_active["segment"].isin(selected_segments)]
        available_grades = sorted([grade for grade in df_filtered_step1["grade"].unique() if grade in allowed_grades])

        selected_grades = st.multiselect("Série:", options=available_grades, default=available_grades, key="filter_grades")
        df_final = df_filtered_step1[df_filtered_step1["grade"].isin(selected_grades)]

        st.markdown("---")
        st.header("🔮 Projeção")

        delinquency = st.slider("Inadimplência Estimada (%)", 0, 50, 10, key="projection_delinquency") / 100
        months_to_forecast = st.number_input("Meses de Projeção", min_value=1, max_value=24, value=6, key="projection_months")
else:
    df_final = df_all_active.copy() if df_all_active is not None else df_all_active
    delinquency = 0.10
    months_to_forecast = 6

# =============================================================================
# ALERTAS GLOBAIS
# =============================================================================

alertas_ativos = []

total_receita = df_all_active["net_tuition"].sum() if df_all_active is not None and not df_all_active.empty else 0
total_despesas = expenses_summary.get("total_despesas", 0)
resultado_global = total_receita - total_despesas
margem_operacional = (resultado_global / total_receita) * 100 if total_receita > 0 else 0
peso_folha = (expenses_summary.get("folha", 0) / total_receita) * 100 if total_receita > 0 else 0

if total_receita > 0:
    if margem_operacional < 0:
        alertas_ativos.append({"tipo": "error", "msg": f"Risco Crítico: Déficit de R$ {abs(resultado_global):,.2f}"})
    elif margem_operacional < 10:
        alertas_ativos.append({"tipo": "warning", "msg": f"Margem baixa: {margem_operacional:.1f}%"})
    if peso_folha > 50:
        alertas_ativos.append({"tipo": "warning", "msg": f"Folha: {peso_folha:.1f}% da receita"})

if churn_data.get("churn_rate", 0) > 10:
    alertas_ativos.append({"tipo": "error", "msg": f"Churn elevado: {churn_data['churn_rate']:.1f}%"})

if alertas_ativos:
    show_alert_container(alertas_ativos, expanded=True)

# =============================================================================
# RENDERIZAÇÃO DE VIEWS
# =============================================================================

views = get_views()

# Mapear parâmetros para cada view
view_params = {
    "overview": {
        "analytics": None, # Mantido None para retrocompatibilidade temporária
        "df_all_active": df_all_active,
        "churn_data": churn_data,
        "expenses_summary": expenses_summary,
        "theme_manager": theme_manager,
    },
    "financial": {
        "analytics": None, 
        "df_filtered": df_final,
        "expenses_summary": expenses_summary,
        "theme_manager": theme_manager,
    },
    "retention": {
        "analytics": None,
        "churn_data": churn_data,
        "theme_manager": theme_manager,
    },
    "forecast": {
        "financial_svc": financial_svc,
        "export_svc": export_svc,
        "df_active": df_all_active,
        "months_to_forecast": months_to_forecast,
        "delinquency_rate": delinquency,
        "theme_manager": theme_manager,
    },
    "admin": {
        "ingestor": ingestor,
        "theme_manager": theme_manager,
    },
}

# Renderizar view selecionada
if selected_page in views:
    view_func = views[selected_page]
    params = view_params.get(selected_page, {})
    view_func(**params)
else:
    # Fallback para overview
    views["overview"](**view_params["overview"])

# =============================================================================
# FOOTER
# =============================================================================

st.markdown("---")
st.caption(f"© {datetime.now().year} CESOL Pro - v2.2 Premium")