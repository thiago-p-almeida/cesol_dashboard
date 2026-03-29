"""
Gerenciamento de temas Dark/Light para CESOL Pro.
Versão estável e compatível com o restante do sistema.
"""

from __future__ import annotations

from typing import Optional

import streamlit as st

from utils.color_schemes import THEMES, get_theme_colors


ICON_FALLBACK = {
    "coins": "💰",
    "revenue": "💰",
    "credit-card": "💳",
    "expense": "💳",
    "users": "👥",
    "people": "👥",
    "students": "👥",
    "chart": "📈",
    "chart-line-up": "📈",
    "graph-up-arrow": "📊",
    "warning": "⚠️",
    "check-circle": "✅",
    "success": "✅",
    "info": "ℹ️",
    "house": "🏠",
    "cash-stack": "💵",
    "gear": "⚙️",
    "trend-up": "📈",
    "trend-down": "📉",
}


class ThemeManager:
    """
    Gerencia tema atual (dark/light), injeção de CSS e utilidades visuais.
    """

    def __init__(self, theme_key: str = "cesol_theme", default_theme: str = "dark"):
        self.theme_key = theme_key
        self.default_theme = default_theme
        self._ensure_theme_initialized()

    def _ensure_theme_initialized(self) -> None:
        """Garante que o tema existe no session_state."""
        if self.theme_key not in st.session_state:
            st.session_state[self.theme_key] = self.default_theme

    def get_current_theme(self) -> str:
        """Retorna o tema atual."""
        return st.session_state.get(self.theme_key, self.default_theme)

    def set_theme(self, theme: str) -> None:
        """Define o tema e força rerun."""
        if theme not in THEMES:
            raise ValueError(f"Tema inválido: {theme}")
        st.session_state[self.theme_key] = theme
        st.rerun()

    def toggle_theme(self) -> None:
        """Alterna entre dark e light."""
        current = self.get_current_theme()
        new_theme = "light" if current == "dark" else "dark"
        self.set_theme(new_theme)

    def get_color(self, token: str) -> str:
        """Retorna um token de cor do tema atual."""
        colors = self.get_theme_colors()
        if token not in colors:
            raise KeyError(f"Token de cor '{token}' não existe no tema atual")
        return colors[token]

    def get_theme_colors(self, theme: Optional[str] = None) -> dict:
        """Retorna o dicionário de cores do tema."""
        resolved_theme = theme or self.get_current_theme()
        return get_theme_colors(resolved_theme)

    def get_icon(self, icon_name: str, size: int = 20) -> str:
        """
        Retorna HTML simples e estável para ícones.
        Mantém compatibilidade com os componentes que esperam uma string HTML.
        """
        icon_char = ICON_FALLBACK.get(icon_name, "📊")
        return (
            f'<span style="font-size:{size}px; line-height:1; '
            f'display:inline-flex; align-items:center; margin-right:8px;">'
            f'{icon_char}</span>'
        )

    def inject_css(self) -> None:
        """
        Injeta CSS global baseado no tema atual.
        """
        colors = self.get_theme_colors()

        css_vars = f"""
            --cesol-bg-primary: {colors['bg_primary']};
            --cesol-bg-surface: {colors['bg_surface']};
            --cesol-bg-interactive: {colors.get('bg_interactive', colors.get('bg_hover', '#334155'))};
            --cesol-text-primary: {colors['text_primary']};
            --cesol-text-secondary: {colors['text_secondary']};
            --cesol-text-tertiary: {colors.get('text_tertiary', '#64748B')};
            --cesol-accent-success: {colors['accent_success']};
            --cesol-accent-info: {colors['accent_info']};
            --cesol-accent-warning: {colors['accent_warning']};
            --cesol-accent-danger: {colors['accent_danger']};
            --cesol-border-subtle: {colors['border_subtle']};
            --cesol-shadow-md: {colors['shadow_md']};
            --cesol-shadow-lg: {colors['shadow_lg']};
        """

        css = f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        :root {{
            {css_vars}
            --font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }}

        html, body, .stApp {{
            font-family: var(--font-family) !important;
            background-color: var(--cesol-bg-primary) !important;
            color: var(--cesol-text-primary) !important;
            transition: background-color 0.3s ease, color 0.3s ease;
        }}

        #MainMenu {{ visibility: hidden !important; }}
        footer {{ visibility: hidden !important; }}
        .stDeployButton {{ display: none !important; }}

        .stApp section[data-testid="stSidebar"] {{
            background-color: var(--cesol-bg-surface) !important;
            border-right: 1px solid var(--cesol-border-subtle) !important;
        }}

        .stApp section[data-testid="stSidebar"] .stMarkdown,
        .stApp section[data-testid="stSidebar"] p,
        .stApp section[data-testid="stSidebar"] span,
        .stApp section[data-testid="stSidebar"] label {{
            color: var(--cesol-text-secondary) !important;
        }}

        .stApp section[data-testid="stSidebar"] h1,
        .stApp section[data-testid="stSidebar"] h2,
        .stApp section[data-testid="stSidebar"] h3 {{
            color: var(--cesol-text-primary) !important;
        }}

        .cesol-card-container {{
            background-color: var(--cesol-bg-surface);
            border-radius: 12px;
            padding: 1.25rem;
            border-left: 4px solid var(--card-accent, var(--cesol-accent-info));
            box-shadow: var(--cesol-shadow-md);
            transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
            margin-bottom: 1rem;
            height: 100%;
        }}

        .cesol-card-container:hover {{
            transform: translateY(-3px);
            box-shadow: var(--cesol-shadow-lg);
        }}

        .cesol-card-header {{
            display: flex;
            align-items: center;
            margin-bottom: 0.75rem;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--cesol-text-tertiary);
            line-height: 1.4;
        }}

        .cesol-card-value {{
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--cesol-text-primary);
            line-height: 1.2;
            margin-bottom: 0.375rem;
            font-family: var(--font-family);
        }}

        .cesol-card-delta {{
            font-size: 0.875rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}

        .cesol-card-delta.positive {{ color: var(--cesol-accent-success); }}
        .cesol-card-delta.negative {{ color: var(--cesol-accent-danger); }}
        .cesol-card-delta.warning {{ color: var(--cesol-accent-warning); }}
        .cesol-card-delta.neutral {{ color: var(--cesol-text-secondary); }}

        .cesol-card-help {{
            margin-left: auto;
            cursor: help;
            opacity: 0.6;
            transition: opacity 0.2s;
        }}

        .cesol-card-help:hover {{
            opacity: 1;
        }}

        .stApp [data-testid="stVerticalBlock"] > div {{
            background-color: transparent;
        }}

        .stApp [data-testid="stMetric"] {{
            background-color: var(--cesol-bg-surface);
            border-radius: 12px;
            padding: 1rem;
            border-left: 4px solid var(--cesol-accent-info);
        }}

        .stApp [data-testid="stMetricLabel"] {{
            color: var(--cesol-text-tertiary) !important;
        }}

        .stApp [data-testid="stMetricValue"] {{
            color: var(--cesol-text-primary) !important;
            font-weight: 700;
        }}

        .stApp [data-testid="stTextInput"] input,
        .stApp [data-testid="stNumberInput"] input,
        .stApp [data-baseweb="select"] > div {{
            background-color: var(--cesol-bg-interactive) !important;
            color: var(--cesol-text-primary) !important;
            border-color: var(--cesol-border-subtle) !important;
            border-radius: 8px !important;
        }}

        .stApp [data-testid="stSlider"] {{
            background-color: transparent !important;
        }}

        .stApp button[kind="primary"] {{
            background-color: var(--cesol-accent-success) !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }}

        .stApp button[kind="primary"]:hover {{
            transform: translateY(-1px);
            box-shadow: var(--cesol-shadow-md);
        }}

        .stApp [data-testid="stDataFrame"] {{
            background-color: var(--cesol-bg-surface) !important;
            border-radius: 8px;
            border: 1px solid var(--cesol-border-subtle);
        }}

        .stApp [data-testid="stExpander"] {{
            background-color: var(--cesol-bg-surface) !important;
            border-radius: 8px;
            border: 1px solid var(--cesol-border-subtle);
        }}

        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: transparent;
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--cesol-border-subtle);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--cesol-text-tertiary);
        }}

        @keyframes slideIn {{
            from {{ transform: translateX(-10px); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}

        .cesol-animate-in {{
            animation: slideIn 0.3s ease-out;
        }}
        </style>
        """

        st.markdown(css, unsafe_allow_html=True)

    def render_toggle(self, position: str = "sidebar") -> None:
        """
        Renderiza toggle de tema.
        """
        current = self.get_current_theme()
        label = f"{'🌙' if current == 'dark' else '☀️'} Tema {current.title()}"

        container = st.sidebar if position == "sidebar" else st
        with container:
            col1, col2 = st.columns([3, 1])

            with col1:
                if st.button(label, key="theme_toggle_btn", width="stretch"):
                    self.toggle_theme()

            with col2:
                indicator_color = "#10B981" if current == "dark" else "#F59E0B"
                st.markdown(
                    f'<div style="width:12px;height:12px;border-radius:50%;background:{indicator_color};margin-top:10px;"></div>',
                    unsafe_allow_html=True,
                )


# Singleton compartilhado do gerenciador de tema
theme_manager = ThemeManager()