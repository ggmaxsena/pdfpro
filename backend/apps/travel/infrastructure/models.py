from django.db import models
from django.utils import timezone
from decimal import Decimal

class PerDiemRate(models.Model):
    cargo = models.CharField(max_length=120, verbose_name="Cargo", default="")
    cds = models.CharField(max_length=10, blank=True, null=True, verbose_name="CDS")
    valor_nacional = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Nacional", default=Decimal('0.00'))
    valor_internacional = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Valor Internacional", default=Decimal('0.00'))
    vigente_desde = models.DateField(verbose_name="Vigente Desde", default=timezone.now)
    vigente_ate = models.DateField(blank=True, null=True, verbose_name="Vigente Até")

    class Meta:
        verbose_name = "Valor de Diária"
        verbose_name_plural = "Valores de Diárias"

    def __str__(self):
        return f"{self.cargo} - R$ {self.valor_nacional}"
