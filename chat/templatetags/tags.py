from django import template

register = template.Library()


@register.filter(name='initials')
def initials(value):
    initial = ''.join(c for c in value.split())
    return initial[:2]
