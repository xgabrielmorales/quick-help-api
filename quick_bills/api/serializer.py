# Django REST Framework
from rest_framework import serializers
# Local
from quick_bills.models import Bill
from quick_clients.models import Client
from quick_products.models import Product


class BillSerializer(serializers.Serializer):
    client = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.all()
    )
    product = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    bill_id = serializers.IntegerField(read_only=True)
    nit = serializers.CharField(max_length=30)
    code = serializers.CharField(max_length=50)
    company_name = serializers.CharField(max_length=120)

    def create(self, validated_data):
        products = validated_data.pop("product")

        instance = Bill(**validated_data)
        instance.save()

        for product_id in products:
            instance.product.add(product_id)

        return instance

    def update(self, instance, validated_data):
        products = validated_data.pop("product")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Delete existing relationships between Bill And Product
        instance.product.clear()

        # ...to add new ones.
        for product_id in products:
            instance.product.add(product_id)

        return instance
