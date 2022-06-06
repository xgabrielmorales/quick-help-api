from django.db import models


class Product(models.Model):
    product_id = models.BigAutoField(
        "Identificador Único de Producto",
        primary_key=True
    )

    name = models.CharField(
        "Nombre",
        max_length=126
    )
    description = models.CharField(
        "Descripción",
        max_length=512,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
