
import re

# ---------------- Masking Functions ---------------- #

def _digits(s: str) -> str:
    """Removes non-digit characters from a string."""
    return re.sub(r"\D", "", s or "")

def mask_cpf(s: str) -> str:
    d = _digits(s)
    return f"XXX.{d[3:6]}.{d[6:9]}-XX" if len(d) == 11 else s

def mask_rg(s: str) -> str:
    d = _digits(s)
    return f"XX{d[2:-2]}XX" if len(d) > 4 else "XX"

def mask_name(s: str) -> str:
    parts = str(s).strip().split()
    if len(parts) > 1:
        return f'{parts[0]} {" ".join(p[0] + "." for p in parts[1:])}'
    return (parts[0][0] + ".") if parts else ""

def mask_email(s: str) -> str:
    if "@" in s:
        user, domain = s.split("@", 1)
        return f'{"x" * len(user)}@{domain}'
    return s

def mask_telefone(s: str) -> str:
    d = _digits(s)
    if len(d) > 4:
        return f'{"*" * (len(d) - 2)}{d[-2:]}'
    return "**"

def mask_address(s: str) -> str:
    # Removes numbers, specific identifiers, keeps general location
    return re.sub(r'\d+|\b(apto|apartamento|bloco|casa|n[º°])\b', '', s, flags=re.I).strip()

def mask_cep(s: str) -> str:
    d = _digits(s)
    return f"{d[:2]}XXX-XXX" if len(d) == 8 else s

def mask_ip(s: str) -> str:
    return "XXX.XXX.XXX.XXX"

def mask_date(s: str) -> str:
    # Keeps the year
    match = re.search(r'(\d{4})', s)
    return f"XX/XX/{match.group(1)}" if match else "XX/XX/XXXX"

def mask_financial(s: str) -> str:
    return "XXXX.XXXX.XXXX.XXXX"

def mask_sensitive_generic(label: str):
    def mask(s: str) -> str:
        return f"[{label}]"
    return mask

def mask_processo(s: str) -> str:
    return "Não informado"

# ---------------- Token Definitions ---------------- #
# Each token is a tuple: (compiled_regex, masking_function)

TOKENS = {
    # Direct Identifiers
    "nome": (re.compile(r'\b(nome(.+)?|titular)\b', re.I), mask_name),
    "cpf": (re.compile(r'\bcpf\b', re.I), mask_cpf),
    "rg": (re.compile(r'\b(rg|identidade)\b', re.I), mask_rg),
    "cnh": (re.compile(r'\bcnh\b', re.I), mask_rg), # Similar masking
    "passport": (re.compile(r'\bpassaporte\b', re.I), mask_rg), # Similar masking
    "titulo_eleitor": (re.compile(r't[íi]tulo.*eleitor', re.I), mask_rg), # Similar
    "pis_pasep": (re.compile(r'\b(pis|pasep)\b', re.I), mask_rg), # Similar

    # Contact / Address
    "email": (re.compile(r'e-?mail', re.I), mask_email),
    "telefone": (re.compile(r'\b(celular|fone|telefone)\b', re.I), mask_telefone),
    "endereco": (re.compile(r'\bendere[cç]o\b', re.I), mask_address),
    "cep": (re.compile(r'\bcep\b', re.I), mask_cep),

    # Device Identifiers
    "ip": (re.compile(r'\bip(_address)?\b', re.I), mask_ip),
    "mac": (re.compile(r'\bmac[_ ]?addr', re.I), mask_ip), # Similar
    "imei": (re.compile(r'\bimei\b', re.I), mask_ip), # Similar

    # Location
    "geoloc": (re.compile(r'\b(lat(itude)?|long(itude)?|geo|gps)\b', re.I), mask_address),

    # Vehicle
    "placa": (re.compile(r'\bplaca.*ve[ií]culo\b', re.I), lambda s: f"XXX-{''.join(filter(str.isdigit, s))[-4:] if any(c.isdigit() for c in s) else 'XXXX'}"),

    # Quasi-identifiers
    "data_nasc": (re.compile(r'\bdata.*nasc', re.I), mask_date),
    "idade": (re.compile(r'\bidade\b', re.I), lambda s: "**"),
    "sexo": (re.compile(r'\b(sexo|g[êe]nero)\b', re.I), lambda s: "[GÊNERO]"),
    "nacionalidade": (re.compile(r'\bnacionalidade\b', re.I), lambda s: "[NACIONALIDADE]"),
    "estado_civil": (re.compile(r'\bestado.?civil\b', re.I), lambda s: "[ESTADO CIVIL]"),

    # Financial
    "cartao": (re.compile(r'\b(cart[aã]o.*cr[eé]dito|cc|nib)\b', re.I), mask_financial),
    "renda": (re.compile(r'\b(renda|sal[aá]rio)\b', re.I), lambda s: "[RENDA]"),

    # Sensitive (art. 5º II)
    "saude": (re.compile(r'\b(laudo|cid|doen[cç]a|sa[úu]de)\b', re.I), mask_sensitive_generic("SAÚDE")),
    "religiao": (re.compile(r'\breligi', re.I), mask_sensitive_generic("RELIGIÃO")),
    "opiniao_politica": (re.compile(r'\bpolitic', re.I), mask_sensitive_generic("OPINIÃO POLÍTICA")),
    "sindicato": (re.compile(r'\bsindic', re.I), mask_sensitive_generic("FILIAÇÃO SINDICAL")),
    "biometria": (re.compile(r'\bbiometr', re.I), mask_sensitive_generic("BIOMETRIA")),

    # Internal Process
    "processo": (re.compile(r'\bprocesso(\s*n[oú]m\.?)?\b', re.I), mask_processo),
}

def discover_tokens_in_headers(headers: list[str]) -> dict[str, list[int]]:
    """
    Scans headers and returns a dictionary mapping detected token keys to the column indices where they were found.
    e.g., {'cpf': [1, 5], 'nome': [0]}
    """
    detected = {}
    for idx, header_text in enumerate(headers):
        if not header_text:
            continue
        for key, (rx, _) in TOKENS.items():
            if rx.search(header_text):
                if key not in detected:
                    detected[key] = []
                detected[key].append(idx)
    return detected
