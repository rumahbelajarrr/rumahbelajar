from django.shortcuts import render
from .models import Siswa, Pemasukan, Pengeluaran, RekapitulasiKeuangan

def beranda(request):
    return render(request, 'keuangan/beranda.html')

def daftar_siswa(request):
    siswa = Siswa.objects.all()
    return render(request, 'keuangan/siswa.html', {'siswa_list': siswa})

def daftar_pemasukan(request):
    pemasukan = Pemasukan.objects.all().order_by('-tanggal')
    return render(request, 'keuangan/pemasukan.html', {'pemasukan_list': pemasukan})

def daftar_pengeluaran(request):
    pengeluaran = Pengeluaran.objects.all().order_by('-tanggal')
    return render(request, 'keuangan/pengeluaran.html', {'pengeluaran_list': pengeluaran})

def rekap_keuangan(request):
    rekap = RekapitulasiKeuangan.objects.all().order_by('-bulan')
    return render(request, 'keuangan/rekap.html', {'rekap_list': rekap})
