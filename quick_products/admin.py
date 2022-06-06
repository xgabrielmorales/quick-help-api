# Django
from django.contrib import admin
# Local
from quick_products.models import Product


class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Atributos", {
            'fields': ['name', 'description']
        }),
    ]

    search_fields = ['name', "description"]
    list_display = ("name",)
    list_filter = ('name',)
    ordering = ("name",)
    filter_horizontal = ()


admin.site.register(Product, ProductAdmin)
