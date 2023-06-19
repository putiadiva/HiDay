from django.urls import include, path

from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home_pengguna, name='home'),
    # path('home_admin/', views.home_admin, name='home_admin'),
    path('pemesanan/', include('pemesanan.urls')),
    path('lumbung/', include('lumbung.urls')),
    path('koin/', include('koin.urls')),
    path('produk/', include('produk.urls')),
    path('proses-produksi/', include('proses_produksi.urls')),
]
