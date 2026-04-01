import streamlit as st
from components.typography import render_page_header, render_section_title, render_info_box

def render_admin_view(ingestor) -> None:
    
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
        colunas_display =["nome", "segmento", "serie", "mensalidade", "desconto", "bolsa"]
        
        # Construção do HTML em linha única (Atomic DOM) para os badges verdes
        badges_html = "<div style='display:flex; flex-wrap:wrap; gap:10px; margin-bottom:15px;'>"
        for col in colunas_display:
            badges_html += f'<div style="background-color:rgba(16,185,129,0.1); border:1px solid #10B981; border-radius:6px; padding:6px 12px; display:flex; align-items:center;"><span style="color:#10B981; font-weight:700; font-family:monospace; font-size:0.95rem;">{col}</span></div>'
        badges_html += "</div>"
        
        st.markdown(badges_html, unsafe_allow_html=True)
        
        st.info("**Taxonomia Obrigatória:** A coluna `segmento` deve conter exatamente: **Ed. Infantil**, **Fundamental I**, ou **Fundamental II**.")

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Área de Importação")

    # ==========================================
    # 3. UPLOADER COM UX WRAPPER (Tradução Nativa)
    # ==========================================
    # Criamos um container nativo para isolar o uploader e dar destaque visual
    with st.container(border=True):
        # Instruções claras em Português formatadas de forma segura (sem quebras de linha que ativam Markdown Code Blocks)
        instrucao_html = '<div style="margin-bottom:10px;"><h4 style="color:#F1F5F9; margin:0 0 5px 0;">📥 Envio de Base de Dados (CSV)</h4><p style="color:#94A3B8; font-size:0.9rem; margin:0;">Clique no botão abaixo ou arraste sua planilha para a área abaixo.</p></div>'
        st.markdown(instrucao_html, unsafe_allow_html=True)
        
        # O Uploader nativo do Streamlit, com o label original oculto
        uploaded_file = st.file_uploader(
            label="Área do Sistema", 
            type=["csv"],
            label_visibility="collapsed" 
        )

    # ==========================================
    # 4. PROCESSAMENTO DA INGESTÃO (Backend Layer)
    # ==========================================
    if uploaded_file is not None:
        render_info_box("Arquivo selecionado", f"Nome: {uploaded_file.name} | Tamanho: {uploaded_file.size / 1024:.2f} KB")

        if st.button("Processar Importação", type="primary", use_container_width=True):
            with st.spinner("Processando importação e traduzindo chaves..."):
                try:
                    # Envia para a camada de serviço onde a tradução (PT -> EN) e validação acontecem
                    msg = ingestor.process_students_csv(uploaded_file, uploaded_file.name)
                    st.success(f"✅ {msg}")
                    st.cache_resource.clear()
                    st.info("🔄 A página será recarregada para atualizar os dados...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro na importação: {e}")
                    render_info_box("Dica de Correção", "Verifique se o arquivo CSV está salvo com codificação UTF-8 e se os nomes das colunas estão exatamente iguais aos destacados em verde acima.")

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Informações do Sistema")

    # ==========================================
    # 5. INFORMAÇÕES TÉCNICAS E STACK
    # ==========================================
    col_info1, col_info2 = st.columns(2)
    with col_info1:
        render_info_box("Versão e UI", "CESOL Pro v2.5 Premium\n\nUI Kit: Lucide Icons / Atomic DOM\n\nFramework: Streamlit 1.40+")
    with col_info2:
        render_info_box("Stack Técnico", "Backend: SQLAlchemy 2.0 + PostgreSQL\n\nFrontend: Streamlit + Plotly\n\nValidação e Tradução: Pandera")