# 📁 Caminho: root/marketplace/stores/models.py

from django.db import models
from django.conf import settings


class Store(models.Model):
    """
    Loja de um vendedor. Cada usuário vendedor possui no máximo uma loja.
    """
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="store",
        verbose_name="Proprietário",
    )
    name = models.CharField("Nome", max_length=150)
    slug = models.SlugField("Slug", max_length=160, unique=True)
    description = models.TextField("Descrição", blank=True)
    logo = models.ImageField("Logo", upload_to="stores/logos/", null=True, blank=True)
    banner = models.ImageField("Banner", upload_to="stores/banners/", null=True, blank=True)
    cnpj_cpf = models.CharField("CNPJ / CPF", max_length=18, blank=True)
    email = models.EmailField("E-mail da loja", blank=True)
    phone = models.CharField("Telefone", max_length=20, blank=True)

    # Endereço da loja (usado no cálculo de frete)
    zip_code = models.CharField("CEP", max_length=9, blank=True)
    street = models.CharField("Rua", max_length=255, blank=True)
    number = models.CharField("Número", max_length=10, blank=True)
    complement = models.CharField("Complemento", max_length=100, blank=True)
    neighborhood = models.CharField("Bairro", max_length=100, blank=True)
    city = models.CharField("Cidade", max_length=100, blank=True)
    state = models.CharField("UF", max_length=2, blank=True)

    is_active = models.BooleanField("Ativa", default=True)
    created_at = models.DateTimeField("Criada em", auto_now_add=True)
    updated_at = models.DateTimeField("Atualizada em", auto_now=True)

    class Meta:
        verbose_name = "Loja"
        verbose_name_plural = "Lojas"
        ordering = ["name"]

    def __str__(self):
        return self.name