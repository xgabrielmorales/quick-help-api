# Django
from django.db import connection
from django.conf import settings
# Django REST Framework
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# Django REST Framework Simple JWT
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# Local
from quick_clients.models.client import Client
from quick_clients.api.serializer import ClientSerializer


class Utilities():

    @classmethod
    def dict_fetch_all(cls, cursor) -> list:
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    @classmethod
    def is_staff(cls, client_id) -> bool:
        """Return True if the given client_id is staff"""

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT is_staff "
                + "FROM quick_clients_client "
                + "WHERE client_id = %s",
                [client_id]
            )
            is_staff = cursor.fetchone()
            is_staff = is_staff[0]

        return is_staff


class ListClients(APIView):
    """
    View to list all clients on the system.

    * Requires Token Authentication
    * Only admin clients can access this view.
    """

    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        """
        Return all clients
        """

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quick_clients_client"
            )

            queryset = Utilities.dict_fetch_all(cursor)
            serializer = ClientSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class GetClient(APIView):
    """
    Get a specific client of the system

    * Requires Token Authentication
    * Only authenticated clients can access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Return a client
        """

        try:
            token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
            tokenBackend = TokenBackend(
                algorithm=settings.SIMPLE_JWT["ALGORITHM"]
            )
            valid_data = tokenBackend.decode(token, verify=False)
            client_id = valid_data["client_id"]

        except Exception:
            return Response(
                {"error_message": "Your token is invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_staff = Utilities.is_staff(client_id)

        if kwargs["pk"] == client_id or is_staff:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT *"
                    + "FROM quick_clients_client "
                    + "WHERE client_id = %s",
                    [kwargs["pk"]]
                )
                client = Utilities.dict_fetch_all(cursor)
            serializer = ClientSerializer(client[0])

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {"error_message": "You are not authorized to perform this action"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class UpdateClient(APIView):
    """
    Update a specific client from the system.

    * Requires Token Authentication
    * Only autenticated clients can access this view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, *args, **kwargs):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            tokenBackend = TokenBackend(
                algorithm=settings.SIMPLE_JWT["ALGORITHM"]
            )
            valid_data = tokenBackend.decode(token, verify=False)
            client_id = valid_data["client_id"]
        except Exception:
            return Response(
                {"error_message": "Your token is invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_staff = Utilities.is_staff(client_id)

        if kwargs["pk"] == client_id or is_staff:
            instance = Client.objects.raw(
                "SELECT * "
                "FROM quick_clients_client "
                "WHERE client_id = %s",
                [kwargs["pk"]]
            )[0]

            serializer = ClientSerializer(
                instance,
                data=request.data,
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            {"error_message": "You are not authorized to perform this action"},
            status=status.HTTP_401_UNAUTHORIZED
        )


class CreateClient(APIView):
    """
    Create a Client in the system

    * Requires Token Authentication
    * Only autenticated clients can access this view.
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        tokenData = {
            "username": request.data["username"],
            "password": request.data["password"]
        }

        tokenSerializer = TokenObtainPairSerializer(data=tokenData)
        tokenSerializer.is_valid(raise_exception=True)

        return Response(
            tokenSerializer.validated_data,
            status=status.HTTP_201_CREATED
        )


class DeleteClient(APIView):
    """
    Remove a specific client from the system.

    * Requires Token Authentication
    * Only autenticated clients can access this view.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        try:
            token = request.META.get("HTTP_AUTHORIZATION").split(" ")[1]
            tokenBackend = TokenBackend(
                algorithm=settings.SIMPLE_JWT["ALGORITHM"]
            )
            valid_data = tokenBackend.decode(token, verify=False)
            client_id = valid_data["client_id"]
        except Exception:
            return Response(
                {"error_message": "Your token is invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        is_staff = Utilities.is_staff(client_id)

        if kwargs["pk"] == client_id or is_staff:
            with connection.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM quick_clients_client "
                    "WHERE client_id = %s",
                    [kwargs["pk"]]
                )

            return Response(
                {"message": "Client deleted successfully"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error_message": "You are not authorized to perform this action"},
            status=status.HTTP_401_UNAUTHORIZED
        )
