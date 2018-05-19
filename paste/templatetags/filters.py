from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(value, arg):
    value.field.widget.attrs.update({"class": arg})
    return value

@register.filter(name='placeholder')
def placeholder(value, arg):
    value.field.widget.attrs.update({"placeholder": arg})
    return value
