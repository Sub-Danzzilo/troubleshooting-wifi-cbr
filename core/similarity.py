# =============================================================================
# core/similarity.py  —  PERHITUNGAN KEMIRIPAN
# =============================================================================
# Fungsi murni (pure function): tidak import Streamlit, tidak baca/tulis file.
#
# ISI FILE INI NANTINYA:
#
# 1. jaccard_similarity(himpunan_a, himpunan_b) -> float
#    - Rumus: |A ∩ B| / |A ∪ B|
#    - Input berupa set nama gejala. Output 0.0 sampai 1.0.
#    - KASUS TEPI: jika gabungan kosong, kembalikan 0.0 (hindari bagi nol).
#
# 2. weighted_jaccard_similarity(himpunan_a, himpunan_b, bobot) -> float
#    - Rumus: jumlah bobot gejala di irisan / jumlah bobot gejala di gabungan.
#    - Gejala yang tidak ada di dict bobot dianggap bobot 1.0.
#    - KASUS TEPI sama seperti di atas.
#
# 3. bandingkan_gejala(gejala_input, gejala_kasus) -> dict
#    - Untuk fitur transparansi/penjelasan (dipakai reuse dan UI).
#    - Mengembalikan 3 kelompok: gejala yang cocok (irisan),
#      gejala hanya ada di input, gejala hanya ada di kasus.
#
# Docstring tiap fungsi: jelaskan rumus dan arti parameter dalam Bahasa Indonesia.
# Tambahkan komentar singkat bahwa pasangan sama-sama False (0-0) diabaikan oleh
# Jaccard, dan itulah alasan "gejala tidak dipilih = tidak dilaporkan".
#
# 4. hitung_rinci(gejala_input, gejala_kasus, mode, bobot) -> dict   [UNTUK VALIDASI MANUAL]
#    - Mengembalikan SEMUA langkah perhitungan supaya bisa ditulis ulang di papan tulis:
#        * himpunan A (input) dan himpunan B (kasus), diurutkan alfabetis
#        * irisan A ∩ B dan gabungan A ∪ B beserta jumlah anggotanya
#        * mode Jaccard biasa: pembilang = |A ∩ B|, penyebut = |A ∪ B|, hasil = pembilang / penyebut
#        * mode Weighted: bobot tiap gejala di irisan dan gabungan, jumlah bobot pembilang,
#          jumlah bobot penyebut, hasil
#    - Hasil dari fungsi ini HARUS sama persis dengan skor yang dipakai retrieve
#      (retrieve sebaiknya memanggil fungsi similarity yang sama, bukan menghitung ulang
#      dengan cara lain).
#
# PRINSIP: perhitungan similarity harus tetap bisa dikerjakan dengan tangan. Jangan
# menambah normalisasi, pembulatan tersembunyi, atau rumus lain yang menyulitkan
# validasi manual. Pembulatan hanya saat TAMPILAN (misal 3 angka di belakang koma).