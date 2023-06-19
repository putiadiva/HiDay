from cProfile import label
from django import forms
from django.db import connection

# from pemesanan.views import detail_pesanan

class BuatPesananForm(forms.Form):
    id_pesanan = forms.CharField(
        label=("ID Pesanan"), required=True, max_length=5)
    nama_pesanan = forms.CharField(
        label=("Nama Pesanan"), required=True, max_length=20)
    jenis_pesanan = forms.CharField(
        label=("Jenis Pesanan"), required=True, max_length=20)

# class BuatDetailPesananForm(forms.Form):
#     id_pesanan = forms.CharField(
#         label=("ID Pesanan"), required=True, max_length=5)