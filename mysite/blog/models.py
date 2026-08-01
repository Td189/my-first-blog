from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    title = models.CharField(max_length=200)
    text = models.TextField()

    created_date = models.DateTimeField(
        default=timezone.now
    )

    published_date = models.DateTimeField(
        blank=True,
        null=True,
    )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
class Product(models.Model):
    name = models.CharField(max_length=100)

    original_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    sale_price = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    inventory = models.PositiveIntegerField(default=0)
    sales = models.PositiveIntegerField(default=0)

    # This can point to a static image or an online image.
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name

