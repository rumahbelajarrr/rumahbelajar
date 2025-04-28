from django import forms
from .models import PembayaranSPP


class BuktiPembayaranForm(forms.ModelForm):
    class Meta:
        model = PembayaranSPP
        fields = ['bukti_pembayaran']
        
        