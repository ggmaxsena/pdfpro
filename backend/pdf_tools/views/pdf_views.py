# pdf_tools/views/pdf_views.py
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..serializers.pdf_serializers import (
    CompressPDFSerializer,
    SplitByPagesSerializer,
    SplitBySizeSerializer,
)
from ..services.pdf_service import PDFService
from ..utils.pdf_utils import as_attachment


class PDFViewSet(viewsets.ViewSet):
    """
    Operações em PDF:
    - compress: comprime um PDF.
    - split_by_pages: divide por intervalo de páginas.
    - split_by_size: divide por tamanho em MB (ZIP).
    """
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"], url_path="compress")
    def compress(self, request):
        serializer = CompressPDFSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        filename, buffer = PDFService.compress(serializer.validated_data["file"])
        return as_attachment(buffer, filename, "application/pdf")

    @action(detail=False, methods=["post"], url_path="split/by-pages")
    def split_by_pages(self, request):
        serializer = SplitByPagesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_obj = serializer.validated_data["file"]
        start, end = serializer.validated_data["pages"]

        filename, buffer = PDFService.split_by_pages(file_obj, start, end)
        return as_attachment(buffer, filename, "application/pdf")

    @action(detail=False, methods=["post"], url_path="split/by-size")
    def split_by_size(self, request):
        serializer = SplitBySizeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_obj = serializer.validated_data["file"]
        size_mb = serializer.validated_data["size"]

        filename, buffer = PDFService.split_by_size(file_obj, size_mb)
        return as_attachment(buffer, filename, "application/zip")

    # Fallback para rota inválida (ex.: /split sem opção)
    def create(self, request):
        return Response(
            {"detail": "Use /compress, /split/by-pages ou /split/by-size."},
            status=status.HTTP_400_BAD_REQUEST,
        )
