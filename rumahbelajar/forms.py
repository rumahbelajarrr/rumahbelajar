from django import forms
from .models import Absensi, Tagihan


class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ['siswa', 'guru', 'tingkat', 'metode_absensi']


class TagihanForm(forms.ModelForm):
    class Meta:
        model = Tagihan
        fields = ['siswa', 'jumlah', 'status', 'tanggal_jatuh_tempo']
