# Generated by Django 4.2.7 on 2025-05-31 07:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyQRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(default=django.utils.timezone.localdate, unique=True)),
                ('qrcode', models.ImageField(upload_to='qr_codes/')),
            ],
        ),
        migrations.CreateModel(
            name='Guru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('nip', models.CharField(blank=True, max_length=20, null=True)),
                ('alamat_guru', models.TextField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rumahbelajar_guru', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Kelas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='MataPelajaran',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama_pelajaran', models.CharField(max_length=100)),
                ('kode_pelajaran', models.CharField(max_length=100)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mata_pelajaran', to='rumahbelajar.kelas')),
            ],
        ),
        migrations.CreateModel(
            name='OrangTua',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('alamat', models.TextField()),
                ('no_telp', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rumahbelajar_orangtua', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Presensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari', models.CharField(max_length=20)),
                ('jam', models.CharField(max_length=20)),
                ('pertemuan_ke', models.PositiveIntegerField(blank=True, null=True)),
                ('kelas', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.kelas')),
                ('mata_pelajaran', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.matapelajaran')),
            ],
        ),
        migrations.CreateModel(
            name='Siswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=100)),
                ('tanggal_lahir', models.DateField()),
                ('jenis_kelamin', models.CharField(max_length=10)),
                ('kelas', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='siswa', to='rumahbelajar.kelas')),
                ('orang_tua', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.orangtua')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rumahbelajar_siswa', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QRCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pertemuan', models.IntegerField()),
                ('kode', models.CharField(max_length=255)),
                ('gambar_qr', models.ImageField(blank=True, null=True, upload_to='qr_code/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('jadwal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.matapelajaran')),
            ],
        ),
        migrations.CreateModel(
            name='PresensiSiswa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('waktu_presensi', models.DateTimeField(auto_now_add=True)),
                ('pertemuan_ke', models.PositiveIntegerField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Hadir', 'Hadir'), ('Tidak Hadir', 'Tidak Hadir')], max_length=20)),
                ('presensi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='presensi_siswa', to='rumahbelajar.presensi')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.siswa')),
            ],
        ),
        migrations.CreateModel(
            name='PresensiGuru',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField()),
                ('jam_masuk', models.TimeField()),
                ('status', models.CharField(choices=[('Hadir', 'Hadir'), ('Izin', 'Izin'), ('Sakit', 'Sakit'), ('Tanpa Keterangan', 'Tanpa Keterangan')], max_length=20)),
                ('keterangan', models.TextField(blank=True, null=True)),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.guru')),
            ],
            options={
                'ordering': ['-tanggal', '-jam_masuk'],
            },
        ),
        migrations.CreateModel(
            name='JadwalLes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hari', models.CharField(max_length=10)),
                ('jam', models.TimeField()),
                ('guru', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.guru')),
                ('mata_pelajaran', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.matapelajaran')),
            ],
        ),
        migrations.CreateModel(
            name='DetailPresensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=20)),
                ('waktu_presensi', models.DateTimeField(auto_now_add=True)),
                ('presensi', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.presensi')),
                ('siswa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.siswa')),
            ],
        ),
        migrations.CreateModel(
            name='Absensi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tanggal', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Hadir', 'Hadir'), ('Tidak Hadir', 'Tidak Hadir')], max_length=20)),
                ('metode_absensi', models.CharField(choices=[('QR Code', 'QR Code'), ('Input Manual', 'Input Manual')], max_length=30)),
                ('jam_absensi', models.TimeField(default=django.utils.timezone.now)),
                ('guru', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.guru')),
                ('siswa', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rumahbelajar.siswa')),
            ],
            options={
                'unique_together': {('guru', 'tanggal')},
            },
        ),
    ]
