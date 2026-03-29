import streamlit as st
from typing import List, Dict, Any

def render_kpi_grid(metrics: List[Dict[str, Any]], columns: List[Any]) -> None:
    """Renderiza grid de KPIs usando o componente nativo st.metric."""
    for i, metric in enumerate(metrics):
        col_idx = i % len(columns)
        with columns[col_idx]:
            st.metric(
                label=metric.get("label", ""),
                value=metric.get("value", ""),
                delta=metric.get("delta")
            )