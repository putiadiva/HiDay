from django.shortcuts import render
from django.db import connection

def opsi_liat_koleksi(request):
    return render(request, 'menu_koleksi.html')

def read_koleksi_dekorasi(request):
    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("select * from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'DK%'")
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
        print(seluruh)
    else:
        id_pengguna = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("select * from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'DK%%' and email = %s", [id_pengguna])
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    return render(request, 'read_koleksi_aset.html', context)

def read_koleksi_bibit(request):
    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("select email, nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'BT%'")
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    else:
        id_pengguna = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("select nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'BT%%' and email = %s", [id_pengguna])
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    return render(request, 'read_koleksi_aset.html', context)

def read_koleksi_kandang(request):
    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("select email, nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'KD%'")
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    else:
        id_pengguna = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("select nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'KD%%' and email = %s", [id_pengguna])
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    return render(request, 'read_koleksi_aset.html', context)

def read_koleksi_hewan(request):
    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("select email, nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'HW%'")
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    else:
        id_pengguna = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("select nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'HW%%' and email = %s", [id_pengguna])
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    return render(request, 'read_koleksi_aset.html', context)

def read_koleksi_alat(request):
    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("select email, nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'AP%'")
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    else:
        id_pengguna = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("select nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'AP%%' and email = %s", [id_pengguna])
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    return render(request, 'read_koleksi_aset.html', context)

def read_koleksi_petak(request):
    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("select email, nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'PS%'")
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    else:
        id_pengguna = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("select nama, minimum_level, harga_beli, jumlah from hi_day.koleksi_aset, hi_day.koleksi_aset_memiliki_aset, hi_day.aset where email = id_koleksi_aset and id_aset = id and id like 'PS%%' and email = %s", [id_pengguna])
            seluruh = dictfetchall(cursor)
        context = {'field': seluruh}
    return render(request, 'read_koleksi_aset.html', context)

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
