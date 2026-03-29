import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Optional

DEFAULT_PALETTE = px.colors.qualitative.Set2

def create_premium_pie(
    data: pd.DataFrame,
    values_col: str,
    names_col: str,
    hole: float = 0.4,
    theme: Optional[str] = None,
    color_discrete_sequence: Optional[List[str]] = None,
    animation: bool = True
) -> go.Figure:
    # Mantém assinatura por compatibilidade, mas usa template nativo.
    palette = color_discrete_sequence or DEFAULT_PALETTE
    fig = px.pie(
        data,
        values=values_col,
        names=names_col,
        hole=hole,
        color_discrete_sequence=palette,
        template="plotly",
    )

    if animation:
        fig.update_traces(
            rotation=90,
            pull=[0.02 if i == 0 else 0 for i in range(len(data))],
            marker=dict(line=dict(width=1)),
        )

    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(size=12),
        ),
        margin=dict(t=30, b=60, l=20, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    return fig


def create_premium_bar(
    data: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    orientation: str = "v",
    theme: Optional[str] = None,
    color_discrete_sequence: bool = False,
    animation: bool = True
) -> go.Figure:
    # Mantém assinatura por compatibilidade, mas usa componentes nativos.
    if color_col:
        fig = px.bar(
            data, x=x_col, y=y_col, color=color_col,
            color_discrete_sequence=DEFAULT_PALETTE if color_discrete_sequence else None,
            template="plotly",
        )
    else:
        fig = px.bar(
            data, x=x_col, y=y_col,
            color_discrete_sequence=[DEFAULT_PALETTE[0]],
            template="plotly",
        )

    if animation:
        fig.update_traces(
            marker=dict(line=dict(width=1)),
            texttemplate="R$ %{y:,.0f}",
            textposition="outside",
            cliponaxis=False,
            hovertemplate="<b>%{x}</b><br>R$ %{y:,.2f}<extra></extra>",
        )
    else:
        fig.update_traces(marker_line_width=1)

    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            title=dict(text=x_col.replace("_", " ").title(), font=dict(size=12)),
        ),
        yaxis=dict(
            showgrid=True,
            title=dict(text='Valor (R$)', font=dict(size=12)),
            tickformat="R$ ,.0f",
        ),
        margin=dict(t=40, b=40, l=60, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False,
        hovermode="x unified",
    )

    return fig


def create_premium_area(
    data: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    theme: Optional[str] = None,
    fill_gradient: bool = True
) -> go.Figure:
    # Mantém assinatura por compatibilidade, sem dependência de tema customizado.
    fig = go.Figure()

    for i, y_col in enumerate(y_cols):
        color = DEFAULT_PALETTE[i % len(DEFAULT_PALETTE)]
        hex_color = color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgba_fill = f"rgba({r}, {g}, {b}, 0.2)"

        if fill_gradient and i == 0:
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                name=y_col,
                fill="tozeroy",
                fillcolor=rgba_fill,
                line=dict(color=color, width=3),
                mode="lines",
            ))
        else:
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                name=y_col,
                line=dict(color=color, width=2),
                mode="lines",
            ))

    fig.update_layout(
        xaxis=dict(showgrid=False),
        yaxis=dict(
            showgrid=True,
            tickformat="R$ ,.0f",
        ),
        margin=dict(t=30, b=40, l=60, r=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        hovermode="x unified",
    )

    return fig
