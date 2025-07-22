from rest_framework import serializers


class CompressPDFSerializer(serializers.Serializer):
    file = serializers.FileField()


class SplitByPagesSerializer(serializers.Serializer):
    file = serializers.FileField()
    pages = serializers.CharField()  # formato "inicio-fim"

    def validate_pages(self, value):
        try:
            start, end = map(int, value.split("-"))
            if start < 1 or end < start:
                raise ValueError
        except ValueError:
            raise serializers.ValidationError("Formato deve ser 'inicio-fim'.")
        return (start, end)


class SplitBySizeSerializer(serializers.Serializer):
    file = serializers.FileField()
    size = serializers.IntegerField(min_value=1)  # MB