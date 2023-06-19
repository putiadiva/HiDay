from django.urls import path
from .views import detail_lumbung, read_upgrade_lumbung_admin, read_upgrade_lumbung_pengguna, create_upgrade_lumbung, isi_lumbung
app_name = 'lumbung'

urlpatterns = [
    path('', detail_lumbung, name='detail_lumbung'),
    path('list_upgrade',read_upgrade_lumbung_pengguna, name='upgrade_pengguna'),
    path('list_upgrade_admin',read_upgrade_lumbung_admin, name='upgrade_admin'),
    path('upgrade_lumbung',create_upgrade_lumbung, name='upgrade_lumbung'),
    path('isi_lumbung',isi_lumbung, name='isi_lumbung'),
]