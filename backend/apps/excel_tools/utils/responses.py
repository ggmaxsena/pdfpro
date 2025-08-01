from django.http import HttpResponse

def as_attachment(buffer, filename, content_type):
    response = HttpResponse(buffer, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
