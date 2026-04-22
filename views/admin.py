import streamlit as st
import pandas as pd
from components.typography import render_page_header, render_section_title, render_info_box

def render_admin_view(
    ingestor, 
    export_svc=None, 
    df_active=None, 
    churn_data=None, 
    expenses_summary=None
) -> None:
    """
    View de Administração: Centraliza Ingestão de Dados (CSV) e 
    Publicação de Contratos de Dados (Parquet para Evidence.dev).
    """
    
    # ==========================================
    # 1. CABEÇALHO PRINCIPAL
    # ==========================================
    render_page_header(
        page_id="admin",
        title="Central de Administração",
        subtitle="Gerenciamento de dados e configurações do sistema"
    )

    # ==========================================
    # 2. REGRAS DE NEGÓCIO E FORMATO DE ARQUIVO
    # ==========================================
    with st.expander("Ver formato de arquivo aceito", expanded=True):
        st.markdown('<p style="color:#F1F5F9; font-size:0.95rem; margin-bottom:10px;">O cabeçalho do arquivo CSV deve conter exatamente as seguintes colunas:</p>', unsafe_allow_html=True)
        
        # Lista de colunas em Português para o usuário final
        colunas_display = ["nome", "segmento", "serie", "mensalidade", "desconto", "bolsa"]
        
        # Construção do HTML em linha única (Atomic DOM) para os badges verdes
        badges_html = "<div style='display:flex; flex-wrap:wrap; gap:10px; margin-bottom:15px;'>"
        for col in colunas_display:
            badges_html += f'<div style="background-color:rgba(16,185,129,0.1); border:1px solid #10B981; border-radius:6px; padding:6px 12px; display:flex; align-items:center;"><span style="color:#10B981; font-weight:700; font-family:monospace; font-size:0.95rem;">{col}</span></div>'
        badges_html += "</div>"
        
        st.markdown(badges_html, unsafe_allow_html=True)
        st.info("**Taxonomia Obrigatória:** A coluna `segmento` deve conter: **Ed. Infantil**, **Fundamental I**, ou **Fundamental II**.")

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Área de Importação")

    # ==========================================
    # 3. UPLOADER COM UX WRAPPER
    # ==========================================
    with st.container(border=True):
        instrucao_html = '<div style="margin-bottom:10px;"><h4 style="color:#F1F5F9; margin:0 0 5px 0;">📥 Envio de Base de Dados (CSV)</h4><p style="color:#94A3B8; font-size:0.9rem; margin:0;">Clique no botão abaixo ou arraste sua planilha para a área abaixo.</p></div>'
        st.markdown(instrucao_html, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader(
            label="Área do Sistema", 
            type=["csv"],
            label_visibility="collapsed" 
        )

    # ==========================================
    # 4. PROCESSAMENTO DA INGESTÃO
    # ==========================================
    if uploaded_file is not None:
        render_info_box("Arquivo selecionado", f"Nome: {uploaded_file.name} | Tamanho: {uploaded_file.size / 1024:.2f} KB")

        if st.button("Processar Importação", type="primary", use_container_width=True):
            with st.spinner("Processando importação e traduzindo chaves..."):
                try:
                    msg = ingestor.process_students_csv(uploaded_file, uploaded_file.name)
                    st.success(f"✅ {msg}")
                    st.cache_resource.clear()
                    st.info("🔄 A página será recarregada para atualizar os dados...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro na importação: {e}")
                    render_info_box("Dica de Correção", "Verifique se o arquivo CSV está em UTF-8 e se as colunas estão corretas.")

    # ==========================================
    # 5. INTEGRAÇÃO MODERN DATA STACK (Evidence.dev)
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Integração Modern Data Stack (Evidence.dev)")

    with st.container(border=True):
        st.markdown(
            '<div style="margin-bottom:10px;">'
            '<h4 style="color:#F1F5F9; margin:0 0 5px 0;">📤 Gerar Relatórios Executivos</h4>'
            '<p style="color:#94A3B8; font-size:0.9rem; margin:0;">Exporta métricas processadas em formato Parquet para a camada de storytelling (Evidence.dev).</p>'
            '</div>', 
            unsafe_allow_html=True
        )

        if export_svc and df_active is not None:
            if st.button("Gerar Contratos de Dados (Parquet)", type="secondary", use_container_width=True):
                with st.spinner("Compilando e comprimindo dados em Parquet..."):
                    try:
                        # 1. Publica Alunos Ativos (Base para Receita e Acadêmico)
                        export_svc.publish_data_contract(df_active, "alunos_ativos")
                        
                        # 2. Publica Motivos de Churn
                        if churn_data and isinstance(churn_data.get('reasons_df'), pd.DataFrame):
                            export_svc.publish_data_contract(churn_data['reasons_df'], "churn_motivos")
                            
                        # 3. Publica Custos Operacionais
                        if expenses_summary and isinstance(expenses_summary.get('details'), pd.DataFrame):
                            export_svc.publish_data_contract(expenses_summary['details'], "custos_operacionais")

                        st.success("✅ Arquivos Parquet gerados com sucesso em `/data/analytics/`!")
                    except Exception as e:
                        st.error(f"❌ Erro ao gerar arquivos Parquet: {e}")
        else:
            st.info("💡 Realize a importação de dados para habilitar a geração de relatórios executivos.")

    # ==========================================
    # 6. INFORMAÇÕES TÉCNICAS E STACK
    # ==========================================
    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Informações do Sistema")
    
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        render_info_box("Versão e UI", "CESOL Pro v2.6.5 Premium\n\nUI Kit: Lucide Icons / Atomic DOM\n\nFramework: Streamlit 1.40+")
    with col_info2:
        render_info_box("Data Stack", "Backend: SQLAlchemy 2.0\n\nEngine de Dados: Pandas + PyArrow (Parquet)\n\nVisualização: Evidence.dev + DuckDB")