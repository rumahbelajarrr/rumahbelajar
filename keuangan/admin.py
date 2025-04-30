from django.contrib import admin

from keuangan.models import PembayaranSPP,Siswa, Pemasukan, Pengeluaran, Tagihan, RekapitulasiKeuangan,OrangTua

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'nis', 'kelas')
    search_fields = ('nama', 'nis', 'kelas')
    list_filter = ('kelas',)

@admin.register(Pemasukan)
class PemasukanAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'tanggal', 'jumlah', 'jenis')
    search_fields = ('siswa__nama', 'jenis')
    list_filter = ('jenis', 'tanggal')

@admin.register(Pengeluaran)
class PengeluaranAdmin(admin.ModelAdmin):
    list_display = ('keterangan', 'tanggal', 'jumlah')
    search_fields = ('keterangan',)
    list_filter = ('tanggal',)

@admin.register(Tagihan)
class TagihanAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'bulan', 'spp', 'catering', 'daftar_ulang')
    search_fields = ('siswa__nama',)
    list_filter = ('bulan',)

@admin.register(RekapitulasiKeuangan)
class RekapitulasiKeuanganAdmin(admin.ModelAdmin):
    list_display = ('bulan', 'total_pemasukan', 'total_pengeluaran')
    list_filter = ('bulan',)

@admin.register(PembayaranSPP)
class PembayaranSPPAdmin(admin.ModelAdmin):
    list_display = ('siswa', 'bulan', 'jumlah_bayar', 'status_bayar', 'tanggal_bayar', 'bukti_pembayaran')
    list_filter = ('bulan', 'status_bayar')
    search_fields = ('siswa__nama', 'bulan')
    list_editable = ('status_bayar',)


@admin.register(OrangTua)
class OrangTuaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'user', 'alamat', 'no_telp')
    search_fields = ('nama', 'user__username', 'no_telp')
    list_filter = ('alamat',)
