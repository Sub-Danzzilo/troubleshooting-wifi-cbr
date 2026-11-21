"""Sidebar: info metode, mode similarity, daftar kasus, dan reset case base."""

import streamlit as st

from core import storage


def _tabel_semua_kasus(case_base):
    baris = [
        {
            "ID": kasus["id"],
            "Nama": kasus["nama_kasus"],
            "Kategori": kasus["kategori_solusi"],
            "Status": kasus["status"],
            "Dipakai": kasus["jumlah_dipakai"],
            "Sumber": kasus["sumber"],
        }
        for kasus in case_base
    ]
    st.dataframe(baris, hide_index=True)


def render():
    with st.sidebar:
        st.header("Tentang Sistem")
        st.write(
            "Sistem pakar **Case-Based Reasoning (CBR)** dengan siklus 4R: "
            "Retrieve, Reuse, Revise, Retain. Kemiripan keluhan dihitung dengan "
            "similarity Jaccard atau Weighted Jaccard."
        )

        st.divider()
        st.subheader("Mode Similarity")
        st.radio(
            "Metode",
            ["jaccard", "weighted"],
            format_func=lambda mode: "Weighted Jaccard" if mode == "weighted" else "Jaccard biasa",
            key="mode_similarity",
        )
        st.caption("Mengubah mode langsung menghitung ulang skor pada halaman hasil.")

        st.divider()
        case_base = st.session_state.get("case_base", [])
        st.metric("Jumlah kasus", len(case_base))
        with st.expander("Lihat semua kasus"):
            _tabel_semua_kasus(case_base)

        st.divider()
        with st.expander("Reset case base"):
            st.write(
                "Kembalikan basis kasus ke 15 kasus awal. Kasus hasil retain akan hilang."
            )
            yakin = st.checkbox("Saya yakin ingin reset", key="konfirmasi_reset")
            if st.button("Reset Case Base", disabled=not yakin):
                st.session_state["case_base"] = storage.reset_case_base()
                st.session_state["reset_form"] = True
                st.session_state["halaman"] = "input"
                st.session_state["gejala_input"] = []
                st.session_state["hasil_retrieve"] = None
                st.session_state["indeks_kandidat"] = 0
                st.session_state["info_retain"] = None
                st.session_state["status_feedback"] = "belum"
                st.rerun()
