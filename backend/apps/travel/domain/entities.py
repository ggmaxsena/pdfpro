from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List

from .value_objects import Money, DateRange, CPF, BankAccount, DailyAllowance

class PerDiemRate:
    def __init__(self, cargo: str, valor_nacional: Money, valor_internacional: Money, vigente_desde: date, cds: Optional[str] = None, vigente_ate: Optional[date] = None):
        if not cargo or not valor_nacional or not valor_internacional or not vigente_desde:
            raise ValueError("Cargo, valores e data de vigência são obrigatórios para a diária")
        self.cargo = cargo
        self.cds = cds
        self.valor_nacional = valor_nacional
        self.valor_internacional = valor_internacional
        self.vigente_desde = vigente_desde
        self.vigente_ate = vigente_ate

    def __str__(self) -> str:
        return f"{self.cargo} - R$ {self.valor_nacional}"

class Traveler:
    def __init__(self, name: str, employee_id: str, role: str, cpf: CPF, bank_account: BankAccount, cds: Optional[str] = None, daily_allowance: Optional[DailyAllowance] = None):
        if not name or not employee_id or not role:
            raise ValueError("Nome, matrícula e cargo do viajante são obrigatórios")
        self.name = name
        self.employee_id = employee_id
        self.role = role
        self.cds = cds
        self.cpf = cpf
        self.bank_account = bank_account
        self.daily_allowance = daily_allowance

    def __str__(self) -> str:
        return f"{self.name} ({self.role})"

class TravelRequest:
    def __init__(self, objective: str, justification: str, travel_period: DateRange, itinerary: str, transportation: str, created_by: str, vehicle: Optional[str] = None, travelers: Optional[List[Traveler]] = None, created_at: Optional[datetime] = None):
        if not objective or not justification or not travel_period or not itinerary or not transportation or not created_by:
            raise ValueError("Campos obrigatórios da solicitação de viagem incompletos")
        self.objective = objective
        self.justification = justification
        self.travel_period = travel_period
        self.itinerary = itinerary
        self.transportation = transportation
        self.vehicle = vehicle
        self.created_by = created_by
        self.travelers = travelers if travelers is not None else []
        self.created_at = created_at if created_at is not None else datetime.now()

    def __str__(self) -> str:
        return f"Viagem para {self.objective} de {self.travel_period.start_date} a {self.travel_period.end_date}"
