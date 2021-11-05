from .models import *

def all_products():
    return products.objects.all()

def all_category():
    return product_category.objects.all()

def search_product(text):
    return products.objects.filter(Product_description__icontains = text)