import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Optional

# =============================================================================
# CONFIGURAÇÕES DE DESIGN SYSTEM (Single Source of Truth)
# =============================================================================
CHART_FONT = "Inter, sans-serif"
SECONDARY_TEXT_COLOR = "#94A3B8"
COLOR_PALETTE = px.colors.qualitative.Set2

def _apply_premium_layout(fig: go.Figure, show_legend: bool = True, margin_b: int = 60):
    """
    Aplica o motor de layout premium. 
    CORREÇÃO: Removida a propriedade 'modebar' que causava conflito de versão.
    """
    fig.update_layout(
        # Mantém a correção para evitar o erro 'undefined' no React
        title=dict(text=""),
        margin=dict(t=10, b=margin_b, l=10, r=10),
        font=dict(family=CHART_FONT, size=14, color=SECONDARY_TEXT_COLOR),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15,
            xanchor="center",
            x=0.5,
            font=dict(size=14)
        )
    )
    
    # Limpeza global de títulos de eixos para evitar vazamento de nomes técnicos
    fig.update_xaxes(title_text="", showgrid=False)
    fig.update_yaxes(title_text="", showgrid=True, gridcolor="rgba(255,255,255,0.05)")
    
    return fig

def create_premium_pie(data: pd.DataFrame, values_col: str, names_col: str, hole: float = 0.4) -> go.Figure:
    """
    Renderiza Gráfico de Pizza/Donut otimizado para Mobile.
    """
    fig = px.pie(
        data,
        values=values_col,
        names=names_col,
        hole=hole,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        marker=dict(line=dict(color='#0F172A', width=2)),
        hovertemplate="<b>%{label}</b><br>Valor: %{value}<br>Participação: %{percent}<extra></extra>"
    )
    
    return _apply_premium_layout(fig, margin_b=80)

def create_premium_bar(
    data: pd.DataFrame, 
    x_col: str, 
    y_col: str, 
    is_currency: bool = True
) -> go.Figure:
    """
    Renderiza Gráfico de Barras Polimórfico (Moeda ou Inteiro).
    """
    fig = px.bar(
        data, 
        x=x_col, 
        y=y_col,
        color_discrete_sequence=[COLOR_PALETTE[0]]
    )
    
    if is_currency:
        text_fmt = "R$ %{y:,.0f}"
        tick_fmt = "R$ ,.0f"
        hover_fmt = "<b>%{x}</b><br>Receita: R$ %{y:,.2f}<extra></extra>"
    else:
        text_fmt = "%{y}"
        tick_fmt = "d"
        hover_fmt = "<b>%{x}</b><br>Quantidade: %{y}<extra></extra>"

    fig.update_traces(
        texttemplate=text_fmt,
        textposition="outside",
        cliponaxis=False,
        hovertemplate=hover_fmt
    )
    
    fig.update_yaxes(tickformat=tick_fmt)
    
    return _apply_premium_layout(fig, show_legend=False)

def create_premium_area(data: pd.DataFrame, x_col: str, y_cols: List[str]) -> go.Figure:
    """
    Renderiza Gráfico de Área para Projeções.
    """
    fig = go.Figure()
    
    for i, y_col in enumerate(y_cols):
        color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            name=y_col,
            fill='tozeroy' if i == 0 else None,
            line=dict(color=color, width=3),
            mode="lines"
        ))
    
    return _apply_premium_layout(fig, margin_b=100)