from uuid import uuid4
from django.core.validators import MinValueValidator

from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    description = models.TextField()
    price = models.FloatField(validators=[MinValueValidator(0.01)])
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey(
        to="accounts.Account",
        on_delete=models.CASCADE,
        related_name="products",
    )
