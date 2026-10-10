#Modul fileio: membaca, menulis, dan menambah data ke file.
from .processing import Pengeluaran
from .validasi import validasi_baris, DataTidakValid

NAMA_FILE_DATA = "data_pengeluaran.txt"
NAMA_FILE_LAPORAN = "laporan_keuangan.txt"

#Mode 'x': membuat file data pertama kali. Kalau sudah ada, isi lama aman dari ketimpa.
def buat_file_data(nama_file=NAMA_FILE_DATA, baris_awal=()):
    try:
        with open(nama_file, "x", encoding="utf-8") as file:
            for baris in baris_awal:
                file.write(baris + "\n")
        print(f"File {nama_file} berhasil dibuat.")
        return True
    except FileExistsError:
        print(f"File {nama_file} sudah ada, tidak dibuat ulang.")
        return False

#Mode 'a': menempelkan satu pengeluaran baru di akhir file tanpa menghapus data lama.
def tambah_data(pengeluaran, nama_file=NAMA_FILE_DATA):
    with open(nama_file, "a", encoding="utf-8") as file:
        file.write(pengeluaran.ke_baris() + "\n")

#Mode 'r': membaca file baris demi baris. Baris rusak dilewati, program tetap jalan.
def baca_data(nama_file=NAMA_FILE_DATA):
    daftar = []
    try:
        with open(nama_file, "r", encoding="utf-8") as file:
            nomor = 0
            for baris in file:  # pembacaan iteratif
                nomor += 1
                if not baris.strip():
                    continue  # baris kosong diabaikan begitu saja
                try:
                    tanggal, kategori, keterangan, nominal, tambahan = validasi_baris(baris)
                    daftar.append(Pengeluaran(tanggal, kategori, keterangan, nominal, **tambahan))
                except (ValueError, DataTidakValid) as error:
                    print(f"Baris {nomor} dilewati: {error}")
    except FileNotFoundError:
        print(f"Error: file {nama_file} belum ada. Buat dulu lewat buat_file_data().")
    return daftar

#Mode 'w': menulis laporan. Isi laporan lama sengaja diganti dengan yang terbaru.
def tulis_laporan(teks, nama_file=NAMA_FILE_LAPORAN):
    with open(nama_file, "w", encoding="utf-8") as file:
        file.write(teks + "\n")