from cProfile import label
from django import forms
from django.db import connection


class CreateProdukForm(forms.Form):
    PRODUK_CHOICES = [("Hasil Panen", "Hasil Panen"),("Produk Hewan", "Produk Hewan"),("Produk Makanan", "Produk Makanan")
    ]
    jenis_produk= forms.ChoiceField(label='Jenis Produk', choices=PRODUK_CHOICES)
    nama = forms.CharField(
        label=("Nama"), required=True, max_length=50)
    harga_jual = forms.IntegerField(
        label=("Harga Jual"), required= True)
    sifat_produk = forms.CharField(
        label=("Sifat Produk"),required=True, max_length=20)

class UpdateProdukForm(forms.Form):
    jenis_produk = forms.CharField(label=("Jenis Produk"), required=True, max_length=50)
    nama = forms.CharField(label=("Nama"), required=True, max_length=50)
    harga_jual = forms.IntegerField(label=("Harga Jual"), required=True)
    sifat_produk = forms.CharField(label=("Sifat Produk"), required=True)

    def __init__(self, *args, **kwargs):
        super(UpdateProdukForm, self).__init__(*args, **kwargs)
        self.fields['jenis_produk'].widget.attrs['readonly'] = True
        self.fields['jenis_produk'].widget.attrs['class'] = 'disabled'
        self.fields['nama'].widget.attrs['readonly'] = True
        self.fields['nama'].widget.attrs['class'] = 'disabled'
