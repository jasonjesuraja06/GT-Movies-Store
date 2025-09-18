from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from movies.models import Movie
from .utils import calculate_cart_total
from .models import Order, Item

def _ensure_carts(session):
    """Make sure session has three cart buckets."""
    if 'carts' not in session:
        session['carts'] = {'1': {}, '2': {}, '3': {}}
    # mark session modified when we mutate nested dicts
    session.modified = True

def _get_selected_cart(session, cart_id: int):
    _ensure_carts(session)
    key = str(cart_id)
    # clamp to 1..3
    if key not in ('1', '2', '3'):
        key = '1'
    return key, session['carts'][key]

def index(request, cart_id: int = 1):
    key, cart = _get_selected_cart(request.session, cart_id)
    movie_ids = list(cart.keys())
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    template_data = {
        'title': f'Cart {key}',
        'cart_id': int(key),
        'movies_in_cart': movies_in_cart,
        'cart_total': cart_total,
        'cart': cart,                   # pass the chosen cart bucket
    }
    return render(request, 'cart/index.html', {'template_data': template_data})

def clear(request, cart_id: int):
    key, cart = _get_selected_cart(request.session, cart_id)
    request.session['carts'][key] = {}
    request.session.modified = True
    return redirect('cart.index_id', cart_id=int(key))

def add(request, id: int):
    """Add a movie to whichever cart was selected in the form."""
    # default to Cart 1 if not supplied
    cart_id = request.POST.get('cart_id', '1')
    key, cart = _get_selected_cart(request.session, cart_id)

    quantity = int(request.POST.get('quantity', 1))
    movie_id = str(id)
    cart[movie_id] = cart.get(movie_id, 0) + quantity

    request.session['carts'][key] = cart
    request.session.modified = True
    return redirect('cart.index_id', cart_id=int(key))

@login_required
def purchase(request, cart_id: int):
    key, cart = _get_selected_cart(request.session, cart_id)
    if not cart:
        return redirect('cart.index_id', cart_id=int(key))

    movie_ids = list(cart.keys())
    movies_in_cart = Movie.objects.filter(id__in=movie_ids)
    cart_total = calculate_cart_total(cart, movies_in_cart)

    order = Order.objects.create(user=request.user, total=cart_total)

    for movie in movies_in_cart:
        Item.objects.create(
            movie=movie,
            price=movie.price,
            order=order,
            quantity=cart[str(movie.id)],
        )

    # clear only the purchased bucket
    request.session['carts'][key] = {}
    request.session.modified = True

    template_data = {'title': 'Purchase confirmation', 'order_id': order.id}
    return render(request, 'cart/purchase.html', {'template_data': template_data})
