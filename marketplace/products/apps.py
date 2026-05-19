from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
 
# Lazy import to avoid circular dependency – adjust if you use AUTH_USER_MODEL setting
from django.conf import settings
 
 
# ---------------------------------------------------------------------------
# Category
# ---------------------------------------------------------------------------
 
class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Nome do ícone (ex: tabler-icon)")
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
    )
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
 
    def __str__(self):
        return self.name
 
 
# ---------------------------------------------------------------------------
# Product
# ---------------------------------------------------------------------------
 
class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    store = models.ForeignKey(
        "stores.Store", on_delete=models.CASCADE, related_name="products"
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=270, unique=True)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    # Shipping attributes (used by Correios API)
    weight_kg = models.DecimalField(max_digits=6, decimal_places=3, default=0)
    length_cm = models.PositiveSmallIntegerField(default=0)
    width_cm = models.PositiveSmallIntegerField(default=0)
    height_cm = models.PositiveSmallIntegerField(default=0)
 
    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
 
    def __str__(self):
        return self.name
 
 
# ---------------------------------------------------------------------------
# Product Image
# ---------------------------------------------------------------------------
 
class ProductImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="products/images/")
    alt_text = models.CharField(max_length=150, blank=True)
    order = models.PositiveSmallIntegerField(default=0)
    is_cover = models.BooleanField(default=False)
 
    class Meta:
        ordering = ["order"]
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens dos Produtos"
 
 
# ---------------------------------------------------------------------------
# Variation Type  (ex: Cor, Tamanho)
# ---------------------------------------------------------------------------
 
class VariationType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)  # "Cor", "Tamanho", "Material"
 
    class Meta:
        verbose_name = "Tipo de Variação"
        verbose_name_plural = "Tipos de Variação"
 
    def __str__(self):
        return self.name
 
 
# ---------------------------------------------------------------------------
# Product Variant  (ex: Azul / M)
# ---------------------------------------------------------------------------
 
class ProductVariant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="variants"
    )
    sku = models.CharField(max_length=100, unique=True)
    price_override = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Se preenchido, substitui o preço base do produto.",
    )
    stock = models.PositiveIntegerField(default=0)
    image = models.ForeignKey(
        ProductImage,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="variants",
    )
 
    class Meta:
        verbose_name = "Variante do Produto"
        verbose_name_plural = "Variantes dos Produtos"
 
    @property
    def effective_price(self):
        return self.price_override if self.price_override is not None else self.product.base_price
 
    def __str__(self):
        return self.sku
 
 
# ---------------------------------------------------------------------------
# Variant Attribute  (ex: variante X → Cor: Azul)
# ---------------------------------------------------------------------------
 
class VariantAttribute(models.Model):
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="attributes"
    )
    type = models.ForeignKey(VariationType, on_delete=models.PROTECT)
    value = models.CharField(max_length=100)
 
    class Meta:
        unique_together = ("variant", "type")
        verbose_name = "Atributo da Variante"
        verbose_name_plural = "Atributos das Variantes"
 
    def __str__(self):
        return f"{self.type.name}: {self.value}"
 
 
# ---------------------------------------------------------------------------
# Cart & CartItem
# ---------------------------------------------------------------------------
 
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        verbose_name = "Carrinho"
        verbose_name_plural = "Carrinhos"
 
    def __str__(self):
        return f"Carrinho de {self.user.email}"
 
 
class CartItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.CASCADE, related_name="cart_items"
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        unique_together = ("cart", "variant")
        verbose_name = "Item do Carrinho"
        verbose_name_plural = "Itens do Carrinho"
 
    @property
    def subtotal(self):
        return self.variant.effective_price * self.quantity
 
 
# ---------------------------------------------------------------------------
# Order & OrderItem
# ---------------------------------------------------------------------------
 
class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Aguardando pagamento"
        PAID = "paid", "Pago"
        PROCESSING = "processing", "Em processamento"
        SHIPPED = "shipped", "Enviado"
        DELIVERED = "delivered", "Entregue"
        CANCELLED = "cancelled", "Cancelado"
        REFUNDED = "refunded", "Reembolsado"
 
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="orders",
    )
    store = models.ForeignKey(
        "stores.Store", on_delete=models.PROTECT, related_name="orders"
    )
    status = models.CharField(
        max_length=15, choices=Status.choices, default=Status.PENDING
    )
    shipping_address = models.ForeignKey(
        "stores.Address",
        null=True,
        on_delete=models.SET_NULL,
        related_name="orders",
    )
 
    # Totals (denormalised for historical accuracy)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
 
    # PIX payment
    pix_txid = models.CharField(max_length=35, blank=True)
    pix_qr_code = models.TextField(blank=True)
    pix_expires_at = models.DateTimeField(null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
 
    # Shipping
    tracking_code = models.CharField(max_length=50, blank=True)
    shipping_service = models.CharField(max_length=50, blank=True, help_text="PAC, SEDEX, etc.")
    estimated_delivery = models.DateField(null=True, blank=True)
 
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
 
    def __str__(self):
        return f"Pedido {self.id} – {self.buyer.email}"
 
 
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    variant = models.ForeignKey(
        ProductVariant, on_delete=models.PROTECT, related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
 
    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens dos Pedidos"
 
    @property
    def subtotal(self):
        return self.unit_price * self.quantity
 
 
# ---------------------------------------------------------------------------
# Review
# ---------------------------------------------------------------------------
 
class Review(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    order_item = models.OneToOneField(
        OrderItem,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="review",
        help_text="Garante que apenas compradores verificados avaliem.",
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=120, blank=True)
    body = models.TextField(blank=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
 
    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Avaliação"
        verbose_name_plural = "Avaliações"
 
    def __str__(self):
        return f"{self.rating}★ – {self.product.name} por {self.author.email}"
