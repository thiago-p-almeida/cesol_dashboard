import streamlit as st
from typing import List, Dict, Any, Optional

def render_sidebar_navigation(
    logo_text: str = "CESOL Pro",
    logo_icon: str = "🎓",
    menu_items: Optional[List[Dict[str, Any]]] = None,
    default_index: int = 0
) -> str:
    
    if menu_items is None:
        menu_items = [
            {"id": "overview", "label": "Dashboard", "icon": "house"},
            {"id": "financial", "label": "Financeiro", "icon": "cash-stack"},
            {"id": "retention", "label": "Retenção", "icon": "people"},
            {"id": "forecast", "label": "Projeções", "icon": "graph-up-arrow"},
            {"id": "admin", "label": "Administração", "icon": "gear"}
        ]
    
    with st.sidebar:
        st.markdown(f"## {logo_icon} {logo_text}")
        st.caption("Gestão Escolar Inteligente")
        st.markdown("---")

        options = [item["label"] for item in menu_items]
        selected = st.radio(
            label="Navegação",
            options=options,
            index=default_index,
            label_visibility="collapsed",
        )

        selected_id = next((item["id"] for item in menu_items if item["label"] == selected), menu_items[0]["id"])

        st.markdown("---")
        st.caption("v2.3 Premium")

        return selected_id