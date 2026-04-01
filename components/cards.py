import streamlit as st
import uuid
from typing import Optional, List, Dict, Any

def get_trend_icon(trend_type: str, color: str) -> str:
    if trend_type == "up":
        return f'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display:inline;margin-right:4px;"><polyline points="18 15 12 9 6 15"></polyline></svg>'
    if trend_type == "down":
        return f'<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" style="display:inline;margin-right:4px;"><polyline points="6 9 12 15 18 9"></polyline></svg>'
    return ""

def render_metric_card(label: str, value: str, delta: Optional[str] = None, type: str = "info", trend: Optional[str] = None) -> None:
    # Identificador Único para forçar o re-render do Streamlit (Nível Gênio)
    card_id = f"card_{uuid.uuid4().hex[:8]}"
    
    colors = {"success": "#10B981", "danger": "#EF4444", "warning": "#F59E0B", "info": "#3B82F6"}
    selected_color = colors.get(type, colors["info"])
    
    icon_svg = get_trend_icon(trend, selected_color) if trend else ""
    
    # Delta construído sem nenhuma quebra de linha ou espaço inicial
    delta_html = f'<div style="display:flex;align-items:center;color:{selected_color};font-size:0.85rem;font-weight:600;margin-top:8px;">{icon_svg}{delta}</div>' if delta else '<div style="margin-top:8px;opacity:0;">&nbsp;</div>'

    # Template em bloco único de memória (Atomic string)
    # Usamos o comentário <!-- {card_id} --> para garantir que o hash do markdown seja sempre único
    raw_parts = [
        f'<div id="{card_id}" style="container-type:inline-size;width:100%;margin-bottom:10px;line-height:1.2;">',
        f'<div style="background-color:#1E293B;border-radius:12px;position:relative;overflow:hidden;min-height:135px;box-shadow:0 10px 15px -3px rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.05);display:flex;align-items:center;">',
        f'<div style="position:absolute;left:0;top:0;bottom:0;width:6px;background-color:{selected_color};"></div>',
        f'<div style="padding:0 22px;width:100%;">',
        f'<div style="font-size:0.7rem;font-weight:600;color:#94A3B8;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:6px;">{label}</div>',
        f'<div style="font-size:clamp(1.1rem, 11cqw, 1.8rem);font-weight:800;color:#F1F5F9;margin:0;letter-spacing:-0.02em;">{value}</div>',
        f'{delta_html}',
        f'</div></div><!-- {card_id} --></div>'
    ]
    
    st.markdown("".join(raw_parts), unsafe_allow_html=True)

def render_kpi_grid(metrics: List[Dict[str, Any]], columns: List[Any]) -> None:
    for i, metric in enumerate(metrics):
        col_idx = i % len(columns)
        with columns[col_idx]:
            render_metric_card(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta"),
                type=metric.get("type", "info"),
                trend=metric.get("trend")
            )