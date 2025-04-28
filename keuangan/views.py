from django.shortcuts import render
from .models import Siswa, Pemasukan, Pengeluaran, RekapitulasiKeuangan, PembayaranSPP
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from .forms import BuktiPembayaranForm
import openpyxl  # Add this import
from io import BytesIO



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




@user_passes_test(Siswa, login_url='/login/')
@login_required
def tagihan_spp(request):
    # Ambil data siswa berdasarkan user yang login
    siswa = get_object_or_404(Siswa, user=request.user)

    # Ambil semua tagihan siswa tersebut
    pembayaran_list = PembayaranSPP.objects.filter(siswa=siswa).order_by('bulan')

    if request.method == 'POST':
        pembayaran_id = request.POST.get('pembayaran_id')
        pembayaran = get_object_or_404(PembayaranSPP, id=pembayaran_id, siswa=siswa)

        form = BuktiPembayaranForm(request.POST, request.FILES, instance=pembayaran)
        if form.is_valid():
            # Simpan bukti pembayaran dan ubah status jadi "pending" atau lainnya
            pembayaran.status = 'pending'  # optional: kalau ada field status
            form.save()

            # Email dimatiin
            # send_mail(
            #     subject=f'Bukti Pembayaran SPP Masuk - {pembayaran.siswa.nama}',
            #     message=f'Siswa {pembayaran.siswa.nama} telah mengupload bukti pembayaran untuk bulan {pembayaran.bulan}. Jumlah yang dibayar: {pembayaran.jumlah_bayar}.',
            #     from_email=settings.EMAIL_HOST_USER,
            #     recipient_list=[settings.ADMIN_EMAIL],
            #     fail_silently=False,
            # )

            return redirect('tagihan_spp')
    else:
        form = BuktiPembayaranForm()

    return render(request, 'keuangan/siswa/tagihan_spp.html', {
        'pembayaran_list': pembayaran_list,
        'form': form
    })


@login_required
def kelola_pembayaran(request):
    # Ambil daftar semua kelas unik
    kelas_list = Siswa.objects.values_list('kelas', flat=True).distinct()

    kelas_terpilih = request.GET.get('kelas')
    search_nama = request.GET.get('search_nama')

    pembayaran_list = PembayaranSPP.objects.all()

    if kelas_terpilih:
        pembayaran_list = pembayaran_list.filter(siswa__kelas=kelas_terpilih)

    if search_nama:
        pembayaran_list = pembayaran_list.filter(siswa_nama_icontains=search_nama)

    pembayaran_list = pembayaran_list.order_by('siswa__nama', 'bulan')

    if request.method == 'POST':
        pembayaran_id = request.POST.get('pembayaran_id')
        pembayaran = get_object_or_404(PembayaranSPP, id=pembayaran_id)

        pembayaran.status_bayar = 'lunas'
        pembayaran.save()

        redirect_url = request.path
        if kelas_terpilih or search_nama:
            redirect_url += '?'
            if kelas_terpilih:
                redirect_url += f'kelas={kelas_terpilih}&'
            if search_nama:
                redirect_url += f'search_nama={search_nama}'

        return redirect(redirect_url)

    return render(request, 'keuangan/admin/kelola_pembayaran.html', {
        'pembayaran_list': pembayaran_list,
        'kelas_list': kelas_list,
        'kelas_terpilih': kelas_terpilih,
        'search_nama': search_nama,
    })


def export_pembayaran_excel(request):
    # Create a new workbook and select the active worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Pembayaran SPP"

    # Header Row
    ws.append(['Nama Siswa', 'Kelas', 'Bulan', 'Jumlah Bayar', 'Status', 'Tanggal Bayar'])

    # Filter PembayaranSPP based on query parameters (kelas and search_nama)
 

    # Start filtering PembayaranSPP
    pembayaran_list = PembayaranSPP.objects.all().order_by('siswa__nama')
    # Adding data rows
    for bayar in pembayaran_list:
        ws.append([
            bayar.siswa.nama,  # Siswa Name
            bayar.siswa.kelas,  # Kelas
            bayar.get_bulan_display(),  # Month using get_bulan_display
            bayar.jumlah_bayar,  # Amount Paid
            bayar.status_bayar,  # Payment Status
            bayar.tanggal_bayar.strftime("%d-%m-%Y") if bayar.tanggal_bayar else '-',  # Payment Date
        ])

    # Save workbook to memory (using BytesIO)
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Return the response with the Excel file for download
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=pembayaran_spp.xlsx'
    return response
    
