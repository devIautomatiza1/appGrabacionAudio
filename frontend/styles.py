"""
Estilos CSS profesionales SaaS para la aplicación
"""

def get_styles():
    """Retorna todos los estilos CSS de la aplicación"""
    return """
    <style>
    /* Reset y Variables de Color */
    :root {
        --primary: #0052CC;
        --primary-light: #0066FF;
        --secondary: #10b981;
        --danger: #ef4444;
        --warning: #f59e0b;
        --info: #3b82f6;
        --dark-bg: #0f1419;
        --darker-bg: #050709;
        --card-bg: #1a1f2e;
        --border-color: #2d3748;
        --text-primary: #e5e7eb;
        --text-secondary: #9ca3af;
    }
    
    /* Tema oscuro profesional */
    body {
        background-color: var(--dark-bg);
        color: var(--text-primary);
    }

    /* Header/Navbar Profesional */
    .navbar {
        position: sticky;
        top: 0;
        z-index: 100;
        background: linear-gradient(135deg, rgba(15, 20, 25, 0.95) 0%, rgba(5, 7, 9, 0.95) 100%);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid var(--border-color);
        padding: 16px 0;
        margin-bottom: 40px;
    }

    .navbar-content {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 40px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .logo {
        font-size: 24px;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-light) 0%, #00d4ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 8px 14px;
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 6px;
        font-size: 12px;
        font-weight: 600;
        color: #34d399;
    }

    .status-dot {
        width: 8px;
        height: 8px;
        background: #34d399;
        border-radius: 50%;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Contenedor principal centrado */
    .main {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 40px;
    }
    
    .stMainBlockContainer {
        max-width: 1400px;
        margin: 0 auto;
    }
    
    [data-testid="stAppViewContainer"] {
        padding: 0;
    }
    
    [data-testid="stAppViewContainer"] > section {
        max-width: 1400px;
        margin: 0 auto;
        padding: 0 40px;
    }
    
    /* Hero Section */
    .hero-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #ffffff 0%, #d1d5db 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: var(--text-secondary);
        margin-bottom: 40px;
        line-height: 1.6;
    }
    
    /* Cards con estilo SaaS */
    .section-card {
        background: linear-gradient(135deg, rgba(26, 31, 46, 0.8) 0%, rgba(15, 20, 25, 0.6) 100%);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 32px;
        margin-bottom: 24px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    .section-card:hover {
        border-color: rgba(0, 102, 255, 0.3);
        box-shadow: 0 8px 16px rgba(0, 102, 255, 0.1);
        transform: translateY(-2px);
    }

    .section-title {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 8px;
        color: #ffffff;
    }

    .section-subtitle {
        font-size: 14px;
        color: var(--text-secondary);
        margin-bottom: 24px;
    }

    /* Grid de dos columnas profesional */
    .two-column {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
        margin-bottom: 32px;
    }

    @media (max-width: 1000px) {
        .two-column {
            grid-template-columns: 1fr;
        }
    }

    /* Audio Recorder Mejorado */
    .recorder-container {
        background: linear-gradient(135deg, rgba(5, 102, 204, 0.1) 0%, rgba(0, 82, 204, 0.05) 100%);
        border: 2px dashed rgba(0, 102, 255, 0.3);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .recorder-container:hover {
        border-color: rgba(0, 102, 255, 0.5);
        background: linear-gradient(135deg, rgba(5, 102, 204, 0.15) 0%, rgba(0, 82, 204, 0.08) 100%);
    }

    .recorder-icon {
        font-size: 48px;
        margin-bottom: 16px;
    }

    /* Upload Area Mejorado */
    .upload-container {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 2px dashed rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .upload-container:hover {
        border-color: rgba(16, 185, 129, 0.5);
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.08) 100%);
    }

    /* Botones Profesionales SaaS */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        padding: 12px 24px;
        transition: all 0.3s ease;
        border: none;
        text-transform: none;
        letter-spacing: 0.5px;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary) 100%);
        color: white;
    }

    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 102, 255, 0.3);
    }

    .stButton > button[kind="secondary"] {
        background: rgba(255, 255, 255, 0.1);
        color: #ffffff;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }

    .stButton > button[kind="secondary"]:hover {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.3);
        transform: translateY(-1px);
    }

    /* Input mejorado */
    .stTextInput input,
    .stSelectbox select,
    .stMultiSelect {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        color: var(--text-primary) !important;
        font-size: 14px !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
    }

    .stTextInput input:focus,
    .stSelectbox select:focus {
        border-color: var(--primary-light) !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 255, 0.1) !important;
        background: rgba(255, 255, 255, 0.08) !important;
    }

    /* Stats Cards */
    .stat-card {
        background: linear-gradient(135deg, rgba(0, 102, 255, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }

    .stat-card:hover {
        border-color: var(--primary-light);
        box-shadow: 0 4px 12px rgba(0, 102, 255, 0.15);
    }

    .stat-value {
        font-size: 32px;
        font-weight: 700;
        color: var(--primary-light);
        margin-bottom: 8px;
    }

    .stat-label {
        font-size: 12px;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    @keyframes pulse-glow {
        0% { 
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0.7);
        }
        70% { 
            box-shadow: 0 0 0 20px rgba(76, 175, 80, 0);
        }
        100% { 
            box-shadow: 0 0 0 0 rgba(76, 175, 80, 0);
        }
    }

    @keyframes slide-in {
        from {
            opacity: 0;
            transform: translateY(-10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes expand {
        from {
            max-width: 40px;
            padding: 8px;
        }
        to {
            max-width: 500px;
            padding: 14px 16px;
        }
    }

    @keyframes avatar-pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
    }

    @keyframes avatar-spin {
        0% {
            transform: rotateY(0deg);
        }
        100% {
            transform: rotateY(360deg);
        }
    }

    .success-pulse {
        animation: pulse-glow 1.5s infinite;
        padding: 12px 16px;
        border-radius: 8px;
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1) 0%, rgba(76, 175, 80, 0.05) 100%);
        border-left: 4px solid #4CAF50;
        font-weight: 500;
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 6px;
        color: white;
        font-weight: 600;
        font-size: 14px;
        margin-right: 8px;
    }

    .badge-recording {
        background: linear-gradient(135deg, #FF6B6B, #FF5252);
    }

    .badge-upload {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
    }

    .badge-saved {
        background: linear-gradient(135deg, #95E77D, #4CAF50);
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
        transition: all 0.3s ease;
        margin: 5px 0;
        position: relative;
    }

    .notification-icon:hover {
        transform: scale(1.1);
    }

    .notification-icon-success {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
        border: 2px solid #34d399;
        color: #10b981;
    }

    .notification-icon-error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 2px solid #f87171;
        color: #dc2626;
    }

    .notification-icon-warning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 2px solid #fbbf24;
        color: #d97706;
    }

    .notification-icon-info {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid #60a5fa;
        color: #2563eb;
    }

    .notification-tooltip {
        visibility: hidden;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.9);
        color: white;
        text-align: center;
        border-radius: 8px;
        padding: 8px 12px;
        white-space: nowrap;
        font-size: 12px;
        font-weight: 500;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
        max-width: 200px;
        word-wrap: break-word;
        white-space: normal;
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
        border-color: rgba(0, 0, 0, 0.9) transparent transparent transparent;
    }

    /* Notificaciones expandidas */
    .notification-expanded {
        animation: slide-in 0.3s ease-out;
        margin: 10px 0;
        border-radius: 8px;
        padding: 14px 16px;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .notification-expanded-success {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15) 0%, rgba(34, 197, 94, 0.08) 100%);
        border-left: 5px solid #34d399;
        color: #10b981;
    }

    .notification-expanded-error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.15) 0%, rgba(239, 68, 68, 0.08) 100%);
        border-left: 5px solid #f87171;
        color: #dc2626;
    }

    .notification-expanded-info {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.15) 0%, rgba(59, 130, 246, 0.08) 100%);
        border-left: 5px solid #60a5fa;
        color: #2563eb;
    }

    .notification-expanded-warning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
        border-left: 5px solid #fbbf24;
        color: #d97706;
    }

    /* Chat mejorado */
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
        animation: slide-in 0.3s ease-out;
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
        border-radius: 12px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 14px;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
        color: white;
        border-radius: 18px 18px 4px 18px;
    }

    .chat-bubble-ai {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.1) 0%, rgba(75, 85, 99, 0.05) 100%);
        color: #e5e7eb;
        border: 1px solid rgba(107, 114, 128, 0.2);
        border-radius: 18px 18px 18px 4px;
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
    }

    .chat-avatar-user {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
    }

    .chat-avatar-ai {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(75, 85, 99, 0.15) 100%);
        border: 1px solid rgba(107, 114, 128, 0.3);
    }

    .avatar-pulse {
        animation: avatar-pulse 2s ease-in-out infinite;
    }

    .avatar-spin {
        animation: avatar-spin 3s linear infinite;
    }

    /* Tipografía mejorada */
    h1 {
        margin-top: 40px;
        margin-bottom: 16px;
        font-weight: 800;
        letter-spacing: -0.5px;
    }

    h2 {
        margin-top: 32px;
        margin-bottom: 12px;
        font-weight: 700;
        letter-spacing: -0.3px;
    }

    h3 {
        margin-top: 24px;
        margin-bottom: 10px;
        font-weight: 600;
    }

    h4 {
        margin-top: 16px;
        margin-bottom: 12px;
        font-weight: 600;
    }

    /* Keyword badges */
    .keyword-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #0052CC 0%, #003d99 100%);
        padding: 10px 14px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(0, 82, 204, 0.25);
        transition: all 0.3s ease;
    }

    .keyword-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 82, 204, 0.35);
    }
    </style>
    """

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 6px;
        color: white;
        font-weight: 600;
        font-size: 14px;
        margin-right: 8px;
    }

    .badge-recording {
        background: linear-gradient(135deg, #FF6B6B, #FF5252);
    }

    .badge-upload {
        background: linear-gradient(135deg, #4ECDC4, #44A08D);
    }

    .badge-saved {
        background: linear-gradient(135deg, #95E77D, #4CAF50);
    }

    /* Estilos para notificaciones compactas con emoticono */
    .notification-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 40px;
        height: 40px;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 5px 0;
        position: relative;
    }

    .notification-icon:hover {
        transform: scale(1.1);
    }

    .notification-icon-success {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.2) 0%, rgba(34, 197, 94, 0.1) 100%);
        border: 2px solid #34d399;
        color: #10b981;
    }

    .notification-icon-error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.2) 0%, rgba(239, 68, 68, 0.1) 100%);
        border: 2px solid #f87171;
        color: #dc2626;
    }

    .notification-icon-warning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.2) 0%, rgba(245, 158, 11, 0.1) 100%);
        border: 2px solid #fbbf24;
        color: #d97706;
    }

    .notification-icon-info {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.2) 0%, rgba(59, 130, 246, 0.1) 100%);
        border: 2px solid #60a5fa;
        color: #2563eb;
    }

    /* Tooltip para el mensaje */
    .notification-tooltip {
        visibility: hidden;
        position: absolute;
        z-index: 1000;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        background-color: rgba(0, 0, 0, 0.9);
        color: white;
        text-align: center;
        border-radius: 8px;
        padding: 8px 12px;
        white-space: nowrap;
        font-size: 12px;
        font-weight: 500;
        opacity: 0;
        transition: opacity 0.3s;
        pointer-events: none;
        max-width: 200px;
        word-wrap: break-word;
        white-space: normal;
    }

    .notification-icon:hover .notification-tooltip {
        visibility: visible;
        opacity: 1;
    }

    /* Arrow para tooltip */
    .notification-tooltip::after {
        content: "";
        position: absolute;
        top: 100%;
        left: 50%;
        margin-left: -5px;
        border-width: 5px;
        border-style: solid;
        border-color: rgba(0, 0, 0, 0.9) transparent transparent transparent;
    }

    /* Estilos para notificaciones expandidas (para debug) */
    .notification-expanded {
        animation: slide-in 0.3s ease-out;
        margin: 10px 0;
        border-radius: 8px;
        padding: 14px 16px;
        font-weight: 500;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .notification-expanded-success {
        background: linear-gradient(135deg, rgba(52, 211, 153, 0.15) 0%, rgba(34, 197, 94, 0.08) 100%);
        border-left: 5px solid #34d399;
        color: #10b981;
    }

    .notification-expanded-error {
        background: linear-gradient(135deg, rgba(248, 113, 113, 0.15) 0%, rgba(239, 68, 68, 0.08) 100%);
        border-left: 5px solid #f87171;
        color: #dc2626;
    }

    .notification-expanded-info {
        background: linear-gradient(135deg, rgba(96, 165, 250, 0.15) 0%, rgba(59, 130, 246, 0.08) 100%);
        border-left: 5px solid #60a5fa;
        color: #2563eb;
    }

    .notification-expanded-warning {
        background: linear-gradient(135deg, rgba(251, 191, 36, 0.15) 0%, rgba(245, 158, 11, 0.08) 100%);
        border-left: 5px solid #fbbf24;
        color: #d97706;
    }

    /* Estilos para el chat */
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
        animation: slide-in 0.3s ease-out;
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
        border-radius: 12px;
        word-wrap: break-word;
        line-height: 1.5;
        font-size: 14px;
    }

    .chat-bubble-user {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
        color: white;
        border-radius: 18px 18px 4px 18px;
    }

    .chat-bubble-ai {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.1) 0%, rgba(75, 85, 99, 0.05) 100%);
        color: #e5e7eb;
        border: 1px solid rgba(107, 114, 128, 0.2);
        border-radius: 18px 18px 18px 4px;
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
    }

    .chat-avatar-user {
        background: linear-gradient(135deg, #3B82F6 0%, #2563eb 100%);
    }

    .chat-avatar-ai {
        background: linear-gradient(135deg, rgba(107, 114, 128, 0.2) 0%, rgba(75, 85, 99, 0.15) 100%);
        border: 1px solid rgba(107, 114, 128, 0.3);
    }

    .avatar-pulse {
        animation: avatar-pulse 2s ease-in-out infinite;
    }

    .avatar-spin {
        animation: avatar-spin 3s linear infinite;
    }

    /* Espaciado mejorado para headers */
    h1 {
        margin-top: 40px;
        margin-bottom: 16px;
    }

    h2 {
        margin-top: 32px;
        margin-bottom: 12px;
    }

    h3 {
        margin-top: 24px;
        margin-bottom: 10px;
    }

    h4 {
        margin-top: 16px;
        margin-bottom: 12px;
    }

    /* Estilos para badges de palabras clave */
    .keyword-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, #0052CC 0%, #003d99 100%);
        padding: 10px 14px;
        border-radius: 6px;
        color: white;
        font-weight: 500;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(0, 82, 204, 0.25);
        transition: all 0.3s ease;
    }

    .keyword-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 82, 204, 0.35);
    }

    /* Botones mejorados */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }

    /* Botones de eliminación (X rojo) */
    button[key*="del_"] {
        color: #EA001B !important;
        border-color: #EA001B !important;
    }

    button[key*="del_"]:hover {
        background-color: rgba(234, 0, 27, 0.1) !important;
    }
    </style>
    """

