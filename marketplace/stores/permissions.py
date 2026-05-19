# 📁 Caminho: root/marketplace/stores/permissions.py

from rest_framework.permissions import BasePermission


class IsStoreOwner(BasePermission):
    """Permite acesso apenas ao dono da loja."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsVendedor(BasePermission):
    """Permite acesso apenas a usuários do tipo vendedor."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_vendedor