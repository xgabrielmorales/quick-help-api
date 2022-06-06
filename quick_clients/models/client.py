# Django
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
# Local
from quick_clients.models.clientManager import ClientManager


class Client(AbstractBaseUser, PermissionsMixin):
    client_id = models.BigAutoField(
        "Identificador Único de Cliente",
        primary_key=True
    )

    document = models.CharField(
       "Documento de Identidad",
       max_length=11,
       unique=True,
    )

    first_name = models.CharField(
        "Nombre",
        max_length=120,
    )
    last_name = models.CharField(
        "Apellido",
        max_length=120
    )

    username = models.CharField(
        'Username',
        max_length=15,
        unique=True
    )

    email = models.EmailField(
        "Email",
        unique=True
    )

    password = models.CharField(
        "Password",
        max_length=256,
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "first_name", "last_name", "document"]

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
