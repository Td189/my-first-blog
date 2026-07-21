from decimal import Decimal

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=120)

    weekly_sales = models.PositiveIntegerField(
        default=0
    )

    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
    )

    sale_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal("0.00"))
        ],
    )

    image_url = models.URLField(
    blank=True,
    help_text="Optional direct URL to a product image.",
)

    color = models.CharField(
    max_length=20,
    default="#2563eb",
)

    is_active = models.BooleanField(default=True)

    def clean(self):
        if self.sale_price > self.original_price:
            raise ValidationError(
                {
                    "sale_price": (
                        "Sale price cannot be greater "
                        "than the original price."
                    )
                }
            )

    def __str__(self):
        return self.name