from django import forms
from django.db import connection

class CreateTransaksiPembelianForm(forms.Form):
    list_aset = []
    aset = forms.ChoiceField(label=("Detail Aset"), choices=list_aset, required=True)
    jumlah = forms.IntegerField(label=("Jumlah"), required=True)

    def __init__(self, *args, **kwargs):
        super(CreateTransaksiPembelianForm, self).__init__(*args, **kwargs)

        with connection.cursor() as cursor:
            detail=[]
            cursor.execute(
                "select case when id like 'DK%' then 'Dekorasi' when id like 'BT%' then 'Bibit Tanaman' when id like 'KD%' then 'Kandang' when id like 'HW%' then 'Hewan' when id like 'AP%' then 'Alat Produksi' when id like 'PS%' then 'Petak Sawah' end as tipe, nama, harga_beli from hi_day.aset")
            tmp = cursor.fetchall()
            for i in tmp:
                combine = i[0] + '-' + i[1] + '-' + str(i[2])
                keep = (i[1], combine)
                detail.append(keep)
            self.fields['aset'].choices = tuple(detail)