from django import template
register = template.Library()

@register.filter
def get_quantity(cart_dict, movie_id):
    """cart_dict is a dict like {'12': 2, '15': 1}"""
    if not cart_dict:
        return 0
    return cart_dict.get(str(movie_id), 0)
