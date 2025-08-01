
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class MyTokenObtainPairView(TokenObtainPairView):
    """
    View personalizada para obter tokens JWT.

    Define cookies HTTP-only para os tokens de acesso e refresh.
    """
    def post(self, request, *args, **kwargs):
        """
        Processa a requisição POST para obter tokens.

        Args:
            request (HttpRequest): O objeto de requisição.
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave.

        Returns:
            Response: A resposta HTTP com os tokens em cookies.
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.pop('access')
            refresh_token = response.data.pop('refresh')

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure=True # Set to True in production
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                samesite='Lax',
                secure=True # Set to True in production
            )
        
        return response

class MyTokenRefreshView(TokenRefreshView):
    """
    View personalizada para atualizar tokens JWT.

    Obtém o token de refresh dos cookies e define um novo token de acesso em cookie.
    """
    def post(self, request, *args, **kwargs):
        """
        Processa a requisição POST para atualizar tokens.

        Args:
            request (HttpRequest): O objeto de requisição.
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave.

        Returns:
            Response: A resposta HTTP com o novo token de acesso em cookie.
        """
        request.data['refresh'] = request.COOKIES.get('refresh_token')
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.pop('access')
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                samesite='Lax',
                secure=True # Set to True in production
            )

        return response

class LogoutView(APIView):
    """
    View para realizar logout.

    Remove os cookies de tokens de acesso e refresh.
    """
    def post(self, request, *args, **kwargs):
        """
        Processa a requisição POST para logout.

        Args:
            request (HttpRequest): O objeto de requisição.
            *args: Argumentos posicionais.
            **kwargs: Argumentos de palavra-chave.

        Returns:
            Response: A resposta HTTP com status 204 (No Content).
        """
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        return response
