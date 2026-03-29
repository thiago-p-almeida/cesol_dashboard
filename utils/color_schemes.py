"""
Sistema de temas CESOL Pro - Paletas Dark e Light
Autogerado com validação automática
"""

from typing import Dict, Any

THEMES: Dict[str, Dict[str, Any]] = {
    "dark": {
        # Backgrounds
        "bg_primary": "#0F172A",
        "bg_surface": "#1E293B", 
        "bg_interactive": "#334155",
        "bg_hover": "#475569",
        
        # Borders
        "border_subtle": "#475569",
        "border_focus": "#64748B",
        
        # Text
        "text_primary": "#F1F5F9",
        "text_secondary": "#94A3B8", 
        "text_tertiary": "#64748B",
        
        # Accents
        "accent_success": "#10B981",
        "accent_info": "#3B82F6",
        "accent_warning": "#F59E0B", 
        "accent_danger": "#EF4444",
        "accent_special": "#8B5CF6",
        
        # Opacidades (rgba strings)
        "opacity_success": "rgba(16, 185, 129, 0.1)",
        "opacity_info": "rgba(59, 130, 246, 0.1)",
        "opacity_warning": "rgba(245, 158, 11, 0.1)",
        "opacity_danger": "rgba(239, 68, 68, 0.1)",
        
        # Sombras
        "shadow_sm": "0 2px 4px rgba(0, 0, 0, 0.3)",
        "shadow_md": "0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3)",
        "shadow_lg": "0 10px 15px -3px rgba(0, 0, 0, 0.5), 0 4px 6px -2px rgba(0, 0, 0, 0.4)",
        
        # Plotly específico
        "plotly_template": "plotly_dark",
        "grid_color": "rgba(241, 245, 249, 0.1)",
    },
    
    "light": {
        "bg_primary": "#F8FAFC",
        "bg_surface": "#FFFFFF",
        "bg_secondary": "#F1F5F9",
        "bg_interactive": "#E2E8F0",
        
        "border_subtle": "#E2E8F0",
        "border_focus": "#CBD5E1",
        
        "text_primary": "#0F172A",
        "text_secondary": "#475569",
        "text_tertiary": "#64748B",
        
        "accent_success": "#10B981",
        "accent_info": "#3B82F6",
        "accent_warning": "#F59E0B",
        "accent_danger": "#EF4444",
        "accent_special": "#8B5CF6",
        
        "opacity_success": "rgba(16, 185, 129, 0.1)",
        "opacity_info": "rgba(59, 130, 246, 0.1)",
        "opacity_warning": "rgba(245, 158, 11, 0.1)",
        "opacity_danger": "rgba(239, 68, 68, 0.1)",
        
        "shadow_sm": "0 1px 2px rgba(0, 0, 0, 0.05)",
        "shadow_md": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "shadow_lg": "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)",
        
        "plotly_template": "plotly_white",
        "grid_color": "rgba(15, 23, 42, 0.1)",
    }
}

# Paleta consistente para gráficos
PREMIUM_PALETTE = ["#10B981", "#3B82F6", "#F59E0B", "#EF4444", "#8B5CF6", "#64748B"]

def get_theme_colors(theme_name: str) -> Dict[str, Any]:
    # Retorna dicionário de cores para o tema especificado.
    if theme_name not in THEMES:
        raise ValueError(f"Tema '{theme_name}' não existe. Use: {list(THEMES.keys())}")
    return THEMES[theme_name]

def get_plotly_template(theme_name: str) -> str:
    # Retorna nome do template Plotly para o tema.
    return THEMES[theme_name]["plotly_template"]
