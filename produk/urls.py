from django.urls import path
from .views import read_produk,update_produk,delete_produk,create_produk

app_name = 'produk'
urlpatterns = [
    # path('', produk, name='produk'),
    path('read_produk/', read_produk, name='read_produk'),
    path('update_produk/', update_produk, name='update_produk'),
    path('delete_produk/', delete_produk, name='delete_produk'),
    path('create_produk/', create_produk, name='create_produk')
]