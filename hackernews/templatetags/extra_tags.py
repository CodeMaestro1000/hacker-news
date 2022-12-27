from django import template

register = template.Library()

@register.filter(name='get')
def get(dictionary, key):
    return dictionary.get(key)

@register.filter(name='pop')
def pop(dictionary, key):
    return dictionary.pop(key)

@register.filter(name='list')
def cast_to_list(data):
    return list(data)