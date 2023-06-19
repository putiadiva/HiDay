import email
from urllib import request
from django import forms
from django.db import connection

# def get_choises(e):
#     with connection.cursor() as cursor:
#         cursor.execute(
#             """
#             select h.id_aset 
#             from hewan h
#             where h.id_aset in (
#                 select a.id
#                 from hi_day.koleksi_aset ka,
#                 join hi_day koleksi_aset_memiliki_aset ma,
#                 on ka.email = ma.id_koleksi_aset,
#                 join aset a,
#                 on ma.id_aset = a.id
#                 where ka.email = %s
#             )            
#             """,format(e)
#         )
#     result = dictfetchall(cursor)
#     return result

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class ProduksiHewanForm(forms.Form):
    pilihan = []
    email_pengguna = forms.CharField(label=("Email Pengguna"), required=True)
    id_hewan = forms.CharField(label=("ID Hewan"), widget=forms.Select(choices=pilihan), required=True)
    jumlah = forms.IntegerField(label=("Jumlah"), required=True)
    xp = forms.IntegerField(label=("XP"), required=True)
    # temp. harusnya: disabled, otomatis terisi sebesar 5 kali “jumlah” yang diisi

    def __init__(self, *args, **kwargs):
        self.email_pengguna = kwargs.pop('email_pengguna')
        super().__init__(*args, **kwargs)
        # self.fields['email_pengguna'].widget.attrs['readonly'] = True
        # self.fields['email_pengguna'].widget.attrs['class'] = 'disabled'
        self.fields['email_pengguna'] = forms.CharField(initial=request.session['email'])

        with connection.cursor() as cursor:
            cursor.execute(
                """
                select h.id_aset 
                from hi_day.hewan h
                where h.id_aset in (
                select a.id
                from hi_day.koleksi_aset ka
                join hi_day.koleksi_aset_memiliki_aset ma
                on ka.email = ma.id_koleksi_aset
                join hi_day.aset a
                on ma.id_aset = a.id
                where ka.email = {}
                """.format(self.email_pengguna)
            )
            pilihan = dictfetchall(cursor)
        self.fields['id_hewan'].choises = pilihan

class CreateHisproMakananForm(forms.Form):
    choicess = []
    jenis_produk= forms.ChoiceField(label='Jenis Produk', choices=choicess, required=True)
    jumlah = forms.IntegerField(
        label=("Jumlah"), required= True)
    XP = forms.IntegerField(
        label=("XP"),required=True, initial=5)

    def __init__(self, *args, **kwargs):
        super(CreateHisproMakananForm, self).__init__(*args, **kwargs)
        self.fields['XP'].widget.attrs['readonly'] = True
        self.fields['XP'].widget.attrs['class'] = 'disabled'
        # self.fields['XP'].initial = 5 * ['jumlah']

        with connection.cursor() as cursor:
            detail=[]
            cursor.execute(
                "select id, nama from hi_day.produk where id like 'PM%%' ")
            tmp = cursor.fetchall()
            for i in tmp:
                combine = i[0] + '-' + i[1]
                keep = (i[0], combine)
                detail.append(keep)
            self.fields['jenis_produk'].choices = tuple(detail)
