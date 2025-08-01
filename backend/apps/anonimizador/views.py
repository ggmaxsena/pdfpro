import json

from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.views import APIView

from .services.anonimization_service import AnonimizationService


@method_decorator(csrf_exempt, name="dispatch")
class AnonymizePreview(APIView):
    """
    View para pré-visualizar a anonimização de um arquivo.

    Recebe um arquivo e retorna os cabeçalhos e tokens detectados.
    """
    parser_classes = (MultiPartParser,)

    def post(self, request, *a, **kw):
        """
        Processa a requisição POST para pré-visualizar a anonimização.

        Args:
            request (HttpRequest): O objeto de requisição.
            *a: Argumentos posicionais.
            **kw: Argumentos de palavra-chave.

        Returns:
            JsonResponse: Um JSON contendo os cabeçalhos e tokens detectados.
        """
        f = request.data.get("file")
        if not f:
            return HttpResponse("arquivo não enviado", status=400)

        resp = AnonimizationService.preview_anonymization(f)
        return JsonResponse(resp)


@method_decorator(csrf_exempt, name="dispatch")
class AnonymizeRun(APIView):
    """
    View para executar a anonimização de um arquivo.

    Recebe um arquivo e regras de anonimização, e retorna o arquivo anonimizado.
    """
    parser_classes = (MultiPartParser, JSONParser)

    def post(self, request, *a, **kw):
        """
        Processa a requisição POST para executar a anonimização.

        Args:
            request (HttpRequest): O objeto de requisição.
            *a: Argumentos posicionais.
            **kw: Argumentos de palavra-chave.

        Returns:
            HttpResponse: O arquivo anonimizado como anexo.
        """
        f = request.data.get("file")
        if not f:
            return HttpResponse("arquivo não enviado", status=400)

        raw_rules = request.data.get("rules", "{}")
        rules = json.loads(raw_rules)
        if not rules:
            return HttpResponse("regras de anonimização não enviadas", status=400)

        out, filename = AnonimizationService.run_anonymization(f, rules)
        return HttpResponse(
            out.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f'attachment; filename={filename}'
            },
        )