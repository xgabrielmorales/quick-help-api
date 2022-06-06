# Django REST Framework
from rest_framework import serializers
# Local
from quick_products.models import Product


class ProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(
        read_only=True
    )
    name = serializers.CharField(
        max_length=126
    )
    description = serializers.CharField(
        max_length=512
    )

    def create(self, validated_data):
        instance = Product(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance
