import email
from multiprocessing import context
from sre_parse import State
from urllib import response
from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from datetime import datetime


from proses_produksi.forms import ProduksiHewanForm,CreateHisproMakananForm

# Create your views here.
def index(request):
    return render(request, 'index_proses_produksi.html')

def produksi_hewan(request): # pengguna create
    # harusnya handle jumlah hewan yg ga cukup.

    email = request.session['email']
    
    if request.method == 'POST':
        id_hewan = request.POST.get('id_hewan')
        jumlah = request.POST.get('jumlah')
        xp = int(jumlah)*5

        print(id_hewan)
        print(jumlah)
        print(xp)

        # TODO bikin query insert ke histori hewan.

        with connection.cursor() as cursor:
            cursor.execute("set search_path to hi_day;")
            
            cursor.execute(
                """
                insert into hi_day.histori_produksi
                values(
                    %s, current_timestamp, current_timestamp,
                    %s, %s
                )
                """,[email, jumlah, xp]
            )
            cursor.execute(
                """
                select waktu_awal from hi_day.histori_produksi
                order by waktu_awal desc limit 1
                """
            )
            temp = dictfetchall(cursor)
            waktu = temp[0]['waktu_awal']
            cursor.execute(
                """
                insert into hi_day.histori_hewan
                values(
                    %s, %s, %s
                )
                """,[email, waktu, id_hewan]
            )
        return HttpResponseRedirect('/proses-produksi/list-histori-pr-hewan/')

    else :
        
        # state = ''
        context = {}
        # context['state': state]
        # id_hewan = ''
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
                where ka.email = %s
                )
                """,[email]
            )
            id_hewan_option = dictfetchall(cursor)
        context['options'] = id_hewan_option
        print(context)
        return render(request, 'c_histori_hewan.html', context)
        
def list_histori_hewan(request): # pengguna read
    email = request.session['email']
    with connection.cursor() as cursor:
        cursor.execute(
            """
            select hp.email, hp.waktu_awal, hp.waktu_selesai,
            hp.jumlah, hp.xp, a.nama
            from hi_day.histori_hewan as hh
            join hi_day.histori_produksi as hp
            on (hh.email, hh.waktu_awal) = (hp.email, hp.waktu_awal)
            join hi_day.aset as a
            on hh.id_hewan = a.id
            where hh.email = '{}'
            """.format(email)
        )
        rekap = dictfetchall(cursor)
    context = {'histori': rekap}
    print(context)
    return render(request, 'r_histori_hewan.html', context)

def produksi_tanaman(request):
    return 0

def list_histori_pr_tanaman(request):
    return 0

def create_produksi_makanan(request):
    form = CreateHisproMakananForm()
    if request.method == "POST":
        email = request.session['email']
        waktu_awal = datetime.now()
        waktu_selesai = waktu_awal
        jumlah = request.POST['jumlah']
        jenis_produk = request.POST['jenis_produk']
        xp = request.POST['XP']
        tmp = [email, waktu_awal, waktu_selesai, jumlah, xp]
        tmp2 = [email, waktu_awal]
        print(tmp)
        with connection.cursor() as cursor:
            cursor.execute("select id_alat_produksi from hi_day.produksi where id_produk_makanan = %s",[jenis_produk])
            temp = dictfetchall(cursor)
            id_alat_produksi= temp[0]['id_alat_produksi']

        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.HISTORI_PRODUKSI VALUES (%s, %s, %s, %s, %s)', tmp)
        
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.HISTORI_PRODUKSI_MAKANAN VALUES (%s, %s, %s, %s)', tmp2, id_alat_produksi, jenis_produk)
        return redirect('proses_produksi:read_histori_pr_makanan')
    return render(request, 'create_histori_produk_makanan.html', {'form': form})

def read_histori_pr_makanan(request):
    if request.session['peran'] == 'admin':
            with connection.cursor() as cursor:
                cursor.execute("SELECT hpr.email,p.waktu_awal,p.waktu_selesai,p.jumlah,p.xp,a.nama,pr.nama as makan FROM HI_DAY.histori_produksi p,HI_DAY.histori_produksi_makanan hpr, HI_DAY.aset a, hi_day.produk pr where\
                p.email = hpr.email and p.waktu_awal = hpr.waktu_awal and hpr.id_alat_produksi = a.id and hpr.id_produk_makanan = pr.id")
                rekap = dictfetchall(cursor)
                context = {'hprm': rekap}

    if request.session['peran'] == 'pengguna':
        email = request.session['email']
        with connection.cursor() as cursor:
            cursor.execute("SELECT p.*, a.nama, pr.nama as makan FROM HI_DAY.histori_produksi p,HI_DAY.histori_produksi_makanan hpr, HI_DAY.aset a, hi_day.produk pr where\
            hpr.email = %s and p.email = hpr.email  and p.waktu_awal = hpr.waktu_awal and hpr.id_alat_produksi = a.id and hpr.id_produk_makanan = pr.id",[email])
            rekap = dictfetchall(cursor)
            context = {'hprm': rekap}

    return render(request, 'read_hispro_makanan.html', context)


def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def create_histori_tanaman(request):
    return render(request, 'create_histori_tanaman.html')
