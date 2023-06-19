from django.shortcuts import render
from django.db import connection
from .forms import CreateProduksiForm

# Create your views here.

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def read_produksi(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT p.id_produk_makanan, pr.nama as nama_makanan, a.nama as nama_alat, p.durasi, p.jumlah_unit_hasil FROM HI_DAY.produksi p, HI_DAY.produk pr, HI_DAY.aset a where  p.id_alat_produksi= a.id and p.id_produk_makanan= pr.id")
        rekap = dictfetchall(cursor)
        print(rekap)
        context = {'produksi': rekap}
        return render(request, 'read_produksi.html', context)

def detail_produksi(request, id_produk_makanan):
    with connection.cursor() as cursor:
        cursor.execute(
           "SELECT p.id_produk_makanan, pr.nama as nama_makanan, a.nama as nama_alat, p.durasi, p.jumlah_unit_hasil FROM HI_DAY.produksi p, HI_DAY.produk pr, HI_DAY.aset a, HI_DAY.PRODUK_DIBUTUHKAN_OLEH_PRODUK_MAKANAN pdopm where p.id_produk_makanan = %s and p.id_alat_produksi= a.id and p.id_produk_makanan= pr.id and p.id_produk_makanan= pdopm.id_produk_makanan ", [id_produk_makanan]
           )
        rekap = dictfetchall(cursor)
        print(rekap)
    context = {'produksi': rekap}
    return render(request, 'detail_produksi.html', context)

def create_produksi(request):
    form = CreateProduksiForm()
    if request.method == "POST":
        new_id=''
        nama_makanan = request.POST['nama_makanan']
        alat_produksi = request.POST['alat_produksi']
        durasi = request.POST['durasi']
        jumlah_produk = request.POST['jumlah_produk']
        bahan = request.POST['bahan']
        jumlah_bahan = request.POST['jumlah_bahan']

        if jenis_produk == "Hasil Panen":
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT ID_PRODUK FROM HI_DAY.HASIL_PANEN WHERE ID_PRODUK LIKE 'HP%' ORDER BY ID_PRODUK DESC LIMIT 1")
                new_id = inc("HP",cursor.fetchall()[0][0][2:])
        id_produk = new_id
        new_data = [id_produk, nama,harga_jual,sifat_produk]

        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO HI_DAY.PRODUK VALUES (%s, %s, %s, %s)", new_data)
        
        if jenis_produk == "Hasil Panen":
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO HI_DAY.HASIL_PANEN VALUES (%s)", [id_produk])
        return redirect('produksi:read_produksi')
        
    return render(request, 'create_produksi.html', {'form': form})  