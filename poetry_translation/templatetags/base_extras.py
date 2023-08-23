from django import template

register = template.Library()

@register.filter
def remove_language(value):
    """Removes language code from url."""
    return value.split('/', 2)[2]
