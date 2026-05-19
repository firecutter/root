# 📁 Caminho: root/marketplace/marketplace/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # Autenticação e usuários
    path("api/auth/", include("accounts.urls")),

    # Lojas
    path("api/stores/", include("stores.urls")),

    # Produtos (a adicionar na próxima etapa)
    # path("api/products/", include("products.urls")),
]

# Serve arquivos de mídia em desenvolvimento
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)