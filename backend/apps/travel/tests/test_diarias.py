from datetime import date
from decimal import Decimal
from unittest.mock import Mock
from django.test import TestCase
from ..services.diarias_service import DiariasService
from ..domain.entities import PerDiemRate as PerDiemRateEntity
from ..domain.value_objects import DateRange, Money, DailyAllowance

class DiariasServiceTest(TestCase):
    def setUp(self):
        self.mock_per_diem_repository = Mock()
        # Configura o mock para retornar uma entidade PerDiemRate com valor 300.00
        self.mock_per_diem_repository.get_rate_by_role.return_value = PerDiemRateEntity(
            cargo="Auditor", 
            valor_nacional=Money(Decimal("300.00")),
            valor_internacional=Money(Decimal("600.00")),
            vigente_desde=date(2024, 1, 1)
        )
        self.service = DiariasService(per_diem_repository=self.mock_per_diem_repository)

    def test_calculate_same_day_travel_no_pernoite(self):
        """Testa o cálculo para uma viagem no mesmo dia sem pernoite (deslocamento < 5h)."""
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 1))
        result = self.service.calculate(cargo="Auditor", travel_period=travel_period, exige_pernoite=False)
        self.assertEqual(result.quantity, Decimal("0.0"))
        self.assertEqual(result.total, Decimal("0.00"))

    def test_calculate_same_day_travel_with_pernoite(self):
        """Testa o cálculo para uma viagem no mesmo dia com pernoite (1 diária)."""
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 1))
        result = self.service.calculate(cargo="Auditor", travel_period=travel_period, exige_pernoite=True)
        self.assertEqual(result.quantity, Decimal("1.0"))
        self.assertEqual(result.total, Decimal("300.00"))

    def test_calculate_overnight_travel(self):
        """Testa o cálculo para uma viagem com pernoite (múltiplos dias)."""
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 3))
        result = self.service.calculate(cargo="Auditor", travel_period=travel_period, exige_pernoite=True)
        self.assertEqual(result.quantity, Decimal("3.0")) # 3 dias completos
        self.assertEqual(result.total, Decimal("900.00"))

    def test_calculate_overnight_travel_no_pernoite(self):
        """Testa o cálculo para uma viagem de múltiplos dias sem pernoite (meia diária no retorno)."""
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 3))
        result = self.service.calculate(cargo="Auditor", travel_period=travel_period, exige_pernoite=False)
        self.assertEqual(result.quantity, Decimal("2.5")) # 2 dias completos + 0.5
        self.assertEqual(result.total, Decimal("750.00"))

    def test_invalid_dates(self):
        """Testa se o serviço levanta um erro para datas inválidas."""
        with self.assertRaises(ValueError):
            DateRange(date(2025, 10, 3), date(2025, 10, 1))

    def test_no_per_diem_rate_found(self):
        """
        Testa se o serviço levanta um erro quando nenhuma taxa de diária é encontrada.
        """
        self.mock_per_diem_repository.get_rate_by_role.return_value = None
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 1))
        with self.assertRaisesRegex(ValueError, "Valor de diária não encontrado para o cargo: Inexistente e CDS: None"):
            self.service.calculate(cargo="Inexistente", travel_period=travel_period)

    def test_fora_do_estado_rule(self):
        """Testa a regra de acréscimo para viagem fora do estado (+100%)."""
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 2))
        result = self.service.calculate(cargo="Auditor", travel_period=travel_period, fora_do_estado=True, exige_pernoite=False)
        self.assertEqual(result.unit_value, Decimal("600.00")) # 300 * 2
        self.assertEqual(result.total, Decimal("900.00")) # 1.5 * 600

    def test_via_aerea_rule(self):
        """Testa a regra de acréscimo para viagem via aérea (+30%)."""
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 2))
        result = self.service.calculate(cargo="Auditor", travel_period=travel_period, via_aerea=True, exige_pernoite=False)
        self.assertEqual(result.unit_value, Decimal("390.00")) # 300 * 1.3
        self.assertEqual(result.total, Decimal("585.00")) # 1.5 * 390

    def test_fora_do_estado_and_via_aerea_rule(self):
        """Testa a combinação das regras fora do estado e via aérea."""
        travel_period = DateRange(date(2025, 10, 1), date(2025, 10, 2))
        result = self.service.calculate(cargo="Auditor", travel_period=travel_period, fora_do_estado=True, via_aerea=True, exige_pernoite=False)
        self.assertEqual(result.unit_value, Decimal("780.00")) # 300 * 2 * 1.3
        self.assertEqual(result.total, Decimal("1170.00")) # 1.5 * 780