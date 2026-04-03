import streamlit as st
from streamlit_option_menu import option_menu
from utils.pages_config import PAGES_CONFIG

def render_sidebar_navigation(
    logo_text: str = "CESOL Pro",
    default_index: int = 0
) -> str:
    
    # Monta as listas lendo diretamente do dicionário central
    page_ids = list(PAGES_CONFIG.keys())
    labels = [config["label"] for config in PAGES_CONFIG.values()]
    icons = [config["sidebar_icon"] for config in PAGES_CONFIG.values()]
    
    with st.sidebar:
        # Trocando o emoji por um SVG Lucide refinado para a logo da escola
        logo_svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#3B82F6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>'''
        
        st.markdown(f'''
            <div style="display:flex; align-items:center; gap:10px; margin-bottom:5px;">
                {logo_svg}
                <h2 style="margin:0; font-size:1.4rem; color:#F1F5F9;">{logo_text}</h2>
            </div>
            <div style="color:#94A3B8; font-size:0.8rem; margin-bottom:20px;">Gestão Escolar Inteligente</div>
            <hr style="margin:10px 0; border-color:rgba(255,255,255,0.1);">
        ''', unsafe_allow_html=True)
        
        selected_label = option_menu(
            menu_title=None,
            options=labels,
            icons=icons,
            menu_icon=None,
            default_index=default_index,
            orientation="vertical"
        )
        
        # Mapeia de volta o label selecionado para o ID da página
        selected_id = page_ids[labels.index(selected_label)]
        
        st.markdown("<hr style='margin:20px 0; border-color:rgba(255,255,255,0.1);'>", unsafe_allow_html=True)
        st.caption("v2.5 Premium")
        
        return selected_id