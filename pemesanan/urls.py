from django.urls import path, include
from django.conf.urls import url
from .views import detail_pesanan_2, index, read_pesanan_admin, read_pesanan_pengguna, create_pesanan, detail_pesanan, update_pesanan, delete_pesanan

app_name = 'pemesanan'

urlpatterns = [
    path('', index, name='pemesanan'),
    path('admin-list-pesanan/', read_pesanan_admin),
    path('admin-create-pesanan/', create_pesanan),
    path('pengguna-list-pesanan/', read_pesanan_pengguna),
    path('<id>/detail-pesanan/', detail_pesanan),
    path('<id>/update-pesanan/', update_pesanan),
    path('<id>/delete-pesanan/', delete_pesanan),
    path('admin-list-pesanan/<id>/detail-pesanan/', detail_pesanan),
    path('admin-list-pesanan/<id>/update-pesanan/', update_pesanan),
    path('admin-list-pesanan/<id>/delete-pesanan/', delete_pesanan),
    path('admin-create-pesanan/<id>/detail-pesanan/', detail_pesanan),
    path('pengguna-list-pesanan/<id>/detail-pesanan/', detail_pesanan_2),
    path('histori-penjualan', include('histori_penjualan.urls')),
]