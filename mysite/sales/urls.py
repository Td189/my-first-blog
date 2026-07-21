from django.urls import path

from . import views


app_name = "sales"

urlpatterns = [
    path(
        "",
        views.sales_dashboard,
        name="dashboard",
    ),
    path(
        "products/new/",
        views.product_new,
        name="product_new",
    ),
    path(
        "products/<int:pk>/edit/",
        views.product_edit,
        name="product_edit",
    ),
]