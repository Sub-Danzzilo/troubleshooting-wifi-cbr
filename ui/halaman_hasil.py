# =============================================================================
# ui/halaman_hasil.py  —  HALAMAN 2: HASIL DIAGNOSIS
# =============================================================================
# ISI FILE INI NANTINYA:
#
# render() yang menggambar:
#   - Tabel top-3 kasus: ID, nama kasus, similarity %, kategori, ringkasan.
#   - Rekomendasi utama: langkah solusi dari kandidat saat ini (hasil reuse).
#   - Confidence bar (st.progress) sesuai similarity. Jika di bawah ambang,
#     tampilkan peringatan "tidak ada kasus yang cukup mirip".
#   - Penjelasan transparan: gejala cocok, gejala hanya di input, gejala hanya di kasus.
#   - Form feedback (Revise): radio Ya/Tidak.
#       * Ya    -> tombol "Simpan ke Basis Kasus" (panggil retain).
#       * Tidak -> tampilkan solusi kandidat berikutnya; bila habis, tampilkan
#                  kolom teks opsional "Solusi yang akhirnya berhasil".
#   - Setelah retain: pesan jelas apakah kasus DITAMBAH (jumlah kasus naik)
#     atau hanya menaikkan jumlah_dipakai (duplikat).
#   - Tombol "Diagnosis Baru" untuk kembali ke halaman input dan membersihkan state.
#
# PENTING: simpan status feedback di st.session_state agar tombol "Simpan"
# tidak hilang saat Streamlit rerun.
#
# TAMBAHAN (VALIDASI MANUAL):
#   - Untuk setiap kasus di top-3, sediakan st.expander "Lihat perhitungan rinci".
#   - Isinya dari similarity.hitung_rinci: himpunan A dan B, irisan, gabungan,
#     jumlah anggota, rumus dengan angka terisi (contoh: "3 / 4 = 0,75"),
#     dan untuk Weighted Jaccard tabel bobot per gejala.
#   - Tujuannya: saat sidang, penguji bisa mencocokkan hitungan papan tulis
#     dengan angka yang ditampilkan aplikasi.