from django.shortcuts import render, redirect
from .models import Absensi, Siswa, Guru, JadwalLes, OrangTua
from .forms import AbsensiForm
from django.contrib.auth.decorators import login_required, group_required
import qrcode
from django.http import HttpResponse
from io import BytesIO
from datetime import date

@login_required
@group_required('Siswa')
def absensi_siswa(request):
    if request.user.groups.filter(name='Siswa').exists():
        siswa = Siswa.objects.get(user=request.user)
        if request.method == 'POST':
            form = AbsensiForm(request.POST)
            if form.is_valid():
                absensi = form.save(commit=False)
                absensi.siswa = siswa
                absensi.save()
                return redirect('absensi_siswa')  # Ganti dengan nama URL kamu
        else:
            form = AbsensiForm()
        return render(request, 'siswa/absensi_siswa.html', {'form': form})
    else:
        return redirect('home')  # Ganti dengan halaman utama

@login_required
@group_required('Siswa')
def lihat_absensi_sendiri(request):
    siswa = request.user.siswa
    absen = Absensi.objects.filter(siswa=siswa)
    return render(request, 'siswa/absensi.html', {'absen': absen})



@login_required
def jadwal_les(request):
    jadwal = JadwalLes.objects.all()
    return render(request, 'jadwal_les.html', {'jadwal': jadwal})


@login_required
@group_required('Guru')
def absen_guru(request):
    if request.user.groups.filter(name='Guru').exists():
        guru = Guru.objects.get(user=request.user)
        if request.method == 'POST':
            form = AbsensiForm(request.POST)
            if form.is_valid():
                absensi = form.save(commit=False)
                absensi.guru = guru
                absensi.save()
                return redirect('absen_guru')  # Ganti dengan nama URL kamu
        else:
            form = AbsensiForm()
        return render(request, 'guru/absen_guru.html', {'form': form})
    else:
        return redirect('home')
    
@login_required
@group_required('Guru')
def absenkan_siswa(request, siswa_id):
    siswa = Siswa.objects.get(id=siswa_id)
    Absensi.objects.create(
        siswa=siswa,
        tanggal=date.today(),
        status='Hadir',
        metode_absensi='Input Manual'
    )
    return redirect('daftar_siswa.html')

@login_required
@group_required('Guru')
def lihat_absensi_siswa(request):
    absen = Absensi.objects.all().order_by('-tanggal')
    return render(request, 'guru/absensi_siswa.html', {'absen': absen})


@login_required
@group_required('Guru')
def lihat_jadwal_guru(request):
    jadwal = JadwalLes.objects.all()
    return render(request, 'guru/jadwal.html', {'jadwal': jadwal})



@login_required
@group_required('Admin')
def dashboard_admin(request):
    semua_absen = Absensi.objects.all()
    semua_jadwal = JadwalLes.objects.all()
    return render(request, 'admin/dashboard.html', {
        'absen': semua_absen,
        'jadwal': semua_jadwal
    })


    
