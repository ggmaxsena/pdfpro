
from django.test import TestCase
from .tokens import discover_tokens_in_headers, MaskingFunctions

class TokenLogicTestCase(TestCase):

    def test_masking_functions(self):
        """Test individual masking functions for correctness."""
        self.assertEqual(MaskingFunctions.mask_cpf("12345678901"), "XXX.456.789-XX")
        self.assertEqual(MaskingFunctions.mask_name("Fulano de Tal"), "Fulano d. T.")
        self.assertEqual(MaskingFunctions.mask_name("Ciclano"), "C.")
        self.assertEqual(MaskingFunctions.mask_email("teste@exemplo.com"), "xxxxx@exemplo.com")

    def test_discover_tokens_in_headers(self):
        """Test the discovery of tokens from a list of header strings."""
        headers = [
            "Nome Completo do Titular",  # nome
            "Documento CPF",             # cpf
            "Endereço de E-mail",        # email
            "Salário Bruto",             # renda
            "Número do Processo"         # processo
        ]
        
        expected_tokens = {
            "nome": [0],
            "cpf": [1],
            "email": [2],
            "renda": [3],
            "processo": [4]
        }
        
        discovered = discover_tokens_in_headers(headers)
        self.assertDictEqual(discovered, expected_tokens)

    def test_discover_tokens_case_insensitivity(self):
        """Ensure token discovery is case-insensitive."""
        headers = ["cpf", "NOME", "E-MAIL"]
        expected_tokens = {"cpf": [0], "nome": [1], "email": [2]}
        discovered = discover_tokens_in_headers(headers)
        self.assertDictEqual(discovered, expected_tokens)

    def test_no_tokens_found(self):
        """Test that no tokens are found when headers don't match."""
        headers = ["Coluna 1", "Coluna 2", "Dados Aleatórios"]
        discovered = discover_tokens_in_headers(headers)
        self.assertDictEqual(discovered, {})
