from django.urls import path
from .views import (
    cart_view,
    add_to_cart,
    remove_from_cart,
    place_order,
    orders_view
)

urlpatterns = [
    path('cart/', cart_view, name='cart'),

    path(
        'add-to-cart/<int:product_id>/',
        add_to_cart,
        name='add_to_cart'
    ),

    path(
        'remove-from-cart/<int:item_id>/',
        remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'place-order/',
        place_order,
        name='place_order'
    ),

    path(
        'orders/',
        orders_view,
        name='orders'
    ),
]