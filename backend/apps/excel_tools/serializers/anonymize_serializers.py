from rest_framework import serializers

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

class AnonymizeNameSerializer(serializers.Serializer):
    """
    Recebe uma planilha Excel (`.xlsx`) e anonimiza apenas a coluna **Nome**.
    """
    file = serializers.FileField()
    sheet = serializers.CharField(
        required=False,
        help_text="Nome da planilha (aba). Se omitido, usa a primeira."
    )
    
    def validate_file(self, value):
        if value.size > MAX_FILE_SIZE:
            raise serializers.ValidationError("Arquivo maior que 10 MB.")
        if not value.name.lower().endswith(".xlsx"):
            raise serializers.ValidationError("Apenas arquivos .xlsx são aceitos.")
        return value
