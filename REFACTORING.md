# Tabel Refactoring

| No | Bagian yang belum diperbaiki | Bagian yang diperbaiki | Teknik | Alasan |
|----|------------------------------|------------------------|--------|--------|
| 1 | Variabel pendek di loop baca file: `t, k, ket, n = baris.split(";")` | `tanggal, kategori, keterangan, nominal = ...` | Rename variable | Nama yang menjelaskan isinya membuat kode terbaca tanpa perlu menebak arti `t`, `k`, atau `n`. |
| 2 | Pengecekan nominal, kategori, dan tanggal ditulis langsung di dalam loop `baca_data` (sekitar 15 baris `if/else` bertumpuk) | Dipindah ke fungsi `validasi_baris()` di `validasi.py`, sedangkan `baca_data` cukup memanggilnya | Extract function | Loop pembaca file jadi pendek dan fokus satu tugas. Aturan validasi juga bisa dipakai ulang oleh input manual dan dites terpisah. |
| 3 | Total per kategori dihitung dengan loop terpisah untuk tiap kategori (`total_makan`, `total_transport`, `total_hiburan`) | Satu fungsi `total_per_kategori()` yang menghasilkan dictionary untuk kategori apa pun | Remove duplicate code | Tiga loop hampir identik diganti satu. Kategori baru otomatis ikut terhitung tanpa menulis kode baru. |
| 4 | Nama file `"data_pengeluaran.txt"` diketik berulang di banyak fungsi | Konstanta `NAMA_FILE_DATA` dan `NAMA_FILE_LAPORAN` di `fileio.py`, dipakai sebagai nilai default parameter | Replace magic string dengan konstanta | Ganti nama file cukup di satu tempat, dan risiko salah ketik di salah satu fungsi hilang. |
