from django.urls import path
from .views import index, produksi_hewan, list_histori_hewan, create_histori_tanaman,read_histori_pr_makanan,create_produksi_makanan

app_name = 'proses_produksi'

urlpatterns = [
    path('', index, name='index'),
    path('produksi-hewan/', produksi_hewan, name='produksi_hewan'),
    path('list-histori-pr-hewan/', list_histori_hewan, name='list_histori_pr_hewan'),
    path('produksi_tanaman/', create_histori_tanaman, name='produksi_tanaman'),
    path('read_histori_pr_makanan/', read_histori_pr_makanan, name='read_histori_pr_makanan'),
    path('create_produksi_makanan/', create_produksi_makanan, name='create_produksi_makanan'),
]
