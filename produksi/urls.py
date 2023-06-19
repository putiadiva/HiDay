from django.urls import path
from .views import read_produksi,create_produksi,detail_produksi

app_name = 'produksi'

urlpatterns = [
    # path('', produk, name='produk'),
    path('read_produksi/', read_produksi, name='read_produksi'),
    path('create_produksi/', create_produksi, name='create_produksi'),
    path('read_produksi/<id_produk_makanan>/detail_produksi/', detail_produksi, name='detail_produksi'),
]