from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "category", "is_featured", "updated_at")
    inlines = [ProductImageInline]
    list_filter = ("category", "is_featured")
    search_fields = ("name", "slug")
    fieldsets = (
        ("Basic Info", {"fields": ("category",
         "name", "slug", "price", "is_featured", "image")}),
        ("Descriptions", {"fields": ("description_en", "description_es")}),
    )

    prepopulated_fields = {"slug": ("name",)}
