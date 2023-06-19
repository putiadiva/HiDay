from django.urls import path
from .views import *

app_name = 'transaksi_pembelian_aset'

urlpatterns = [
    path('create', create_transaksi_pembelian, name='create_transaksi_pembelian'),
    path('list-transaksi', read_transaksi_pembelian, name='read_transaksi_pembelian'),
]