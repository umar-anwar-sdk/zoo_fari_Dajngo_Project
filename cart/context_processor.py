from .utils import get_cart_totals


def cart_total_amount(request):
    totals = get_cart_totals(request)
    return {
        'cart_total_items': totals['total_items'],
        'cart_total_amount': totals['total_amount'],
    }
