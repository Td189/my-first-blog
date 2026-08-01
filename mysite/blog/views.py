from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
import json
from django.db import transaction
from django.http import JsonResponse
from .forms import PostForm
from .models import Post
from django.views.decorators.http import require_POST
from .models import Product

def post_list(request):
    posts = Post.objects.filter(
        published_date__lte=timezone.now()
    ).order_by("published_date")

    return render(
        request,
        "blog/post_list.html",
        {"posts": posts},
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    return render(
        request,
        "blog/post_detail.html",
        {"post": post},
    )


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()

    return render(
        request,
        "blog/post_edit.html",
        {"form": form},
    )


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()

            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(
        request,
        "blog/post_edit.html",
        {"form": form},
    )
def product_list(request):
    products = Product.objects.all().order_by("-sales", "name")

    return render(
        request,
        "blog/product_list.html",
        {
            "products": products
        }
    )


@require_POST
def sell_product(request, product_id):
    with transaction.atomic():
        product = get_object_or_404(
            Product.objects.select_for_update(),
            id=product_id
        )

        if product.inventory <= 0:
            return JsonResponse(
                {
                    "success": False,
                    "message": f"{product.name} is out of stock.",
                    "inventory": product.inventory,
                    "sales": product.sales,
                },
                status=400
            )

        product.inventory -= 1
        product.sales += 1

        product.save(
            update_fields=[
                "inventory",
                "sales",
            ]
        )

    return JsonResponse(
        {
            "success": True,
            "message": f"Sold one {product.name}.",
            "inventory": product.inventory,
            "sales": product.sales,
        }
    )


@require_POST
def restock_product(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    try:
        body = json.loads(
            request.body.decode("utf-8")
        )

        amount = int(body.get("amount", 0))
    except (
        json.JSONDecodeError,
        TypeError,
        ValueError,
    ):
        return JsonResponse(
            {
                "success": False,
                "message": "The restock amount is invalid.",
            },
            status=400
        )

    if amount <= 0:
        return JsonResponse(
            {
                "success": False,
                "message": "The restock amount must be greater than zero.",
            },
            status=400
        )

    product.inventory += amount
    product.save(update_fields=["inventory"])

    return JsonResponse(
        {
            "success": True,
            "message": (
                f"Added {amount} units to "
                f"{product.name}."
            ),
            "inventory": product.inventory,
            "sales": product.sales,
        }
    )


@require_POST
def remove_product(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    product_name = product.name
    product.delete()

    return JsonResponse(
        {
            "success": True,
            "message": f"Removed {product_name}.",
        }
    )