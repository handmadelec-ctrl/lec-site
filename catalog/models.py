from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_featured = models.BooleanField(default=False)
    description_en = models.TextField("Description (English)", blank=True)
    description_es = models.TextField("Descripción (Español)", blank=True)

    image = models.ImageField(upload_to="products/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/gallery/")
    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.product.name} - image {self.id}"
