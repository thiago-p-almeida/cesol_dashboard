import streamlit as st
from utils.pages_config import PAGES_CONFIG

def render_page_header(page_id: str, title: str, subtitle: str = "") -> None:
    """
    Cabeçalho de página inteligente que injeta SVGs do Lucide Icons automaticamente.
    """
    # Busca a configuração da página, com fallback seguro caso o ID não exista
    config = PAGES_CONFIG.get(page_id, {})
    svg_icon = config.get("header_svg", "")

    # Flexbox para alinhar o SVG com o texto do título perfeitamente
    html = f'''
    <div style="margin-bottom:25px;">
        <div style="display:flex; align-items:center; gap:12px; color:#F1F5F9;">
            <div style="display:flex; align-items:center; justify-content:center; color:#3B82F6;">
                {svg_icon}
            </div>
            <h2 style="margin:0; font-size:1.75rem; font-weight:700;">{title}</h2>
        </div>
    '''
    if subtitle:
        html += f'<p style="color:#94A3B8; font-size:0.9rem; margin:8px 0 0 40px;">{subtitle}</p>'
    
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)

def render_section_title(title: str) -> None:
    """Título de seção com margem controlada."""
    st.markdown(f'<h3 style="color:#F1F5F9;font-size:1.2rem;margin:30px 0 15px 0;display:flex;align-items:center;gap:10px;">{title}</h3>', unsafe_allow_html=True)

def render_info_box(title: str, content: str) -> None:
    """Box de informação com estilo nativo e seguro."""
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.write(content)