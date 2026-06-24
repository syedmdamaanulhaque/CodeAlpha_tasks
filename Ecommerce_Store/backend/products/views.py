from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            name__icontains=query
        )
    else:
        products = Product.objects.all()

    return render(
        request,
        'home.html',
        {
            'products': products,
            'query': query
        }
    )


def product_detail(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'product_detail.html',
        {
            'product': product
        }
    )