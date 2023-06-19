from django.shortcuts import render, redirect
from django.db import connection
from .forms import CreateProdukForm,UpdateProdukForm
from django.http import HttpResponseRedirect
from django.urls import reverse

def inc(code, inc_id):
        res = code
        nilai = int(inc_id)
        nilai += 1
        res += str(nilai).zfill(3)
        return res

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def update_produk(request):
    if request.method == 'GET':
        print(request.GET)
        if request.GET.get('id') is not None:
            id_produk = request.GET.get('id')
            if id_produk[0:2] == "HP":
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select id, nama, harga_jual, sifat_produk from hi_day.PRODUK,hi_day.Hasil_Panen where id = id_produk and id like 'HP%%' and id=%s", [id_produk])
                    data = dictfetchall(cursor)
                data_aset = {}
                print(data)
                data_aset['jenis_produk'] = 'Hasil Panen'
            elif id_produk[0:2] == "PH":
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select id, nama, harga_jual, sifat_produk from hi_day.PRODUK,hi_day.PRODUK_HEWAN where id = id_produk and id like 'PH%%' and id=%s", [id_produk])
                    data = dictfetchall(cursor)
                data_aset = {}
                print(data)
                data_aset['jenis_produk'] = 'Produk Hewan'
            elif id_produk[0:2] == "PM":
                with connection.cursor() as cursor:
                    cursor.execute(
                        "select id, nama, harga_jual, sifat_produk from hi_day.PRODUK,hi_day.PRODUK_MAKANAN where id = id_produk and id like 'PM%%' and id=%s", [id_produk])
                    data = dictfetchall(cursor)
                data_aset = {}
                print(data)
                data_aset['jenis_produk'] = 'Produk Makanan'
            data_aset['nama'] = data[0]['nama']
            data_aset['harga_jual'] = data[0]['harga_jual']
            data_aset['sifat_produk'] = data[0]['sifat_produk']
            form = UpdateProdukForm(initial=data_aset)
    else:
        nama = request.POST['nama']
        harga_jual = request.POST['harga_jual']
        sifat_produk = request.POST['sifat_produk']
        tmp_aset = [harga_jual, sifat_produk, nama]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE HI_DAY.PRODUK SET harga_jual = %s, sifat_produk = %s WHERE nama = %s", tmp_aset)
        return redirect('produk:read_produk')
    return render(request, 'update_produk.html', {'form':form})

def delete_produk(request):
    if request.method == 'GET':
        if request.GET.get('id') is not None:
            id_produk = request.GET.get('id')
            with connection.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM HI_DAY.PRODUK WHERE id = %s', [id_produk])
    return HttpResponseRedirect(reverse('produk:read_produk'))

def read_produk(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM HI_DAY.produk")
        rekap = dictfetchall(cursor)

        for i in range(len(rekap)):
            deletion = False
            temp = rekap[i]['id']
            cursor.execute("select * from hi_day.detail_pesanan where id_produk= %s", [temp]) 
            avail = dictfetchall(cursor)

            cursor.execute("select * from hi_day.lumbung_memiliki_produk where id_produk= %s", [temp]) 
            refer_lmp = dictfetchall(cursor)

            cursor.execute("select * from hi_day.produk_dibutuhkan_oleh_produk_makanan where id_produk_makanan= %s and id_produk= %s", [temp,temp]) 
            refer_pdopm = dictfetchall(cursor)

            cursor.execute("select * from hi_day.produksi where id_produk_makanan= %s", [temp]) 
            refer_p = dictfetchall(cursor)

            cursor.execute("select * from hi_day.hewan_menghasilkan_produk_hewan where id_produk_hewan= %s", [temp]) 
            refer_hmph = dictfetchall(cursor)
            
            cursor.execute("select * from hi_day.bibit_tanaman_menghasilkan_hasil_panen where id_hasil_panen= %s", [temp]) 
            refer_btmhp = dictfetchall(cursor)

            if avail == [] and refer_lmp == [] and refer_pdopm == [] and refer_p == [] and refer_hmph == [] and refer_btmhp == []:
                deletion = True
            
            rekap[i]['deletion'] = deletion
            print(rekap)
        context = {'produk': rekap}
        return render(request, 'read_produk.html', context)


def create_produk(request):
    form = CreateProdukForm()
    if request.method == "POST":
        new_id=''
        jenis_produk = request.POST['jenis_produk']
        nama = request.POST['nama']
        harga_jual = request.POST['harga_jual']
        sifat_produk = request.POST['sifat_produk']

        if jenis_produk == "Hasil Panen":
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ID_PRODUK FROM HI_DAY.HASIL_PANEN WHERE ID_PRODUK LIKE 'HP%' ORDER BY ID_PRODUK DESC LIMIT 1")
                new_id = inc("HP",cursor.fetchall()[0][0][2:])
        elif jenis_produk == "Produk Hewan":
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ID_PRODUK FROM HI_DAY.PRODUK_HEWAN WHERE ID_PRODUK LIKE 'PH%' ORDER BY ID_PRODUK DESC LIMIT 1")
                new_id = inc("PH",cursor.fetchall()[0][0][2:])
        elif jenis_produk == "Produk Makanan":
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ID_PRODUK FROM HI_DAY.PRODUK_MAKANAN WHERE ID_PRODUK LIKE 'PM%' ORDER BY ID_PRODUK DESC LIMIT 1")
                new_id = inc("PM",cursor.fetchall()[0][0][2:])
        id_produk = new_id
        new_data = [id_produk, nama,harga_jual,sifat_produk]

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO HI_DAY.PRODUK VALUES (%s, %s, %s, %s)", new_data)
        
        if jenis_produk == "Hasil Panen":
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO HI_DAY.HASIL_PANEN VALUES (%s)", [id_produk])
        elif jenis_produk == "Produk Hewan":
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO HI_DAY.PRODUK_HEWAN VALUES (%s)", [id_produk])
        elif jenis_produk == "Produk Makanan":
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO HI_DAY.PRODUK_MAKANAN VALUES (%s)", [id_produk])
        return redirect('produk:read_produk')
        
    return render(request, 'create_produk.html', {'form': form})  