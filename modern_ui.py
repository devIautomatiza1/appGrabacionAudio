import streamlit as st

# ============================================================================
# SISTEMA DE DISEÑO MODERNO - AudioPro Intelligence
# Colores: Deep Navy (#0A0E27), Cian (#00FBFF), Violeta (#8A2BE2)
# ============================================================================

COLORS = {
    "navy": "#0A0E27",
    "cian": "#00FBFF",
    "violeta": "#8A2BE2",
    "dark_bg": "#0F1419",
    "card_bg": "rgba(15, 20, 25, 0.6)",
    "red": "#FF3B5C",
    "yellow": "#FFB700",
    "green": "#00CC88",
    "gray": "#B0B8C1"
}


def inject_modern_css():
    """
    Inyecta todo el CSS moderno de la aplicación.
    Debe ser llamado PRIMERO en index.py, antes de cualquier elemento Streamlit.
    """
    css = f"""
    <style>
        /* ===== VARIABLES GLOBALES ===== */
        :root {{
            --navy: {COLORS['navy']};
            --cian: {COLORS['cian']};
            --violeta: {COLORS['violeta']};
            --dark-bg: {COLORS['dark_bg']};
            --card-bg: {COLORS['card_bg']};
            --red: {COLORS['red']};
            --yellow: {COLORS['yellow']};
            --green: {COLORS['green']};
            --gray: {COLORS['gray']};
        }}

        /* ===== FONDO GENERAL ===== */
        .stApp {{
            background: linear-gradient(135deg, {COLORS['navy']} 0%, #1a1f3a 100%);
            color: white;
        }}
        
        /* ===== TEXTO Y TIPOGRAFÍA ===== */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Inter+Tight:wght@700;800&display=swap');
        
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, {COLORS['navy']} 0%, #1a1f3a 100%);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter Tight', sans-serif;
            letter-spacing: -0.5px;
            font-weight: 700;
        }}

        /* ===== DIVIDERS ===== */
        hr {{
            border: none;
            height: 1px;
            background: linear-gradient(90deg, transparent, {COLORS['cian']}, transparent);
            margin: 1.5rem 0;
            opacity: 0.3;
        }}

        /* ===== NOTIFICACIONES TOAST MODERNAS ===== */
        [data-testid="stNotification"] {{
            position: fixed;
            top: 20px;
            right: 20px;
            z-index: 9999;
            padding: 16px 24px;
            border-radius: 12px;
            backdrop-filter: blur(20px);
            box-shadow: 0 20px 60px rgba(0, 251, 255, 0.2);
            border: 1px solid rgba(0, 251, 255, 0.3);
            animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
            font-weight: 500;
        }}

        @keyframes slideInRight {{
            from {{
                transform: translateX(400px);
                opacity: 0;
            }}
            to {{
                transform: translateX(0);
                opacity: 1;
            }}
        }}

        /* ===== BOTONES ===== */
        .stButton > button {{
            background: linear-gradient(135deg, {COLORS['cian']}, {COLORS['violeta']});
            color: {COLORS['navy']};
            border: none;
            border-radius: 8px;
            padding: 10px 24px;
            font-weight: 600;
            font-size: 0.95rem;
            transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
            box-shadow: 0 0 20px rgba(0, 251, 255, 0.3);
            cursor: pointer;
        }}

        .stButton > button:hover {{
            box-shadow: 0 0 30px rgba(0, 251, 255, 0.6);
            transform: translateY(-2px);
        }}

        .stButton > button:active {{
            transform: translateY(0);
        }}

        /* ===== INPUTS ===== */
        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select {{
            background: {COLORS['card_bg']} !important;
            border: 1px solid rgba(0, 251, 255, 0.2) !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-family: 'Inter', sans-serif !important;
            transition: all 0.3s ease !important;
        }}

        .stTextInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus,
        .stSelectbox > div > div > select:focus {{
            border-color: {COLORS['cian']} !important;
            box-shadow: 0 0 15px rgba(0, 251, 255, 0.3) !important;
            background: rgba(15, 20, 25, 0.8) !important;
        }}

        /* ===== CONTENEDORES ===== */
        [data-testid="element-container"] > div > div {{
            animation: fadeIn 0.5s ease-in;
        }}

        @keyframes fadeIn {{
            from {{
                opacity: 0;
                transform: translateY(10px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}

        /* ===== EXPANDERS ===== */
        .streamlit-expanderHeader {{
            background: {COLORS['card_bg']} !important;
            border: 1px solid rgba(0, 251, 255, 0.2) !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
        }}

        .streamlit-expanderHeader:hover {{
            background: rgba(0, 251, 255, 0.05) !important;
            border-color: {COLORS['cian']} !important;
        }}

        /* ===== TABS ===== */
        [data-baseweb="tab-list"] {{
            border-bottom: 1px solid rgba(0, 251, 255, 0.1) !important;
        }}

        [data-baseweb="tab"] {{
            color: {COLORS['gray']} !important;
            font-weight: 500 !important;
        }}

        [data-baseweb="tab"][aria-selected="true"] {{
            color: {COLORS['cian']} !important;
            border-bottom: 2px solid {COLORS['cian']} !important;
        }}

        /* ===== CARDS Y CONTENEDORES CON BORDE ===== */
        [data-testid="element-container"] > div[data-testid="stContainer"] {{
            background: {COLORS['card_bg']};
            border: 1px solid rgba(0, 251, 255, 0.2);
            border-radius: 12px;
            padding: 20px;
            backdrop-filter: blur(15px);
            transition: all 0.3s ease;
        }}

        [data-testid="element-container"] > div[data-testid="stContainer"]:hover {{
            border-color: {COLORS['cian']};
            box-shadow: 0 0 20px rgba(0, 251, 255, 0.2);
        }}

        /* ===== SCROLLBAR ===== */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: {COLORS['card_bg']};
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb {{
            background: linear-gradient(180deg, {COLORS['cian']}, {COLORS['violeta']});
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: linear-gradient(180deg, {COLORS['violeta']}, {COLORS['cian']});
        }}

        /* ===== GLOW ANIMATIONS ===== */
        @keyframes glow {{
            0%, 100% {{
                box-shadow: 0 0 5px {COLORS['cian']}, 0 0 10px {COLORS['violeta']};
            }}
            50% {{
                box-shadow: 0 0 15px {COLORS['cian']}, 0 0 25px {COLORS['violeta']};
            }}
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ============================================================================
# NOTIFICACIONES TOAST MODERNAS
# ============================================================================

def success_toast(message: str):
    """
    Muestra un mensaje de éxito tipo toast en la esquina superior derecha.
    """
    toast_html = f"""
    <div style="
        position: fixed;
        top: 15px;
        right: 15px;
        background: rgba(0, 204, 136, 0.15);
        border: 1px solid #00CC88;
        border-radius: 10px;
        padding: 14px 20px;
        color: #00CC88;
        font-weight: 600;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 204, 136, 0.2);
        font-family: 'Inter', sans-serif;
        z-index: 9999;
        animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 1.2rem;">✅</span>
        <span>{message}</span>
    </div>
    """
    st.markdown(toast_html, unsafe_allow_html=True)


def error_toast(message: str):
    """
    Muestra un mensaje de error tipo toast en la esquina superior derecha.
    """
    toast_html = f"""
    <div style="
        position: fixed;
        top: 15px;
        right: 15px;
        background: rgba(255, 59, 92, 0.15);
        border: 1px solid #FF3B5C;
        border-radius: 10px;
        padding: 14px 20px;
        color: #FF3B5C;
        font-weight: 600;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(255, 59, 92, 0.2);
        font-family: 'Inter', sans-serif;
        z-index: 9999;
        animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 1.2rem;">❌</span>
        <span>{message}</span>
    </div>
    """
    st.markdown(toast_html, unsafe_allow_html=True)


def warning_toast(message: str):
    """
    Muestra un mensaje de advertencia tipo toast en la esquina superior derecha.
    """
    toast_html = f"""
    <div style="
        position: fixed;
        top: 15px;
        right: 15px;
        background: rgba(255, 183, 0, 0.15);
        border: 1px solid #FFB700;
        border-radius: 10px;
        padding: 14px 20px;
        color: #FFB700;
        font-weight: 600;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(255, 183, 0, 0.2);
        font-family: 'Inter', sans-serif;
        z-index: 9999;
        animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 1.2rem;">⚠️</span>
        <span>{message}</span>
    </div>
    """
    st.markdown(toast_html, unsafe_allow_html=True)


def info_toast(message: str):
    """
    Muestra un mensaje informativo tipo toast en la esquina superior derecha.
    """
    toast_html = f"""
    <div style="
        position: fixed;
        top: 15px;
        right: 15px;
        background: rgba(0, 251, 255, 0.15);
        border: 1px solid #00FBFF;
        border-radius: 10px;
        padding: 14px 20px;
        color: #00FBFF;
        font-weight: 600;
        backdrop-filter: blur(20px);
        box-shadow: 0 8px 32px rgba(0, 251, 255, 0.2);
        font-family: 'Inter', sans-serif;
        z-index: 9999;
        animation: slideInRight 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
        display: flex;
        align-items: center;
        gap: 10px;
    ">
        <span style="font-size: 1.2rem;">ℹ️</span>
        <span>{message}</span>
    </div>
    """
    st.markdown(toast_html, unsafe_allow_html=True)


# ============================================================================
# COMPONENTES REUTILIZABLES
# ============================================================================

def section_header(title: str, subtitle: str = ""):
    """
    Crea un encabezado de sección modernizado.
    """
    st.markdown(f"""
    <div style="
        margin: 2rem 0 1.5rem 0;
        padding-bottom: 1rem;
        border-bottom: 2px solid rgba(0, 251, 255, 0.3);
    ">
        <h2 style="
            margin: 0 0 0.5rem 0;
            font-size: 1.8rem;
            background: linear-gradient(135deg, #00FBFF, #8A2BE2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">{title}</h2>
        {f'<p style="margin: 0; color: #B0B8C1; font-size: 0.95rem;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def stat_card(label: str, value: str, icon: str = "", color: str = "cyan"):
    """
    Crea una tarjeta de estadística modernizada.
    """
    color_map = {
        "cyan": "#00FBFF",
        "purple": "#8A2BE2",
        "red": "#FF3B5C",
        "yellow": "#FFB700",
        "green": "#00CC88",
        "low": "#B0B8C1"
    }
    
    color_value = color_map.get(color, color)
    
    st.markdown(f"""
    <div style="
        background: rgba(15, 20, 25, 0.6);
        border: 1px solid rgba(0, 251, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    ">
        <div style="font-size: 1.8rem; margin-bottom: 0.5rem;">{icon}</div>
        <div style="color: #B0B8C1; font-size: 0.85rem; margin-bottom: 0.5rem;">{label}</div>
        <div style="
            font-size: 2.5rem;
            font-weight: 700;
            color: {color_value};
            font-family: 'Inter Tight', sans-serif;
        ">{value}</div>
    </div>
    """, unsafe_allow_html=True)


def create_metric_row(metrics: dict, cols: int = 3):
    """
    Crea una fila de métricas en columnas.
    """
    columns = st.columns(cols)
    metrics_list = list(metrics.items())
    
    for idx, col in enumerate(columns):
        if idx < len(metrics_list):
            label, value = metrics_list[idx]
            with col:
                stat_card(label, value)


def badge(text: str, badge_type: str = "status-new"):
    """
    Crea una etiqueta/badge moderno.
    """
    color_map = {
        "status-new": ("#00FBFF", "rgba(0, 251, 255, 0.15)"),
        "status-progress": ("#FFB700", "rgba(255, 183, 0, 0.15)"),
        "status-closed": ("#00CC88", "rgba(0, 204, 136, 0.15)"),
        "priority-high": ("#FF3B5C", "rgba(255, 59, 92, 0.15)"),
        "priority-medium": ("#FFB700", "rgba(255, 183, 0, 0.15)"),
        "priority-low": ("#00CC88", "rgba(0, 204, 136, 0.15)"),
    }
    
    color, bg = color_map.get(badge_type, ("#00FBFF", "rgba(0, 251, 255, 0.15)"))
    
    st.markdown(f"""
    <span style="
        background: {bg};
        border: 1px solid {color};
        color: {color};
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
        margin: 0.25rem 0.25rem 0.25rem 0;
    ">{text}</span>
    """, unsafe_allow_html=True)


def opportunity_card_modern(ticket_number: int, title: str, description: str, status: str = "new", 
                           priority: str = "Medium", notes: str = "", created_at: str = ""):
    """
    Crea una tarjeta moderna para oportunidades de negocio.
    """
    status_colors = {
        "new": ("#00FBFF", "🆕"),
        "in_progress": ("#FFB700", "⏳"),
        "closed": ("#00CC88", "✅"),
        "won": ("#8A2BE2", "🏆")
    }
    
    priority_colors = {
        "Low": "#00CC88",
        "Medium": "#FFB700",
        "High": "#FF3B5C"
    }
    
    status_color, status_icon = status_colors.get(status, ("#00FBFF", "ℹ️"))
    priority_color = priority_colors.get(priority, "#000")
    
    st.markdown(f"""
    <div style="
        background: rgba(15, 20, 25, 0.6);
        border-left: 4px solid {status_color};
        border: 1px solid rgba(0, 251, 255, 0.2);
        border-left: 4px solid {status_color};
        border-radius: 12px;
        padding: 20px;
        margin: 1rem 0;
        backdrop-filter: blur(15px);
        transition: all 0.3s ease;
    ">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <div>
                <div style="
                    font-size: 1.5rem;
                    font-weight: 700;
                    color: {status_color};
                    margin-bottom: 0.5rem;
                ">#{ticket_number} {status_icon} {title}</div>
                <div style="color: #B0B8C1; font-size: 0.85rem;">📅 {created_at}</div>
            </div>
            <div style="
                background: {priority_colors.get(priority, '#000')};
                color: {COLORS['navy']};
                padding: 6px 12px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 0.85rem;
            ">{priority}</div>
        </div>
        
        <div style="
            background: rgba(0, 251, 255, 0.05);
            border: 1px solid rgba(0, 251, 255, 0.2);
            border-radius: 8px;
            padding: 12px;
            margin: 1rem 0;
            color: #B0B8C1;
            font-size: 0.95rem;
        ">{description}</div>
    </div>
    """, unsafe_allow_html=True)
