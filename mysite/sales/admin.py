from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "weekly_sales",
        "original_price",
        "sale_price",
        "is_active",
    )

    list_editable = (
        "weekly_sales",
        "sale_price",
        "is_active",
    )

    list_filter = ("is_active",)
    search_fields = ("name",)
    ordering = ("-weekly_sales",)   