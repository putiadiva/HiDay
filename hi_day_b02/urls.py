"""hi_day_b02 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('pemesanan/', include('pemesanan.urls')),
    path('lumbung/', include('lumbung.urls')),
    path('koin/', include('koin.urls')),
    path('produk/', include('produk.urls')),
    path('produksi/', include('produksi.urls')),
    path('aset/', include('aset.urls')),
    path('koleksi-aset/', include('koleksi_aset.urls')),
    path('pembelian-aset/', include('transaksi_pembelian_aset.urls')),    
    path('proses-produksi/', include('proses_produksi.urls')),
    path('user/', include('user.urls')),
    path('histori_produksi/', include('histori_produksi.urls')),
    path('histori-penjualan/', include('histori_penjualan.urls')),

]
