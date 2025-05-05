from django.shortcuts import render
from django.http import JsonResponse
from .models import Product

def product_list(request):
    products = Product.objects.all()
    data = [{"name": p.product_name, "price": float(p.price), "url": p.url} for p in products]
    return JsonResponse(data, safe=False)

# Create your views here.
