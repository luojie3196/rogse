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


@register.filter(name='t_range')
def t_range(start, end):
    total_page = len(end)//20
    if total_page % 20 != 0:
        total_page += 1
    item = range(start, total_page, 1)
    if len(item) <= 10:
        return item
    else:
        new_item = []
        for n in item[:5]:
            new_item.append(n)
        for n in item[-6:-1]:
            new_item.append(n)
        return new_item
