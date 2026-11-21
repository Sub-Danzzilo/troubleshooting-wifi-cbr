# =============================================================================
# evaluasi/jalankan_evaluasi.py  —  SKRIP EVALUASI
# =============================================================================
# Dijalankan dari terminal: python -m evaluasi.jalankan_evaluasi
#
# ISI FILE INI NANTINYA:
#
# 1. Uji leave-one-out pada CASE_BASE_AWAL:
#    - Tiap kasus diambil sebagai "kasus uji", lalu di-retrieve terhadap 14 lainnya.
#    - Hitung akurasi top-1 dan top-3 berdasarkan kategori_solusi.
#
# 2. Uji 5 skenario baru dari skenario_uji.py:
#    - Hitung akurasi top-1 dan top-3 terhadap kategori_diharapkan.
#
# 3. Bandingkan dua mode: Jaccard biasa vs Weighted Jaccard.
#
# 4. Keluaran:
#    - Cetak tabel ringkas ke terminal.
#    - Tulis hasil lengkap (tabel + daftar kasus yang salah) ke docs/hasil_evaluasi.md.
#
# CATATAN: pakai CASE_BASE_AWAL langsung (jangan case_base.json), supaya hasil
# evaluasi tidak berubah karena kasus hasil retain.
#
# TAMBAHAN (VALIDASI MANUAL):
#    - Untuk 5 skenario uji, cetak juga rincian perhitungan (hitung_rinci) kasus top-1
#      dan top-3 ke terminal dan docs/hasil_evaluasi.md, supaya mudah dicocokkan
#      dengan hitungan tangan di docs/validasi_manual.md.