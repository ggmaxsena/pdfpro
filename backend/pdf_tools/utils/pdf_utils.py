from django.http import HttpResponse


def as_attachment(buffer, filename, content_type):
    """Transforma BytesIO em HttpResponse para download."""
    response = HttpResponse(buffer.read(), content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response