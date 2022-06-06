# Django REST Framwork
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
# Local
from quick_bills.models.bill import Bill
from quick_bills.api.serializer import BillSerializer


class Utilities():
    @classmethod
    def dict_fetch_all(cls, cursor) -> list:
        "Return all rows from a cursor as a dict"
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class GetBill(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        bill_id = kwargs["pk"]

        try:
            bill = Bill.objects.get(bill_id=bill_id)
        except Bill.DoesNotExist:
            error_message = f"There is not a bill with id {bill_id}"
            return Response(
                {"error_message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = BillSerializer(bill)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class ListBills(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, *args, **kwargs):
        queryset = Bill.objects.all()
        serializer = BillSerializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class CreateBill(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = BillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "Bill created successfullly."},
            status=status.HTTP_201_CREATED
        )


class DeleteBill(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, *args, **kwargs):
        bill_id = kwargs["pk"]

        try:
            bill = Bill.objects.get(bill_id=bill_id)
        except Bill.DoesNotExist:
            error_message = f"There is not a bill with id {bill_id}"
            return Response(
                {"error_message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        bill.delete()

        return Response(
            {"message": "Bill deleted successfully"},
            status=status.HTTP_200_OK
        )


class UpdateBill(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, *args, **kwargs):
        bill_id = kwargs["pk"]

        try:
            bill = Bill.objects.get(bill_id=bill_id)
        except Bill.DoesNotExist:
            error_message = f"There is not a bill with id {bill_id}"
            return Response(
                {"error_message": error_message},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = BillSerializer(
            bill,
            data=request.data,
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
