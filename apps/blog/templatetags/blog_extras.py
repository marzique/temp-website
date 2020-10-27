from django import template

register = template.Library()   

@register.filter
def liked_by(value, arg):
    return value.liked_by(arg)

@register.filter
def disliked_by(value, arg):
    return value.disliked_by(arg)
