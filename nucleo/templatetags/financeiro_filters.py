from django import template

register = template.Library()

@register.filter
def sum_total_valor(queryset, field_name='valor'):
    if not queryset:
        return 0
    return sum(getattr(item, field_name, 0) or 0 for item in queryset)

@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0
