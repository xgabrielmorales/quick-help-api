# Django Rest Framework
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# Local
from quick_products.models import Product
from quick_products.api.serializer import ProductSerializer


class ListProducts(APIView):
    """
    List all products of the system.

    * Everybody can access this view.
    * Token is not necessary
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class GetProduct(APIView):
    """
    Get a specific Product of the system

    * Everybody can access this view.
    * Token is not necessary
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        product_id = kwargs["pk"]

        try:
            product = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            error_message = f"There is not a product with id {product_id}"
            return Response(
                {"error_message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductSerializer(product)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class CreateProduct(APIView):
    """
    Create a Product in the system

    * Only autenticated clients can access this view.
    """

    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Product created successfully"},
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class UpdateProduct(APIView):
    """
    Update a system product.

    * Only autenticated clients can access this view.
    """

    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        product_id = kwargs["pk"]
        try:
            instance = Product.objects.get(product_id=product_id)
        except Product.DoesNotExist:
            error_message = f"There is not a product with id {product_id}"
            return Response(
                {"error_message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = ProductSerializer(instance, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class DeleteProduct(APIView):
    """
    Delete a system product.

    * Only autenticated clients can access this view.
    """

    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        product_id = kwargs["pk"]

        try:
            instance = Product.objects.get(product_id=product_id)
            instance.delete()
        except Product.DoesNotExist:
            error_message = f"There is not a product with id {product_id}"
            return Response(
                {"error_message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {"message": "Product deleted successfully"},
            status=status.HTTP_200_OK,
        )
