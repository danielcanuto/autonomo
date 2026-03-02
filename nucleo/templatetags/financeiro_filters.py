from django import template

register = template.Library()

@register.filter
def sum_total_valor(queryset):
    if not queryset:
        return 0
    return sum(item.valor for item in queryset)

@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0
