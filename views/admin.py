# View Administração - Ingestão de Dados
# Autogerado com validação automática

import streamlit as st
from typing import Any, Optional

from utils.theme_manager import ThemeManager


def render_admin_view(
    ingestor: Any,
    theme_manager: Optional[ThemeManager] = None
) -> None:
    """
    Renderiza view de administração e ingestão de dados.

    Args:
        ingestor: Instância DataIngestionService
        theme_manager: Instância ThemeManager (auto-cria se None)
    """
    if theme_manager is None:
        theme_manager = ThemeManager()

    theme = theme_manager.get_current_theme()
    colors = theme_manager.get_theme_colors(theme)

    # Header
    st.markdown(
        f"""
        <h2 style="
            color: {colors['text_primary']};
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        ">⚙️ Central de Administração</h2>
        <p style="
            color: {colors['text_secondary']};
            font-size: 0.875rem;
            margin-bottom: 2rem;
        ">Gerenciamento de dados e configurações do sistema</p>
        """,
        unsafe_allow_html=True
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
    st.markdown(
        f"""
        <h4 style="color: {colors['text_primary']}; font-size: 1.125rem; margin: 1.5rem 0 1rem;">
            📤 Importar Dados de Alunos
        </h4>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader(
        "Escolha o arquivo CSV de alunos",
        type=["csv"],
        help="O arquivo deve estar no formato CSV com as colunas especificadas acima."
    )

    if uploaded_file is not None:
        st.markdown(
            f"""
            <div style="
                background-color: {colors['opacity_info']};
                border-left: 4px solid {colors['accent_info']};
                border-radius: 8px;
                padding: 1rem;
                margin: 1rem 0;
            ">
                <strong>Arquivo selecionado:</strong> {uploaded_file.name}<br>
                <strong>Tamanho:</strong> {uploaded_file.size / 1024:.2f} KB
            </div>
            """,
            unsafe_allow_html=True
        )

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
                    st.markdown(
                        f"""
                        <div style="
                            background-color: {colors['opacity_danger']};
                            border-left: 4px solid {colors['accent_danger']};
                            border-radius: 8px;
                            padding: 1rem;
                            margin: 1rem 0;
                        ">
                            <strong>Dica:</strong> Verifique se o arquivo CSV está no formato correto e se todas as colunas obrigatórias estão presentes.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

    # Seção de informações do sistema
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <h4 style="color: {colors['text_primary']}; font-size: 1.125rem; margin: 1.5rem 0 1rem;">
            ℹ️ Informações do Sistema
        </h4>
        """,
        unsafe_allow_html=True
    )

    col_info1, col_info2 = st.columns(2)

    with col_info1:
        st.markdown(
            f"""
            <div style="
                background-color: {colors['bg_surface']};
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: {colors['shadow_md']};
            ">
                <h5 style="color: {colors['text_primary']}; margin-bottom: 1rem;">📊 Versão</h5>
                <p style="color: {colors['text_secondary']}; margin: 0;">
                    <strong>CESOL Pro</strong> v2.0 Premium<br>
                    UI Kit: Midnight Scholar / Scholar Pro<br>
                    Streamlit: 1.55.0
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_info2:
        st.markdown(
            f"""
            <div style="
                background-color: {colors['bg_surface']};
                border-radius: 12px;
                padding: 1.5rem;
                box-shadow: {colors['shadow_md']};
            ">
                <h5 style="color: {colors['text_primary']}; margin-bottom: 1rem;">🔧 Stack Técnico</h5>
                <p style="color: {colors['text_secondary']}; margin: 0;">
                    <strong>Backend:</strong> SQLAlchemy 2.0 + PostgreSQL<br>
                    <strong>Frontend:</strong> Streamlit + Plotly 6.6<br>
                    <strong>UI/UX:</strong> Inter + Phosphor Icons
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )