# =============================================================================
# ui/halaman_input.py  —  HALAMAN 1: INPUT GEJALA
# =============================================================================
# ISI FILE INI NANTINYA:
#
# render() yang menggambar:
#   - Judul "Sistem Pakar Troubleshooting WiFi (CBR)" + deskripsi singkat metode.
#   - Section 1 "Keluhan Utama": st.checkbox untuk gejala Kelompok A.
#   - Section 2 "Status Indikator Lampu Router": st.radio horizontal untuk
#     POWER, PON, LOS, INTERNET, WLAN, LAN. Opsi default "Tidak tahu".
#   - Section 3 "Informasi Tambahan": checkbox Kelompok C.
#   - Tombol besar "Diagnosis".
#
# Fungsi bantu di file ini:
#   - konversi_pilihan_ke_gejala(...): ubah pilihan radio + checkbox menjadi
#     list nama gejala boolean (memakai PILIHAN_LAMPU dari core.case_base).
#   - validasi_input(...): hanya peringatan input kontradiktif
#     (hanya_1_perangkat + semua_perangkat bersamaan; belum memilih gejala sama sekali).
#     Ini validasi form, BUKAN inferensi.
#
# Perilaku:
#   - Jika router_tidak_punya_indikator dicentang: section lampu di-disable.
#   - Saat tombol Diagnosis ditekan dan input valid: panggil core.cbr_engine.retrieve,
#     simpan hasil ke st.session_state, set halaman = "hasil", lalu rerun.
