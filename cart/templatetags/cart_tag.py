from django import template
from django.utils.safestring import mark_safe
from cart.utils import get_cart_totals

register = template.Library()

@register.simple_tag(takes_context=True)
def cart_total_count(context):
    request = context['request']
    totals = get_cart_totals(request)
    return totals['total_items']

@register.simple_tag(takes_context=True)
def cart_total_amount(context):
    request = context['request']
    totals = get_cart_totals(request)
    return totals['total_amount']

@register.simple_tag(takes_context=True)
def cart_total_amount_display(context):
    request = context['request']
    totals = get_cart_totals(request)
    return mark_safe(f"${totals['total_amount']:.2f}")
