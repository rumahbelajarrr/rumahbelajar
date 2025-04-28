from django.shortcuts import render, redirect
from .models import Absensi, Siswa, Guru, JadwalLes, OrangTua
from .forms import AbsensiForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
import qrcode
from django.http import HttpResponse
from io import BytesIO
from datetime import date
from django.contrib.auth import authenticate, login,logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages



# Dekorator custom
def group_required(group_name):
    def in_group(user):
        return user.is_authenticated and user.groups.filter(name=group_name).exists()
    return user_passes_test(in_group, login_url='home')  # Redirect kalau gak sesuai grup

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
    
def redirect_dashboard(request):
    if request.user.groups.filter(name='Admin').exists():
        return redirect('rumahbelajar:dashboard_admin')
    elif request.user.groups.filter(name='Guru').exists():
        return redirect('rumahbelajar:dashboard_guru')
    elif request.user.groups.filter(name='Siswa').exists():
        return redirect('rumahbelajar:dashboard_Siswa')
    elif request.user.groups.filter(name='OrangTua').exists():
        return redirect('rumahbelajar:dashboard_OrangTua')
    else:
        return redirect('home')  # Jika role tidak terdaftar
 
@login_required
@group_required('Guru')   
def dashboard_guru(request):
    return render(request, 'guru/dashboard_guru.html')

@login_required
@group_required('Siswa')
def dashboard_siswa(request):
    return render(request, 'siswa/dashboard_Siswa.html')

@login_required
@group_required('OrangTua')
def dashboard_orangtua(request):
    return render(request, 'orangtua/dashboard_OrangTua.html')


def home(request):
    """Halaman Home - Halaman utama aplikasi"""
    return render(request, 'absensi/home.html')  

def logout_view(request):
    logout(request)
    return redirect('home') 


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('rumahbelajar:redirect_dashboard')  # Ganti ke halaman utama lo
        else:
            messages.error(request, 'Username atau password salah!')
    return render(request, 'absensi/login.html')  # Pastikan ada template login.html



