from django.db import models
from subscriptions.models import Subscription
from mptt.models import MPTTModel, TreeForeignKey
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from api.utils import generate_unique_slug
import uuid

class Category(MPTTModel):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=100)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    class MPTTModel:
        order_insertion_by = ['name']

    class Meta:
        unique_together = ('subscription', 'parent', 'name')
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='products',
        db_index=True
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products',
        db_index=True
    )
    name = models.CharField(
        max_length=100,
        db_index=True,
        help_text="Product name (up to 100 characters)"
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text="URL-friendly identifier for the product"
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Detailed description of the product"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="Regular price of the product"
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0.01)],
        help_text="Discounted price, if applicable"
    )
    stock = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Current stock quantity"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the product is available for purchase"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the product was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the product was last updated"
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ['subscription', 'slug']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['price']),
        ]
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_slug(self, self.name, Product)
        super().save(*args, **kwargs)

    def get_final_price(self):
        return self.discount_price if self.discount_price and self.discount_price > 0 else self.price

    def is_in_stock(self):
        return self.stock > 0

    def reduce_stock(self, quantity):
        if quantity < 0:
            raise ValueError("Quantity cannot be negative")
        if quantity > self.stock:
            raise ValueError("Insufficient stock")
        self.stock -= quantity
        self.save()

    @property
    def has_discount(self):
        return self.discount_price is not None and self.discount_price < self.price
