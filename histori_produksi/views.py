from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import connection
from datetime import datetime

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def read_histori_tanaman_pengguna(request):
    email = request.session['email']

    with connection.cursor() as cursor:
        # cursor.execute("SELECT * FROM HI_DAY.HISTORI_TANAMAN HT, HI_DAY.HISTORI_PRODUKSI HP, HI_DAY.BIBIT_TANAMAN BT, HI_DAY.ASET A WHERE HT.EMAIL = %s AND HT.EMAIL = HP.EMAIL AND HT.WAKTU_AWAL = HP.WAKTU_AWAL AND HT.ID_BIBIT_TANAMAN = ID_ASET AND BT.ID_ASET = A.ID", [email])
        cursor.execute("SELECT p.*, a.nama FROM HI_DAY.histori_produksi p ,HI_DAY.histori_tanaman ht, HI_DAY.aset a where\
        ht.email = %s and p.email = ht.email and p.waktu_awal = ht.waktu_awal and ht.id_bibit_tanaman = a.id",[email])
        rekap = dictfetchall(cursor)
        context = {'histori': rekap}
        return render(request, 'read_histori_tanaman_pengguna.html', context)

def read_histori_tanaman_admin(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.*, a.nama FROM HI_DAY.histori_produksi p ,HI_DAY.histori_tanaman ht, HI_DAY.aset a where\
        p.email = ht.email and p.waktu_awal = ht.waktu_awal and ht.id_bibit_tanaman = a.id")

        rekap = dictfetchall(cursor)
        context = {'histori': rekap}
        return render(request, 'read_histori_tanaman_admin.html', context)

def create_histori_tanaman(request):
    email = request.session['email']
    waktu = datetime.now()
    state = ''
    context = {'state': state}
    id_bibit = ''
    with connection.cursor() as cursor:
        cursor.execute("set search_path to hi_day;")

        cursor.execute(
            "SELECT id, nama, jumlah FROM HI_DAY.ASET, HI_DAY.KOLEKSI_ASET_MEMILIKI_ASET WHERE ID=ID_ASET AND id_koleksi_aset = %s AND ID_ASET LIKE 'BT%%' ORDER BY ID ASC", [email])
        data_bibit = dictfetchall(cursor)
        context['data_bibit'] = data_bibit
    print(context)
    if request.method == "POST":
        jenis_tanaman = request.POST.get('jenis_bibit')
        jumlah = request.POST.get('jumlah')
        xp = int(jumlah) * 5
        for bibit in data_bibit:
            if bibit['nama'] == jenis_tanaman:
                id_bibit = bibit['id']
                if int(jumlah) > bibit['jumlah']:
                    print("masuk")
                    context['state'] = 'kurang'
                    return render(request, 'create_histori_tanaman.html', context)
        with connection.cursor() as cursor:
            cursor.execute("set search_path to hi_day;")
            cursor.execute(
                'INSERT INTO HI_DAY.HISTORI_PRODUKSI VALUES (%s, %s, %s, %s, %s)', [email, waktu, waktu, jumlah, xp])
            cursor.execute(
                'SELECT waktu_awal FROM HI_DAY.HISTORI_PRODUKSI ORDER BY waktu_awal DESC LIMIT 1')
            cursor.execute(
                'INSERT INTO HI_DAY.HISTORI_TANAMAN VALUES (%s, %s, %s)', [email, waktu, id_bibit])
            return redirect('histori_produksi:histori_tanaman_pengguna')
    return render(request, 'create_histori_tanaman.html', context)

def list_histori_pr_hewan(request): # admin read
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select *
            from hi_day.histori_hewan as hh
            join hi_day.histori_produksi as hp
            on (hh.email, hh.waktu_awal) = (hp.email, hp.waktu_awal)
            join hi_day.aset as a
            on hh.id_hewan = a.id
            """
        )
        rekap = dictfetchall(cursor)
    context = {'histori': rekap}
    return render(request, 'r_histori_hewan_admin.html', context)