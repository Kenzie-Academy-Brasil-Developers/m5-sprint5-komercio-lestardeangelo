from uuid import uuid4
from django.db import models


class Product(models.Model):

    product_uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    description = models.TextField()
    price = models.FloatField()
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    user = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="products"
    )
