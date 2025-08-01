
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    """
    Gerenciador de modelos personalizado para CustomUser.
    """
    def create_user(self, email, name, password=None, **extra_fields):
        """
        Cria e salva um usuário com o e-mail e senha fornecidos.

        Args:
            email (str): O endereço de e-mail do usuário.
            name (str): O nome do usuário.
            password (str, optional): A senha do usuário. Defaults to None.
            **extra_fields: Campos adicionais para o modelo de usuário.

        Returns:
            CustomUser: O objeto de usuário criado.

        Raises:
            ValueError: Se o e-mail não for fornecido.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """
        Cria e salva um superusuário com o e-mail e senha fornecidos.

        Args:
            email (str): O endereço de e-mail do superusuário.
            name (str): O nome do superusuário.
            password (str, optional): A senha do superusuário. Defaults to None.
            **extra_fields: Campos adicionais para o modelo de superusuário.

        Returns:
            CustomUser: O objeto de superusuário criado.

        Raises:
            ValueError: Se is_staff ou is_superuser não forem True.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuário personalizado que usa e-mail como identificador.
    """
    email: models.EmailField = models.EmailField(unique=True)
    name: models.CharField = models.CharField(max_length=255)
    is_active: models.BooleanField = models.BooleanField(default=True)
    is_staff: models.BooleanField = models.BooleanField(default=False)
    date_joined: models.DateTimeField = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """
        Retorna a representação em string do usuário (e-mail).
        """
        return self.email
