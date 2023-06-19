from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.db import connection

# Create your views here.
def r_admin(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from hi_day.histori_penjualan")
        rekap = dictfetchall(cursor)
        context = {'penjualan': rekap}
    return render(request, 'read_admin.html', context)

def r_pengguna(request):
    email = request.session['email']
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select * from hi_day.histori_penjualan
            where email = %s
            """, [email]
            )
        rekap = dictfetchall(cursor)
        context = {'penjualan': rekap}
    return render(request, 'read_pengguna.html', context)

def c_pengguna(request):
    # dihandle dari halaman detail pesanan.
    return 0

def detail_penjualan(request,id):
    # email, waktu, id pesanan,
    # nama pesanan, jenis, status
    email = request.session['email']
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select hp.email, hp.waktu_penjualan,
            p.id, p.nama, p.jenis, p.status
            from hi_day.pesanan as p
            join hi_day.detail_pesanan as dp
            on p.id = dp.id_pesanan
            join hi_day.histori_penjualan as hp
            on p.id = hp.id_pesanan
            where email = %s
            """,[email]
        )
    if request.session['peran'] == 'admin':
        return HttpResponseRedirect('/histori-pejualan/admin-read/')
    else :
        return HttpResponseRedirect('/histori-pejualan/pengguna-read/')

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
