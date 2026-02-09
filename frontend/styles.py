"""
Estilos CSS modernos estilo Salesforce/Holded
Diseño limpio, minimalista y profesional
"""

def get_styles():
    """Retorna todos los estilos CSS de la aplicación"""
    return """
    <style>
    /* Paleta de colores Salesforce/Holded */
    :root {
        --primary: #0052CC;
        --primary-light: #0078D4;
        --success: #09A741;
        --danger: #EA001B;
        --warning: #FFA500;
        --info: #0052CC;
        --bg-light: #F3F3F3;
        --bg-white: #FFFFFF;
        --text-dark: #171717;
        --text-secondary: #8E92A9;
        --border-color: #DCDCDC;
        --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.08);
        --shadow-md: 0 2px 8px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 4px 16px rgba(0, 0, 0, 0.12);
    }

    /* Contenedor principal centrado */
    .main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px 40px;
        background: #FFFFFF;
    }
    
    .stMainBlockContainer {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0;
        background: #F3F3F3;
    }
    
    [data-testid="stAppViewContainer"] > section {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 40px;
        background: #FFFFFF;
    }
    
    /* Centrar input de chat */
    [data-testid="stInputBase"] {
        max-width: 100%;
    }
    
    .stChatInputContainer {
        max-width: 100%;
        margin: 0 auto;
    }
    
    /* Animaciones sutiles */
    @keyframes fade-in {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }

    @keyframes slide-in-up {
        from {
            opacity: 0;
            transform: translateY(4px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Badges modernos */
    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 4px;
        color: white;
        font-weight: 600;
        font-size: 13px;
        margin-right: 8px;
        animation: fade-in 0.3s ease-out;
    }

    .badge-recording {
        background: #EA001B;
        color: white;
    }

    .badge-upload {
        background: #0078D4;
        color: white;
    }

    .badge-saved {
        background: #09A741;
        color: white;
    }

    /* Notificaciones mejoradas */
    .notification-icon {
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
    }

    .notification-icon:hover {
        transform: scale(1.05);
    }

    .notification-icon-success {
        background: #E8F5E9;
        border: 1px solid #09A741;
        color: #09A741;
    }

    .notification-icon-error {
        background: #FFEBEE;
        border: 1px solid #EA001B;
        color: #EA001B;
    }

    .notification-icon-warning {
        background: #FFF3E0;
        border: 1px solid #FFA500;
        color: #FFA500;
    }

    .notification-icon-info {
        background: #E3F2FD;
        border: 1px solid #0052CC;
        color: #0052CC;
    }

    /* Tooltip moderno */
    .notification-tooltip {
        visibility: hidden;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: #171717;
        color: white;
        text-align: center;
        border-radius: 4px;
        padding: 8px 12px;
        white-space: nowrap;
        font-size: 12px;
        font-weight: 500;
        opacity: 0;
        transition: opacity 0.2s;
        pointer-events: none;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
    }

    .notification-icon:hover .notification-tooltip {
        visibility: visible;
        opacity: 1;
    }

    .notification-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: #171717 transparent transparent transparent;
    }

    /* Notificaciones expandidas */
    .notification-expanded {
        animation: slide-in-up 0.3s ease-out;
        margin: 10px 0;
        border-radius: 4px;
        padding: 12px 16px;
        font-weight: 500;
        box-shadow: var(--shadow-sm);
        border-left: 3px solid;
    }

    .notification-expanded-success {
        background: #E8F5E9;
        border-left-color: #09A741;
        color: #09A741;
    }

    .notification-expanded-error {
        background: #FFEBEE;
        border-left-color: #EA001B;
        color: #EA001B;
    }

    .notification-expanded-info {
        background: #E3F2FD;
        border-left-color: #0052CC;
        color: #0052CC;
    }

    /* Chat moderno */
    .chat-container {
        display: flex;
        flex-direction: column;
        gap: 16px;
        padding: 20px 0;
    }

    .chat-message {
        display: flex;
        gap: 12px;
        margin-bottom: 16px;
        animation: slide-in-up 0.3s ease-out;
    }

    .chat-message-user {
        justify-content: flex-end;
    }

    .chat-message-ai {
        justify-content: flex-start;
    }

    .chat-bubble {
        max-width: 70%;
        padding: 12px 16px;
        border-radius: 8px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 14px;
        box-shadow: var(--shadow-sm);
    }

    .chat-bubble-user {
        background: #0052CC;
        color: white;
        border-radius: 12px 12px 2px 12px;
    }

    .chat-bubble-ai {
        background: #E8EAED;
        color: #171717;
        border-radius: 12px 12px 12px 2px;
    }

    .chat-avatar {
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
    }

    .chat-avatar-user {
        background: #0052CC;
        color: white;
    }

    .chat-avatar-ai {
        background: #FFFFFF;
        color: #8E92A9;
        border: 1px solid #DCDCDC;
    }
    </style>
    """

