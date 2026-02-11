"""
Módulo para compartir transcripciones y resúmenes via email y WhatsApp
"""
from urllib.parse import quote


def generate_email_link(recipient_email: str, subject: str, content: str) -> str:
    """
    Genera un enlace mailto para abrir el cliente de email
    
    Args:
        recipient_email: Email del destinatario
        subject: Asunto del email
        content: Contenido del email
    
    Returns:
        URL mailto
    """
    encoded_subject = quote(subject)
    encoded_body = quote(content)
    mailto_url = f"mailto:{recipient_email}?subject={encoded_subject}&body={encoded_body}"
    return mailto_url


def generate_whatsapp_link(phone_number: str, content: str) -> str:
    """
    Genera un enlace para WhatsApp Web con el mensaje preformulado
    
    Args:
        phone_number: Número de teléfono (ej: +34632123456)
        content: Contenido del mensaje
    
    Returns:
        URL para abrir en WhatsApp
    """
    # Encodificar el contenido para la URL
    encoded_message = quote(content)
    # Formato: https://wa.me/NUMERO?text=MENSAJE
    whatsapp_url = f"https://wa.me/{phone_number.replace('+', '').replace(' ', '')}?text={encoded_message}"
    return whatsapp_url


def format_content_for_sharing(selected_audio: str, content: str, is_summary: bool = False) -> str:
    """
    Formatea el contenido para compartir
    
    Args:
        selected_audio: Nombre del audio
        content: Contenido a compartir
        is_summary: Si es un resumen o transcripción completa
    
    Returns:
        Contenido formateado
    """
    header = f"{'RESUMEN' if is_summary else 'TRANSCRIPCIÓN'} - {selected_audio}\n"
    separator = "=" * 70 + "\n\n"
    footer = f"\n\n{'─' * 70}\nGenerado automáticamente desde la aplicación de grabación de audios"
    
    return header + separator + content + footer
