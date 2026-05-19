# 📁 Caminho: root/marketplace/stores/views.py

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import Store
from .serializers import StoreSerializer, StorePublicSerializer
from .permissions import IsStoreOwner


class StoreListPublicView(generics.ListAPIView):
    """
    GET /api/stores/
    Lista pública de lojas ativas (carrossel da home).
    """
    serializer_class = StorePublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Store.objects.filter(is_active=True).order_by("name")


class StoreDetailPublicView(generics.RetrieveAPIView):
    """
    GET /api/stores/<slug>/
    Página pública de uma loja.
    """
    serializer_class = StorePublicSerializer
    permission_classes = [permissions.AllowAny]
    queryset = Store.objects.filter(is_active=True)
    lookup_field = "slug"


class MyStoreView(APIView):
    """
    GET    /api/stores/me/  → retorna a loja do vendedor logado
    POST   /api/stores/me/  → cria a loja (somente se não existir)
    PUT    /api/stores/me/  → atualiza a loja
    PATCH  /api/stores/me/  → atualização parcial
    DELETE /api/stores/me/  → desativa a loja (soft delete)
    """
    permission_classes = [permissions.IsAuthenticated]

    def _get_store(self, user):
        return get_object_or_404(Store, owner=user)

    def get(self, request):
        store = self._get_store(request.user)
        return Response(StoreSerializer(store).data)

    def post(self, request):
        if hasattr(request.user, "store"):
            return Response(
                {"detail": "Você já possui uma loja."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = StoreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        store = self._get_store(request.user)
        serializer = StoreSerializer(store, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        store = self._get_store(request.user)
        serializer = StoreSerializer(store, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        store = self._get_store(request.user)
        store.is_active = False
        store.save()
        return Response({"detail": "Loja desativada."}, status=status.HTTP_200_OK)