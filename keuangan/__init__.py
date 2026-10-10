# Package keuangan: pencatat pengeluaran pribadi.

# Pembagian tugas modul:
# - fileio     : baca, tulis, dan tambah data ke file
# - processing : class dan fungsi perhitungan serta analisis
# - validasi   : pengecekan input dan data
# - testing    : pengujian program (unittest)

# Modul diimpor langsung oleh pemakainya, contoh: from keuangan import fileio.
from . import fileio, processing, validasi

__all__ = ["fileio", "processing", "validasi"]