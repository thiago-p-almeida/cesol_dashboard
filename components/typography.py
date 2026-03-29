import streamlit as st
from typing import Optional
from utils.theme_manager import ThemeManager

def render_page_header(title: str, subtitle: str = "", theme_manager: Optional[ThemeManager] = None) -> None:
    """Renderiza o cabeçalho principal da página (H2)."""
    if theme_manager is None:
        theme_manager = ThemeManager()
    
    colors = theme_manager.get_theme_colors()
    
    # HTML em uma única linha para evitar que o Markdown interprete os espaços como "bloco de código"
    html = f'<h2 style="color: {colors["text_primary"]}; font-size: 1.5rem; font-weight: 600; margin-bottom: 0.5rem;">{title}</h2>'
    
    if subtitle:
        html += f'<p style="color: {colors["text_secondary"]}; font-size: 0.875rem; margin-bottom: 2rem;">{subtitle}</p>'
        
    st.markdown(html, unsafe_allow_html=True)


def render_section_title(title: str, theme_manager: Optional[ThemeManager] = None) -> None:
    """Renderiza o título de uma subseção (H3/H4)."""
    if theme_manager is None:
        theme_manager = ThemeManager()
        
    colors = theme_manager.get_theme_colors()
    
    html = f'<h3 style="color: {colors["text_primary"]}; font-size: 1.125rem; font-weight: 600; margin-bottom: 1rem; margin-top: 1rem;">{title}</h3>'
    st.markdown(html, unsafe_allow_html=True)


def render_info_box(title: str, content: str, theme_manager: Optional[ThemeManager] = None) -> None:
    """Renderiza um card de informação estilizado."""
    if theme_manager is None:
        theme_manager = ThemeManager()
        
    colors = theme_manager.get_theme_colors()
    
    html = f"""
<div style="background-color: {colors['bg_surface']}; border-radius: 12px; padding: 1.5rem; border-left: 4px solid {colors['accent_info']}; box-shadow: {colors['shadow_md']}; margin-bottom: 1rem;">
    <h5 style="color: {colors['text_primary']}; margin-bottom: 0.5rem;">{title}</h5>
    <div style="color: {colors['text_secondary']}; line-height: 1.6;">{content}</div>
</div>
"""
    # Usando strip() para remover qualquer espaço extra indesejado no início e no fim
    st.markdown(html.strip(), unsafe_allow_html=True)