from django.db import models
from django.contrib.auth.models import User




class OrangTua(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rumahbelajar_orangtua')
    nama = models.CharField(max_length=100)
    alamat = models.TextField()
    no_telp = models.CharField(max_length=15)

    def __str__(self):
        return self.nama


class Siswa(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rumahbelajar_siswa')
    nama = models.CharField(max_length=100)
    tanggal_lahir = models.DateField()
    jenis_kelamin = models.CharField(max_length=10)
    orang_tua = models.ForeignKey(OrangTua, on_delete=models.CASCADE)

    def __str__(self):
        return self.nama


class Guru(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nama = models.CharField(max_length=100)
    no_telp = models.CharField(max_length=15)
    mata_pelajaran = models.CharField(max_length=100)

    def __str__(self):
        return self.nama


class JadwalLes(models.Model):
    hari = models.CharField(max_length=10)  # Senin, Selasa, dst
    jam = models.TimeField()
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.hari} - {self.jam} - {self.guru.nama}"


class Absensi(models.Model):
    STATUS_CHOICES = [
        ('Hadir', 'Hadir'),
        ('Tidak Hadir', 'Tidak Hadir'),
    ]

    METODE_ABSEN_CHOICES = [
        ('QR Code', 'QR Code'),
        ('Input Manual', 'Input Manual'),
    ]

    siswa = models.ForeignKey(Siswa, on_delete=models.CASCADE, null=True, blank=True)
    guru = models.ForeignKey(Guru, on_delete=models.CASCADE, null=True, blank=True)
    tanggal = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    metode_absensi = models.CharField(max_length=30, choices=METODE_ABSEN_CHOICES)

    def __str__(self):
        if self.siswa:
            return f"Absensi Siswa - {self.siswa.nama} - {self.tanggal}"
        elif self.guru:
            return f"Absensi Guru - {self.guru.nama} - {self.tanggal}"
        return "Absensi Tidak Lengkap"

