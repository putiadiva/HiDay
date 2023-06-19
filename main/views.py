from django.shortcuts import render
from django.shortcuts import redirect
from django.db import connection
from decimal import Context



def user_login_required(function):
    def wrapper(request, *args, **kwargs):
        if 'is_login' not in request.session:
            return redirect('user:login_or_register')
        else:
            return function(request, *args, **kwargs)
    return wrapper

# @user_login_required
# def home_admin(request):
#     if request.session['peran'] != 'admin':
#         return redirect('user:login_or_register')
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT * FROM HI_DAY.ADMIN")
#         admin = dictfetchall(cursor)
#     context = {'adm': admin}
# return render(request, 'main/home_admin.html')

def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

@user_login_required
def home_pengguna(request):
    if 'is_login' not in request.session:
        return render(request, 'login_or_register.html')
    else:
        if request.session['peran'] == 'admin':
            email = request.session['email']
            context = {'email': email}

        if request.session['peran'] == 'pengguna':
            email = request.session['email']
            with connection.cursor() as cursor:
                    cursor.execute("SELECT * FROM HI_DAY.PENGGUNA WHERE email= %s", [email] )
                    data_pengguna = dictfetchall(cursor)
                    context = data_pengguna[0]

    return render(request, 'main/home_pengguna.html', context)


