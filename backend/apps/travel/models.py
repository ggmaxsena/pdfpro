from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from decimal import Decimal
from .utils.fields import EncryptedCharField

TIPO_TRANSPORTE = [
    ('oficial', 'Oficial'),
    ('proprio', 'Próprio'),
    ('comercial', 'Comercial'),
]

MEIO_TRANSPORTE = [
    ('aereo', 'Aéreo'),
    ('terrestre', 'Terrestre'),
    ('fluvial', 'Fluvial'),
]

class TravelRequest(models.Model):
    unidade_orcamentaria = models.CharField(max_length=120, verbose_name="Unidade Orçamentária", default="")
    orgao_solicitante = models.CharField(max_length=120, verbose_name="Órgão Solicitante", default="")
    justificativa = models.TextField(verbose_name="Justificativa")
    objetivo = models.TextField(verbose_name="Objetivo")
    itinerario = models.CharField(max_length=255, verbose_name="Itinerário")
    data_ida = models.DateField(verbose_name="Data de Ida")
    data_retorno = models.DateField(verbose_name="Data de Retorno")
    transporte_tipo = models.CharField(max_length=20, choices=TIPO_TRANSPORTE, verbose_name="Tipo de Transporte", default="oficial")
    transporte_meio = models.CharField(max_length=20, choices=MEIO_TRANSPORTE, verbose_name="Meio de Transporte", default="terrestre")
    descricao_veiculo = models.CharField(max_length=255, blank=True, null=True, verbose_name="Descrição do Veículo")
    criado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name="Criado Por", default=1) # Default para o superuser
    data_criacao = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")

    class Meta:
        verbose_name = "Solicitação de Viagem"
        verbose_name_plural = "Solicitações de Viagem"

    def __str__(self):
        return f"Viagem para {self.objetivo} de {self.data_ida} a {self.data_retorno}"

class Traveler(models.Model):
    travel = models.ForeignKey(TravelRequest, related_name='travelers', on_delete=models.CASCADE)
    nome = models.CharField(max_length=120, verbose_name="Nome")
    matricula = models.CharField(max_length=20, verbose_name="Matrícula")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    cds = models.CharField(max_length=10, blank=True, null=True, verbose_name="CDS")
    cpf = EncryptedCharField(max_length=255, verbose_name="CPF") # Alterado para EncryptedCharField
    banco = EncryptedCharField(max_length=255, verbose_name="Banco") # Alterado para EncryptedCharField
    agencia = EncryptedCharField(max_length=255, verbose_name="Agência") # Alterado para EncryptedCharField
    conta_corrente = EncryptedCharField(max_length=255, verbose_name="Conta Corrente") # Alterado para EncryptedCharField
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Unitário", default=Decimal('0.00'))
    qtd_diarias = models.DecimalField(max_digits=4, decimal_places=1, verbose_name="Quantidade de Diárias", default=Decimal('0.0'))
    valor_total = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Valor Total", default=Decimal('0.00'))
    tipo = models.CharField(max_length=15, choices=[('motorista','Motorista'), ('passageiro','Passageiro')], verbose_name="Tipo", default="passageiro")

    class Meta:
        verbose_name = "Viajante"
        verbose_name_plural = "Viajantes"

    def __str__(self):
        return self.nome
