# 📁 Caminho: root/marketplace/stores/serializers.py

from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source="owner.email", read_only=True)

    class Meta:
        model = Store
        fields = (
            "id", "owner_email", "name", "slug", "description",
            "logo", "banner", "cnpj_cpf", "email", "phone",
            "zip_code", "street", "number", "complement",
            "neighborhood", "city", "state",
            "is_active", "created_at", "updated_at",
        )
        read_only_fields = ("id", "owner_email", "created_at", "updated_at")


class StorePublicSerializer(serializers.ModelSerializer):
    """Versão reduzida para listagem pública (carrossel da home)."""

    class Meta:
        model = Store
        fields = ("id", "name", "slug", "description", "logo", "banner", "city", "state")