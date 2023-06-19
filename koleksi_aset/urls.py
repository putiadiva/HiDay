from django.urls import path
from .views import *

app_name = 'koleksi_aset'

urlpatterns = [
    path('', opsi_liat_koleksi, name='opsi_koleksi'),
    path('dekorasi', read_koleksi_dekorasi, name='read_koleksi_dekorasi'),
    path('bibit-tanaman', read_koleksi_bibit, name='read_koleksi_bibit'),
    path('kandang', read_koleksi_kandang, name='read_koleksi_kandang'),
    path('hewan', read_koleksi_hewan, name='read_koleksi_hewan'),
    path('alat-produksi', read_koleksi_alat, name='read_koleksi_alat'),
    path('petak-sawah', read_koleksi_petak, name='read_koleksi_petak'),
]