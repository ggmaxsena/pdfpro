from django.http import HttpResponse


def as_attachment(buf, filename: str, content_type: str) -> HttpResponse:
    """
    Constrói uma resposta HTTP para download de um arquivo.

    Args:
        buf (BytesIO): O buffer de bytes contendo o conteúdo do arquivo.
        filename (str): O nome do arquivo para o download.
        content_type (str): O tipo de conteúdo (MIME type) do arquivo.

    Returns:
        HttpResponse: Uma resposta HTTP configurada para download.
    """
    response = HttpResponse(buf.read(), content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
