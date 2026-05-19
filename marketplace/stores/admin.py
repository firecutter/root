# 📁 Caminho: root/marketplace/stores/admin.py

from django.contrib import admin
from .models import Store


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "city", "state", "is_active", "created_at")
    list_filter = ("is_active", "state")
    search_fields = ("name", "owner__email", "slug", "cnpj_cpf")
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")