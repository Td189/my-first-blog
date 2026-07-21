from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product

        fields = (
            "name",
            "weekly_sales",
            "original_price",
            "sale_price",
            "image_url",
            "color",
            "is_active",
        )

        widgets = {
            "name": forms.TextInput(
                attrs={
                    "placeholder": "Gaming Mouse",
                }
            ),
            "weekly_sales": forms.NumberInput(
                attrs={
                    "min": 0,
                    "placeholder": "80",
                }
            ),
            "original_price": forms.NumberInput(
                attrs={
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "49.99",
                }
            ),
            "sale_price": forms.NumberInput(
                attrs={
                    "min": 0,
                    "step": "0.01",
                    "placeholder": "34.99",
                }
            ),
            "image_url": forms.URLInput(
                attrs={
                    "placeholder": (
                        "https://example.com/product.jpg"
                    ),
                }
            ),
            "color": forms.TextInput(
                attrs={
                    "type": "color",
                }
            ),
        }