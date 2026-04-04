import streamlit as st
import pandas as pd
import plotly.express as px
from components.cards import render_kpi_grid
from components.charts import create_premium_bar, _apply_premium_layout
from components.typography import render_page_header, render_section_title

def render_academic_view(
    academic_svc,
    df_active: pd.DataFrame,
    df_all: pd.DataFrame
) -> None:
    """
    Renderiza a view Acadêmica e Operacional com métricas reais de BI.
    Ajustada para exibir contagens numéricas puras (sem R$) e layout blindado.
    """
    
    # 1. Cabeçalho Principal (Sincronizado com Lucide Icons via PAGES_CONFIG)
    render_page_header(
        page_id="academic",
        title="Acadêmico & Operacional",
        subtitle="Análise de eficiência de turmas e desempenho pedagógico"
    )

    if df_active is None or df_active.empty:
        st.warning("Nenhum dado disponível para análise acadêmica.")
        return

    # ==========================================
    # 2. PROCESSAMENTO DE DADOS DE BI
    # ==========================================
    density = academic_svc.get_class_density(df_active)
    occupancy_data = academic_svc.get_occupancy_metrics(df_active)
    pedagogical_data = academic_svc.get_pedagogical_insights(df_all)

    # ==========================================
    # 3. LÓGICA DE CORES DINÂMICAS (UX SEMÂNTICA)
    # ==========================================
    
    # Lógica para Card de Ocupação
    occ_val = occupancy_data['global_occupancy']
    if occ_val > 100:
        occ_type = "danger"
    elif occ_val > 90:
        occ_type = "warning"
    elif occ_val >= 70:
        occ_type = "success"
    else:
        occ_type = "info"

    # Lógica para Card de Distorção
    dist_val = pedagogical_data['distortion_rate']
    if dist_val > 15:
        dist_type = "danger"
    elif dist_val >= 5:
        dist_type = "warning"
    else:
        dist_type = "success"

    # ==========================================
    # 4. GRADE DE KPIs REAIS
    # ==========================================
    cols = st.columns(3)
    
    metrics = [
        {
            "label": "Média Alunos / Turma", 
            "value": f"{density}", 
            "delta": "Densidade atual",
            "type": "info"
        },
        {
            "label": "Taxa de Ocupação", 
            "value": f"{occ_val}%", 
            "delta": "Capacidade Total",
            "type": occ_type,
            "trend": "up" if occ_val > 90 else None
        },
        {
            "label": "Distorção Idade-Série", 
            "value": f"{dist_val}%", 
            "delta": "Alunos com atraso",
            "type": dist_type,
            "trend": "up" if dist_val > 10 else "down"
        }
    ]
    
    render_kpi_grid(metrics, cols)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # ==========================================
    # 5. SEÇÕES DE ANÁLISE GRÁFICA (Layout v2.6)
    # ==========================================
    
    col_graph1, col_graph2 = st.columns(2)

    with col_graph1:
        render_section_title("Eficiência Operacional")
        occ_df = occupancy_data['occupancy_df']
        
        if not occ_df.empty:
            # Gráfico comparativo: Ativos vs Capacidade por Segmento
            fig_occ = px.bar(
                occ_df, 
                x="Segmento", 
                y=["Ativos", "Capacidade"],
                barmode="group",
                color_discrete_sequence=[px.colors.qualitative.Set2[0], px.colors.qualitative.Set2[7]],
                template="plotly_dark"
            )
            
            # CORREÇÃO: Aplica o motor de layout interno para remover 'undefined' e fixar margens
            fig_occ = _apply_premium_layout(fig_occ, margin_b=40)
            
            st.plotly_chart(fig_occ, use_container_width=True)
        else:
            st.info("Dados de ocupação insuficientes.")

    with col_graph2:
        render_section_title("Análise Pedagógica")
        dist_df = pedagogical_data['distortion_by_grade']
        
        if not dist_df.empty:
            # CORREÇÃO: is_currency=False remove o "R$" do gráfico de contagem de alunos
            fig_dist = create_premium_bar(
                dist_df, 
                x_col="grade", 
                y_col="Alunos Atrasados",
                is_currency=False
            )
            st.plotly_chart(fig_dist, use_container_width=True)
        else:
            st.success("✅ Nenhuma distorção idade-série significativa detectada.")