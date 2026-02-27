from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('catalog/', views.catalog, name='catalog'),
    path('contact/', views.contact, name='contact'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
