"""
Sistema de alertas (CESOL Pro).

Renderiza alertas premium via HTML seguro no Streamlit.
"""

from __future__ import annotations

import html
from typing import Any, Dict, List, Literal, Optional

import streamlit as st

from utils.theme_manager import ThemeManager

AlertType = Literal["error", "warning", "success", "info"]


def show_alert_premium(
    message: str,
    alert_type: AlertType = "info",
    title: Optional[str] = None,
    icon: Optional[str] = None,
    theme_manager: Optional[ThemeManager] = None,
) -> None:
    """
    Exibe um alerta estilizado.
    """
    if theme_manager is None:
        theme_manager = ThemeManager()

    theme = theme_manager.get_current_theme()
    colors = theme_manager.get_theme_colors(theme)

    type_config = {
        "error": {
            "accent": colors["accent_danger"],
            "bg": colors["opacity_danger"],
            "icon_default": "⛔",
            "title_default": "Crítico",
        },
        "warning": {
            "accent": colors["accent_warning"],
            "bg": colors["opacity_warning"],
            "icon_default": "⚠️",
            "title_default": "Atenção",
        },
        "success": {
            "accent": colors["accent_success"],
            "bg": colors["opacity_success"],
            "icon_default": "✅",
            "title_default": "Sucesso",
        },
        "info": {
            "accent": colors["accent_info"],
            "bg": colors["opacity_info"],
            "icon_default": "ℹ️",
            "title_default": "Informação",
        },
    }

    config = type_config.get(alert_type, type_config["info"])
    display_icon = icon or config["icon_default"]
    display_title = title or config["title_default"]

    safe_message = html.escape(str(message))
    safe_title = html.escape(str(display_title))

    alert_html = f"""
<div style="
    background-color: {config['bg']};
    border-left: 4px solid {config['accent']};
    border-radius: 8px;
    padding: 1rem;
    margin: 1rem 0;
    display: flex;
    gap: 0.75rem;
    align-items: flex-start;
">
  <div style="font-size: 20px; flex-shrink: 0; line-height: 1;">{display_icon}</div>
  <div style="flex: 1;">
    <div style="
        font-weight: 700;
        color: {config['accent']};
        margin-bottom: 0.25rem;
        font-size: 0.875rem;
    ">{safe_title}</div>
    <div style="
        color: {colors['text_secondary']};
        font-size: 0.875rem;
        line-height: 1.5;
    ">{safe_message}</div>
  </div>
</div>
    """

    st.markdown(alert_html, unsafe_allow_html=True)


def show_alert_container(
    alerts: List[Dict[str, Any]],
    expanded: bool = True,
    title: str = "Sistema de Alertas Gerenciais",
    key: str = "alert_container",
    theme_manager: Optional[ThemeManager] = None,
) -> None:
    """
    Renderiza um container (expander) com múltiplos alertas.
    """
    if not alerts:
        return

    if theme_manager is None:
        theme_manager = ThemeManager()

    with st.expander(f"🚨 {title}", expanded=expanded):
        for a in alerts:
            show_alert_premium(
                message=a.get("msg") or a.get("message") or "",
                alert_type=a.get("tipo") or a.get("type") or "info",
                title=a.get("title"),
                icon=a.get("icon"),
                theme_manager=theme_manager,
            )