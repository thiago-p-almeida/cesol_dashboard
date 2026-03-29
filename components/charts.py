
# Wrappers Plotly com temas e animações premium
# Autogerado com validação automática


import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Optional, List, Any
from utils.theme_manager import ThemeManager
from utils.color_schemes import PREMIUM_PALETTE

def create_premium_pie(
    data: pd.DataFrame,
    values_col: str,
    names_col: str,
    hole: float = 0.4,
    theme: Optional[str] = None,
    color_discrete_sequence: Optional[List[str]] = None,
    animation: bool = True
) -> go.Figure:
    # Gráfico de pizza/donut premium.
    if theme is None:
        theme = ThemeManager().get_current_theme()
    
    colors = ThemeManager().get_theme_colors(theme)
    palette = color_discrete_sequence or PREMIUM_PALETTE
    
    fig = px.pie(
        data,
        values=values_col,
        names=names_col,
        hole=hole,
        color_discrete_sequence=palette,
        template=colors['plotly_template']
    )
    
    # Animação de rotação inicial
    if animation:
        fig.update_traces(
            rotation=90,
            pull=[0.02 if i == 0 else 0 for i in range(len(data))],
            marker=dict(line=dict(color=colors['bg_surface'], width=2))
        )
    
    # Layout premium
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.1,
            xanchor="center",
            x=0.5,
            font=dict(family="Inter", size=12, color=colors['text_secondary'])
        ),
        margin=dict(t=30, b=60, l=20, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color=colors['text_primary']),
        hoverlabel=dict(
            bgcolor=colors['bg_surface'],
            font_color=colors['text_primary'],
            font_family="Inter",
            bordercolor=colors['border_subtle']
        )
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
    # Gráfico de barras premium com cantos arredondados.
    if theme is None:
        theme = ThemeManager().get_current_theme()
    
    colors = ThemeManager().get_theme_colors(theme)
    
    # Criar figura base
    if color_col:
        fig = px.bar(
            data, x=x_col, y=y_col, color=color_col,
            color_discrete_sequence=PREMIUM_PALETTE if color_discrete_sequence else None,
            template=colors['plotly_template']
        )
    else:
        fig = px.bar(
            data, x=x_col, y=y_col,
            color_discrete_sequence=[colors['accent_success']],
            template=colors['plotly_template']
        )
    
    # Animação: barras crescendo de baixo
    if animation:
        fig.update_traces(
            marker=dict(
                line=dict(color=colors['bg_surface'], width=1),
                cornerradius=8
            ),
            texttemplate='R$ %{y:,.0f}',
            textposition='outside',
            cliponaxis=False,
            hovertemplate=f'<b>%{{x}}</b><br>R$ %{{y:,.2f}}<extra></extra>'
        )
    else:
        fig.update_traces(
            marker_line_color=colors['bg_surface'],
            marker_line_width=1
        )
    
    # Layout
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            color=colors['text_secondary'],
            title=dict(text=x_col.replace('_', ' ').title(), font=dict(size=12))
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=colors['grid_color'],
            color=colors['text_secondary'],
            title=dict(text='Valor (R$)', font=dict(size=12)),
            tickformat='R$ ,.0f'
        ),
        margin=dict(t=40, b=40, l=60, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color=colors['text_primary']),
        showlegend=False,
        hovermode='x unified'
    )
    
    return fig


def create_premium_area(
    data: pd.DataFrame,
    x_col: str,
    y_cols: List[str],
    theme: Optional[str] = None,
    fill_gradient: bool = True
) -> go.Figure:
    # Gráfico de área/linha para projeções.
    if theme is None:
        theme = ThemeManager().get_current_theme()
    
    colors = ThemeManager().get_theme_colors(theme)
    
    fig = go.Figure()
    
    for i, y_col in enumerate(y_cols):
        color = PREMIUM_PALETTE[i % len(PREMIUM_PALETTE)]
        
        # Converter hex para rgba para fill
        hex_color = color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgba_fill = f'rgba({r}, {g}, {b}, 0.2)'
        
        # Gradiente suave
        if fill_gradient and i == 0:  # Apenas primeira série com fill
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                name=y_col,
                fill='tozeroy',
                fillcolor=rgba_fill,
                line=dict(color=color, width=3),
                mode='lines'
            ))
        else:
            fig.add_trace(go.Scatter(
                x=data[x_col],
                y=data[y_col],
                name=y_col,
                line=dict(color=color, width=2),
                mode='lines'
            ))
    
    fig.update_layout(
        xaxis=dict(
            showgrid=False,
            color=colors['text_secondary']
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor=colors['grid_color'],
            color=colors['text_secondary'],
            tickformat='R$ ,.0f'
        ),
        margin=dict(t=30, b=40, l=60, r=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter", color=colors['text_primary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor=colors['bg_surface'],
            font_color=colors['text_primary'],
            font_family="Inter",
            bordercolor=colors['border_subtle']
        )
    )
    
    return fig
