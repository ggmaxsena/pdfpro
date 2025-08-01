import re
from typing import Callable, Dict, List, Pattern, Tuple


class MaskingFunctions:
    """
    Funções de mascaramento para diferentes tipos de dados sensíveis.
    """

    @staticmethod
    def _digits(s: str) -> str:
        """
        Remove caracteres não numéricos de uma string.

        Args:
            s: A string de entrada.

        Returns:
            A string contendo apenas dígitos.
        """
        return re.sub(r"\D", "", s or "")

    @classmethod
    def mask_cpf(cls, s: str) -> str:
        """
        Mascarar um CPF.

        Args:
            s: O CPF a ser mascarado.

        Returns:
            O CPF mascarado.
        """
        d = cls._digits(s)
        return f"XXX.{d[3:6]}.{d[6:9]}-XX" if len(d) == 11 else s

    @classmethod
    def mask_rg(cls, s: str) -> str:
        """
        Mascarar um RG.

        Args:
            s: O RG a ser mascarado.

        Returns:
            O RG mascarado.
        """
        d = cls._digits(s)
        return f"XX{d[2:-2]}XX" if len(d) > 4 else "XX"

    @classmethod
    def mask_name(cls, s: str) -> str:
        """
        Mascarar um nome.

        Args:
            s: O nome a ser mascarado.

        Returns:
            O nome mascarado.
        """
        parts = str(s).strip().split()
        if len(parts) > 1:
            return f'{parts[0]} {" ".join(p[0] + "." for p in parts[1:])}'
        return (parts[0][0] + ".") if parts else ""

    @classmethod
    def mask_email(cls, s: str) -> str:
        """
        Mascarar um endereço de e-mail.

        Args:
            s: O e-mail a ser mascarado.

        Returns:
            O e-mail mascarado.
        """
        if "@" in s:
            user, domain = s.split("@", 1)
            return f'{"x" * len(user)}@{domain}'
        return s

    @classmethod
    def mask_telefone(cls, s: str) -> str:
        """
        Mascarar um número de telefone.

        Args:
            s: O telefone a ser mascarado.

        Returns:
            O telefone mascarado.
        """
        d = cls._digits(s)
        if len(d) > 4:
            return f'{"*" * (len(d) - 2)}{d[-2:]}'
        return "**"

    @classmethod
    def mask_address(cls, s: str) -> str:
        """
        Mascarar um endereço.

        Args:
            s: O endereço a ser mascarado.

        Returns:
            O endereço mascarado.
        """
        return re.sub(r'\d+|\b(apto|apartamento|bloco|casa|n[º°])\b', '', s, flags=re.I).strip()

    @classmethod
    def mask_cep(cls, s: str) -> str:
        """
        Mascarar um CEP.

        Args:
            s: O CEP a ser mascarado.

        Returns:
            O CEP mascarado.
        """
        d = cls._digits(s)
        return f"{d[:2]}XXX-XXX" if len(d) == 8 else s

    @classmethod
    def mask_ip(cls, s: str) -> str:
        """
        Mascarar um endereço IP.

        Args:
            s: O IP a ser mascarado.

        Returns:
            O IP mascarado.
        """
        return "XXX.XXX.XXX.XXX"

    @classmethod
    def mask_date(cls, s: str) -> str:
        """
        Mascarar uma data, mantendo apenas o ano.

        Args:
            s: A data a ser mascarada.

        Returns:
            A data mascarada.
        """
        match = re.search(r'(\d{4})', s)
        return f"XX/XX/{match.group(1)}" if match else "XX/XX/XXXX"

    @classmethod
    def mask_financial(cls, s: str) -> str:
        """
        Mascarar dados financeiros.

        Args:
            s: Os dados financeiros a serem mascarados.

        Returns:
            Os dados financeiros mascarados.
        """
        return "XXXX.XXXX.XXXX.XXXX"

    @staticmethod
    def mask_sensitive_generic(label: str) -> Callable[[str], str]:
        """
        Gera uma função de mascaramento genérica para dados sensíveis.

        Args:
            label: O rótulo para o dado sensível.

        Returns:
            Uma função que mascara a string com o rótulo.
        """
        def mask(s: str) -> str:
            return f"[{label}]"
        return mask

    @classmethod
    def mask_processo(cls, s: str) -> str:
        """
        Mascarar um número de processo.

        Args:
            s: O número de processo a ser mascarado.

        Returns:
            O número de processo mascarado.
        """
        return "Não informado"


# ---------------- Token Definitions ---------------- #
# Each token is a tuple: (compiled_regex, masking_function)

TOKENS: Dict[str, Tuple[Pattern[str], Callable[[str], str]]] = {
    # Direct Identifiers
    "nome": (re.compile(r'\b(nome(.+)?|titular)\b', re.I), MaskingFunctions.mask_name),
    "cpf": (re.compile(r'\bcpf\b', re.I), MaskingFunctions.mask_cpf),
    "rg": (re.compile(r'\b(rg|identidade)\b', re.I), MaskingFunctions.mask_rg),
    "cnh": (re.compile(r'\bcnh\b', re.I), MaskingFunctions.mask_rg), # Similar masking
    "passport": (re.compile(r'\bpassaporte\b', re.I), MaskingFunctions.mask_rg), # Similar masking
    "titulo_eleitor": (re.compile(r't[íi]tulo.*eleitor', re.I), MaskingFunctions.mask_rg), # Similar
    "pis_pasep": (re.compile(r'\b(pis|pasep)\b', re.I), MaskingFunctions.mask_rg), # Similar

    # Contact / Address
    "email": (re.compile(r'e-?mail', re.I), MaskingFunctions.mask_email),
    "telefone": (re.compile(r'\b(celular|fone|telefone)\b', re.I), MaskingFunctions.mask_telefone),
    "endereco": (re.compile(r'\bendere[cç]o\b', re.I), MaskingFunctions.mask_address),
    "cep": (re.compile(r'\bcep\b', re.I), MaskingFunctions.mask_cep),

    # Device Identifiers
    "ip": (re.compile(r'\bip(_address)?\b', re.I), MaskingFunctions.mask_ip),
    "mac": (re.compile(r'\bmac[_ ]?addr', re.I), MaskingFunctions.mask_ip), # Similar
    "imei": (re.compile(r'\bimei\b', re.I), MaskingFunctions.mask_ip), # Similar

    # Location
    "geoloc": (re.compile(r'\b(lat(itude)?|long(itude)?|geo|gps)\b', re.I), MaskingFunctions.mask_address),

    # Vehicle
    "placa": (re.compile(r'\bplaca.*ve[ií]culo\b', re.I), lambda s: f"XXX-{''.join(filter(str.isdigit, s))[-4:] if any(c.isdigit() for c in s) else 'XXXX'}"),

    # Quasi-identifiers
    "data_nasc": (re.compile(r'\bdata.*nasc', re.I), MaskingFunctions.mask_date),
    "idade": (re.compile(r'\bidade\b', re.I), lambda s: "**"),
    "sexo": (re.compile(r'\b(sexo|g[êe]nero)\b', re.I), lambda s: "[GÊNERO]"),
    "nacionalidade": (re.compile(r'\bnacionalidade\b', re.I), MaskingFunctions.mask_sensitive_generic("NACIONALIDADE")),
    "estado_civil": (re.compile(r'\bestado.?civil\b', re.I), MaskingFunctions.mask_sensitive_generic("ESTADO CIVIL")),

    # Financial
    "cartao": (re.compile(r'\b(cart[aã]o.*cr[eé]dito|cc|nib)\b', re.I), MaskingFunctions.mask_financial),
    "renda": (re.compile(r'\b(renda|sal[aá]rio)\b', re.I), MaskingFunctions.mask_sensitive_generic("RENDA")),

    # Sensitive (art. 5º II)
    "saude": (re.compile(r'\b(laudo|cid|doen[cç]a|sa[úu]de)\b', re.I), MaskingFunctions.mask_sensitive_generic("SAÚDE")),
    "religiao": (re.compile(r'\breligi', re.I), MaskingFunctions.mask_sensitive_generic("RELIGIÃO")),
    "opiniao_politica": (re.compile(r'\bpolitic', re.I), MaskingFunctions.mask_sensitive_generic("OPINIÃO POLÍTICA")),
    "sindicato": (re.compile(r'\bsindic', re.I), MaskingFunctions.mask_sensitive_generic("FILIAÇÃO SINDICAL")),
    "biometria": (re.compile(r'\bbiometr', re.I), MaskingFunctions.mask_sensitive_generic("BIOMETRIA")),

    # Internal Process
    "processo": (re.compile(r'\bprocesso(\s*n[oú]m\.?)?\b', re.I), MaskingFunctions.mask_processo),
}

def discover_tokens_in_headers(headers: list[str]) -> dict[str, list[int]]:
    """
    Scans headers and returns a dictionary mapping detected token keys to the column indices where they were found.
    e.g., {'cpf': [1, 5], 'nome': [0]}
    """
    detected: Dict[str, List[int]] = {}
    for idx, header_text in enumerate(headers):
        if not header_text:
            continue
        for key, (rx, _) in TOKENS.items():
            if rx.search(header_text):
                if key not in detected:
                    detected[key] = []
                detected[key].append(idx)
    return detected