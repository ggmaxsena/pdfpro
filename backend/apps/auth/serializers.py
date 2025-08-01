
from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de novos usuários.

    Valida e cria um novo usuário com e-mail, nome e senha.
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        """
        Cria e retorna um novo usuário.

        Args:
            validated_data (dict): Dados validados para a criação do usuário.

        Returns:
            CustomUser: O objeto de usuário criado.
        """
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir detalhes do usuário.

    Exibe e-mail e nome do usuário.
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'name')
