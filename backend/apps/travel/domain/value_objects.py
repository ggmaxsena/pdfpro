import re
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Union

class CPF:
    def __init__(self, value: str):
        if not isinstance(value, str):
            raise TypeError("CPF deve ser uma string")
        self.value = self._clean(value)
        if not self.is_valid(self.value):
            raise ValueError("CPF inválido")

    def _clean(self, cpf: str) -> str:
        return re.sub(r'[^0-9]', '', cpf)

    @staticmethod
    def is_valid(cpf: str) -> bool:
        cpf = re.sub(r'[^0-9]', '', cpf) # Garante que o CPF esteja limpo para validação

        if len(cpf) != 11 or not cpf.isdigit():
            return False

        # Elimina CPFs com todos os dígitos iguais
        if len(set(cpf)) == 1:
            return False

        # Validação dos dígitos verificadores
        def calculate_digit(numbers_str, weights):
            soma = 0
            for i in range(len(numbers_str)):
                soma += int(numbers_str[i]) * weights[i]
            resto = (soma * 10) % 11
            return resto if resto < 10 else 0

        # Pesos para o primeiro dígito verificador
        weights_1 = list(range(10, 1, -1)) # [10, 9, 8, 7, 6, 5, 4, 3, 2]
        primeiro_digito = calculate_digit(cpf[:9], weights_1)
        if primeiro_digito != int(cpf[9]):
            return False

        # Pesos para o segundo dígito verificador
        weights_2 = list(range(11, 1, -1)) # [11, 10, 9, 8, 7, 6, 5, 4, 3, 2]
        segundo_digito = calculate_digit(cpf[:10], weights_2)
        if segundo_digito != int(cpf[10]):
            return False

        return True

    def masked(self) -> str:
        return f"***.***.{self.value[6:9]}-{self.value[9:]}"

    def __str__(self) -> str:
        return f"{self.value[:3]}.{self.value[3:6]}.{self.value[6:9]}-{self.value[9:]}"

    def __eq__(self, other):
        if not isinstance(other, CPF):
            return NotImplemented
        return self.value == other.value

    def __hash__(self):
        return hash(self.value)

class Money:
    def __init__(self, value: Union[str, float, Decimal]):
        try:
            self.amount = Decimal(value).quantize(Decimal("0.01"))
        except (InvalidOperation, TypeError):
            raise ValueError("Valor monetário inválido")

    def __str__(self) -> str:
        return f"R$ {self.amount:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def __repr__(self) -> str:
        return f"Money(amount={self.amount})"

    def __eq__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount == other.amount

    def __hash__(self):
        return hash(self.amount)

class BankAccount:
    def __init__(self, agency: str, account_number: str, bank_name: str):
        if not agency or not account_number or not bank_name:
            raise ValueError("Dados da conta bancária incompletos")
        self.agency = agency
        self.account_number = account_number
        self.bank_name = bank_name

    def __str__(self) -> str:
        return f"{self.bank_name} - Ag: {self.agency}, C/C: {self.account_number}"

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.agency == other.agency and \
               self.account_number == other.account_number and \
               self.bank_name == other.bank_name

    def __hash__(self):
        return hash((self.agency, self.account_number, self.bank_name))

class DateRange:
    def __init__(self, start_date: date, end_date: date):
        if not isinstance(start_date, date) or not isinstance(end_date, date):
            raise TypeError("As datas devem ser objetos date")
        if end_date < start_date:
            raise ValueError("A data final não pode ser anterior à data inicial")
        self.start_date = start_date
        self.end_date = end_date

    def days(self) -> int:
        return (self.end_date - self.start_date).days + 1

    def __str__(self) -> str:
        return f"{self.start_date.strftime('%d/%m/%Y')} a {self.end_date.strftime('%d/%m/%Y')}"

    def __eq__(self, other):
        if not isinstance(other, DateRange):
            return NotImplemented
        return self.start_date == other.start_date and self.end_date == other.end_date

    def __hash__(self):
        return hash((self.start_date, self.end_date))

class DailyAllowance:
    def __init__(self, quantity: Decimal, unit_value: Decimal, total: Decimal):
        if not isinstance(quantity, Decimal) or not isinstance(unit_value, Decimal) or not isinstance(total, Decimal):
            raise TypeError("Quantidade, valor unitário e total devem ser Decimais")
        if quantity < 0 or unit_value < 0 or total < 0:
            raise ValueError("Valores não podem ser negativos")
        self.quantity = quantity
        self.unit_value = unit_value
        self.total = total

    def __str__(self) -> str:
        return f"Diárias: {self.quantity}, Unitário: R$ {self.unit_value}, Total: R$ {self.total}"

    def __eq__(self, other):
        if not isinstance(other, DailyAllowance):
            return NotImplemented
        return self.quantity == other.quantity and \
               self.unit_value == other.unit_value and \
               self.total == other.total

    def __hash__(self):
        return hash((self.quantity, self.unit_value, self.total))