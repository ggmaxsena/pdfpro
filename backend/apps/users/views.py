
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import RegisterSerializer, CustomUserSerializer

class RegisterView(generics.CreateAPIView):
    """
    View para registro de novos usuários.

    Permite que usuários não autenticados criem uma nova conta.
    """
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

class UserView(generics.RetrieveAPIView):
    """
    View para recuperar os detalhes do usuário autenticado.

    Requer autenticação.
    """
    serializer_class = CustomUserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        """
        Retorna o objeto de usuário autenticado.

        Returns:
            User: O objeto de usuário autenticado.
        """
        return self.request.user

