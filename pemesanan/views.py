import email
from multiprocessing import context
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from pemesanan.forms import BuatPesananForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_pesanan(request): # form nya bingung.
    if request.method == 'POST':

        id_pesanan = request.POST.get('id_pesanan')
        nama_pesanan = request.POST.get('nama_pesanan')
        jenis_pesanan = request.POST.get('jenis_pesanan')
        nama_detail = request.POST.get('nama_detail')
        jumlah_detail = request.POST.get('jumlah_detail')
        subtotal_detail = jumlah_detail # masih salah. ada pengali harga jual.
        id_produk = '' # masih salah. cari dgn info nama_detail.
        status_pesanan = 'default'

        with connection.cursor() as cursor:
            cursor.execute('set search_path to hi_day')
            cursor.execute(
                """
                insert into pesanan values (
                    %s, %s, %s, %s, 0
                )
                """,[id_pesanan, status_pesanan, jenis_pesanan, nama_pesanan]
            )
            cursor.execute(
                """
                insert into detail_pesanan values (
                    %s, 1, %s, %s, %s
                )
                """,[id_pesanan, subtotal_detail, jumlah_detail, id_produk]
            )
        return HttpResponseRedirect('/pemesanan/admin-list-pesanan/')
    else:
        with connection.cursor() as cursor:
            cursor.execute("select nama from hi_day.produk")
            rekap = dictfetchall(cursor)
        context = {'pilihan': rekap}
        # return render(request, 'create_pesanan.html', context)
        return render(request, 'create_pesanan_2.html', context)

def read_pesanan_admin(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from hi_day.pesanan")
        rekap = dictfetchall(cursor)
    context = {'pesanan':rekap}
    return render(request, 'r_admin.html', context)

def read_pesanan_pengguna(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from hi_day.pesanan")
        rekap = dictfetchall(cursor)
    context = {'pesanan':rekap}
    return render(request, 'r_pengguna.html', context)

def detail_pesanan(request,id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select * 
            from hi_day.pesanan p
            join hi_day.detail_pesanan d
            on p.id = d.id_pesanan
            where p.id = %s
            """, [id]
        )
        rekap = dictfetchall(cursor)
        print(rekap)
    context = {'detail_pesanan':rekap}
    return render(request, 'detail_pesanan.html', context)

def detail_pesanan_2(request,id):
    context = {}
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select * 
            from hi_day.pesanan p
            join hi_day.detail_pesanan d
            on p.id = d.id_pesanan
            where p.id = %s
            """, [id]
        )
        rekap = dictfetchall(cursor)
        print(rekap)
    context['detail_pesanan'] = rekap

    if request.method == 'POST':
        email = request.session['email']
        koin = rekap[0]['total']
        xp = 10
        id_pesanan = rekap[0]['id']

        with connection.cursor() as cursor:
            cursor.execute("set search_path to hi_day;")
            cursor.execute(
                """
                insert into histori_penjualan values (
                    %s, current_timestamp, %s, %s, %s
                )
                """,[email, koin, xp, id_pesanan]
            )
        return HttpResponseRedirect('/histori-penjualan/pengguna-read/')
    else:
        return render(request, 'detail_pesanan.html', context)


def update_pesanan(request, id):
    if request.method == 'POST':
        # data baru
        nama_pesanan = request.POST['nama_pesanan']
        jenis_pesanan = request.POST['jenis_pesanan']
        status_pesanan = request.POST['status_pesanan']

        with connection.cursor() as cursor:
            cursor.execute(
                """
                update hi_day.pesanan
                set 
                status = %s,
                jenis = %s,
                nama = %s
                where id = %s
                """,[status_pesanan, jenis_pesanan, nama_pesanan, id]
            )
        return redirect('/pemesanan/admin-list-pesanan/')
    else:
        pesanan = []
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select * from hi_day.pesanan p
                where p.id = %s
                """,[id]
            )
            pesanan = dictfetchall(cursor)[0]
        print(pesanan)
        context = {}
        context['pesanan'] = pesanan # ini maksudnya buat prefill form TODO.
        return render(request, 'update_pesanan.html', context)

def delete_pesanan(request, id):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            delete from hi_day.pesanan
            where id = %s
            """,[id]
        )
    return HttpResponseRedirect('/pemesanan/admin-list-pesanan/')

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
