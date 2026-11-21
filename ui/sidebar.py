# =============================================================================
# ui/sidebar.py  —  SIDEBAR
# =============================================================================
# ISI FILE INI NANTINYA:
#
# render() yang menggambar:
#   - Info metode singkat (CBR, Jaccard).
#   - Toggle "Jaccard biasa / Weighted Jaccard" -> simpan ke st.session_state["mode_similarity"].
#   - Jumlah kasus di case base saat ini (len dari session_state["case_base"]).
#   - Expander "Lihat Semua Kasus" (tabel: id, nama, kategori, status, jumlah_dipakai, sumber).
#   - Tombol "Reset Case Base" (panggil core.storage.reset_case_base, perbarui
#     session_state, kembali ke halaman input). Tambahkan konfirmasi agar tidak
#     terpencet tanpa sengaja saat demo.
