# Django
from django.db import models
# Local
from quick_clients.models import Client
from quick_products.models import Product


class Bill(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    product = models.ManyToManyField(
        Product
    )

    bill_id = models.BigAutoField(
        primary_key=True
    )
    nit = models.CharField(
        max_length=30,
        unique=True
    )
    code = models.CharField(
        max_length=50,
        unique=True
    )
    company_name = models.CharField(
        max_length=120
    )

    class Meta:
        ordering = ["company_name"]

    def __str__(self):
        return self.company_name
