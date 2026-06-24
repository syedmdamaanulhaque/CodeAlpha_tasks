from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from products.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    items = CartItem.objects.filter(cart=cart)

    total = sum(item.product.price * item.quantity for item in items)

    return render(
        request,
        "cart.html",
        {
            "items": items,
            "total": total
        }
    )


@login_required
def add_to_cart(request, product_id):
    cart, created = Cart.objects.get_or_create(user=request.user)

    product = get_object_or_404(Product, id=product_id)

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("/cart/")


# ADD THESE BELOW add_to_cart()

@login_required
def place_order(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect('/cart/')

    total = sum(item.product.price * item.quantity for item in items)

    order = Order.objects.create(
        user=request.user,
        total_amount=total
    )

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    items.delete()

    return redirect('/orders/')


@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)

    return render(
        request,
        'orders.html',
        {
            'orders': orders
        }
    )

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect('/cart/')