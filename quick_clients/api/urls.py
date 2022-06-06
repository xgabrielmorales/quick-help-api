from django.urls import path
from quick_clients.api import views_API, views

urlpatterns = [
    path(
        "<int:pk>",
        views_API.GetClient.as_view()
    ),
    path(
        "",
        views_API.ListClients.as_view()
    ),
    path(
        "create",
        views_API.CreateClient.as_view()
    ),
    path(
        "update/<int:pk>",
        views_API.UpdateClient.as_view()
    ),
    path(
        "delete/<int:pk>",
        views_API.DeleteClient.as_view()
    ),
    path(
        "export/csv",
        views.ExportClientsToCSV.as_view()
    ),
    path(
        "import/csv",
        views.ImportClientsFromCSV.as_view()
    )
]
