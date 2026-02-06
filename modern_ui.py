# modern_ui.py
"""
Sistema de Diseño Moderno para Audio Recorder & Opportunity Manager
- Paleta: Dark Navy, Cian Eléctrico, Violeta Neón
- Estética: Glassmorphism con Efectos Glow
- Tipografía: Inter / Inter Tight
"""

import streamlit as st
from typing import Literal
import json

# ============================================================================
# CONFIGURACIÓN DE COLORES (PALETA MODERNA)
# ============================================================================

COLORS = {
    # Fondos
    "bg_primary": "#0A0E27",      # Deep Navy (fondo principal)
    "bg_secondary": "#141829",    # Slightly lighter navy
    "bg_tertiary": "#1A1F3A",     # Para tarjetas
    
    # Acentos
    "accent_cyan": "#00FBFF",     # Cian eléctrico
    "accent_purple": "#8A2BE2",   # Violeta neón
    "accent_blue": "#00D9FF",     # Cian más claro
    
    # Prioridades
    "priority_high": "#FF3B5C",   # Rojo neón
    "priority_medium": "#FFB700", # Amarillo/Naranja
    "priority_low": "#00CC88",    # Verde neón
    
    # Estados
    "status_new": "#00FBFF",
    "status_progress": "#FFB700",
    "status_closed": "#00CC88",
    "status_won": "#8A2BE2",
    
    # Texto
    "text_primary": "#F0F2F5",
    "text_secondary": "#B0B8C1",
    "text_muted": "#717D8D",
}

# ============================================================================
# INYECTAR CSS MODERNO EN STREAMLIT
# ============================================================================

def inject_modern_css():
    """
    Inyecta todo el CSS personalizado en la aplicación
    Llama ANTES de cualquier otro código en index.py
    """
    css = f"""
    <style>
        /* ============================================================
           1. RESET Y CONFIGURACIÓN GLOBAL
           ============================================================ */
        
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Inter+Tight:wght@400;600;700;800&display=swap');
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html, body, [data-testid="stAppViewContainer"] {{
            background: linear-gradient(135deg, {COLORS['bg_primary']} 0%, {COLORS['bg_secondary']} 100%);
            color: {COLORS['text_primary']};
            font-family: 'Inter', sans-serif;
            min-height: 100vh;
        }}
        
        /* ============================================================
           2. TIPOGRAFÍA
           ============================================================ */
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter Tight', sans-serif;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: {COLORS['text_primary']};
        }}
        
        h1 {{
            font-size: 2.5rem;
            margin-bottom: 1.5rem;
            background: linear-gradient(135deg, {COLORS['accent_cyan']} 0%, {COLORS['accent_purple']} 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        h2 {{
            font-size: 1.875rem;
            margin-bottom: 1.25rem;
            color: {COLORS['accent_cyan']};
        }}
        
        h3 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: {COLORS['text_primary']};
        }}
        
        p, li {{
            font-size: 1rem;
            line-height: 1.6;
            color: {COLORS['text_secondary']};
        }}
        
        /* ============================================================
           3. BOTONES MODERNOS CON GLOW
           ============================================================ */
        
        button[kind="primary"] {{
            background: linear-gradient(135deg, {COLORS['accent_cyan']} 0%, {COLORS['accent_blue']} 100%);
            color: {COLORS['bg_primary']};
            border: none;
            padding: 12px 28px;
            border-radius: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 0 20px rgba(0, 251, 255, 0.3);
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        button[kind="primary"]:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 32px rgba(0, 251, 255, 0.5);
            background: linear-gradient(135deg, {COLORS['accent_blue']} 0%, {COLORS['accent_cyan']} 100%);
        }}
        
        button[kind="primary"]:active {{
            transform: translateY(0);
            box-shadow: 0 4px 16px rgba(0, 251, 255, 0.3);
        }}
        
        /* Botones secundarios */
        button[kind="secondary"] {{
            background: {COLORS['bg_tertiary']};
            color: {COLORS['accent_cyan']};
            border: 2px solid {COLORS['accent_cyan']};
            padding: 10px 24px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
        }}
        
        button[kind="secondary"]:hover {{
            background: {COLORS['accent_cyan']};
            color: {COLORS['bg_primary']};
            box-shadow: 0 0 20px rgba(0, 251, 255, 0.4);
        }}
        
        /* Botones destrucción */
        button[kind="danger"] {{
            background: transparent;
            color: {COLORS['priority_high']};
            border: 2px solid {COLORS['priority_high']};
            padding: 10px 24px;
            border-radius: 10px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Inter', sans-serif;
        }}
        
        button[kind="danger"]:hover {{
            background: {COLORS['priority_high']};
            color: white;
            box-shadow: 0 0 20px rgba(255, 59, 92, 0.4);
        }}
        
        /* ============================================================
           4. INPUTS Y SELECTORES MODERNOS
           ============================================================ */
        
        input, textarea, select {{
            background: {COLORS['bg_secondary']};
            color: {COLORS['text_primary']};
            border: 2px solid {COLORS['accent_cyan']};
            border-radius: 10px;
            padding: 12px 16px;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            transition: all 0.3s ease;
            backdrop-filter: blur(10px);
        }}
        
        input:focus, textarea:focus, select:focus {{
            outline: none;
            border-color: {COLORS['accent_purple']};
            box-shadow: 0 0 20px rgba(138, 43, 226, 0.3);
            background: {COLORS['bg_tertiary']};
        }}
        
        input::placeholder {{
            color: {COLORS['text_muted']};
        }}
        
        /* ============================================================
           5. CONTENEDORES GLASSMORPHISM
           ============================================================ */
        
        [data-testid="stVerticalBlock"] > [style*="display: block"] {{
            background: rgba(20, 24, 41, 0.4);
            backdrop-filter: blur(20px);
            border-radius: 16px;
            border: 1px solid rgba(0, 251, 255, 0.1);
            padding: 2rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }}
        
        [data-testid="stVerticalBlock"] > [style*="display: block"]:hover {{
            border-color: rgba(0, 251, 255, 0.3);
            box-shadow: 0 8px 32px rgba(0, 251, 255, 0.1);
        }}
        
        /* Expanders */
        [data-testid="stExpander"] {{
            background: rgba(20, 24, 41, 0.6) !important;
            border: 1px solid rgba(0, 251, 255, 0.2) !important;
            border-radius: 12px !important;
        }}
        
        /* Expandable content */
        [data-testid="stExpander"] > div {{
            background: transparent !important;
        }}
        
        /* ============================================================
           6. TARJETAS PARA OPORTUNIDADES
           ============================================================ */
        
        .opportunity-card {{
            background: rgba(26, 31, 58, 0.6);
            backdrop-filter: blur(15px);
            border-radius: 14px;
            padding: 20px;
            margin: 12px 0;
            border-left: 4px solid;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        }}
        
        .opportunity-card:hover {{
            transform: translateX(4px);
            box-shadow: 0 12px 48px rgba(0, 251, 255, 0.15);
        }}
        
        /* Prioridad High */
        .opportunity-high {{
            border-left-color: {COLORS['priority_high']};
            box-shadow: inset 0 0 20px rgba(255, 59, 92, 0.05);
        }}
        
        .opportunity-high:hover {{
            box-shadow: 0 12px 48px rgba(255, 59, 92, 0.2),
                        inset 0 0 20px rgba(255, 59, 92, 0.05);
            border-left-color: {COLORS['priority_high']};
        }}
        
        /* Prioridad Medium */
        .opportunity-medium {{
            border-left-color: {COLORS['priority_medium']};
            box-shadow: inset 0 0 20px rgba(255, 183, 0, 0.05);
        }}
        
        .opportunity-medium:hover {{
            box-shadow: 0 12px 48px rgba(255, 183, 0, 0.2),
                        inset 0 0 20px rgba(255, 183, 0, 0.05);
            border-left-color: {COLORS['priority_medium']};
        }}
        
        /* Prioridad Low */
        .opportunity-low {{
            border-left-color: {COLORS['priority_low']};
            box-shadow: inset 0 0 20px rgba(0, 204, 136, 0.05);
        }}
        
        .opportunity-low:hover {{
            box-shadow: 0 12px 48px rgba(0, 204, 136, 0.2),
                        inset 0 0 20px rgba(0, 204, 136, 0.05);
            border-left-color: {COLORS['priority_low']};
        }}
        
        /* ============================================================
           7. BADGES Y ETIQUETAS
           ============================================================ */
        
        .badge {{
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 600;
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.3px;
            margin-right: 8px;
            margin-bottom: 8px;
            backdrop-filter: blur(10px);
        }}
        
        .badge-status-new {{
            background: rgba(0, 251, 255, 0.15);
            color: {COLORS['status_new']};
            border: 1px solid {COLORS['status_new']};
        }}
        
        .badge-status-progress {{
            background: rgba(255, 183, 0, 0.15);
            color: {COLORS['status_progress']};
            border: 1px solid {COLORS['status_progress']};
        }}
        
        .badge-status-closed {{
            background: rgba(0, 204, 136, 0.15);
            color: {COLORS['status_closed']};
            border: 1px solid {COLORS['status_closed']};
        }}
        
        .badge-status-won {{
            background: rgba(138, 43, 226, 0.15);
            color: {COLORS['status_won']};
            border: 1px solid {COLORS['status_won']};
        }}
        
        .badge-priority-high {{
            background: rgba(255, 59, 92, 0.15);
            color: {COLORS['priority_high']};
            border: 1px solid {COLORS['priority_high']};
        }}
        
        .badge-priority-medium {{
            background: rgba(255, 183, 0, 0.15);
            color: {COLORS['priority_medium']};
            border: 1px solid {COLORS['priority_medium']};
        }}
        
        .badge-priority-low {{
            background: rgba(0, 204, 136, 0.15);
            color: {COLORS['priority_low']};
            border: 1px solid {COLORS['priority_low']};
        }}
        
        /* ============================================================
           8. ELEMENTOS DE ESTADO Y INFORMACIÓN
           ============================================================ */
        
        [data-testid="stAlert"] {{
            background: rgba(26, 31, 58, 0.8);
            border-radius: 12px;
            border: 1px solid;
            backdrop-filter: blur(15px);
            padding: 16px;
        }}
        
        [data-testid="stAlert"][data-alert-type="success"] {{
            border-color: {COLORS['priority_low']};
            background: rgba(0, 204, 136, 0.1);
        }}
        
        [data-testid="stAlert"][data-alert-type="error"] {{
            border-color: {COLORS['priority_high']};
            background: rgba(255, 59, 92, 0.1);
        }}
        
        [data-testid="stAlert"][data-alert-type="warning"] {{
            border-color: {COLORS['priority_medium']};
            background: rgba(255, 183, 0, 0.1);
        }}
        
        [data-testid="stAlert"][data-alert-type="info"] {{
            border-color: {COLORS['accent_cyan']};
            background: rgba(0, 251, 255, 0.1);
        }}
        
        /* ============================================================
           9. TABLAS Y DATAFRAMES
           ============================================================ */
        
        [data-testid="stDataFrame"] {{
            background: transparent !important;
        }}
        
        [data-testid="stDataFrame"] table {{
            background: rgba(20, 24, 41, 0.4) !important;
            border-collapse: collapse;
        }}
        
        [data-testid="stDataFrame"] th {{
            background: rgba(0, 251, 255, 0.1) !important;
            color: {COLORS['accent_cyan']} !important;
            border-bottom: 2px solid {COLORS['accent_cyan']} !important;
            font-weight: 600;
            padding: 12px !important;
        }}
        
        [data-testid="stDataFrame"] td {{
            border-bottom: 1px solid rgba(0, 251, 255, 0.1) !important;
            color: {COLORS['text_secondary']} !important;
            padding: 12px !important;
        }}
        
        [data-testid="stDataFrame"] tr:hover {{
            background: rgba(0, 251, 255, 0.05) !important;
        }}
        
        /* ============================================================
           10. SELECTBOX Y MULTISELECT
           ============================================================ */
        
        [data-testid="stSelectbox"], [data-testid="stMultiSelect"] {{
            background: {COLORS['bg_secondary']};
        }}
        
        [data-testid="stSelectbox"] > div > div {{
            background: {COLORS['bg_secondary']};
            border: 2px solid {COLORS['accent_cyan']};
            border-radius: 10px;
            color: {COLORS['text_primary']};
        }}
        
        /* ============================================================
           11. SIDEBAR
           ============================================================ */
        
        [data-testid="stSidebar"] {{
            background: {COLORS['bg_primary']};
            border-right: 1px solid rgba(0, 251, 255, 0.2);
        }}
        
        [data-testid="stSidebar"] > div {{
            padding: 20px;
        }}
        
        /* ============================================================
           12. DIVIDERS Y SEPARADORES
           ============================================================ */
        
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, 
                transparent, 
                {COLORS['accent_cyan']}33,
                transparent);
            margin: 20px 0;
        }}
        
        /* ============================================================
           13. SCROLLBAR MODERNO
           ============================================================ */
        
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: {COLORS['bg_secondary']};
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: {COLORS['accent_cyan']};
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: {COLORS['accent_purple']};
        }}
        
        /* ============================================================
           14. ANIMACIONES
           ============================================================ */
        
        @keyframes glow {{
            0%, 100% {{
                box-shadow: 0 0 10px rgba(0, 251, 255, 0.3);
            }}
            50% {{
                box-shadow: 0 0 20px rgba(0, 251, 255, 0.6);
            }}
        }}
        
        @keyframes slideInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; }}
            to {{ opacity: 1; }}
        }}
        
        .glow {{
            animation: glow 2s ease-in-out infinite;
        }}
        
        .slide-in {{
            animation: slideInUp 0.5s ease-out;
        }}
        
        /* ============================================================
           15. RESPONSIVE DESIGN
           ============================================================ */
        
        @media (max-width: 768px) {{
            h1 {{ font-size: 1.875rem; }}
            h2 {{ font-size: 1.5rem; }}
            h3 {{ font-size: 1.25rem; }}
            
            [data-testid="stVerticalBlock"] > [style*="display: block"] {{
                padding: 1.25rem;
            }}
            
            .opportunity-card {{
                padding: 16px;
            }}
            
            button {{
                padding: 10px 20px;
                font-size: 0.85rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            h1 {{ font-size: 1.5rem; }}
            h2 {{ font-size: 1.25rem; }}
            
            [data-testid="stVerticalBlock"] > [style*="display: block"] {{
                padding: 1rem;
            }}
        }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# COMPONENTES REUTILIZABLES
# ============================================================================

def card_container(content, priority: Literal["High", "Medium", "Low"] = "Medium"):
    """
    Crea una tarjeta glassmorphism con borde de color según prioridad
    """
    priority_map = {
        "High": "opportunity-high",
        "Medium": "opportunity-medium",
        "Low": "opportunity-low"
    }
    
    html = f"""
    <div class="opportunity-card {priority_map.get(priority, 'opportunity-medium')}">
        {content}
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def badge(text: str, badge_type: str = "info"):
    """
    Crea un badge/etiqueta con estilo moderno
    
    badge_type: 'status-new', 'status-progress', 'status-closed', 'status-won',
                'priority-high', 'priority-medium', 'priority-low'
    """
    st.markdown(
        f'<span class="badge badge-{badge_type}">{text}</span>',
        unsafe_allow_html=True
    )


def glow_button(label: str, key: str = None, on_click=None, args=(), kwargs=None):
    """
    Botón con efecto glow para acciones principales
    """
    if kwargs is None:
        kwargs = {}
    
    return st.button(
        label,
        key=key,
        on_click=on_click,
        args=args,
        kwargs=kwargs,
        use_container_width=False
    )


def section_header(title: str, subtitle: str = ""):
    """
    Encabezado de sección con estilo moderno
    """
    html = f"""
    <div style="margin: 2rem 0 1.5rem 0;">
        <h2 style="margin: 0; padding-bottom: 0.5rem; border-bottom: 2px solid rgba(0, 251, 255, 0.3);">
            {title}
        </h2>
    """
    
    if subtitle:
        html += f'<p style="color: {COLORS["text_secondary"]}; margin-top: 0.5rem; font-size: 0.95rem;">{subtitle}</p>'
    
    html += "</div>"
    
    st.markdown(html, unsafe_allow_html=True)


def stat_card(label: str, value: str, icon: str = "📊", color: str = "cyan"):
    """
    Tarjeta para mostrar estadísticas
    """
    color_map = {
        "cyan": COLORS["accent_cyan"],
        "purple": COLORS["accent_purple"],
        "high": COLORS["priority_high"],
        "medium": COLORS["priority_medium"],
        "low": COLORS["priority_low"]
    }
    
    chosen_color = color_map.get(color, COLORS["accent_cyan"])
    
    html = f"""
    <div style="
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 12px;
        border: 1px solid rgba(0, 251, 255, 0.2);
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    ">
        <div style="font-size: 2.5rem; margin-bottom: 10px;">{icon}</div>
        <div style="
            font-size: 2rem;
            font-weight: 700;
            color: {chosen_color};
            margin-bottom: 8px;
        ">{value}</div>
        <div style="
            font-size: 0.9rem;
            color: {COLORS['text_secondary']};
            font-weight: 500;
        ">{label}</div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def opportunity_card_modern(
    ticket_number: int,
    title: str,
    description: str,
    status: str,
    priority: str,
    notes: str,
    created_at: str
):
    """
    Tarjeta moderna para mostrar oportunidades
    """
    status_colors = {
        "new": ("status-new", COLORS["status_new"]),
        "in_progress": ("status-progress", COLORS["status_progress"]),
        "closed": ("status-closed", COLORS["status_closed"]),
        "won": ("status-won", COLORS["status_won"])
    }
    
    priority_colors = {
        "High": ("priority-high", COLORS["priority_high"]),
        "Medium": ("priority-medium", COLORS["priority_medium"]),
        "Low": ("priority-low", COLORS["priority_low"])
    }
    
    status_badge = status_colors.get(status, ("status-new", COLORS["status_new"]))
    priority_badge = priority_colors.get(priority, ("priority-medium", COLORS["priority_medium"]))
    
    html = f"""
    <div class="opportunity-card opportunity-{priority.lower()}">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 12px;">
            <div>
                <h4 style="margin: 0; color: {COLORS['text_primary']}; font-size: 1.1rem;">
                    #{ticket_number} - {title}
                </h4>
            </div>
            <span class="badge badge-{status_badge[0]}" style="margin: 0;">{status.replace('_', ' ').title()}</span>
        </div>
        
        <p style="color: {COLORS['text_secondary']}; margin: 12px 0; line-height: 1.6;">
            {description}
        </p>
        
        {f'<p style="color: {COLORS["text_secondary"]}; font-style: italic; margin: 12px 0; padding: 12px; background: rgba(0, 251, 255, 0.05); border-radius: 8px;"><strong>Notas:</strong> {notes}</p>' if notes else ''}
        
        <div style="display: flex; gap: 12px; margin-top: 12px; flex-wrap: wrap;">
            <span class="badge badge-{priority_badge[0]}">Priority: {priority}</span>
            <span style="
                display: inline-block;
                padding: 4px 8px;
                border-radius: 6px;
                font-size: 0.75rem;
                color: {COLORS['text_muted']};
                background: transparent;
            ">{created_at}</span>
        </div>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def audio_player_modern(file_path: str, file_name: str):
    """
    Reproductor de audio con estilo moderno
    """
    html = f"""
    <div style="
        background: rgba(26, 31, 58, 0.6);
        backdrop-filter: blur(15px);
        border-radius: 12px;
        padding: 16px;
        border: 1px solid rgba(0, 251, 255, 0.2);
        margin: 12px 0;
    ">
        <p style="color: {COLORS['accent_cyan']}; margin-bottom: 12px; font-weight: 600;">
            🎵 {file_name}
        </p>
        <audio controls style="
            width: 100%;
            accent-color: {COLORS['accent_cyan']};
        ">
            <source src="{file_path}" type="audio/wav">
            Tu navegador no soporta el elemento de audio.
        </audio>
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def loading_spinner(text: str = "Procesando..."):
    """
    Spinner de loading con efecto glow
    """
    html = f"""
    <div style="text-align: center; padding: 2rem;">
        <div style="
            display: inline-block;
            width: 40px;
            height: 40px;
            border: 3px solid rgba(0, 251, 255, 0.3);
            border-top-color: {COLORS['accent_cyan']};
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
        "></div>
        <p style="
            color: {COLORS['text_secondary']};
            margin-top: 12px;
            font-weight: 500;
        ">{text}</p>
    </div>
    <style>
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
    </style>
    """
    
    st.markdown(html, unsafe_allow_html=True)


def gradient_text(text: str, colors: list = None):
    """
    Texto con gradiente de colores
    """
    if colors is None:
        colors = [COLORS["accent_cyan"], COLORS["accent_purple"]]
    
    gradient = ", ".join(colors)
    
    html = f"""
    <span style="
        background: linear-gradient(135deg, {gradient});
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    ">{text}</span>
    """
    
    st.markdown(html, unsafe_allow_html=True)


# ============================================================================
# UTILIDADES DE LAYOUT
# ============================================================================

def create_metric_row(metrics: dict, cols: int = 4):
    """
    Crea una fila de métricas con tarjetas
    
    metrics: {
        'label': 'value',
        'Grabaciones': '42',
        ...
    }
    """
    columns = st.columns(cols)
    
    for idx, (label, value) in enumerate(metrics.items()):
        with columns[idx % cols]:
            stat_card(label, str(value), icon="📊")


def sidebar_menu():
    """
    Menú lateral moderno
    """
    with st.sidebar:
        st.markdown(f"""
        <h1 style="color: {COLORS['accent_cyan']}; text-align: center; margin-bottom: 2rem;">
            🎙️ AudioPro <br>
            <span style="font-size: 0.6em; color: {COLORS['text_muted']};">Intelligence</span>
        </h1>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Menú items
        menu_items = {
            "🏠 Dashboard": "dashboard",
            "🎵 Grabaciones": "recordings",
            "📋 Oportunidades": "opportunities",
            "💬 Chat IA": "chat",
            "⚙️ Configuración": "settings",
        }
        
        for label, page in menu_items.items():
            if st.button(label, use_container_width=True, key=f"menu_{page}"):
                st.session_state.current_page = page
        
        st.divider()
        
        # Footer sidebar
        st.markdown(f"""
        <div style="
            margin-top: auto;
            padding-top: 20px;
            border-top: 1px solid rgba(0, 251, 255, 0.2);
            text-align: center;
            color: {COLORS['text_muted']};
            font-size: 0.85rem;
        ">
            <p>v1.0.0 | 2026</p>
            <p>Powered by AI 🚀</p>
        </div>
        """, unsafe_allow_html=True)


# Ejecutar al importar
if __name__ == "__main__":
    # Test visual
    inject_modern_css()
    
    st.title("🎨 Modern UI Components Test")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        stat_card("Total Audios", "42", "🎵", "cyan")
    with col2:
        stat_card("Tickets", "128", "📋", "purple")
    with col3:
        stat_card("En Progreso", "15", "⏱️", "medium")
    with col4:
        stat_card("Completados", "113", "✅", "low")
    
    st.divider()
    
    section_header("Oportunidades Recientes", "Las 5 últimas oportunidades generadas")
    
    opportunity_card_modern(
        ticket_number=1,
        title="Presupuesto",
        description="El cliente mencionó necesidad de presupuesto para proyecto trimestral. Contexto completo disponible.",
        status="new",
        priority="High",
        notes="Cliente VIP - Seguimiento prioritario necesario",
        created_at="2026-02-06 14:30"
    )
