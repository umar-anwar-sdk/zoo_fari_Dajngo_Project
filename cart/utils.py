from booking.models import CartItem


def get_cart_queryset(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.save()
        session_key = request.session.session_key

    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    return CartItem.objects.filter(session_key=session_key)


def get_cart_totals(request):
    queryset = get_cart_queryset(request)
    total_amount = sum(item.line_total for item in queryset)
    total_items = queryset.count()
    return {'total_items': total_items, 'total_amount': total_amount}
