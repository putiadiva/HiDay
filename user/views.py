from django.shortcuts import render, redirect
from django.forms import formset_factory
from django.db import connection
from .forms import LoginForm, RegisterAdminForm, RegisterPenggunaForm


def login(request):
    # Belum Login
    if 'is_login' not in request.session:
        form = LoginForm()
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                # check di tabel user
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"SELECT * FROM HI_DAY.PENGGUNA WHERE email='{email}' AND password='{password}'")
                    data_pengguna = cursor.fetchone()

                    cursor.execute(
                        f"SELECT * FROM HI_DAY.ADMIN WHERE email='{email}' AND password='{password}'")
                    data_admin = cursor.fetchone()

                # User Ketemu
                if data_pengguna:
                    # cari tipe user
                    request.session['email'] = email
                    request.session['peran'] = "pengguna"
                    request.session['is_login'] = True

                    return redirect('main:home')

                if data_admin:
                    # cari tipe user
                    request.session['email'] = email
                    request.session['peran'] = "admin"
                    request.session['is_login'] = True

                    return redirect('main:home')
                # User Tidak Ketemu
                else:
                    return render(request, 'login.html', {'form': form, 'message': 'User tidak ditemukan!'})
        # Method Get (Halaman Login)
        return render(request, 'login.html', {'form': form})
    # Sudah Login
    else:
        return redirect('user:login_or_register')


def login_or_register(request):
    # Belum Login
    if 'is_login' not in request.session:
        return render(request, 'login_or_register.html')
    else:
        email = request.session['email']
        peran = request.session['peran']
        context = {'email': email, 'peran': peran}
        if peran == 'pengguna':
            return redirect('main:home')
        if peran == 'admin':
            return redirect('main:home')


def pilih_role(request):
    if 'is_login' in request.session:
        return redirect('user:login')
    return render(request, 'pilih_role.html')


def register_admin(request):
    if 'is_login' in request.session:
        return redirect('main:home_admin')
    # Belum Login
    form = RegisterAdminForm()
    if request.method == "POST":
        form = RegisterAdminForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            new_data = [email, password]
            # lolos trigger
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO HI_DAY.AKUN VALUES (%s)", [email])
                    cursor.execute(
                        f"INSERT INTO HI_DAY.ADMIN VALUES (%s, %s)", new_data)

                request.session['email'] = email
                request.session['peran'] = 'admin'
                request.session['is_login'] = True
                return redirect('user:login_or_register')
            # galolos trigger
            except:
                print('galolos trigger')
                return render(request, 'register_admin.html', {'form': form, 'message': 'Password Anda belum memenuhi syarat, silahkan pastikan bahwa password minimal terdapat 1 huruf kapital dan 1 angka!'})
    # Method Get (Halaman Login)
    return render(request, 'register_admin.html', {'form': form})


def register_pengguna(request):
    if 'is_login' in request.session:
        return redirect('main:home_pengguna')
    # Belum login
    form = RegisterPenggunaForm()
    if request.method == "POST":
        form = RegisterPenggunaForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            nama_area = form.cleaned_data['nama_area']
            new_data = [email, password, nama_area]
            # lolos trigger
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO HI_DAY.AKUN VALUES (%s)", [email])
                    cursor.execute(
                        f"INSERT INTO HI_DAY.PENGGUNA VALUES (%s, %s, %s)", new_data)

                request.session['email'] = email
                request.session['peran'] = 'pengguna'
                request.session['is_login'] = True
                return redirect('user:login_or_register')
            # galolos trigger
            except:
                print('galolos trigger')
                return render(request, 'register_pengguna.html', {'form': form, 'message': 'Password Anda belum memenuhi syarat, silahkan pastikan bahwa password minimal terdapat 1 huruf kapital dan 1 angka!'})
    # Method Get (Halaman Login)
    return render(request, 'register_pengguna.html', {'form': form})

def logout_view(request):
    del request.session['email']
    del request.session['peran']
    del request.session['is_login']
    return redirect('user:login')

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
