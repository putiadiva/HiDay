from cProfile import label
from django import forms
from django.db import connection


class CreateProduksiForm(forms.Form):
    choicess = []
    chociess2 = []
    chociess3 = []
    nama_makanan= forms.ChoiceField(label='Nama Produk Makanan', choices=choicess, required=True)
    alat_produksi= forms.ChoiceField(label='Alat Produksi', choices=chociess2, required=True)
    durasi = forms.IntegerField(
        label=("Durasi Produksi (dalam menit) "), required= True)
    jumlah_produk = forms.IntegerField(
        label=("Jumlah Produk yang dihasilkan"),required=True)
    bahan= forms.ChoiceField(label='Bahan', choices=chociess3, required=True)
    jumlah_bahan = forms.IntegerField(
        label=("Jumlah"),required=True)

    def __init__(self, *args, **kwargs):
        super(CreateProduksiForm, self).__init__(*args, **kwargs)
        with connection.cursor() as cursor:
            detail=[]
            cursor.execute(
                "select nama from hi_day.produk where id like 'PM%%' ")
            tmp = cursor.fetchall()
            for i in tmp:
                combine = i[0]
                keep = (i[0], combine)
                detail.append(keep)
            self.fields['nama_makanan'].choices = tuple(detail)

        with connection.cursor() as cursor:
            detail=[]
            cursor.execute(
                "select nama from hi_day.aset where id like 'AP%%' ")
            tmp = cursor.fetchall()
            for i in tmp:
                combine = i[0]
                keep = (i[0], combine)
                detail.append(keep)
            self.fields['alat_produksi'].choices = tuple(detail)
