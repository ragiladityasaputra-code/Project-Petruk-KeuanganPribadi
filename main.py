from keuangan import fileio
from keuangan.processing import Pengeluaran, PencatatKeuangan
from keuangan.validasi import DataTidakValid

DATA_AWAL = [
    "2026-10-01;Makan;Nasi goreng;15000",
    "2026-10-01;Transport;Ojek online;22000;metode=QRIS",
    "2026-10-02;Makan;Ayam geprek;18000",
    "2026-10-02;Hiburan;Langganan musik;54000;catatan=bulanan",
    "2026-10-04;Transport;Bensin;50000",
    "2026-10-05;Makan;Bakso;20000",
    "2026-10-05;Pendidikan;Fotokopi materi;7500",
    "2026-10-03;Makan;Kopi susu;abc",
    "2026-10-03;Belanja;Sabun;-12000",
    "2026-10-04;;Parkir;3000",
]

def muat_pencatat(nama_file):
    pencatat = PencatatKeuangan()
    for pengeluaran in fileio.baca_data(nama_file):
        pencatat.tambah(pengeluaran)
    return pencatat

def input_pengeluaran():
    while True:
        try:
            tanggal = input("Tanggal (YYYY-MM-DD): ")
            kategori = input("Kategori: ")
            keterangan = input("Keterangan: ")
            nominal = input("Nominal (angka): ")
            metode = input("Metode bayar (boleh dikosongkan): ").strip()
            info = {"metode": metode} if metode else {}
            return Pengeluaran(tanggal=tanggal, kategori=kategori, keterangan=keterangan, nominal=nominal, **info)
        except (ValueError, DataTidakValid) as error:
            print("Input tidak valid:", error)
            print("Silakan isi ulang.")
            
def tampilkan_menu():
    print("\n=== MENU KEUANGAN PRIBADI ===")
    print("1. Lihat semua pengeluaran")
    print("2. Tambah pengeluaran baru")
    print("3. Lihat ringkasan dan analisis")
    print("4. Simpan laporan ke file")
    print("5. Uji pesan file tidak ditemukan")
    print("0. Keluar")
    
def main():
    nama_file = fileio.NAMA_FILE_DATA
    fileio.buat_file_data(nama_file, DATA_AWAL)
    pencatat = muat_pencatat(nama_file)
    
    while True:
        tampilkan_menu()
        pilihan = input("Pilih menu (0-5): ").strip()
        if pilihan == "1":
            for pengeluaran in pencatat.daftar:
                print(pengeluaran)
        elif pilihan == "2":
            baru = input_pengeluaran()
            pencatat.tambah(baru)
            fileio.tambah_data(baru, nama_file=nama_file)
            print("Tersimpan:", baru)
        elif pilihan == "3":
            print(pencatat.buat_laporan())
        elif pilihan == "4":
            fileio.tulis_laporan(pencatat.buatlaporan())
            print("Laporan disimpan ke", fileio.NAMA_FILE_LAPORAN)
        elif pilihan == "5":
            fileio.baca_data("file_tidak_ada.txt")
        elif pilihan == "0":
            print("Sampai jumpa.")
            break
        else:
            print("Menu tidak valid, pilih angka 0 sampai 5.")
            
            
if __name__ == "__main__":
    main()