
from io import BytesIO
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
import pikepdf

class CompressPDFView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        pdf = pikepdf.open(file_obj)
        output = BytesIO()
        pdf.save(output, compress_streams=True, linearize=True)
        output.seek(0)

        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=compressed_{file_obj.name}'
        return response

class SplitPDFView(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        file_obj = request.data['file']
        pages_range = request.data.get('pages', '')
        
        try:
            start_page, end_page = map(int, pages_range.split('-'))
        except ValueError:
            return Response({"error": "Invalid page range format. Use 'start-end'."}, status=400)

        reader = PdfReader(file_obj)
        writer = PdfWriter()

        for i in range(start_page - 1, end_page):
            writer.add_page(reader.pages[i])

        output = BytesIO()
        writer.write(output)
        output.seek(0)

        response = HttpResponse(output.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename=split_{file_obj.name}'
        return response
