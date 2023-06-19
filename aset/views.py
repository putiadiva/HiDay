from django.shortcuts import render, redirect
from .forms import *
from django.db import connection
from django.http import HttpResponseRedirect
from django.urls import reverse

def opsi_buat_aset(request):
    return render(request, 'opsi_buat_aset.html')

def opsi_liat_aset(request):
    return render(request, 'opsi_liat_aset.html')

def hewan_menghasilkan_produk_hewan(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from hi_day.hewan_menghasilkan_produk_hewan")
        tmp = dictfetchall(cursor)
    context = {'list': tmp}
    return render(request, 'hewan_menghasilkan_produk_hewan.html', context)

def bibit_menghasilkan_panen(request):
    with connection.cursor() as cursor:
        cursor.execute("select * from hi_day.bibit_tanaman_menghasilkan_hasil_panen")
        tmp = dictfetchall(cursor)
    context = {'list': tmp}
    return render(request, 'bibit_tanaman_menghasilkan_hasil_panen.html', context)

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def create_dekorasi(request):
    form = CreateDekorasiForm()
    if request.method == "POST":
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        harga_jual = request.POST['harga_jual']
        tmp_aset = [id_aset, nama, minimum_level, harga_beli]
        tmp_dekor = [id_aset, harga_jual]
        
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.ASET VALUES (%s, %s, %s, %s)', tmp_aset)
            cursor.execute(
                'INSERT INTO HI_DAY.DEKORASI VALUES (%s, %s)', tmp_dekor)
        return redirect('aset:list_dekorasi')
    return render(request, 'create_aset.html', {'form': form, 'type':'Dekorasi'})

def update_dekorasi(request):
    if request.method == 'GET':
        print(request.GET)
        if request.GET.get('id_aset') is not None:
            id_aset = request.GET.get('id_aset')
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id, nama, minimum_level, harga_beli, harga_jual from hi_day.aset, hi_day.dekorasi where id = id_aset and id like 'DK%%' and id=%s", [id_aset])
                data = dictfetchall(cursor)
            data_aset = {}
            print(data)
            data_aset['id_aset'] = data[0]['id']
            data_aset['nama'] = data[0]['nama']
            data_aset['minimum_level'] = data[0]['minimum_level']
            data_aset['harga_beli'] = data[0]['harga_beli']
            data_aset['harga_jual'] = data[0]['harga_jual']
            form = UpdateDekorasiForm(initial=data_aset)
    else:
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        harga_jual = request.POST['harga_jual']
        tmp_aset = [minimum_level, harga_beli, id_aset, nama]
        tmp_dekor = [harga_jual, id_aset]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE HI_DAY.ASET SET minimum_level = %s, harga_beli = %s WHERE id = %s and nama = %s", tmp_aset)
            cursor.execute(
                "UPDATE HI_DAY.DEKORASI SET harga_jual = %s WHERE id_aset = %s", tmp_dekor)
        return redirect('aset:list_dekorasi')
    return render(request, 'update_aset.html', {'form': form, 'type':'Dekorasi'})

def read_dekorasi(request):
    with connection.cursor() as cursor:
        cursor.execute("select id_aset, nama, minimum_level, harga_beli, harga_jual from hi_day.aset, hi_day.dekorasi where id = id_aset and id like 'DK%' order by id asc")
        tmp = dictfetchall(cursor)

        for i in range(len(tmp)):
            deletion = False
            temp = tmp[i]['id_aset']
            cursor.execute("select * from hi_day.koleksi_aset_memiliki_aset where id_aset= %s", [temp]) 
            avail = dictfetchall(cursor)

            if avail == []:
                deletion = True
            
            tmp[i]['deletion'] = deletion
    context = {'list': tmp, 'type': 'Dekorasi'}
    return render(request, 'list_aset.html', context)

def create_bibit_tanaman(request):
    form = CreateBibitTanamanForm()
    if request.method == "POST":
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        durasi_panen = request.POST['durasi_panen']
        tmp_aset = [id_aset, nama, minimum_level, harga_beli]
        tmp_dekor = [id_aset, durasi_panen]
        
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.ASET VALUES (%s, %s, %s, %s)', tmp_aset)
            cursor.execute(
                'INSERT INTO HI_DAY.BIBIT_TANAMAN VALUES (%s, %s)', tmp_dekor)
        return redirect('aset:list_bibit_tanaman')
    return render(request, 'create_aset.html', {'form': form, 'type':'Bibit Tanaman'})

def update_bibit(request):
    if request.method == 'GET':
        print(request.GET)
        if request.GET.get('id_aset') is not None:
            id_aset = request.GET.get('id_aset')
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id, nama, minimum_level, harga_beli, durasi_panen from hi_day.aset, hi_day.bibit_tanaman where id = id_aset and id like 'BT%%' and id=%s", [id_aset])
                data = dictfetchall(cursor)
            data_aset = {}
            print(data)
            data_aset['id_aset'] = data[0]['id']
            data_aset['nama'] = data[0]['nama']
            data_aset['minimum_level'] = data[0]['minimum_level']
            data_aset['harga_beli'] = data[0]['harga_beli']
            data_aset['durasi_panen'] = data[0]['durasi_panen']
            form = UpdateBibitForm(initial=data_aset)
    else:
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        durasi_panen = request.POST['durasi_panen']
        tmp_aset = [minimum_level, harga_beli, id_aset, nama]
        tmp_bibit = [durasi_panen, id_aset]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE HI_DAY.ASET SET minimum_level = %s, harga_beli = %s WHERE id = %s and nama = %s", tmp_aset)
            cursor.execute(
                "UPDATE HI_DAY.BIBIT_TANAMAN SET durasi_panen = %s WHERE id_aset = %s", tmp_bibit)
        return redirect('aset:list_bibit_tanaman')
    return render(request, 'update_aset.html', {'form': form, 'type':'Bibit Tanaman'})

def read_bibit_tanaman(request):
    with connection.cursor() as cursor:
        cursor.execute("select id_aset, nama, minimum_level, harga_beli, durasi_panen from hi_day.aset, hi_day.bibit_tanaman where id = id_aset and id like 'BT%' order by id_aset asc")
        tmp = dictfetchall(cursor)

        for i in range(len(tmp)):
            deletion = False
            temp = tmp[i]['id_aset']
            cursor.execute("select * from hi_day.koleksi_aset_memiliki_aset where id_aset= %s", [temp]) 
            avail = dictfetchall(cursor)

            cursor.execute("select * from hi_day.bibit_tanaman_menghasilkan_hasil_panen where id_bibit_tanaman= %s", [temp]) 
            refer_btmhp = dictfetchall(cursor)

            cursor.execute("select * from hi_day.histori_tanaman where id_bibit_tanaman= %s", [temp]) 
            refer_hh = dictfetchall(cursor)

            if avail == [] and refer_btmhp == [] and refer_hh == []:
                deletion = True
            
            tmp[i]['deletion'] = deletion
    context = {'list': tmp, 'type': 'Bibit Tanaman'}
    return render(request, 'list_aset.html', context)

def create_kandang(request):
    form = CreateKandangForm()
    if request.method == "POST":
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        kapasitas_maks = request.POST['kapasitas_maks']
        jenis_hewan = request.POST['jenis_hewan']
        tmp_aset = [id_aset, nama, minimum_level, harga_beli]
        tmp_kandang = [id_aset, kapasitas_maks, jenis_hewan]
        
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.ASET VALUES (%s, %s, %s, %s)', tmp_aset)
            cursor.execute(
                'INSERT INTO HI_DAY.KANDANG VALUES (%s, %s, %s)', tmp_kandang)
        return redirect('aset:list_kandang')
    return render(request, 'create_aset.html', {'form': form, 'type':'Kandang'})

def update_kandang(request):
    if request.method == 'GET':
        print(request.GET)
        if request.GET.get('id_aset') is not None:
            id_aset = request.GET.get('id_aset')
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id, nama, minimum_level, harga_beli, kapasitas_maks, jenis_hewan from hi_day.aset, hi_day.kandang where id = id_aset and id like 'KD%%' and id=%s"
                     , [id_aset])
                data = dictfetchall(cursor)
            data_aset = {}
            data_aset['id_aset'] = data[0]['id']
            data_aset['nama'] = data[0]['nama']
            data_aset['minimum_level'] = data[0]['minimum_level']
            data_aset['harga_beli'] = data[0]['harga_beli']
            data_aset['kapasitas_maks'] = data[0]['kapasitas_maks']
            data_aset['jenis_hewan'] = data[0]['jenis_hewan']
            form = UpdateKandangForm(initial=data_aset)
    else:
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        kapasitas_maks = request.POST['kapasitas_maks']
        jenis_hewan = request.POST['jenis_hewan']
        tmp_aset = [minimum_level, harga_beli, id_aset, nama]
        tmp_kandang = [kapasitas_maks, jenis_hewan, id_aset]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE HI_DAY.ASET SET minimum_level = %s, harga_beli = %s WHERE id = %s and nama = %s", tmp_aset)
            cursor.execute(
                "UPDATE HI_DAY.KANDANG SET kapasitas_maks = %s, jenis_hewan = %s  WHERE id_aset = %s", tmp_kandang)
        return redirect('aset:list_kandang')
    return render(request, 'update_aset.html', {'form': form, 'type':'Kandang'})

def read_kandang(request):
    with connection.cursor() as cursor:
        cursor.execute("select id_aset, nama, minimum_level, harga_beli, kapasitas_maks, jenis_hewan from hi_day.aset, hi_day.kandang where id = id_aset and id like 'KD%' order by id_aset asc")
        tmp = dictfetchall(cursor)

        for i in range(len(tmp)):
            deletion = False
            temp = tmp[i]['id_aset']
            cursor.execute("select * from hi_day.koleksi_aset_memiliki_aset where id_aset= %s", [temp]) 
            avail = dictfetchall(cursor)

            if avail == []:
                deletion = True
            
            tmp[i]['deletion'] = deletion
    context = {'list': tmp, 'type': 'Kandang'}
    return render(request, 'list_aset.html', context)

def create_hewan(request):
    form = CreateHewanForm()
    state = ''
    if request.method == "POST":
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        durasi_produksi = request.POST['durasi_produksi']
        tmp_aset = [id_aset, nama, minimum_level, harga_beli]
        tmp_hewan = [id_aset, durasi_produksi]
        
        with connection.cursor() as cursor:
            cursor.execute(
                'select id_aset from hi_day.kandang where jenis_hewan =%s', [nama])
            try:
                id_kandang = str(cursor.fetchall()[0][0])
                tmp_hewan.append(id_kandang)
                cursor.execute(
                    'INSERT INTO HI_DAY.ASET VALUES (%s, %s, %s, %s)', tmp_aset)
                cursor.execute(
                    'INSERT INTO HI_DAY.HEWAN VALUES (%s, %s, %s)', tmp_hewan)
                return redirect('aset:list_hewan')
            except IndexError:
                state = 'not available'
    return render(request, 'create_aset.html', {'form': form, 'type':'Hewan', 'state': state})

def update_hewan(request):
    if request.method == 'GET':
        print(request.GET)
        if request.GET.get('id_aset') is not None:
            id_aset = request.GET.get('id_aset')
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id, nama, minimum_level, harga_beli, durasi_produksi, id_kandang from hi_day.aset, hi_day.hewan where id = id_aset and id like 'HW%%' and id=%s"
                     , [id_aset])
                data = dictfetchall(cursor)
            data_aset = {}
            data_aset['id_aset'] = data[0]['id']
            data_aset['nama'] = data[0]['nama']
            data_aset['minimum_level'] = data[0]['minimum_level']
            data_aset['harga_beli'] = data[0]['harga_beli']
            data_aset['durasi_produksi'] = data[0]['durasi_produksi']
            data_aset['id_kandang'] = data[0]['id_kandang']
            form = UpdateHewanForm(initial=data_aset)
    else:
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        durasi_produksi = request.POST['durasi_produksi']
        id_kandang = request.POST['id_kandang']
        tmp_aset = [minimum_level, harga_beli, id_aset, nama]
        tmp_hewan = [durasi_produksi, id_aset, id_kandang]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE HI_DAY.ASET SET minimum_level = %s, harga_beli = %s WHERE id = %s and nama = %s", tmp_aset)
            cursor.execute(
                "UPDATE HI_DAY.HEWAN SET durasi_produksi = %s WHERE id_aset = %s and id_kandang = %s", tmp_hewan)
        return redirect('aset:list_hewan')
    return render(request, 'update_aset.html', {'form': form, 'type':'Hewan'})

def read_hewan(request):
    with connection.cursor() as cursor:
        cursor.execute("select id_aset, nama, minimum_level, harga_beli, durasi_produksi, id_kandang from hi_day.aset, hi_day.hewan where id = id_aset and id like 'HW%' order by id_aset asc")
        tmp = dictfetchall(cursor)

        for i in range(len(tmp)):
            deletion = False
            temp = tmp[i]['id_aset']
            cursor.execute("select * from hi_day.koleksi_aset_memiliki_aset where id_aset= %s", [temp]) 
            avail = dictfetchall(cursor)

            cursor.execute("select * from hi_day.hewan_menghasilkan_produk_hewan where id_hewan= %s", [temp]) 
            refer_hmph = dictfetchall(cursor)

            cursor.execute("select * from hi_day.histori_hewan where id_hewan= %s", [temp]) 
            refer_hh = dictfetchall(cursor)

            if avail == [] and refer_hmph == [] and refer_hh == []:
                deletion = True
            
            tmp[i]['deletion'] = deletion
    context = {'list': tmp, 'type': 'Hewan'}
    return render(request, 'list_aset.html', context)

def create_alat(request):
    form = CreateAlatForm()
    state = ''
    if request.method == "POST":
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        kapasitas_maks = request.POST['kapasitas_maks']
        tmp_aset = [id_aset, nama, minimum_level, harga_beli]
        tmp_alat = [id_aset, kapasitas_maks]
        
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.ASET VALUES (%s, %s, %s, %s)', tmp_aset)
            cursor.execute(
                'INSERT INTO HI_DAY.ALAT_PRODUKSI VALUES (%s, %s)', tmp_alat)
            return redirect('aset:list_alat')
    return render(request, 'create_aset.html', {'form': form, 'type':'Alat Produksi', 'state': state})

def update_alat(request):
    if request.method == 'GET':
        print(request.GET)
        if request.GET.get('id_aset') is not None:
            id_aset = request.GET.get('id_aset')
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id, nama, minimum_level, harga_beli, kapasitas_maks from hi_day.aset, hi_day.alat_produksi where id = id_aset and id like 'AP%%' and id=%s"
                     , [id_aset])
                data = dictfetchall(cursor)
            data_aset = {}
            data_aset['id_aset'] = data[0]['id']
            data_aset['nama'] = data[0]['nama']
            data_aset['minimum_level'] = data[0]['minimum_level']
            data_aset['harga_beli'] = data[0]['harga_beli']
            data_aset['kapasitas_maks'] = data[0]['kapasitas_maks']
            form = UpdateAlatForm(initial=data_aset)
    else:
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        kapasitas_maks = request.POST['kapasitas_maks']
        tmp_aset = [minimum_level, harga_beli, id_aset, nama]
        tmp_alat = [kapasitas_maks, id_aset]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE HI_DAY.ASET SET minimum_level = %s, harga_beli = %s WHERE id = %s and nama = %s", tmp_aset)
            cursor.execute(
                "UPDATE HI_DAY.ALAT_PRODUKSI SET kapasitas_maks = %s WHERE id_aset = %s", tmp_alat)
        return redirect('aset:list_alat')
    return render(request, 'update_aset.html', {'form': form, 'type':'Alat Produksi'})

def read_alat(request):
    with connection.cursor() as cursor:
        cursor.execute("select id_aset, nama, minimum_level, harga_beli, kapasitas_maks from hi_day.aset, hi_day.alat_produksi where id = id_aset and id like 'AP%' order by id_aset asc")
        tmp = dictfetchall(cursor)

        for i in range(len(tmp)):
            deletion = False
            temp = tmp[i]['id_aset']
            cursor.execute("select * from hi_day.koleksi_aset_memiliki_aset where id_aset= %s", [temp]) 
            avail = dictfetchall(cursor)

            cursor.execute("select * from hi_day.produksi where id_alat_produksi= %s", [temp]) 
            refer_btmhp = dictfetchall(cursor)

            cursor.execute("select * from hi_day.histori_produksi_makanan where id_alat_produksi= %s", [temp]) 
            refer_hpm = dictfetchall(cursor)

            if avail == [] and refer_btmhp == [] and refer_hpm == []:
                deletion = True
            
            tmp[i]['deletion'] = deletion
    context = {'list': tmp, 'type': 'Alat Produksi'}
    return render(request, 'list_aset.html', context)

def create_petak(request):
    form = CreatePetakSawahForm()
    if request.method == "POST":
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        jenis_tanaman = request.POST['jenis_tanaman']
        tmp_aset = [id_aset, nama, minimum_level, harga_beli]
        tmp_petak = [id_aset, jenis_tanaman]
        
        with connection.cursor() as cursor:
            cursor.execute(
                'INSERT INTO HI_DAY.ASET VALUES (%s, %s, %s, %s)', tmp_aset)
            cursor.execute(
                'INSERT INTO HI_DAY.PETAK_SAWAH VALUES (%s, %s)', tmp_petak)
            return redirect('aset:list_petak')
    return render(request, 'create_aset.html', {'form': form, 'type':'Petak Sawah'})

def update_petak(request):
    if request.method == 'GET':
        print(request.GET)
        if request.GET.get('id_aset') is not None:
            id_aset = request.GET.get('id_aset')
            with connection.cursor() as cursor:
                cursor.execute(
                    "select id, nama, minimum_level, harga_beli, jenis_tanaman from hi_day.aset, hi_day.petak_sawah where id = id_aset and id like 'PS%%' and id=%s"
                     , [id_aset])
                data = dictfetchall(cursor)
            data_aset = {}
            data_aset['id_aset'] = data[0]['id']
            data_aset['nama'] = data[0]['nama']
            data_aset['minimum_level'] = data[0]['minimum_level']
            data_aset['harga_beli'] = data[0]['harga_beli']
            data_aset['jenis_tanaman'] = data[0]['jenis_tanaman']
            form = UpdatePetakSawahForm(initial=data_aset)
    else:
        id_aset = request.POST['id_aset']
        nama = request.POST['nama']
        minimum_level = request.POST['minimum_level']
        harga_beli = request.POST['harga_beli']
        jenis_tanaman = request.POST['jenis_tanaman']
        tmp_aset = [minimum_level, harga_beli, id_aset, nama]
        tmp_alat = [jenis_tanaman, id_aset]
        
        with connection.cursor() as cursor:
            cursor.execute(
                "UPDATE HI_DAY.ASET SET minimum_level = %s, harga_beli = %s WHERE id = %s and nama = %s", tmp_aset)
            cursor.execute(
                "UPDATE HI_DAY.petak_sawah SET jenis_tanaman = %s WHERE id_aset = %s", tmp_alat)
        return redirect('aset:list_petak')
    return render(request, 'update_aset.html', {'form': form, 'type':'Petak Sawah'})

def read_petak(request):
    with connection.cursor() as cursor:
        cursor.execute("select id_aset, nama, minimum_level, harga_beli, jenis_tanaman from hi_day.aset, hi_day.petak_sawah where id = id_aset and id like 'PS%' order by id_aset asc")
        tmp = dictfetchall(cursor)
        
        for i in range(len(tmp)):
            deletion = False
            temp = tmp[i]['id_aset']
            cursor.execute("select * from hi_day.koleksi_aset_memiliki_aset where id_aset= %s", [temp]) 
            avail = dictfetchall(cursor)

            if avail == []:
                deletion = True
            
            tmp[i]['deletion'] = deletion
    context = {'list': tmp, 'type': 'Petak Sawah'}
    return render(request, 'list_aset.html', context)

def delete_aset(request):
    if request.method == 'GET':
        if request.GET.get('id_aset') is not None:
            id_aset = request.GET.get('id_aset')
            with connection.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM HI_DAY.ASET WHERE id = %s', [id_aset])
    return HttpResponseRedirect(reverse('aset:liat_aset'))