from django import template

register = template.Library()

@register.filter
def spaces(value):
    return ' ' * value