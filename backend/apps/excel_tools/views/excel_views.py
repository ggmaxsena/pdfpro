from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from ..serializers.anonymize_serializers import AnonymizeNameSerializer
from ..services.excel_service import ExcelService
from ..utils.responses import as_attachment

class AnonymizeNameView(APIView):
    parser_classes = (MultiPartParser,)
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = AnonymizeNameSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        file_obj = serializer.validated_data["file"]
        sheet = serializer.validated_data.get("sheet")

        fname, buf = ExcelService.anonymize_name(file_obj, sheet)
        return as_attachment(buf, fname, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
