"""
Estilos CSS modernos estilo Salesforce/Holded
Diseño limpio, minimalista y profesional con soporte para tema claro/oscuro
"""

def get_styles(theme="dark"):
    """Retorna CSS con soporte para tema claro y oscuro"""
    
    # Definir paletas por tema
    if theme == "light":
        colors = {
            "bg_primary": "#FFFFFF",
            "bg_secondary": "#F8F9FA",
            "text_primary": "#171717",
            "text_secondary": "#6B7280",
            "border": "#E5E7EB",
            "input_bg": "#F3F4F6",
            "input_text": "#171717",
            "chat_ai_bg": "#E3F2FD",
            "chat_ai_text": "#171717",
            "notification_success_bg": "#E8F5E9",
            "notification_error_bg": "#FFEBEE",
            "notification_info_bg": "#E3F2FD",
        }
    else:  # dark theme por defecto
        colors = {
            "bg_primary": "#1E1E1E",
            "bg_secondary": "#2D2D2D",
            "text_primary": "#FFFFFF",
            "text_secondary": "#B4B4B4",
            "border": "#404040",
            "input_bg": "#2D2D2D",
            "input_text": "#FFFFFF",
            "chat_ai_bg": "#2D2D2D",
            "chat_ai_text": "#E5E7EB",
            "notification_success_bg": "#1B5E20",
            "notification_error_bg": "#5D0000",
            "notification_info_bg": "#0D47A1",
        }
    
    css = f"""
    <style>
    :root {{
        --primary: #0052CC;
        --primary-light: #0078D4;
        --success: #09A741;
        --danger: #EA001B;
        --warning: #FFA500;
        --bg-primary: {colors['bg_primary']};
        --bg-secondary: {colors['bg_secondary']};
        --text-primary: {colors['text_primary']};
        --text-secondary: {colors['text_secondary']};
        --border-color: {colors['border']};
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
    }}

    .main {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px 40px;
        background: {colors['bg_primary']};
        color: {colors['text_primary']};
    }}
    
    .stMainBlockContainer {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
        background: {colors['bg_primary']};
        color: {colors['text_primary']};
    }}
    
    [data-testid="stAppViewContainer"] {{
        padding: 0;
        background: {colors['bg_secondary']};
    }}
    
    [data-testid="stAppViewContainer"] > section {{
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 40px;
        background: {colors['bg_primary']};
        color: {colors['text_primary']};
    }}
    
    input, textarea {{
        background-color: {colors['input_bg']} !important;
        color: {colors['input_text']} !important;
        border-color: {colors['border']} !important;
    }}

    @keyframes fade-in {{
        from {{ opacity: 0; }}
        to {{ opacity: 1; }}
    }}

    @keyframes slide-in-up {{
        from {{ opacity: 0; transform: translateY(4px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}

    .badge {{
        display: inline-block;
        padding: 6px 12px;
        border-radius: 4px;
        color: white;
        font-weight: 600;
        font-size: 13px;
        margin-right: 8px;
        animation: fade-in 0.3s ease-out;
    }}

    .badge-recording {{ background: #EA001B; }}
    .badge-upload {{ background: #0078D4; }}
    .badge-saved {{ background: #09A741; }}

    .notification-icon {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 40px;
        height: 40px;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.2s ease;
        margin: 5px 0;
        position: relative;
    }}

    .notification-icon:hover {{ transform: scale(1.05); }}

    .notification-icon-success {{
        background: {colors['notification_success_bg']};
        border: 1px solid #09A741;
        color: #09A741;
    }}

    .notification-icon-error {{
        background: {colors['notification_error_bg']};
        border: 1px solid #EA001B;
        color: #EA001B;
    }}

    .notification-icon-info {{
        background: {colors['notification_info_bg']};
        border: 1px solid #0052CC;
        color: #0052CC;
    }}

    .notification-expanded {{
        animation: slide-in-up 0.3s ease-out;
        margin: 10px 0;
        border-radius: 4px;
        padding: 12px 16px;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
        border-left: 3px solid;
    }}

    .notification-expanded-success {{
        background: {colors['notification_success_bg']};
        border-left-color: #09A741;
        color: #09A741;
    }}

    .notification-expanded-error {{
        background: {colors['notification_error_bg']};
        border-left-color: #EA001B;
        color: #EA001B;
    }}

    .notification-expanded-info {{
        background: {colors['notification_info_bg']};
        border-left-color: #0052CC;
        color: #0052CC;
    }}

    .chat-container {{
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding: 20px 0;
    }}

    .chat-message {{
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
        animation: slide-in-up 0.3s ease-out;
    }}

    .chat-message-user {{ justify-content: flex-end; }}
    .chat-message-ai {{ justify-content: flex-start; }}

    .chat-bubble {{
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 8px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 14px;
        box-shadow: var(--shadow-sm);
    }}

    .chat-bubble-user {{
        background: #0052CC;
        color: white;
        border-radius: 12px 12px 2px 12px;
    }}

    .chat-bubble-ai {{
        background: {colors['chat_ai_bg']};
        color: {colors['chat_ai_text']};
        border-radius: 12px 12px 12px 2px;
    }}

    .chat-avatar {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
        margin-top: 4px;
        box-shadow: var(--shadow-sm);
    }}

    .chat-avatar-user {{ background: #0052CC; color: white; }}
    .chat-avatar-ai {{
        background: {colors['bg_secondary']};
        color: {colors['text_secondary']};
        border: 1px solid {colors['border']};
    }}
    </style>
    """
    
    return css
