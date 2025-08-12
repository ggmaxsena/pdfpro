from rest_framework import serializers

SIZE_LIMIT_BYTES = 1 * 1024 * 1024 * 1024  # 1 GB

class CompressPDFSerializer(serializers.Serializer):
    """
    Serializer para comprimir um arquivo PDF.
    """
    file = serializers.FileField()

class SplitByPagesSerializer(serializers.Serializer):
    """
    Serializer para dividir um arquivo PDF por páginas.
    """
    file = serializers.FileField()
    pages = serializers.CharField(help_text="Intervalo de páginas (ex: '1-5', '2,4,6')")

class SplitBySizeSerializer(serializers.Serializer):
    """
    Recebe o PDF original e o tamanho (em MB) desejado para
    cada parte gerada.
    """
    file = serializers.FileField()
    size_mb = serializers.IntegerField(
        min_value=1,
        max_value=1024,
        help_text="Tamanho máximo de cada parte, em MB (1-1024)."
    )

    def validate_file(self, value):
        """
        Garante que o arquivo de entrada não excede 1 GB.

        Args:
            value (File): O arquivo a ser validado.

        Raises:
            serializers.ValidationError: Se o arquivo exceder 1 GB.

        Returns:
            File: O arquivo validado.
        """
        if value.size > SIZE_LIMIT_BYTES:
            raise serializers.ValidationError("Arquivo acima de 1 GB.")
        return value