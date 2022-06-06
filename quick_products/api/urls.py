from django.urls import path
from quick_products.api import views as api_views

urlpatterns = [
    path(
        "<int:pk>",
        api_views.GetProduct.as_view()
    ),
    path(
        "",
        api_views.ListProducts.as_view()
    ),
    path(
        "create",
        api_views.CreateProduct.as_view()
    ),
    path(
        "update/<int:pk>",
        api_views.UpdateProduct.as_view()
    ),
    path(
        "delete/<int:pk>",
        api_views.DeleteProduct.as_view()
    ),
]
