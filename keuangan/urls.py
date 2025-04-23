from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('siswa/', views.daftar_siswa, name='daftar_siswa'),
    path('pemasukan/', views.daftar_pemasukan, name='daftar_pemasukan'),
    path('pengeluaran/', views.daftar_pengeluaran, name='daftar_pengeluaran'),
    path('rekap/', views.rekap_keuangan, name='rekap_keuangan'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)