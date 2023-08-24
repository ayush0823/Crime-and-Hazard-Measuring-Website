from django import template
from django.template.defaulttags import register

register = template.Library()

@register.filter(name='sub')
def sub(value, arg):
    return value - arg


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)