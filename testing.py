#Modul testing. pengujian program memakai library unittest.
#Jalankan dari folder proyek: python -m keuangan.testing.

import contextlib
import io
import os
import tempfile
import unittest

from keuangan import fileio
from keuangan.processing import Pengeluaran, PencatatKeuangan, jumlahkan
from keuangan.validasi import DataTidakValid, validasi_nominal, validasi_kategori

def senyap(fungsi, *args, **kwargs): #Jalankan fungsi menangkap print-nya, hasilnya (nilai, teks-output).
    penampung = io.StringIO()
    with contextlib.redirect_stdout(penampung):
        nilai = fungsi(*args, **kwargs)
    return nilai, penampung.getvalue()

class TestKeuangan(unittest.TestCase):
    def setUp(self): #Data contoh dibuat ulang sebelum setiap pengujian.
        self.pencatat = PencatatKeuangan()
        contoh = [
            ("2026-10-01", "makan", "Nasi goreng", 15000),
            ("2026-10-01", "transport", "Ojek", 22000),
            ("2026-10-02", "makan", "Ayam geprek", 18000),
            ("2026-10-02", "hiburan", "Langganan musik", 54000),
        ]
        for tanggal, kategori, keterangan, nominal in contoh:
            self.pencatat.tambah(Pengeluaran(tanggal=tanggal, kategori=kategori, keterangan=keterangan, nominal=nominal))

    #Validasi dan Raise            
    def test_nominal_valid(self):
        self.assertEqual(validasi_nominal("15000"), 15000)
        
    def test_nominal_negatif_memicu_raise(self):
        with self.assertRaises(DataTidakValid):
            validasi_nominal("-500")
            
    def test_kategori_kosong(self):
        with self.assertRaises(DataTidakValid):
            validasi_kategori("   ")
            

    #Perhitungan dan analisis
    def test_jumlahkan_args(self):
        self.assertEqual(jumlahkan(1000, 2000, 3000), 6000)
        self.assertEqual(jumlahkan(), 0)

    def test_total_dan_rata_rata_harian(self):
        self.assertEqual(self.pencatat.total(), 109000)
        self.assertAlmostEqual(self.pencatat.rata_rata_harian(), 54500)

    def test_total_per_kategori(self):
        hasil = self.pencatat.total_per_kategori()
        self.assertEqual(hasil["Makan"], 33000)
        self.assertEqual(hasil["Hiburan"], 54000)

    def test_urutkan_terboros(self):
        teratas = self.pencatat.urutkan_terboros(jumlah=2)
        self.assertEqual([p.keterangan for p in teratas], ["Langganan musik", "Ojek"])

    def test_filter_kategori(self):
        self.assertEqual(len(self.pencatat.filter_kategori("makan")), 2)

    def test_data_kosong(self):
        kosong = PencatatKeuangan()
        self.assertEqual(kosong.total(), 0)
        self.assertEqual(kosong.rata_rata_harian(), 0)
        self.assertIsNone(kosong.kategori_terboros())
        
    #Assert dan Kwargs
    def test_tambah_bukan_pengeluaran_ditolak_assert(self):
        with self.assertRaises(AssertionError):
            self.pencatat.tambah("bukan objek Pengeluaran")

    def test_kwargs_info_tambahan(self):
        p = Pengeluaran("2026-10-03", "makan", "Bakso", 20000, metode="QRIS")
        self.assertEqual(p.info_tambahan, {"metode": "QRIS"})
        self.assertTrue(p.ke_baris().endswith("metode=QRIS"))

    #File handling
    def test_baca_data_lewati_baris_rusak(self):
        isi = ("2026-10-01;Makan;Nasi goreng;15000\n"
            "2026-10-01;Makan;Kopi;abc\n"
            "2026-10-02;Belanja;Sabun;-12000\n"
            "2026-10-02;;Parkir;3000\n"
            "\n"
            "2026-10-03;Transport;Bensin;50000\n")
        with tempfile.TemporaryDirectory() as folder:
            jalur = os.path.join(folder, "data.txt")
            with open(jalur, "w", encoding="utf-8") as file:
                file.write(isi)
            hasil, keluaran = senyap(fileio.baca_data, jalur)
        self.assertEqual(len(hasil), 2)
        self.assertEqual(keluaran.count("dilewati"), 3)

    def test_file_tidak_ada(self):
        hasil, keluaran = senyap(fileio.baca_data, "file_yang_tidak_ada.txt")
        self.assertEqual(hasil, [])
        self.assertIn("belum ada", keluaran)

    def test_buat_file_mode_x_tidak_menimpa(self):
        with tempfile.TemporaryDirectory() as folder:
            jalur = os.path.join(folder, "data.txt")
            pertama, _ = senyap(fileio.buat_file_data, jalur, ["2026-10-01;Makan;Nasi;15000"])
            kedua, _ = senyap(fileio.buat_file_data, jalur, ["isi lain"])
            with open(jalur, "r", encoding="utf-8") as file:
                isi = file.read()
        self.assertTrue(pertama)
        self.assertFalse(kedua)
        self.assertIn("Nasi", isi)

    def test_tambah_data_mode_a_lalu_baca_lagi(self):
        with tempfile.TemporaryDirectory() as folder:
            jalur = os.path.join(folder, "data.txt")
            senyap(fileio.buat_file_data, jalur, ["2026-10-01;Makan;Nasi;15000"])
            fileio.tambah_data(Pengeluaran("2026-10-02", "makan", "Bakso", 20000, metode="Tunai"), nama_file=jalur)
            hasil, _ = senyap(fileio.baca_data, jalur)
        self.assertEqual(len(hasil), 2)
        self.assertEqual(hasil[1].info_tambahan, {"metode": "Tunai"})

    def test_tulis_laporan_mode_w_menimpa(self):
        with tempfile.TemporaryDirectory() as folder:
            jalur = os.path.join(folder, "laporan.txt")
            fileio.tulis_laporan("laporan lama", nama_file=jalur)
            fileio.tulis_laporan(self.pencatat.buat_laporan(), nama_file=jalur)
            with open(jalur, "r", encoding="utf-8") as file:
                isi = file.read()
        self.assertNotIn("laporan lama", isi)
        self.assertIn("Rp109.000", isi)
        
if __name__ == "__main__":
    unittest.main(verbosity=2)