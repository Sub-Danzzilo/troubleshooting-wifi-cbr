"""Halaman 1: input gejala dari pengguna.

Semua widget disimpan di st.session_state lewat key-nya masing-masing agar
pilihan tidak hilang saat Streamlit rerun.
"""

import streamlit as st

from core.case_base import DAFTAR_GEJALA, PILIHAN_LAMPU


def _gejala_kelompok(kelompok):
    return [gejala for gejala in DAFTAR_GEJALA if gejala["kelompok"] == kelompok]


def konversi_pilihan_ke_gejala(pilihan_lampu, gejala_terpilih):
    """Ubah pilihan radio lampu + checkbox menjadi daftar nama gejala boolean.

    Parameter:
        pilihan_lampu  : dict {nama_lampu: nama_gejala atau None}
        gejala_terpilih: list nama gejala dari checkbox Kelompok A dan C
    Opsi "Tidak tahu" dipetakan ke None sehingga tidak menambah gejala.
    """
    gejala = list(gejala_terpilih)
    for nama_gejala in (pilihan_lampu or {}).values():
        if nama_gejala:
            gejala.append(nama_gejala)
    return sorted(set(gejala))


def validasi_input(gejala):
    """Peringatan form (bukan inferensi): input kosong atau kontradiktif."""
    peringatan = []
    if not gejala:
        peringatan.append("Pilih minimal satu gejala sebelum menekan Diagnosis.")
    if "hanya_1_perangkat" in gejala and "semua_perangkat" in gejala:
        peringatan.append(
            "Input kontradiktif: gangguan hanya di satu perangkat sekaligus di semua "
            "perangkat. Periksa kembali pilihan Anda."
        )
    return peringatan


def render():
    st.title("📶 Sistem Pakar Troubleshooting WiFi (CBR)")
    st.write(
        "Sistem ini mencocokkan keluhan WiFi Anda dengan kasus-kasus lama yang paling "
        "mirip (Case-Based Reasoning). Pilih gejala yang dialami, lalu tekan **Diagnosis**."
    )

    st.header("1. Keluhan Utama")
    for gejala in _gejala_kelompok("A"):
        st.checkbox(gejala["label"], key=f"gejala_{gejala['nama']}")

    st.header("2. Status Indikator Lampu Router")
    tanpa_indikator = st.session_state.get("gejala_router_tidak_punya_indikator", False)
    if tanpa_indikator:
        st.info(
            "Router ditandai tidak memiliki lampu indikator, jadi bagian status lampu "
            "dilewati. Hapus centang pada bagian Informasi Tambahan bila ingin mengisi."
        )
    for nama_lampu, pilihan in PILIHAN_LAMPU.items():
        st.radio(
            nama_lampu,
            [label for label, _ in pilihan],
            index=0,
            horizontal=True,
            key=f"pilihan_{nama_lampu}",
            disabled=tanpa_indikator,
        )

    st.header("3. Informasi Tambahan")
    for gejala in _gejala_kelompok("C"):
        st.checkbox(gejala["label"], key=f"gejala_{gejala['nama']}")
    st.caption(
        "Bila 'Router tidak memiliki lampu indikator' dicentang, seluruh pilihan pada "
        "bagian status lampu otomatis dinonaktifkan."
    )

    st.divider()
    tombol_diagnosis = st.button("🔍 Diagnosis", type="primary")
    if not tombol_diagnosis:
        return

    tanpa_indikator = st.session_state.get("gejala_router_tidak_punya_indikator", False)
    gejala_terpilih = [
        gejala["nama"]
        for gejala in DAFTAR_GEJALA
        if gejala["kelompok"] in ("A", "C")
        and st.session_state.get(f"gejala_{gejala['nama']}")
    ]

    pilihan_lampu = {}
    if not tanpa_indikator:
        for nama_lampu, pilihan in PILIHAN_LAMPU.items():
            label_terpilih = st.session_state.get(f"pilihan_{nama_lampu}", "Tidak tahu")
            pasangan = {label: nama_gejala for label, nama_gejala in pilihan}
            pilihan_lampu[nama_lampu] = pasangan.get(label_terpilih)

    gejala = konversi_pilihan_ke_gejala(pilihan_lampu, gejala_terpilih)
    peringatan = validasi_input(gejala)
    if not gejala:
        for pesan in peringatan:
            st.error(pesan)
        return

    for pesan in peringatan:
        st.warning(pesan)

    st.session_state["gejala_input"] = gejala
    st.session_state["indeks_kandidat"] = 0
    st.session_state["info_retain"] = None
    st.session_state["status_feedback"] = "belum"
    st.session_state["halaman"] = "hasil"
    st.rerun()
