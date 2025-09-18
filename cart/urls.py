from django.urls import path
from . import views

urlpatterns = [
    # default -> Cart 1 (keeps your old navbar link working)
    path('', views.index, name='cart.index'),

    # explicit cart views
    path('<int:cart_id>/', views.index, name='cart.index_id'),
    path('<int:cart_id>/purchase/', views.purchase, name='cart.purchase'),
    path('<int:cart_id>/clear/', views.clear, name='cart.clear'),

    # add-to-cart stays movie-centric; cart is chosen via POST in the form
    path('add/<int:id>/', views.add, name='cart.add'),
]
