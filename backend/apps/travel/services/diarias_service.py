from datetime import date
from decimal import Decimal
from ..repositories.per_diem_repository import PerDiemRepository
from ..domain.value_objects import DateRange, DailyAllowance, Money
from ..domain.entities import PerDiemRate as PerDiemRateEntity

class DiariasService:
    def __init__(self, per_diem_repository: PerDiemRepository = None):
        self.per_diem_repository = per_diem_repository or PerDiemRepository()

    def calculate(
        self, 
        cargo: str, 
        travel_period: DateRange, 
        cds: str = None, 
        fora_do_estado: bool = False, 
        via_aerea: bool = False, 
        exige_pernoite: bool = True
    ) -> DailyAllowance:
        """
        Calcula a quantidade de diárias e o valor total com base nas regras do Decreto.
        """
        if travel_period.end_date < travel_period.start_date:
            raise ValueError("A data de retorno não pode ser anterior à data de ida.")

        # Obter o valor unitário do repositório
        # Por enquanto, o repositório não usa CDS nem data de vigência
        per_diem_entity = self.per_diem_repository.get_rate_by_role(cargo, travel_period.start_date, cds)
        if not per_diem_entity:
            raise ValueError(f"Valor de diária não encontrado para o cargo: {cargo} e CDS: {cds}")
        
        base_unit_price = per_diem_entity.valor_nacional.amount # Usar valor_nacional como base

        dias = travel_period.days()
        qtd_diarias = Decimal("0.0")

        # Regra: Deslocamento inferior a 5 horas (Art. 6º, II)
        # Se a viagem é no mesmo dia e não exige pernoite, assume-se que é curta (< 5h)
        if dias == 1 and not exige_pernoite:
            qtd_diarias = Decimal("0.0")
        elif exige_pernoite:
            # Regra: Viagem exige pernoite (Diária cheia)
            # Cada dia conta como uma diária completa.
            qtd_diarias = Decimal(dias)
        else:
            # Regra: Retorno à sede no mesmo dia (Meia diária) para viagens de múltiplos dias sem pernoite
            # ou para viagens de um dia que não exigem pernoite e não são consideradas curtas.
            # A lógica anterior era: Decimal(dias - 1) + Decimal("1.0")
            # Vamos manter a lógica de (dias - 1) dias completos + 0.5 para o dia de retorno
            # para viagens de múltiplos dias sem pernoite explícita.
            qtd_diarias = Decimal(dias - 1) + Decimal("0.5")

        valor_unitario_calculado = base_unit_price

        # Regra: Viagem para fora do estado (Acréscimo +100%)
        if fora_do_estado:
            valor_unitario_calculado *= Decimal("2.0")

        # Regra: Viagem aérea (Acréscimo +30%)
        if via_aerea:
            valor_unitario_calculado *= Decimal("1.3")

        # Regra: Participação em cursos (16+ dias) - Redução 50% a partir da 16ª diária
        # Esta regra é mais complexa e pode ser implementada em uma iteração futura
        # ou como uma lógica separada que ajusta o total final.

        # Regra: Agente multiplicador (50% do menor valor de diária)
        # Esta regra também é mais complexa e pode ser implementada em uma iteração futura.

        # Regra: Despesas pagas por outro ente (Sem direito à diária)
        # Esta regra deve ser tratada na lógica de negócio que chama o serviço, 
        # possivelmente impedindo a chamada ou zerando o resultado.

        total_value = qtd_diarias * valor_unitario_calculado

        return DailyAllowance(
            quantity=qtd_diarias,
            unit_value=valor_unitario_calculado, # Passando Decimal
            total=total_value # Passando Decimal
        )
