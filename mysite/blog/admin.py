from django.contrib import admin

from .models import Post, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "sale_price",
        "inventory",
        "sales",
    )

    search_fields = ("name",)


admin.site.register(Post)