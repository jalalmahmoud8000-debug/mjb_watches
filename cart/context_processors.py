from .models import Cart


def cart_summary(request):
    """Return cart summary: items_count and total_price for templates."""
    items_count = 0
    total = 0

    # try to find existing cart; do not create one
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if session_key:
            cart = Cart.objects.filter(session_key=session_key).first()

    if cart:
        items = cart.items.all()
        items_count = sum(i.quantity for i in items)
        total = sum(i.total_price() for i in items)

    return {
        'cart_items_count': items_count,
        'cart_total_price': total,
    }
