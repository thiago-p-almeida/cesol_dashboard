"""
Navegação Lateral Premium com streamlit-option-menu
Autogerado com validação automática
"""

import streamlit as st
from typing import List, Dict, Any, Optional
from streamlit_option_menu import option_menu
from utils.theme_manager import ThemeManager

def render_sidebar_navigation(
    logo_text: str = "CESOL Pro",
    logo_icon: str = "🎓",
    menu_items: Optional[List[Dict[str, Any]]] = None,
    default_index: int = 0,
    theme_manager: Optional[ThemeManager] = None
) -> str:
    """
    Renderiza menu de navegação lateral premium.
    
    Returns:
        str: ID da página selecionada
    """
    if theme_manager is None:
        theme_manager = ThemeManager()
    
    theme = theme_manager.get_current_theme()
    colors = theme_manager.get_theme_colors(theme)
    
    # Configuração padrão do menu se não fornecida
    if menu_items is None:
        menu_items = [
            {"id": "overview", "label": "Dashboard", "icon": "house"},
            {"id": "financial", "label": "Financeiro", "icon": "cash-stack"},
            {"id": "retention", "label": "Retenção", "icon": "people"},
            {"id": "forecast", "label": "Projeções", "icon": "graph-up-arrow"},
            {"id": "admin", "label": "Administração", "icon": "gear"}
        ]
    
    with st.sidebar:
        # Logo/Brand
        st.markdown(f"""
        <div style="
            padding: 1rem 0;
            margin-bottom: 1rem;
            border-bottom: 1px solid {colors['border_subtle']};
        ">
            <div style="
                font-size: 1.5rem;
                font-weight: 700;
                color: {colors['text_primary']};
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                <span>{logo_icon}</span>
                <span>{logo_text}</span>
            </div>
            <div style="
                font-size: 0.75rem;
                color: {colors['text_tertiary']};
                margin-top: 0.25rem;
            ">
                Gestão Escolar Inteligente
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu Option-Menu
        selected = option_menu(
            menu_title=None,
            options=[item["label"] for item in menu_items],
            icons=[item["icon"] for item in menu_items],
            menu_icon=None,
            default_index=default_index,
            orientation="vertical",
            styles={
                "container": {
                    "padding": "0",
                    "background-color": "transparent"
                },
                "icon": {
                    "color": colors["text_secondary"],
                    "font-size": "18px"
                },
                "nav-link": {
                    "font-size": "14px",
                    "text-align": "left",
                    "padding": "12px 16px",
                    "margin": "4px 0",
                    "border-radius": "8px",
                    "color": colors["text_secondary"],
                    "font-family": "Inter, sans-serif"
                },
                "nav-link-selected": {
                    "background-color": colors["opacity_info"].replace("0.1", "0.15"),
                    "color": colors["accent_info"],
                    "font-weight": "600",
                    "border-left": f"3px solid {colors['accent_info']}"
                },
                "nav-link-hover": {
                    "background-color": colors["bg_interactive"],
                    "color": colors["text_primary"]
                }
            },
            key="main_navigation"
        )
        
        # Mapear label selecionado para ID
        selected_id = next(
            (item["id"] for item in menu_items if item["label"] == selected),
            menu_items[0]["id"]
        )
        
        # Separador e toggle de tema
        st.markdown(f"<hr style='border-color: {colors['border_subtle']}; margin: 2rem 0 1rem 0;'>", unsafe_allow_html=True)
        
        # Toggle de tema
        theme_manager.render_toggle(position="sidebar")
        
        # Versão no footer
        st.markdown(f"""
        <div style="
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid {colors['border_subtle']};
            font-size: 0.75rem;
            color: {colors['text_tertiary']};
            text-align: center;
        ">
            v2.0 Premium<br>
            <span style="font-size: 0.65rem;">UI Kit CESOL</span>
        </div>
        """, unsafe_allow_html=True)
        
        return selected_id
