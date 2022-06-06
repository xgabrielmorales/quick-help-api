from django.urls import path
from quick_bills.api import views as api_views

urlpatterns = [
    path(
        "<int:pk>",
        api_views.GetBill.as_view()
    ),
    path(
        "",
        api_views.ListBills.as_view()
    ),
    path(
        "create/",
        api_views.CreateBill.as_view()
    ),
    path(
        "update/<int:pk>",
        api_views.UpdateBill.as_view()
    ),
    path(
        "delete/<int:pk>",
        api_views.DeleteBill.as_view()
    ),
]
