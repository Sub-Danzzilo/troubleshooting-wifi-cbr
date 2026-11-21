"""Halaman 1: input gejala dari pengguna.

Semua widget disimpan di st.session_state lewat key-nya masing-masing agar
pilihan tidak hilang saat Streamlit rerun.
"""

import streamlit as st

from core.case_base import DAFTAR_GEJALA, PILIHAN_LAMPU
from ui.komponen import tampilkan_header


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
        peringatan.append("Pilih minimal satu gejala sebelum menjalankan diagnosis.")
    if "hanya_1_perangkat" in gejala and "semua_perangkat" in gejala:
        peringatan.append(
            "Input kontradiktif: gangguan hanya di satu perangkat sekaligus di semua "
            "perangkat. Periksa kembali pilihan Anda."
        )
    return peringatan


def render():
    tampilkan_header(
        "Sistem Pakar Troubleshooting WiFi",
        "Case-Based Reasoning (CBR) dengan siklus Retrieve, Reuse, Revise, dan Retain.",
    )
    st.caption(
        "Langkah 1 dari 2 — pilih gejala yang dialami, lalu jalankan diagnosis. "
        "Gejala yang tidak diketahui cukup dibiarkan kosong."
    )

    with st.container(border=True):
        st.subheader("1. Keluhan Utama")
        st.caption("Centang semua keluhan yang sesuai dengan kondisi saat ini.")
        for gejala in _gejala_kelompok("A"):
            st.checkbox(gejala["label"], key=f"gejala_{gejala['nama']}")

    tanpa_indikator = st.session_state.get("gejala_router_tidak_punya_indikator", False)

    with st.container(border=True):
        st.subheader("2. Status Indikator Lampu Router")
        st.caption(
            "Pilih satu status untuk tiap lampu. Gunakan opsi Tidak tahu bila status "
            "lampu tidak dapat diamati."
        )
        if tanpa_indikator:
            st.info(
                "Router ditandai tidak memiliki lampu indikator, jadi bagian ini dilewati. "
                "Hapus centang pada bagian Informasi Tambahan bila ingin mengisi."
            )
        kolom_kiri, kolom_kanan = st.columns(2)
        for urutan, (nama_lampu, pilihan) in enumerate(PILIHAN_LAMPU.items()):
            wadah = kolom_kiri if urutan < 3 else kolom_kanan
            with wadah:
                st.radio(
                    nama_lampu,
                    [label for label, _ in pilihan],
                    index=0,
                    horizontal=True,
                    key=f"pilihan_{nama_lampu}",
                    disabled=tanpa_indikator,
                )

    with st.container(border=True):
        st.subheader("3. Informasi Tambahan")
        st.caption(
            "Centang bila sesuai. Bila router tidak memiliki lampu indikator, seluruh "
            "pilihan pada bagian status lampu otomatis dinonaktifkan."
        )
        for gejala in _gejala_kelompok("C"):
            st.checkbox(gejala["label"], key=f"gejala_{gejala['nama']}")

    st.write("")
    tombol_diagnosis = st.button("Jalankan Diagnosis", type="primary", width="stretch")
    if not tombol_diagnosis:
        return

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
