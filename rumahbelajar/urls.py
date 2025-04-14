from django.urls import path
from . import views

urlpatterns = [
    path('absensi/siswa/', views.absensi_siswa, name='absensi_siswa'),
    path('jadwal/', views.jadwal_les, name='jadwal_les'),
    path('absen/guru/', views.absen_guru, name='absen_guru'),
    path('lihat_absensi_sendiri/', views.lihat_absensi_sendiri, name='lihat_absensi_sendiri'),
    path('absenkan_siswa/<int:siswa_id>/', views.absenkan_siswa, name='absenkan_siswa'),
    path('lihat_absensi_siswa/', views.lihat_absensi_siswa, name='lihat_absensi_siswa'),
    path('lihat_jadwal_guru/', views.lihat_jadwal_guru, name='lihat_jadwal_guru'),
    path('dashboard_admin/', views.dashboard_admin, name='dashboard_admin'),
]
