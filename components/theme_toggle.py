
# Toggle de Tema Dark/Light (wrapper se necessário)
# Autogerado com validação automática


import streamlit as st
from utils.theme_manager import ThemeManager

def render_theme_toggle_standalone(position: str = "sidebar") -> None:
    
    # Versão standalone do toggle se necessário fora do navigation.
    
    manager = ThemeManager()
    manager.render_toggle(position=position)
