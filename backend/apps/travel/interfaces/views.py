from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from django.http import HttpResponse
from ..services.diarias_service import DiariasService
from ..services.pdf_generator import PdfGeneratorService
from ..models import TravelRequest, Traveler
from .serializers import DiariasCalculatorSerializer, TravelRequestSerializer, TravelerSerializer

class CalculateDiariasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = DiariasCalculatorSerializer(data=request.data)
        if serializer.is_valid():
            service = DiariasService()
            try:
                # Passa o objeto DateRange e os novos parâmetros para o serviço
                result = service.calculate(
                    cargo=serializer.validated_data['role'], # Renomeado de 'role' para 'cargo'
                    cds=serializer.validated_data.get('cds', None),
                    travel_period=serializer.validated_data['travel_period'],
                    fora_do_estado=serializer.validated_data['fora_do_estado'],
                    via_aerea=serializer.validated_data['via_aerea'],
                    exige_pernoite=serializer.validated_data['exige_pernoite']
                )
                # Retorna os dados do DailyAllowance
                return Response({
                    "quantity": result.quantity,
                    "unit_price": result.unit_value.amount,
                    "total_value": result.total.amount
                })
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TravelRequestViewSet(viewsets.ModelViewSet):
    queryset = TravelRequest.objects.all()
    serializer_class = TravelRequestSerializer
    permission_classes = [DjangoModelPermissions]

    def perform_create(self, serializer):
        # Define o usuário logado como o criador da solicitação
        serializer.save(criado_por=self.request.user)

class TravelerViewSet(viewsets.ModelViewSet):
    queryset = Traveler.objects.all()
    serializer_class = TravelerSerializer
    permission_classes = [DjangoModelPermissions]

# class GeneratePdfView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, *args, **kwargs):
#         # Recebe o ID da solicitação de viagem
#         travel_request_id = request.data.get('travel_request_id')
#         if not travel_request_id:
#             return Response({"error": "ID da solicitação de viagem é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             travel_request = TravelRequest.objects.get(id=travel_request_id)
#         except TravelRequest.DoesNotExist:
#             return Response({"error": "Solicitação de viagem não encontrada"}, status=status.HTTP_404_NOT_FOUND)

#         # Adiciona os resultados do cálculo ao travel_request_data para o PDF
#         # Isso deve vir do frontend ou ser recalculado aqui
#         # Para o PDF, vamos passar os dados diretamente do modelo
#         travel_request_data = {
#             'id': travel_request.id,
#             'unidade_orcamentaria': travel_request.unidade_orcamentaria,
#             'orgao_solicitante': travel_request.orgao_solicitante,
#             'justificativa': travel_request.justificativa,
#             'objetivo': travel_request.objetivo,
#             'itinerario': travel_request.itinerario,
#             'data_ida': travel_request.data_ida,
#             'data_retorno': travel_request.data_retorno,
#             'transporte_tipo': travel_request.transporte_tipo,
#             'transporte_meio': travel_request.transporte_meio,
#             'descricao_veiculo': travel_request.descricao_veiculo,
#             'criado_por': travel_request.criado_por,
#             'data_criacao': travel_request.data_criacao,
#             'travelers': [],
#             'calculated_quantity': request.data.get('calculated_quantity', 0),
#             'calculated_unit_price': request.data.get('calculated_unit_price', 0),
#             'calculated_total_value': request.data.get('calculated_total_value', 0),
#         }

#         for traveler in travel_request.travelers.all():
#             travel_request_data['travelers'].append({
#                 'nome': traveler.nome,
#                 'matricula': traveler.matricula,
#                 'cargo': traveler.cargo,
#                 'cds': traveler.cds,
#                 'cpf': traveler.cpf,
#                 'banco': traveler.banco,
#                 'agencia': traveler.agencia,
#                 'conta_corrente': traveler.conta_corrente,
#                 'tipo': traveler.tipo,
#             })

#         pdf_service = PdfGeneratorService()
#         pdf_bytes = pdf_service.generate_travel_request_pdf(travel_request_data)

#         response = HttpResponse(pdf_bytes, content_type='application/pdf')
#         response['Content-Disposition'] = 'attachment; filename="solicitacao_viagem.pdf"'
#         return response
