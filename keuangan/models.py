from django.db import models
from django.contrib.auth.models import User

# Model untuk siswa
class Siswa(models.Model):
    nama = models.CharField(max_length=100)
    nis = models.CharField(max_length=20, unique=True)
    kelas = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.nama} ({self.nis})"

# Model untuk pemasukan
class Pemasukan(models.Model):
    JENIS_PEMASUKAN = [
        ('SPP', 'SPP'),
        ('CATERING', 'Catering'),
        ('DAFTAR_ULANG', 'Daftar Ulang'),
        ('LAINNYA', 'Lain-lain'),
    ]
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)
    jenis = models.CharField(max_length=20, choices=JENIS_PEMASUKAN)

    def __str__(self):
        return f"{self.jenis} - {self.jumlah}"

# Model untuk pengeluaran
class Pengeluaran(models.Model):
    keterangan = models.TextField()
    tanggal = models.DateField(auto_now_add=True)
    jumlah = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.keterangan} - {self.jumlah}"

# Model tagihan siswa
class Tagihan(models.Model):
    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE)
    bulan = models.DateField()
    spp = models.BooleanField(default=False)
    catering = models.BooleanField(default=False)
    daftar_ulang = models.BooleanField(default=False)

    def __str__(self):
        return f"Tagihan {self.siswa.nama} - {self.bulan.strftime('%B %Y')}"

# Model rekapitulasi keuangan
class RekapitulasiKeuangan(models.Model):
    bulan = models.DateField()
    total_pemasukan = models.DecimalField(max_digits=12, decimal_places=2)
    total_pengeluaran = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Rekap {self.bulan.strftime('%B %Y')}"