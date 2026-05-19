# 📁 Caminho: root/marketplace/accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Usuário customizado do marketplace.
    Substitui o User padrão do Django (AUTH_USER_MODEL = 'accounts.User').
    """

    class UserType(models.TextChoices):
        VENDEDOR = "vendedor", "Vendedor"
        COMPRADOR = "comprador", "Comprador"

    user_type = models.CharField(
        max_length=20,
        choices=UserType.choices,
        default=UserType.COMPRADOR,
    )
    phone = models.CharField(max_length=20, blank=True, null=True)

    # Usamos email como identificador de login
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email

    @property
    def is_vendedor(self):
        return self.user_type == self.UserType.VENDEDOR

    @property
    def is_comprador(self):
        return self.user_type == self.UserType.COMPRADOR