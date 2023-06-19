from django.urls import path
from .views import delete_paket_koin, read_paket_koin_pengguna, read_transaksi_pembelian_pengguna, read_paket_koin_admin, read_transaksi_pembelian_admin, create_paket_koin, create_transaksi_koin, update_paket_koin, delete_paket_koin

app_name = 'koin'

urlpatterns = [
    path('paket_koin/', read_paket_koin_pengguna, name='paket_koin_pengguna'),
    path('paket_koin_admin/', read_paket_koin_admin, name='paket_koin_admin'),
    path('transaksi_pembelian/', read_transaksi_pembelian_pengguna, name='transaksi_pembelian_pengguna'),
    path('transaksi_pembelian_admin/', read_transaksi_pembelian_admin, name='transaksi_pembelian_admin'),
    path('create_paket/', create_paket_koin, name='create_paket_koin'),
    path('beli_paket/(?P<jumlah>)/(?P<harga>)/$', create_transaksi_koin, name='beli_paket'),
    path('update_paket/(?P<jumlah>)/(?P<harga>)/$', update_paket_koin, name='update_paket'),
    path('delete_paket/(?P<jumlah>)/$', delete_paket_koin, name='delete_paket'),
]
