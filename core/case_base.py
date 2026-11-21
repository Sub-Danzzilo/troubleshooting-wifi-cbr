# =============================================================================
# core/case_base.py  —  DATA & PARAMETER (bukan logika)
# =============================================================================
# File ini HANYA berisi data dan konstanta. Tidak boleh ada fungsi inferensi.
#
# ISI FILE INI NANTINYA:
#
# 1. DAFTAR_GEJALA
#    - 25 gejala sesuai spesifikasi, dikelompokkan: Kelompok A (keluhan utama),
#      Kelompok B (lampu router), Kelompok C (informasi tambahan).
#    - Tiap entri: nama_gejala (snake_case), label tampilan Bahasa Indonesia, kelompok.
#
# 2. PILIHAN_LAMPU
#    - Pemetaan tiap lampu (POWER, PON, LOS, INTERNET, WLAN, LAN) ke daftar pilihan
#      radio: label UI -> nama gejala boolean.
#    - Setiap lampu WAJIB punya opsi "Tidak tahu" yang dipetakan ke "tidak ada gejala".
#    - Dipakai UI untuk mengonversi pilihan radio menjadi gejala boolean.
#
# 3. BOBOT_GEJALA
#    - dict {nama_gejala: bobot}. Default 1.0.
#    - Usulan awal: gejala menyimpang dari kondisi normal = 2.0,
#      gejala kondisi normal = 0.5, sisanya 1.0.
#    - Beri komentar alasan tiap kelompok bobot (untuk dijelaskan di sidang).
#
# 4. PARAMETER SISTEM
#    - AMBANG_MIN_SIMILARITY (default 0.30): di bawah ini = "tidak ada kasus mirip".
#    - AMBANG_DUPLIKAT (default 1.0): di atas/sama dengan ini = kasus dianggap duplikat.
#    - TOP_K (default 3): jumlah kasus teratas yang ditampilkan.
#    - PATH_CASE_BASE_JSON: lokasi file persistensi (data/case_base.json).
#
# 5. CASE_BASE_AWAL  (15 kasus)
#    - Struktur tiap kasus (semua field wajib):
#        id, nama_kasus, gejala (list nama_gejala), solusi (list langkah konkret),
#        kategori_solusi, status ("berhasil"), jumlah_dipakai (1), sumber ("awal")
#    - Sebaran kategori (minimal 2 kasus per kategori agar leave-one-out bermakna):
#        kabel_optik_bermasalah (3), router_mati_daya (2), gangguan_isp (2),
#        wlan_nonaktif (2), password_salah (2), sinyal_lemah_interferensi (2),
#        masalah_perangkat_klien (2)
#    - Kasus harus realistis: kombinasi gejala masuk akal secara fisik
#      (contoh: power_mati tidak mungkin bersamaan dengan wlan_nyala).
#    - Solusi berisi langkah nyata, bukan placeholder atau sekadar "hubungi teknisi".
#    - Minimal satu kasus memakai router_tidak_punya_indikator.
#
# LARANGAN:
#    - Tidak ada struktur "rules", tidak ada if/else yang memetakan gejala ke kesimpulan.
#
# CATATAN VALIDASI MANUAL:
#    - Dosen akan menguji dengan menghitung similarity di papan tulis, jadi:
#        * Tiap kasus cukup 4-9 gejala (mudah ditulis dan dihitung manual).
#        * Bobot hanya memakai nilai sederhana (0.5, 1.0, 2.0), tanpa pecahan rumit.
#    - Siapkan tabel ringkas 15 kasus (ID + daftar gejala) di laporan/slide
#      sebagai contekan saat menghitung di papan tulis.