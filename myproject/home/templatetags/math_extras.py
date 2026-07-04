from django import template

register = template.Library()

@register.filter(name='mul')
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except Exception:
        return ''

@register.filter(name='div')
def div(value, arg):
    try:
        return float(value) / float(arg)
    except Exception:
        return ''
