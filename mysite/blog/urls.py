from django.urls import path
from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/new/", views.post_new, name="post_new"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path(
        "products/",
        views.product_list,
        name="product_list"
    ),

    path(
        "products/<int:product_id>/sell/",
        views.sell_product,
        name="sell_product"
    ),

    path(
        "products/<int:product_id>/restock/",
        views.restock_product,
        name="restock_product"
    ),

    path(
        "products/<int:product_id>/remove/",
        views.remove_product,
        name="remove_product"
    ),
]