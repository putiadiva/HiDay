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

def read_paket_koin_pengguna(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM HI_DAY.PAKET_KOIN")
        rekap = dictfetchall(cursor)
    context = {'paket': rekap}
    return render(request, 'read_paket_koin_pengguna.html', context)

def read_paket_koin_admin(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM HI_DAY.PAKET_KOIN where exists (select * from hi_day.transaksi_pembelian_koin where jumlah_koin = paket_koin)")
        rekap = dictfetchall(cursor)
        cursor.execute("SELECT * FROM HI_DAY.PAKET_KOIN where not exists (select * from hi_day.transaksi_pembelian_koin where jumlah_koin = paket_koin)")
        rekap1 = dictfetchall(cursor)
    context = {'paket_non_delete': rekap, 'paket_delete': rekap1}
    return render(request, 'read_paket_koin_admin.html', context)

def create_paket_koin(request):
    if request.method == "POST":
        jumlah = request.POST.get('jumlah')
        harga = request.POST.get('harga')
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.PAKET_KOIN VALUES (%s, %s)', [jumlah, harga])
        return redirect('koin:paket_koin_admin')
    return render(request, 'create_paket_koin.html')

def update_paket_koin(request, jumlah, harga ):
    if request.method == "POST":
        harga = request.POST.get('harga')
        with connection.cursor() as cursor:
            cursor.execute(
                'UPDATE HI_DAY.PAKET_KOIN SET HARGA = %s WHERE jumlah_koin = %s', [harga, jumlah])
        return redirect('koin:paket_koin_admin')
    return render(request, 'update_paket_koin.html', {'jumlah':jumlah,'harga':harga})

def read_transaksi_pembelian_pengguna(request):
    email = request.session['email']
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM HI_DAY.TRANSAKSI_PEMBELIAN_KOIN WHERE EMAIL = %s", [email])
        rekap = dictfetchall(cursor)
        context = {'transaksi': rekap}
        return render(request, 'read_transaksi_pembelian_pengguna.html', context)

def read_transaksi_pembelian_admin(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM HI_DAY.TRANSAKSI_PEMBELIAN_KOIN")
        rekap = dictfetchall(cursor)
        context = {'transaksi': rekap}
        return render(request, 'read_transaksi_pembelian_admin.html', context)

def create_transaksi_koin(request, jumlah, harga):
    email = request.session['email']
    if request.method == "POST":
        jumlah_beli = request.POST.get('jumlah')
        total_biaya = int(jumlah_beli) * int(harga)
        cara = request.POST.get('cara')
        waktu = datetime.now()
        with connection.cursor() as cursor:
            cursor.execute("set search_path to hi_day;")
            cursor.execute(
                'INSERT INTO HI_DAY.TRANSAKSI_PEMBELIAN_KOIN VALUES (%s, %s, %s, %s, %s, %s)', [email, waktu, jumlah_beli, cara, jumlah,total_biaya])
        return redirect('koin:transaksi_pembelian_pengguna')
    return render(request, 'create_transaksi_koin.html', {'jumlah':jumlah,'harga':harga})

def delete_paket_koin(request, jumlah):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM HI_DAY.PAKET_KOIN WHERE jumlah_koin = %s", [jumlah])
        return redirect('koin:paket_koin_admin')