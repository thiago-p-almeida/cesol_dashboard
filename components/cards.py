"""
Componentes de Cards de Métricas - versão ultra-estável para Streamlit.
Prioriza compatibilidade e simplicidade de renderização.
"""

from __future__ import annotations

import html
from typing import Any, Dict, List, Literal, Optional

import streamlit as st

from utils.theme_manager import ThemeManager

DeltaColor = Literal["success", "warning", "danger", "neutral"]
Variant = Literal["default", "success", "info", "warning", "danger"]


_ICON_TEXT_MAP: Dict[str, str] = {
    "coins": "💰",
    "revenue": "💰",
    "cash-stack": "💵",
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
    "gear": "⚙️",
    "trend-up": "📈",
    "trend-down": "📉",
}


def _get_icon_text(icon: Optional[str]) -> str:
    if not icon:
        return ""
    return _ICON_TEXT_MAP.get(str(icon).strip(), "📊")


def _get_delta_prefix(delta_color: DeltaColor) -> str:
    if delta_color == "success":
        return "↑ "
    if delta_color == "danger":
        return "↓ "
    if delta_color == "warning":
        return "⚠ "
    return ""


def render_metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    delta_color: DeltaColor = "success",
    icon: Optional[str] = None,
    variant: Variant = "default",
    help_text: Optional[str] = None,
    theme_manager: Optional[ThemeManager] = None,
) -> None:
    """
    Renderiza card de KPI com componentes nativos do Streamlit.
    Não usa HTML estrutural complexo.
    """
    if theme_manager is None:
        theme_manager = ThemeManager()

    colors = theme_manager.get_theme_colors()

    icon_text = _get_icon_text(icon)
    label_text = f"{icon_text} {label}".strip()
    safe_label = html.escape(str(label_text))
    safe_value = html.escape(str(value))
    safe_help = html.escape(str(help_text)) if help_text else ""

    delta_prefix = _get_delta_prefix(delta_color)
    safe_delta = html.escape(str(delta)) if delta is not None else ""

    delta_colors = {
        "success": colors["accent_success"],
        "warning": colors["accent_warning"],
        "danger": colors["accent_danger"],
        "neutral": colors["text_secondary"],
    }
    delta_color_value = delta_colors.get(delta_color, colors["text_secondary"])

    with st.container():
        st.caption(safe_label)

        st.markdown(
            f"""
<span style="
    font-size: 2rem;
    font-weight: 700;
    line-height: 1.2;
    color: {colors['text_primary']};
">{safe_value}</span>
""",
            unsafe_allow_html=True,
        )

        if delta:
            st.markdown(
                f"""
<span style="
    font-size: 0.9rem;
    font-weight: 600;
    color: {delta_color_value};
">{html.escape(delta_prefix)}{safe_delta}</span>
""",
                unsafe_allow_html=True,
            )

        if help_text:
            st.caption(safe_help)

        st.divider()


def render_kpi_grid(
    metrics: List[Dict[str, Any]],
    columns: List[Any],
    theme_manager: Optional[ThemeManager] = None,
) -> None:
    """
    Renderiza grid de KPIs em colunas.
    Mantém compatibilidade com a API existente das views.
    """
    if theme_manager is None:
        theme_manager = ThemeManager()

    if not columns:
        return

    for i, metric in enumerate(metrics):
        col_idx = i % len(columns)
        with columns[col_idx]:
            render_metric_card(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta"),
                delta_color=metric.get("delta_color", "success"),
                icon=metric.get("icon"),
                variant=metric.get("variant", "default"),
                help_text=metric.get("help_text"),
                theme_manager=theme_manager,
            )