"""Entry point Streamlit: konfigurasi halaman, state, sidebar, dan router.

Tidak ada logika CBR di file ini. Percabangan hanya untuk navigasi halaman.
"""

import streamlit as st

from core import storage
from ui import halaman_hasil, halaman_input, sidebar
from ui.komponen import LOGO_PATH, sinkronkan_tema, terapkan_gaya

st.set_page_config(
    page_title="Sistem Pakar Troubleshooting WiFi (CBR)",
    page_icon=str(LOGO_PATH),
    layout="wide",
)

terapkan_gaya()
sinkronkan_tema()
st.logo(str(LOGO_PATH), size="large")

# Inisialisasi state cukup sekali; nilai widget tidak disimpan di sini.
if "case_base" not in st.session_state:
    st.session_state["case_base"] = storage.muat_case_base()
if "halaman" not in st.session_state:
    st.session_state["halaman"] = "input"
if "gejala_input" not in st.session_state:
    st.session_state["gejala_input"] = []
if "hasil_retrieve" not in st.session_state:
    st.session_state["hasil_retrieve"] = None
if "indeks_kandidat" not in st.session_state:
    st.session_state["indeks_kandidat"] = 0
if "status_feedback" not in st.session_state:
    st.session_state["status_feedback"] = "belum"
if "mode_similarity" not in st.session_state:
    st.session_state["mode_similarity"] = "jaccard"
if "info_retain" not in st.session_state:
    st.session_state["info_retain"] = None
if "reset_form" not in st.session_state:
    st.session_state["reset_form"] = False

# Pembersihan form dilakukan SEBELUM widget digambar, karena menghapus state
# widget yang sudah digambar tidak diizinkan oleh Streamlit.
if st.session_state["reset_form"]:
    st.session_state["reset_form"] = False
    awalan = ("gejala_", "pilihan_", "konfirmasi_reset")
    for kunci in [k for k in st.session_state.keys() if k.startswith(awalan)]:
        del st.session_state[kunci]

sidebar.render()

if st.session_state["halaman"] == "hasil":
    halaman_hasil.render()
else:
    halaman_input.render()
