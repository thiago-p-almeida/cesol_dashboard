import streamlit as st
import pandas as pd
from components.cards import render_kpi_grid
from components.charts import create_premium_pie, create_premium_bar
from components.typography import render_page_header, render_section_title

def render_financial_view(
    financial_svc, 
    df_filtered: pd.DataFrame, 
    df_all: pd.DataFrame, 
    expenses_summary: dict
) -> None:
    """
    Renderiza a view de Performance Financeira e Eficiência de Aquisição.
    Utiliza o motor de gráficos v2.5 para limpeza automática de eixos e títulos.
    """
    
    # 1. Cabeçalho Principal (Sincronizado com Lucide Icons via PAGES_CONFIG)
    render_page_header(
        page_id="financial",
        title="Performance Financeira",
        subtitle="Análise detalhada de receitas e custos por segmento"
    )
    
    if df_filtered is None or df_filtered.empty:
        st.warning("Nenhum dado disponível para os filtros selecionados.")
        return

    # ==========================================
    # 2. CORE FINANCEIRO (KPIs de Resultado)
    # ==========================================
    receita_total = float(df_filtered["net_tuition"].sum())
    ticket_medio = float(df_filtered["net_tuition"].mean())
    qtd_alunos = len(df_filtered)
    meta_ticket = 800.0

    cols = st.columns(3)
    metrics = [
        {
            "label": "Alunos na Seleção", 
            "value": f"{qtd_alunos}", 
            "type": "info"
        },
        {
            "label": "Ticket Médio",
            "value": f"R$ {ticket_medio:,.2f}",
            "delta": f"{(ticket_medio - meta_ticket):+,.2f} vs meta",
            "trend": "up" if ticket_medio >= meta_ticket else "down",
            "type": "success" if ticket_medio >= meta_ticket else "warning"
        },
        {
            "label": "Receita Líquida",
            "value": f"R$ {receita_total:,.2f}",
            "delta": "Faturamento Total do Recorte",
            "type": "success"
        }
    ]
    render_kpi_grid(metrics, cols)

    # ==========================================
    # 3. EFICIÊNCIA DE AQUISIÇÃO (Unit Economics)
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Eficiência de Aquisição (Unit Economics)")

    # Extração de métricas via FinancialService
    marketing_budget = expenses_summary.get("marketing", 0.0)
    ltv = financial_svc.calculate_ltv(df_all)
    cac = financial_svc.calculate_cac(df_all, marketing_budget)
    
    # Cálculo da Proporção LTV/CAC
    ltv_cac_ratio = (ltv / cac) if cac > 0 else 0.0
    
    # Lógica Semântica para o Ratio
    ratio_type = "success" if ltv_cac_ratio >= 3.0 else "danger"
    ratio_trend = "up" if ltv_cac_ratio >= 3.0 else "down"
    ratio_delta = "Ideal (≥ 3.0x)" if ltv_cac_ratio >= 3.0 else "Abaixo do ideal (3.0x)"

    cols_ue = st.columns(3)
    metrics_ue = [
        {
            "label": "Custo de Aquisição (CAC)",
            "value": f"R$ {cac:,.2f}",
            "delta": f"Base: R$ {marketing_budget:,.0f} em Marketing",
            "type": "warning"
        },
        {
            "label": "Lifetime Value (LTV)",
            "value": f"R$ {ltv:,.2f}",
            "delta": "Valor médio gerado por aluno",
            "type": "success"
        },
        {
            "label": "Ratio LTV / CAC",
            "value": f"{ltv_cac_ratio:.1f}x",
            "delta": ratio_delta,
            "trend": ratio_trend,
            "type": ratio_type
        }
    ]
    render_kpi_grid(metrics_ue, cols_ue)

    # ==========================================
    # 4. GRÁFICOS (Layout Purificado)
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    
    with c1:
        render_section_title("Composição de Custos")
        df_costs = expenses_summary.get("details")
        if isinstance(df_costs, pd.DataFrame) and not df_costs.empty:
            # O motor agora remove o 'undefined' e gerencia legendas nativamente
            fig_costs = create_premium_pie(df_costs, "valor", "categoria")
            st.plotly_chart(fig_costs, use_container_width=True)
        else:
            st.info("Sem dados de custos para exibir.")

    with c2:
        render_section_title("Receita por Série")
        if "grade" in df_filtered.columns:
            df_grade = df_filtered.groupby("grade")["net_tuition"].sum().reset_index()
            # O motor agora traduz nomes técnicos e remove o 'undefined'
            fig_grade = create_premium_bar(df_grade, "grade", "net_tuition")
            st.plotly_chart(fig_grade, use_container_width=True)
        else:
            st.info("Informação de série não encontrada nos dados.")