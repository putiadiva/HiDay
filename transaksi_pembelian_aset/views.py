from django.shortcuts import render, redirect
from .forms import *
from django.db import connection
from datetime import datetime

def opsi_buat_aset(request):
    return render(request, 'opsi_buat_aset.html')

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def create_transaksi_pembelian(request):
    form = CreateTransaksiPembelianForm()
    if request.method == "POST":
        email = request.session['email']
        waktu = datetime.now()
        jumlah = request.POST['jumlah']
        aset = request.POST['aset']
        tmp = [email, waktu, jumlah]
        print(tmp)
        with connection.cursor() as cursor:
            cursor.execute("select id from hi_day.aset where nama = %s",[aset])
            temp = dictfetchall(cursor)
            id_aset = temp[0]['id']

            tmp.append(id_aset)
            cursor.execute(
                'INSERT INTO HI_DAY.TRANSAKSI_PEMBELIAN VALUES (%s, %s, %s, %s)', tmp)
        return redirect('transaksi_pembelian_aset:read_transaksi_pembelian')
    return render(request, 'create_tp.html', {'form': form})

def read_transaksi_pembelian(request):
    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute(
                "select email, waktu, case when id like 'DK%' then 'Dekorasi' when id like 'BT%' then 'Bibit Tanaman' when id like 'KD%' then 'Kandang' when id like 'HW%' then 'Hewan' when id like 'AP%' then 'Alat Produksi' when id like 'PS%' then 'Petak Sawah' end as jenis, nama, jumlah, jumlah*harga_beli as total_harga from hi_day.aset, hi_day.transaksi_pembelian where id_aset = id")
            tmp = dictfetchall(cursor)
    else:
        id_pengguna = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select waktu, 
                case when id like 'DK%%' then 'Dekorasi' 
                when id like 'BT%%' then 'Bibit Tanaman' 
                when id like 'KD%%' then 'Kandang' 
                when id like 'HW%%' then 'Hewan' 
                when id like 'AP%%' then 'Alat Produksi' 
                when id like 'PS%%' then 'Petak Sawah' 
                end as jenis, 
                nama, jumlah, jumlah*harga_beli as total_harga 
                from hi_day.aset, hi_day.transaksi_pembelian 
                where id_aset = id and email = %s""",[id_pengguna] )
            tmp = dictfetchall(cursor)
    context = {'list': tmp}
    return render(request, 'list_tp.html', context)