from django.urls import path
from .views import login, register_pengguna, register_admin, pilih_role, logout_view, login_or_register

app_name = 'user'
urlpatterns = [
    path('login/', login, name='login'),
    path('login_or_register/', login_or_register, name='login_or_register'),
    path('register_pengguna/', register_pengguna, name='register_pengguna'),
    path('register_admin/', register_admin, name='register_admin'),
    path('pilih_role/', pilih_role, name='pilih_role'),
    path('logout/', logout_view, name='logout'),
]