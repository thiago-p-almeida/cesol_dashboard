"""Sistema de alertas nativo do Streamlit (CESOL Pro)."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

import streamlit as st


AlertType = Literal["error", "warning", "success", "info"]


def show_alert_premium(
    message: str,
    alert_type: AlertType = "info",
    title: Optional[str] = None,
    icon: Optional[str] = None,
) -> None:
    """Exibe um alerta com componentes nativos do Streamlit."""
    display_title = title or {
        "error": "Crítico",
        "warning": "Atenção",
        "success": "Sucesso",
        "info": "Informação",
    }.get(alert_type, "Informação")

    display_icon = icon or {
        "error": "⛔",
        "warning": "⚠️",
        "success": "✅",
        "info": "ℹ️",
    }.get(alert_type, "ℹ️")

    content = f"{display_icon} **{display_title}:** {message}"
    if alert_type == "error":
        st.error(content)
    elif alert_type == "warning":
        st.warning(content)
    elif alert_type == "success":
        st.success(content)
    else:
        st.info(content)


def show_alert_container(
    alerts: List[Dict[str, Any]],
    expanded: bool = True,
    title: str = "Sistema de Alertas Gerenciais",
    key: str = "alert_container",
) -> None:
    """Renderiza um container com múltiplos alertas."""
    if not alerts:
        return

    with st.expander(f"🚨 {title}", expanded=expanded):
        for a in alerts:
            show_alert_premium(
                message=a.get("msg") or a.get("message") or "",
                alert_type=a.get("tipo") or a.get("type") or "info",
                title=a.get("title"),
                icon=a.get("icon"),
            )