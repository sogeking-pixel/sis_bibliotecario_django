from django import template

register = template.Library()

@register.filter
def get_item(obj, key):
    return getattr(obj, key)

@register.filter
def starts_with(value, arg):
    if not arg:
        return value == '' or value == '/'
    return value.startswith(arg)