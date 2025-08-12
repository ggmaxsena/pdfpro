from datetime import date
from decimal import Decimal
from typing import Optional

from ..infrastructure.models import PerDiemRate as PerDiemRateORM
from ..domain.entities import PerDiemRate as PerDiemRateEntity
from ..domain.value_objects import Money

class PerDiemRepository:
    def get_rate_by_role(self, cargo: str, effective_date: date, cds: Optional[str] = None) -> Optional[PerDiemRateEntity]:
        """
        Retorna a taxa de diária para um determinado cargo, CDS e data de vigência.
        """
        try:
            # Busca no ORM
            # Considera CDS se fornecido, e vigência
            if cds:
                per_diem_orm = PerDiemRateORM.objects.get(
                    cargo=cargo,
                    cds=cds,
                    vigente_desde__lte=effective_date,
                    vigente_ate__gte=effective_date
                )
            else:
                per_diem_orm = PerDiemRateORM.objects.get(
                    cargo=cargo,
                    cds__isnull=True, # Garante que pegue o sem CDS se não for fornecido
                    vigente_desde__lte=effective_date,
                    vigente_ate__gte=effective_date
                )
            # Converte para entidade de domínio
            return PerDiemRateEntity(
                cargo=per_diem_orm.cargo,
                cds=per_diem_orm.cds,
                valor_nacional=Money(per_diem_orm.valor_nacional),
                valor_internacional=Money(per_diem_orm.valor_internacional),
                vigente_desde=per_diem_orm.vigente_desde,
                vigente_ate=per_diem_orm.vigente_ate
            )
        except PerDiemRateORM.DoesNotExist:
            return None

    def create_rate(self, cargo: str, valor_nacional: Decimal, valor_internacional: Decimal, vigente_desde: date, cds: Optional[str] = None, vigente_ate: Optional[date] = None) -> PerDiemRateEntity:
        per_diem_orm = PerDiemRateORM.objects.create(
            cargo=cargo,
            cds=cds,
            valor_nacional=valor_nacional,
            valor_internacional=valor_internacional,
            vigente_desde=vigente_desde,
            vigente_ate=vigente_ate
        )
        return PerDiemRateEntity(
            cargo=per_diem_orm.cargo,
            cds=per_diem_orm.cds,
            valor_nacional=Money(per_diem_orm.valor_nacional),
            valor_internacional=Money(per_diem_orm.valor_internacional),
            vigente_desde=per_diem_orm.vigente_desde,
            vigente_ate=per_diem_orm.vigente_ate
        )
