from atexit import register
from django import template

register=template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(dish,cart):
    if str(dish) in cart.keys():
        return True
    return False

@register.filter(name='cart_count')
def cart_count(dish,cart):
    if str(dish) in cart.keys():
        return cart.get(str(dish))
    return 0

@register.filter(name='dish_amt')
def dish_amt(dish,cart):
    return dish.RATE * cart_count(dish.id,cart)

@register.filter(name='cart_total')
def cart_total(dish,cart):
    sum=0
    for d in dish:
        sum+=dish_amt(d,cart)
    return sum