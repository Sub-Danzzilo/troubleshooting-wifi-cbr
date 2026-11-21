# =============================================================================
# app.py  —  ENTRY POINT STREAMLIT
# Dijalankan dengan: streamlit run app.py
# =============================================================================
# ISI FILE INI NANTINYA:
#
# 1. Konfigurasi halaman (st.set_page_config): judul "Sistem Pakar Troubleshooting
#    WiFi (CBR)", layout "wide", ikon yang relevan.
#
# 2. Inisialisasi st.session_state HANYA jika kunci belum ada. Kunci yang dipakai:
#      - case_base          : list kasus (dimuat dari core.storage)
#      - halaman            : "input" atau "hasil"
#      - gejala_input       : list nama gejala dari form pengguna
#      - hasil_retrieve     : list top-k kasus beserta skor similarity
#      - indeks_kandidat    : indeks kandidat solusi yang sedang ditampilkan (0 = terbaik)
#      - status_feedback    : "belum" / "berhasil" / "gagal"
#      - mode_similarity    : "jaccard" atau "weighted"
#
# 3. Muat case base lewat core.storage (JANGAN baca file JSON langsung di sini).
#
# 4. Panggil ui.sidebar.render() untuk menggambar sidebar.
#
# 5. Router halaman sederhana: baca st.session_state["halaman"], lalu panggil
#    ui.halaman_input.render() ATAU ui.halaman_hasil.render().
#
# LARANGAN:
#    - Jangan taruh perhitungan similarity / logika diagnosis di sini.
#    - Percabangan di file ini HANYA untuk navigasi halaman, bukan inferensi.
