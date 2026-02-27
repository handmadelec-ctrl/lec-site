from django.conf import settings
from urllib.parse import quote_plus


def whatsapp_context(request):
    phone = getattr(settings, "WHATSAPP_NUMBER", "").strip()
    message = getattr(settings, "WHATSAPP_DEFAULT_MESSAGE", "").strip()

    whatsapp_url = ""
    if phone and message:
        whatsapp_url = f"https://wa.me/{phone}?text={quote_plus(message)}"

    return {
        "WHATSAPP_NUMBER": phone,
        "WHATSAPP_DEFAULT_MESSAGE": message,
        "WHATSAPP_URL": whatsapp_url,
    }
