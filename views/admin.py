# View Administração - Ingestão de Dados
# Autogerado com validação automática

import streamlit as st
from typing import Any
from components.typography import render_page_header, render_section_title




def render_admin_view(
    ingestor: Any,
) -> None:
    """
    Renderiza view de administração e ingestão de dados.

    Args:
        ingestor: Instância DataIngestionService
    """
    render_page_header(
        title="⚙️ Central de Administração",
        subtitle="Gerenciamento de dados e configurações do sistema",
    )

    # Expander com formato do arquivo
    with st.expander("📂 Ver formato de arquivo aceito", expanded=True):
        # Importar COLUMN_MAP do schema
        try:
            from src.schemas.student_schema import COLUMN_MAP
            colunas_necessarias = ", ".join(COLUMN_MAP.keys())
        except ImportError:
            colunas_necessarias = (
                "name, segment, grade, full_tuition, discount_value, scholarship_value"
            )

        st.markdown(f"**O CSV deve conter as colunas:** `{colunas_necessarias}`")
        st.info(
            "💡 **Taxonomia Obrigatória:** O segmento deve ser categorizado como: "
            "**Ed. Infantil**, **Fundamental I**, ou **Fundamental II**."
        )

    # Upload de arquivo
    render_section_title("📤 Importar Dados de Alunos")

    uploaded_file = st.file_uploader(
        "Escolha o arquivo CSV de alunos",
        type=["csv"],
        help="O arquivo deve estar no formato CSV com as colunas especificadas acima."
    )

    if uploaded_file is not None:
        with st.container(border=True):
            st.write(f"**Arquivo selecionado:** {uploaded_file.name}")
            st.write(f"**Tamanho:** {uploaded_file.size / 1024:.2f} KB")

        if st.button("🚀 Processar Importação", type="primary", use_container_width=True):
            with st.spinner("Processando importação..."):
                try:
                    msg = ingestor.process_students_csv(uploaded_file, uploaded_file.name)
                    st.success(f"✅ {msg}")
                    st.cache_resource.clear()
                    st.info("🔄 A página será recarregada para atualizar os dados...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro na importação: {e}")
                    st.info(
                        "Dica: verifique se o CSV está no formato correto e com todas as colunas obrigatórias."
                    )

    # Seção de informações do sistema
    st.write("")
    render_section_title("ℹ️ Informações do Sistema")

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        with st.container(border=True):
            st.markdown("##### 📊 Versão")
            st.write("**CESOL Pro** v2.0 Premium")
            st.write("Streamlit: 1.55.0")

    with col_info2:
        with st.container(border=True):
            st.markdown("##### 🔧 Stack Técnico")
            st.write("**Backend:** SQLAlchemy 2.0 + PostgreSQL")
            st.write("**Frontend:** Streamlit + Plotly")