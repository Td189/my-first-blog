from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product


def sales_dashboard(request):
    products = Product.objects.filter(
        is_active=True
    ).order_by("-weekly_sales")

    product_data = [
        {
            "id": product.id,
            "name": product.name,
            "weeklySales": product.weekly_sales,
            "originalPrice": float(product.original_price),
            "salePrice": float(product.sale_price),
            "imageUrl": product.image_url,
            "color": product.color,
        }
        for product in products
    ]

    return render(
        request,
        "sales/dashboard.html",
        {
            "products": products,
            "product_data": product_data,
        },
    )


@staff_member_required
def product_new(request):
    if request.method == "POST":
        form = ProductForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("sales:dashboard")
    else:
        form = ProductForm()

    return render(
        request,
        "sales/product_form.html",
        {
            "form": form,
            "page_title": "Add Product",
            "button_text": "Add Product",
        },
    )


@staff_member_required
def product_edit(request, pk):
    product = get_object_or_404(
        Product,
        pk=pk,
    )

    if request.method == "POST":
        form = ProductForm(
            request.POST,
            instance=product,
        )

        if form.is_valid():
            form.save()
            return redirect("sales:dashboard")
    else:
        form = ProductForm(
            instance=product
        )

    return render(
        request,
        "sales/product_form.html",
        {
            "form": form,
            "page_title": "Edit Product",
            "button_text": "Save Changes",
            "product": product,
        },
    )