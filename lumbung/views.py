from decimal import Context
from django.shortcuts import render, redirect
from django.db import connection
from datetime import datetime

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def detail_lumbung(request):

    if request.session['peran'] == 'admin':
        with connection.cursor() as cursor:
            cursor.execute("""select email, id_produk, nama, harga_jual, sifat_produk, jumlah 
            from hi_day.lumbung l, hi_day.lumbung_memiliki_produk lmp, hi_day.produk p
            where l.email = lmp.id_lumbung
            and lmp.id_produk = p.id
            and id_produk like 'HP%'
            """)
            tmp_panen = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute("""
            select email, id_produk, nama, harga_jual, sifat_produk, jumlah 
            from hi_day.lumbung l, hi_day.lumbung_memiliki_produk lmp, hi_day.produk p
            where l.email = lmp.id_lumbung
            and lmp.id_produk = p.id
            and id_produk like 'PH%'
            """)
            tmp_hewan = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute("""
            select email, id_produk, nama, harga_jual, sifat_produk, jumlah 
            from hi_day.lumbung l, hi_day.lumbung_memiliki_produk lmp, hi_day.produk p
            where l.email = lmp.id_lumbung
            and lmp.id_produk = p.id
            and id_produk like 'PM%'
            """)
            tmp_makanan = dictfetchall(cursor)
        context = {'panen': tmp_panen, 'hewan': tmp_hewan, 'makanan': tmp_makanan}
        
    
    else:
        email = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("select level from hi_day.pengguna where email = %s", [email])
            tmp_level = dictfetchall(cursor)
            level=tmp_level[0]['level']

        with connection.cursor() as cursor:
            cursor.execute("select total, kapasitas_maksimal from hi_day.lumbung where email = %s", [email])
            tmp_lumbung = dictfetchall(cursor)
            total=tmp_lumbung[0]['total']
            kapasitas_maksimal=tmp_lumbung[0]['kapasitas_maksimal']

        with connection.cursor() as cursor:
            cursor.execute(
            """
            select email, id_produk, nama, harga_jual, sifat_produk, jumlah 
            from hi_day.lumbung l, hi_day.lumbung_memiliki_produk lmp, hi_day.produk p
            where l.email = lmp.id_lumbung
            and lmp.id_produk = p.id
            and id_produk like 'HP%%'
            and email=%s
            """, [email])
            tmp_panen = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute("""
            select email, id_produk, nama, harga_jual, sifat_produk, jumlah 
            from hi_day.lumbung l, hi_day.lumbung_memiliki_produk lmp, hi_day.produk p
            where l.email = lmp.id_lumbung
            and lmp.id_produk = p.id
            and id_produk like 'PH%%'
            and email = %s
            """, [email])
            tmp_hewan = dictfetchall(cursor)

        with connection.cursor() as cursor:
            cursor.execute("""
            select email, id_produk, nama, harga_jual, sifat_produk, jumlah 
            from hi_day.lumbung l, hi_day.lumbung_memiliki_produk lmp, hi_day.produk p
            where l.email = lmp.id_lumbung
            and lmp.id_produk = p.id
            and id_produk like 'PM%%'
            and email = %s
            """, [email])
            tmp_makanan = dictfetchall(cursor)
        context = {'panen': tmp_panen, 'hewan': tmp_hewan, 'makanan': tmp_makanan, 'level': level, 'total': total, 'kapasitas_maksimal': kapasitas_maksimal}
    return render(request, 'detailLumbung.html', context)

def read_upgrade_lumbung_admin(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM HI_DAY.TRANSAKSI_UPGRADE_LUMBUNG")
        rekap = dictfetchall(cursor)
        context = {'transaksi': rekap}
        return render(request, 'read_upgrade_admin.html', context)

def read_upgrade_lumbung_pengguna(request):
    email = request.session['email']
    with connection.cursor() as cursor:
        cursor.execute("SELECT waktu FROM HI_DAY.TRANSAKSI_UPGRADE_LUMBUNG WHERE EMAIL = %s", [email])
        rekap = dictfetchall(cursor)
        context = {'transaksi': rekap}
        return render(request, 'read_upgrade_pengguna.html', context)

def create_upgrade_lumbung(request):
    email = request.session['email']
    waktu = datetime.now()
    state = ''
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select * from hi_day.lumbung
            where email = %s
            """, [email]
        )
        rekap = dictfetchall(cursor)
        cursor.execute(
            """
            select * from hi_day.pengguna
            where email = %s
            """, [email]
        )
        data = dictfetchall(cursor)
    context = {'isi': rekap, 'state':state}
    print(rekap)
    if request.method == "POST":
        if data[0]["koin"] < 200:
            state = 'kurang'
            context = {'isi': rekap, 'state':state}
            return render(request, 'create_upgrade_lumbung.html', context)
        level_baru = rekap[0]["level"] + 1
        kapasitas_baru = rekap[0]["kapasitas_maksimal"] + 50
        with connection.cursor() as cursor:
            cursor.execute("set search_path to hi_day;")
            cursor.execute(
                'UPDATE HI_DAY.LUMBUNG SET KAPASITAS_MAKSIMAL = %s WHERE email = %s', [kapasitas_baru, email])
            cursor.execute(
                'UPDATE HI_DAY.LUMBUNG SET LEVEL = %s WHERE email = %s', [level_baru, email])
            cursor.execute('INSERT INTO HI_DAY.TRANSAKSI_UPGRADE_LUMBUNG VALUES (%s, %s)', [email, waktu])
        return redirect('lumbung:upgrade_pengguna')
    return render(request, 'create_upgrade_lumbung.html', context)

def isi_lumbung(request):
    email = request.session['email']
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select * from hi_day.lumbung
            where email = %s
            """, [email]
        )
        rekap = dictfetchall(cursor)
    context = {'isi': rekap}
    return render(request, 'isi_lumbung.html', context)