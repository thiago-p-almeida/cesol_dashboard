import streamlit as st

def render_page_header(title: str, subtitle: str = "") -> None:
    """Renderiza o cabeçalho usando o estilo nativo do Streamlit."""
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)
    st.markdown("---")

def render_section_title(title: str) -> None:
    """Renderiza o título de uma subseção."""
    st.markdown(f"### {title}")

def render_info_box(title: str, content: str) -> None:
    """Renderiza um card de informação usando o box nativo do Streamlit."""
    with st.container(border=True):
        st.subheader(title)
        st.write(content)