# Django REST Framework
from rest_framework import serializers
# Local
from quick_clients.models.client import Client


class ClientSerializer(serializers.Serializer):
    client_id = serializers.IntegerField(read_only=True)

    first_name = serializers.CharField(max_length=120)
    last_name = serializers.CharField(max_length=120)

    document = serializers.CharField(max_length=11)

    username = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    password = serializers.CharField(
        max_length=128,
        write_only=True,
    )

    def create(self, validated_data):
        password = validated_data.pop("password")

        instance = Client(**validated_data)
        instance.set_password(password)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop("password")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.set_password(password)
        instance.save()

        return instance
