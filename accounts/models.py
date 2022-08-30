from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.manager import AccountManager


class Account(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(max_length=150, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField(default=False)

    username = None

    objects = AccountManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
