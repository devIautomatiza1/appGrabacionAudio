"""
Funciones centralizadas para mostrar notificaciones
"""
import streamlit as st


# Configuración de estilos por tipo de notificación
NOTIFICATION_STYLES = {
    "success": {"icon": "✓", "class": "notification-icon-success"},
    "error": {"icon": "✕", "class": "notification-icon-error"},
    "warning": {"icon": "⚠", "class": "notification-icon-warning"},
    "info": {"icon": "ℹ", "class": "notification-icon-info"},
}

NOTIFICATION_EXPANDED_STYLES = {
    "success": "notification-expanded-success",
    "error": "notification-expanded-error",
    "info": "notification-expanded-info",
}


def _show_notification(message: str, notification_type: str) -> None:
    """
    Función interna para mostrar notificaciones compactas con tooltip.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo de notificación ('success', 'error', 'warning', 'info')
    """
    style = NOTIFICATION_STYLES.get(notification_type)
    if not style:
        return
    
    st.markdown(f"""
    <div class="notification-icon {style['class']}">
        {style['icon']}
        <span class="notification-tooltip">{message}</span>
    </div>
    """, unsafe_allow_html=True)


def _show_notification_expanded(message: str, notification_type: str) -> None:
    """
    Función interna para mostrar notificaciones expandidas con colores personalizados.
    
    Args:
        message: Texto a mostrar
        notification_type: Tipo de notificación ('success', 'error', 'info', 'warning')
    """
    icon = NOTIFICATION_STYLES.get(notification_type, {}).get("icon", "•")
    
    # Colores personalizados para cada tipo
    colors = {
        "success": {"bg": "#10b981", "text": "white"},  # Verde
        "error": {"bg": "#ef4444", "text": "white"},    # Rojo
        "warning": {"bg": "#f59e0b", "text": "white"},  # Amarillo
        "info": {"bg": "#3b82f6", "text": "white"}      # Azul
    }
    
    color_style = colors.get(notification_type, colors["info"])
    
    st.markdown(f"""
    <div style="
        background-color: {color_style['bg']};
        color: {color_style['text']};
        padding: 12px 16px;
        border-radius: 8px;
        margin: 8px 0;
        font-weight: 600;
        font-size: 14px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        animation: slideInRight 0.3s ease-out;
        display: inline-block;
    ">
        {icon} {message}
    </div>
    <style>
        @keyframes slideInRight {{
            from {{
                opacity: 0;
                transform: translateX(20px);
            }}
            to {{
                opacity: 1;
                transform: translateX(0);
            }}
        }}
    </style>
    """, unsafe_allow_html=True)


def _create_notification_function(notification_type: str, style_variant: str):
    """Factory que crea funciones de notificación dinámicamente
    
    Args:
        notification_type: 'success', 'error', 'warning', 'info'
        style_variant: 'compact', 'expanded', 'debug'
    """
    def notification_func(message: str) -> None:
        if style_variant == 'compact':
            _show_notification(message, notification_type)
        elif style_variant == 'expanded':
            _show_notification_expanded(message, notification_type)
        elif style_variant == 'debug':
            icon = NOTIFICATION_STYLES.get(notification_type, {}).get("icon", "•")
            st.markdown(f'<div class="notification-expanded notification-expanded-{notification_type}">{icon} {message}</div>', unsafe_allow_html=True)
    
    return notification_func

# API pública - Generar funciones automáticamente
show_success = _create_notification_function("success", "compact")
show_error = _create_notification_function("error", "compact")
show_warning = _create_notification_function("warning", "compact")
show_info = _create_notification_function("info", "compact")

show_success_expanded = _create_notification_function("success", "expanded")
show_error_expanded = _create_notification_function("error", "expanded")
show_info_expanded = _create_notification_function("info", "expanded")
show_warning_expanded = _create_notification_function("warning", "expanded")

show_success_debug = _create_notification_function("success", "debug")
show_error_debug = _create_notification_function("error", "debug")
show_info_debug = _create_notification_function("info", "debug")

