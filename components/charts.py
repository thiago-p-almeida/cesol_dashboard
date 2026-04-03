import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Optional

# =============================================================================
# CONFIGURAÇÕES DE DESIGN SYSTEM (Single Source of Truth para Gráficos)
# =============================================================================
CHART_FONT = "Inter, sans-serif"
SECONDARY_TEXT_COLOR = "#94A3B8"
# Paleta Set2: Cores pastéis que garantem contraste e elegância no Dark Mode
COLOR_PALETTE = px.colors.qualitative.Set2

def _apply_premium_layout(fig: go.Figure, show_legend: bool = True, margin_b: int = 60):
    """
    Motor central de layout. Garante espaçamentos, tipografia fluida e previne bugs do Plotly.
    """
    fig.update_layout(
        # CORREÇÃO 1 (Undefined): Passar string vazia em vez de None evita o bug no React
        title=dict(text=""),
        
        # MARGENS: O 'b' (bottom) dinâmico garante que o gráfico não esmague a legenda
        margin=dict(t=10, b=margin_b, l=10, r=10),
        
        # TIPOGRAFIA E FUNDO: Fundo transparente para herdar a cor do dashboard
        font=dict(family=CHART_FONT, size=14, color=SECONDARY_TEXT_COLOR),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        
        # LEGENDA INTELIGENTE: Ancorada no centro inferior, com espaço para respirar
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.15, # Distância segura do eixo X
            xanchor="center",
            x=0.5,
            font=dict(size=14) # Tamanho legível em tablets/mobile
        ),
        
        # TOOLTIP PREMIUM: Deixa a caixa de hover escura e elegante
        hoverlabel=dict(
            bgcolor="#1E293B",
            font_size=14,
            font_family=CHART_FONT,
            bordercolor="rgba(255,255,255,0.1)"
        )
    )
    return fig

def create_premium_pie(data: pd.DataFrame, values_col: str, names_col: str, hole: float = 0.4) -> go.Figure:
    """
    Renderiza Gráfico de Pizza/Donut otimizado para Mobile (Inside Labels).
    """
    fig = px.pie(
        data,
        values=values_col,
        names=names_col,
        hole=hole,
        color_discrete_sequence=COLOR_PALETTE
    )
    
    # CORREÇÃO 2 (Corte no Mobile): Textos para DENTRO da fatia, exibindo apenas porcentagem.
    # O nome da categoria fica na legenda e no hover (tooltip).
    fig.update_traces(
        textposition='inside',
        textinfo='percent',
        marker=dict(line=dict(color='#0F172A', width=2)),
        # Tooltip customizado para mostrar todos os detalhes ao tocar/passar o mouse
        hovertemplate="<b>%{label}</b><br>Valor: %{value}<br>Participação: %{percent}<extra></extra>"
    )
    
    # Margem inferior estendida (80) para caber legendas longas divididas em linhas
    return _apply_premium_layout(fig, margin_b=80)

def create_premium_bar(data: pd.DataFrame, x_col: str, y_col: str) -> go.Figure:
    """
    Renderiza Gráfico de Barras com eixos limpos e rótulos externos.
    """
    fig = px.bar(
        data, 
        x=x_col, 
        y=y_col,
        color_discrete_sequence=[COLOR_PALETTE[0]] # Usa a primeira cor da paleta
    )
    
    fig.update_traces(
        texttemplate="R$ %{y:,.0f}",
        textposition="outside",
        cliponaxis=False, # Permite que o texto de barras altas passe do limite do eixo
        hovertemplate="<b>%{x}</b><br>Receita: R$ %{y:,.2f}<extra></extra>"
    )
    
    # CORREÇÃO 3 (net_tuition e grade): title_text="" limpa os nomes técnicos da tela
    fig.update_yaxes(
        title_text="", 
        showgrid=True, 
        gridcolor="rgba(255,255,255,0.05)", 
        tickformat="R$ ,.0f"
    )
    fig.update_xaxes(
        title_text="", 
        showgrid=False
    )
    
    # Gráfico de barras geralmente não precisa de legenda (os rótulos do eixo X bastam)
    return _apply_premium_layout(fig, show_legend=False)

def create_premium_area(data: pd.DataFrame, x_col: str, y_cols: List[str]) -> go.Figure:
    """
    Renderiza Gráfico de Área (Projeções) com eixo X dinâmico (Auto-Rotate).
    """
    fig = go.Figure()
    
    # Renderiza múltiplas linhas (ex: Receita vs Risco)
    for i, y_col in enumerate(y_cols):
        color = COLOR_PALETTE[i % len(COLOR_PALETTE)]
        fig.add_trace(go.Scatter(
            x=data[x_col],
            y=data[y_col],
            name=y_col,
            fill='tozeroy' if i == 0 else None, # Preenche apenas a linha de base
            line=dict(color=color, width=3),
            mode="lines"
        ))
    
    # CORREÇÃO 4 (Datas abarrotadas): Removido o 'tickangle=0'. 
    # O Plotly agora vai inclinar as datas sozinho no mobile se o espaço apertar.
    fig.update_xaxes(
        title_text="", 
        showgrid=False
    )
    
    fig.update_yaxes(
        title_text="",
        showgrid=True, 
        gridcolor="rgba(255,255,255,0.05)", 
        tickformat="R$ ,.0f"
    )
    
    # Margem inferior generosa (100) para evitar que as datas longas toquem na legenda
    return _apply_premium_layout(fig, margin_b=100)