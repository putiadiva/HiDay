from django.urls import path
from .views import read_histori_tanaman_pengguna, read_histori_tanaman_admin, list_histori_pr_hewan, create_histori_tanaman

app_name = 'histori_produksi'

urlpatterns = [
    path('histori_tanaman/', read_histori_tanaman_pengguna, name='histori_tanaman_pengguna'),
    path('histori_tanaman_admin/', read_histori_tanaman_admin, name='histori_tanaman_admin'),
    path('histori_hewan_admin/', list_histori_pr_hewan, name='histori_tanaman_admin'),
    path('create_histori_tanaman/', create_histori_tanaman, name='create_histori_tanaman'),

]
