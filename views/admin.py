import streamlit as st
from components.typography import render_page_header, render_section_title, render_info_box

def render_admin_view(ingestor) -> None:
    
    render_page_header(
        page_id="admin",
        title="Central de Administração",
        subtitle="Gerenciamento de dados e configurações do sistema"
    )

    with st.expander("Ver formato de arquivo aceito", expanded=True):
        try:
            from src.schemas.student_schema import COLUMN_MAP
            colunas_necessarias = ", ".join(COLUMN_MAP.keys())
        except ImportError:
            colunas_necessarias = "name, segment, grade, full_tuition, discount_value, scholarship_value"

        st.markdown(f"**O CSV deve conter as colunas:** `{colunas_necessarias}`")
        st.info("**Taxonomia Obrigatória:** O segmento deve ser categorizado como: **Ed. Infantil**, **Fundamental I**, ou **Fundamental II**.")

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Importar Dados de Alunos")

    uploaded_file = st.file_uploader(
        "Escolha o arquivo CSV de alunos",
        type=["csv"],
        help="O arquivo deve estar no formato CSV com as colunas especificadas acima."
    )

    if uploaded_file is not None:
        render_info_box("Arquivo selecionado", f"Nome: {uploaded_file.name} | Tamanho: {uploaded_file.size / 1024:.2f} KB")

        if st.button("Processar Importação", type="primary", use_container_width=True):
            with st.spinner("Processando importação..."):
                try:
                    msg = ingestor.process_students_csv(uploaded_file, uploaded_file.name)
                    st.success(f"✅ {msg}")
                    st.cache_resource.clear()
                    st.info("🔄 A página será recarregada para atualizar os dados...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro na importação: {e}")
                    render_info_box("Dica", "Verifique se o arquivo CSV está no formato correto e se todas as colunas obrigatórias estão presentes.")

    st.markdown("<br>", unsafe_allow_html=True)
    render_section_title("Informações do Sistema")

    col_info1, col_info2 = st.columns(2)
    with col_info1:
        render_info_box("Versão", "CESOL Pro v2.4 Premium\n\nUI Kit: Lucide Icons / Atomic DOM\n\nStreamlit: 1.40+")
    with col_info2:
        render_info_box("Stack Técnico", "Backend: SQLAlchemy 2.0 + PostgreSQL\n\nFrontend: Streamlit + Plotly\n\nUI/UX: Inter + Lucide")