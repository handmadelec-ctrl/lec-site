from django.shortcuts import render, get_object_or_404
from django.conf import settings
from .models import Product


def home(request):
    featured_products = Product.objects.filter(
        is_featured=True).order_by("-updated_at")
    return render(request, "catalog/home.html", {
        "featured_products": featured_products
    })


def catalog(request):
    products = Product.objects.all().order_by("-id")
    return render(request, "catalog/catalog.html", {"products": products})


def contact(request):
    return render(request, "catalog/contact.html")


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    whatsapp_number = getattr(settings, "WHATSAPP_NUMBER", "")
    return render(
        request,
        "catalog/product_detail.html",
        {"product": product, "whatsapp_number": whatsapp_number},
    )


def custom_404(request, exception):
    return render(request, "catalog/404.html", status=404)
