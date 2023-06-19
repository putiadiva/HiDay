from django.urls import path
from .views import r_admin, r_pengguna, c_pengguna, detail_penjualan

app_name = 'histori_penjualan'

urlpatterns = [
    path('admin-read/', r_admin),
    path('pengguna-read/', r_pengguna),
    path('pengguna-create/', c_pengguna),
    path('<id>/detail-penjualan/', detail_penjualan),
]
