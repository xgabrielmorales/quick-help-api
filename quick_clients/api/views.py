# Django
from django.db import connection
from django.http import HttpResponse
# Django REST Framework
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
# Local
from quick_clients.models.client import Client
from quick_clients.api.views_API import Utilities
# Others
import io
import csv


class ExportClientsToCSV(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        """Export all clients in the system to a CSV file"""

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="export.csv"'

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT document, first_name, last_name "
                "FROM quick_clients_client"
            )
            queryset = Utilities.dict_fetch_all(cursor)

        writer = csv.DictWriter(
            response,
            fieldnames=["document", "first_name", "last_name"]
        )
        writer.writeheader()
        list(map(writer.writerow, queryset))

        return response


class ImportClientsFromCSV(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Import a list of clients from a CSV file

        * The imported file is read in memory
        * The imported file is never stored
        """

        file_in_memory = request.FILES['file']
        file = file_in_memory.read().decode('utf-8')
        reader = csv.DictReader(io.StringIO(file))

        # It is not a good idea to do this using RAW SQL because it is
        # necessary to hash the password of each Client.
        for row in reader:
            client = Client.objects.get_or_create(
                first_name=row["first_name"],
                last_name=row["last_name"],
                document=row["document"],
                username=row["username"],
                email=row["email"],
            )

            client[0].set_password(row["password"])
            client[0].save()

        return Response(
            {"message": "Clients imported successfully"},
            status=status.HTTP_201_CREATED
        )
