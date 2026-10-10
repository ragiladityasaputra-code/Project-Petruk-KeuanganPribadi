#Modul validasi: pengecekan input dan data pengeluaran.
from datetime import datetime

#Exception bautan sendiri untuk data yang melanggar aturan program.
class DataTidakValid(Exception):
    pass

def validasi_nominal(nominal): #Ubah nominal ke int. non-angka = ValueError, - = DataTidakValid.
        try:
            angka = int(nominal)
        except (ValueError, TypeError):
            raise ValueError(f"Nominal bukan angka: {nominal!r}") from None
        if angka < 0:
            raise DataTidakValid(f"Nominal tidak boleh negatif: {angka}")
        return angka

def validasi_kategori(kategori): #Pastikan kategori tidak kosong, lalu rapikan huruf.
    bersih = str(kategori).strip()
    if not bersih:
        raise DataTidakValid("Kategori tidak boleh kosong")
    return bersih.title()

def validasi_keterangan(keterangan): #Pastikan keterangan tidak kosong.
    bersih = str(keterangan).strip()
    if not bersih:
        raise DataTidakValid("Keterangan tidak boleh kosong")
    return bersih

def validasi_tanggal(tanggal): #Pastikan tanggal tidak kosong, dan berformat.
    bersih = str(tanggal).strip()
    try:
        datetime.strptime(bersih, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"Format tanggal salah (harus YYYY-MM-DD): {bersih!r}") from None
    return bersih

def validasi_baris(baris): #Pecah satu baris file
    bagian = [b.strip() for b in baris.split(";")]
    if len(bagian) < 4:
        raise DataTidakValid(f"Kolom kurang, butuh minimal 4 kolom: {baris!r}")
    
    tambahan = {}
    for item in bagian[4:]:
        if "=" not in item:
            raise DataTidakValid(f"Info tambahan harus berbentuk kunci=nilai: {item!r}")
        kunci, nilai = item.split("=", 1)
        tambahan[kunci.strip()] = nilai.strip()
        
    tanggal = validasi_tanggal(bagian[0])
    kategori = validasi_kategori(bagian[1])
    keterangan = validasi_keterangan(bagian[2])
    nominal = validasi_nominal(bagian[3])
    return tanggal, kategori, keterangan, nominal, tambahan

if __name__ == "__main__": #Pengujian lokal: hanya jalan kalau dieksekusi langsung (python -m keuangan.validasi)
    print("Nominal valid :", validasi_nominal("15000"))
    for contoh in ("-500", "abc"):
        try:
            validasi_nominal(contoh)
        except (ValueError, DataTidakValid) as error:
            print("Ditolak   :", error)