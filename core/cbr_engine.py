# =============================================================================
# core/cbr_engine.py  —  SIKLUS 4R (Retrieve, Reuse, Revise, Retain)
# =============================================================================
# Satu fungsi per tahap. Tidak import Streamlit. Tidak ada rule-based.
#
# ISI FILE INI NANTINYA:
#
# 1. retrieve(gejala_input, case_base, mode_similarity, top_k) -> list
#    - Hitung similarity gejala_input terhadap SETIAP kasus (pakai core.similarity).
#    - Lewati kasus berstatus "belum_terselesaikan".
#    - Urutkan menurun, kembalikan top_k kasus beserta skor.
#    - Jika skor tertinggi < AMBANG_MIN_SIMILARITY, tandai hasil sebagai
#      "tidak ada kasus cukup mirip" (jangan paksa diagnosis).
#
# 2. reuse(kasus_terpilih, gejala_input) -> dict
#    - Salin solusi kasus terpilih APA ADANYA (tanpa adaptasi if-then).
#    - Sertakan selisih gejala (dari similarity.bandingkan_gejala) sebagai
#      catatan "hal yang perlu diverifikasi".
#
# 3. revise(hasil_retrieve, indeks_sekarang, berhasil, solusi_baru=None) -> dict
#    - Menangkap umpan balik pengguna.
#    - Jika berhasil: kembalikan keputusan "lanjut ke retain".
#    - Jika gagal: kembalikan kandidat peringkat berikutnya (jika masih ada).
#    - Jika semua kandidat habis: terima solusi_baru (opsional) dari pengguna.
#
# 4. retain(gejala_input, kasus_acuan, solusi, status, case_base) -> case_base baru
#    - Hitung similarity kasus baru terhadap case base.
#    - Jika >= AMBANG_DUPLIKAT: JANGAN tambah kasus, cukup naikkan jumlah_dipakai
#      pada kasus lama.
#    - Jika tidak: tambah kasus baru (id otomatis K16, K17, ...; sumber = "retain";
#      kategori_solusi mengikuti kasus acuan atau "baru" bila solusi dari pengguna).
#    - Status: "berhasil" atau "belum_terselesaikan".
#    - Kembalikan juga keterangan apa yang terjadi (ditambah / hanya naikkan counter)
#      agar UI bisa menampilkan pesan yang jelas.
#
# 5. buat_id_kasus_baru(case_base) -> str   (fungsi bantu untuk retain)
#
# Docstring tiap fungsi: sebutkan nama tahap CBR-nya secara eksplisit.
# LARANGAN: tidak ada pemetaan "gejala X -> kesimpulan Y" di file ini.
