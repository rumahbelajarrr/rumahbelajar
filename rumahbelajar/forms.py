from django import forms
from .models import Absensi


class AbsensiForm(forms.ModelForm):
    class Meta:
        model = Absensi
        fields = ['siswa', 'guru', 'status', 'metode_absensi']

