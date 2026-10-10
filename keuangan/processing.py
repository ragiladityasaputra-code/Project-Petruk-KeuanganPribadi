#Modul processing: class, perhitungan, dan analisis data pengeluaran.
from . import validasi


def format_rupiah(angka): #Ubah angka jadi teks rupiah
    return "Rp" + f"{angka:,.0f}".replace(",", ".")

def jumlahkan(*nominal): #Menjumlahkan nominal sebanyak apapun lewat *args
    return sum(nominal)


class Pengeluaran: #Satu catatan pengeluaran.
    def __init__(self, tanggal, kategori, keterangan, nominal, **info_tambahan):
        #Semua field divalidasi lewat modul validasi, data tidak valid memicu exception.
        self.tanggal = validasi.validasi_tanggal(tanggal)
        self.kategori = validasi.validasi_kategori(kategori)
        self.keterangan = validasi.validasi_keterangan(keterangan)
        self.nominal = validasi.validasi_nominal(nominal)
        #**kwargs menampung atribut yang bervariasi, misal metode = QRIS
        self.info_tambahan = info_tambahan

    def ke_baris(self):
        #Ubah objek jadi satu baris teks siap simpan ke file.
        bagian = [self.tanggal, self.kategori, self.keterangan, str(self.nominal)]
        bagian += [f"{kunci}={nilai}" for kunci, nilai in self.info_tambahan.items()]
        return ";".join(bagian)

    def __str__(self):
        #Tampilan satu baris yang rapi di layar.
        teks = (f"{self.tanggal} | {self.kategori:<10} | "
                f"{self.keterangan:<22} | {format_rupiah(self.nominal):>10}")
        if self.info_tambahan:
            teks += " | " + ", ".join(f"{k}={v}" for k, v in self.info_tambahan.items())
        return teks


class PencatatKeuangan: #Kumpulan pengeluaran beserta fungsi analisisnya.
    def __init__(self):
        self.daftar = []

    def tambah(self, pengeluaran): #Menambah satu pengeluaran. Assert menjaga agar isi daftar selalu objek Pengeluaran.
        assert isinstance(pengeluaran, Pengeluaran), "Yang ditambahkan harus objek Pengeluaran"
        self.daftar.append(pengeluaran)

    def total(self): #Total seluruh pengeluaran
        return jumlahkan(*[p.nominal for p in self.daftar])

    def total_per_kategori(self): #Dictionary kategori ke total nominalnya.
        hasil = {}
        for p in self.daftar:
            hasil[p.kategori] = hasil.get(p.kategori, 0) + p.nominal
        return hasil

    def filter_kategori(self, kategori): #Ambil pengeluaran milik satu kategori
        return list(filter(lambda p: p.kategori == kategori.title(), self.daftar))

    def urutkan_terboros(self, jumlah=3): #Pengeluaran terebesar. Lambda dipakai sebagai key pada sorted()
        return sorted(self.daftar, key=lambda p: p.nominal, reverse=True)[:jumlah]

    def rata_rata_harian(self): #Total dibagi jumlah hari yang punya catatan. Kosong = 0
        hari = {p.tanggal for p in self.daftar}
        if not hari:
            return 0
        return self.total() / len(hari)

    def kategori_terboros(self): #Pasangan (kategori, total) yang paling besar, atau None kalo data kosong.
        per_kategori = self.total_per_kategori()
        if not per_kategori:
            return None
        return max(per_kategori.items(), key=lambda item: item[1])

    def buat_laporan(self): #Susun teks laporan lengkap: daftar, ringkasan, dan 3 pengeluaran terbesar.
        baris = ["LAPORAN KEUANGAN PRIBADI", "=" * 60]
        if not self.daftar:
            baris.append("Belum ada data pengeluaran.")
            return "\n".join(baris)

        baris += [str(p) for p in self.daftar]
        baris.append("-" * 60)
        baris.append(f"Jumlah transaksi   : {len(self.daftar)}")
        baris.append(f"Total pengeluaran  : {format_rupiah(self.total())}")
        baris.append(f"Rata-rata per hari : {format_rupiah(self.rata_rata_harian())}")
        nama, nilai = self.kategori_terboros()
        baris.append(f"Kategori terboros  : {nama} ({format_rupiah(nilai)})")
        baris.append("Total per kategori :")
        for kategori, jumlah in sorted(self.total_per_kategori().items()):
            baris.append(f"  {kategori:<12}{format_rupiah(jumlah):>12}")
        baris.append("3 pengeluaran terbesar:")
        for urutan, p in enumerate(self.urutkan_terboros(jumlah=3), start=1):
            baris.append(f"  {urutan}. {p.keterangan} ({format_rupiah(p.nominal)})")
        return "\n".join(baris)


if __name__ == "__main__":
    # Pengujian lokal: python -m keuangan.processing
    contoh = PencatatKeuangan()
    contoh.tambah(Pengeluaran("2026-10-01", "makan", "Nasi goreng", 15000))
    contoh.tambah(Pengeluaran("2026-10-01", "transport", "Ojek", 22000, metode="QRIS"))
    print(contoh.buat_laporan())