from django.contrib import admin
from .models import OrangTua, Siswa, Guru, JadwalLes, Absensi

@admin.register(OrangTua)
class OrangTuaAdmin(admin.ModelAdmin):
    list_display = ['nama', 'user', 'no_telp']
    search_fields = ['nama', 'user__username']

@admin.register(Siswa)
class SiswaAdmin(admin.ModelAdmin):
    list_display = ['nama', 'user', 'orang_tua', 'tanggal_lahir', 'jenis_kelamin']
    search_fields = ['nama', 'user__username']
    list_filter = ['jenis_kelamin']

@admin.register(Guru)
class GuruAdmin(admin.ModelAdmin):
    list_display = ['nama', 'user', 'no_telp', 'mata_pelajaran']
    search_fields = ['nama', 'mata_pelajaran']

@admin.register(JadwalLes)
class JadwalLesAdmin(admin.ModelAdmin):
    list_display = ['hari', 'jam', 'guru']
    list_filter = ['hari', 'guru']

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    list_display = ['tanggal', 'siswa', 'guru', 'status', 'metode_absensi']
    list_filter = ['status', 'metode_absensi', 'tanggal']
    search_fields = ['siswa__nama', 'guru__nama']
