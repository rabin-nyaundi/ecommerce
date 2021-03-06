from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('cart/', views.cart_view, name = 'cart'),
    path('checkout/', views.checkout_view, name = 'checkout'),
    path('updateItem/', views.updateItem, name='updateItem'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('<str:id>/searchCategory/', views.searchCategory, name='searchCategory'),
] 
