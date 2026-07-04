from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def index(indexable, i):
    try:
        return indexable[i]
    except:
        return None

@register.filter
def price_for(flight, travel_class):
    try:
        return flight.get_price_for_class(travel_class)
    except:
        return Decimal('0.00')

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except:
        return 0

@register.filter
def div(value, arg):
    try:
        return float(value) / float(arg)
    except:
        return 0
