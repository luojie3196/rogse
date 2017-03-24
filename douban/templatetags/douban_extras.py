from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


# @register.filter
# @stringfilter
def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

register.filter('lower', lower)


@register.filter(name='cut')
def cut(value, arg):
    """Removes all values of arg from the given string"""
    return value.replace(arg, '')