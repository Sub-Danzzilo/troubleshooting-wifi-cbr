"""Halaman 2: hasil diagnosis, perhitungan rinci, dan umpan balik (Revise)."""

from collections.abc import Iterable
from typing import Any

import streamlit as st

from core import cbr_engine, storage
from core.case_base import BOBOT_GEJALA, TOP_K, Kasus
from core.similarity import hitung_rinci
from ui.komponen import (
    format_persen,
    kembali_ke_input,
    nama_mode_similarity,
    tampilkan_header,
    tampilkan_langkah_solusi,
    tampilkan_penjelasan_gejala,
    tampilkan_perhitungan_rinci,
    tampilkan_tabel_kasus,
)


def _simpan_retain(
    gejala_input: Iterable[str],
    kasus_acuan: Kasus | None,
    solusi: Iterable[str],
) -> None:
    """Jalankan Retain, persist ke JSON, dan simpan hasilnya di session_state."""
    case_base_baru, info = cbr_engine.retain(
        gejala_input,
        kasus_acuan,
        solusi,
        "berhasil",
        st.session_state["case_base"],
    )
    storage.simpan_case_base(case_base_baru)
    st.session_state["case_base"] = case_base_baru
    st.session_state["info_retain"] = info
    st.session_state["status_feedback"] = "berhasil"
    st.rerun()


def _terapkan_revise(
    hasil: dict[str, Any],
    indeks: int,
    gejala_input: Iterable[str],
    berhasil: bool,
    solusi_baru: str | None = None,
) -> None:
    """Jalankan tahap Revise, lalu Retain bila keputusannya menyimpan kasus."""
    keputusan = cbr_engine.revise(hasil, indeks, berhasil, solusi_baru=solusi_baru)
    if keputusan["keputusan"] == "retain":
        kasus_acuan = keputusan["kasus_terpilih"]
        _simpan_retain(gejala_input, kasus_acuan, kasus_acuan["solusi"])
    elif keputusan["keputusan"] == "solusi_baru":
        _simpan_retain(gejala_input, None, [keputusan["solusi_baru"]])


def render() -> None:
    gejala_input = st.session_state.get("gejala_input") or []
    if not gejala_input:
        tampilkan_header("Hasil Diagnosis")
        st.info("Belum ada diagnosis. Isi gejala terlebih dahulu di halaman input.")
        if st.button("Kembali ke halaman input", width="stretch"):
            kembali_ke_input()
        return

    mode = st.session_state.get("mode_similarity", "jaccard")
    if st.session_state.get("mode_hasil") not in (None, mode):
        st.session_state["indeks_kandidat"] = 0
    st.session_state["mode_hasil"] = mode
    hasil = cbr_engine.retrieve(gejala_input, st.session_state["case_base"], mode)
    st.session_state["hasil_retrieve"] = hasil
    kandidat = hasil["kandidat"]

    if not kandidat:
        tampilkan_header("Hasil Diagnosis")
        st.error("Basis kasus kosong. Gunakan tombol Reset Case Base di sidebar.")
        return

    indeks = max(0, int(st.session_state.get("indeks_kandidat", 0)))
    indeks = min(indeks, len(kandidat) - 1)
    st.session_state["indeks_kandidat"] = indeks

    tampilkan_header(
        "Hasil Diagnosis",
        "Keluhan Anda dibandingkan dengan setiap kasus lama menggunakan himpunan gejala.",
    )
    st.caption(
        f"Langkah 2 dari 2 · Mode {nama_mode_similarity(mode)} · Ambang minimum "
        f"{format_persen(hasil['ambang_min'])} · {len(gejala_input)} gejala dipilih"
    )

    if hasil["ada_kecocokan"]:
        teratas = kandidat[0]
        st.success(
            f"Kasus paling mirip: **{teratas['kasus']['id']} — {teratas['kasus']['nama_kasus']}**."
        )
    else:
        st.warning(
            f"Tidak ada kasus yang cukup mirip: skor tertinggi "
            f"{format_persen(hasil['skor_tertinggi'])} di bawah ambang "
            f"{format_persen(hasil['ambang_min'])}. Kasus terdekat tetap ditampilkan "
            "sebagai rujukan, tetapi solusinya belum tentu tepat."
        )

    metrik = st.columns(3)
    metrik[0].metric(
        "Similarity tertinggi", f"{kandidat[0]['skor']:.4f}", border=True
    )
    metrik[1].metric(
        "Kandidat", f"{indeks + 1} dari {len(kandidat)}", border=True
    )
    metrik[2].metric(
        "Kasus di basis", len(st.session_state["case_base"]), border=True
    )

    with st.container(border=True):
        st.subheader(f"Top-{min(TOP_K, len(kandidat))} Kasus Paling Mirip")
        tampilkan_tabel_kasus(kandidat[:TOP_K])
        st.caption(
            "Tabel memakai skor dari fungsi similarity yang sama dengan perhitungan rinci."
        )

    st.caption("Buka kasus di bawah untuk melihat perhitungan similarity secara rinci.")
    for urutan, item in enumerate(kandidat[:TOP_K], start=1):
        judul = (
            f"Perhitungan rinci — {urutan}. {item['kasus']['id']} "
            f"(skor {item['skor']:.4f})"
        )
        with st.expander(judul):
            rinci = hitung_rinci(
                gejala_input,
                item["kasus"]["gejala"],
                hasil["mode_similarity"],
                BOBOT_GEJALA,
            )
            tampilkan_perhitungan_rinci(rinci)

    pilihan = kandidat[indeks]
    kasus = pilihan["kasus"]
    reuse = cbr_engine.reuse(kasus, gejala_input)

    with st.container(border=True):
        st.subheader("Rekomendasi Solusi")
        st.caption(
            f"Kandidat {indeks + 1} dari {len(kandidat)} · "
            f"Kategori {kasus['kategori_solusi']} · Sumber {kasus['sumber']} · "
            f"Sudah dipakai {kasus['jumlah_dipakai']} kali"
        )
        st.markdown(f"**{kasus['id']} — {kasus['nama_kasus']}**")
        st.progress(
            max(0.0, min(1.0, pilihan["skor"])),
            text=f"Similarity {pilihan['skor']:.4f} ({format_persen(pilihan['skor'])})",
        )
        tampilkan_langkah_solusi(reuse["solusi"])
        st.divider()
        st.markdown("**Penjelasan gejala**")
        tampilkan_penjelasan_gejala(reuse["penjelasan"])

    with st.container(border=True):
        st.subheader("Umpan Balik")
        st.caption(
            "Tahap Revise: nilai apakah solusi berhasil. Jika berhasil, kasus disimpan "
            "ke basis kasus lewat tahap Retain."
        )
        info_retain = st.session_state.get("info_retain")
        if info_retain:
            if info_retain["aksi"] == "ditambahkan":
                st.success(info_retain["pesan"])
            else:
                st.info(info_retain["pesan"])
            st.caption(f"Jumlah kasus pada basis kasus: {info_retain['jumlah_kasus']}")
        else:
            jawaban = st.radio(
                "Apakah solusi di atas berhasil?",
                ["Belum dijawab", "Ya, berhasil", "Tidak berhasil"],
                index=0,
                horizontal=True,
                key=f"pilihan_feedback_{indeks}",
            )

            if jawaban == "Ya, berhasil":
                if st.button("Simpan ke Basis Kasus", type="primary"):
                    _terapkan_revise(hasil, indeks, gejala_input, berhasil=True)

            elif jawaban == "Tidak berhasil":
                hasil_revise = cbr_engine.revise(hasil, indeks, False)
                if hasil_revise["keputusan"] == "kandidat_berikutnya":
                    st.info(hasil_revise["pesan"])
                    if st.button("Coba Kandidat Berikutnya", type="primary"):
                        st.session_state["indeks_kandidat"] = hasil_revise["indeks_kandidat"]
                        st.rerun()
                else:
                    st.warning(hasil_revise["pesan"])
                    with st.form("form_solusi_pengguna"):
                        teks_solusi = st.text_area(
                            "Solusi yang akhirnya berhasil (opsional)",
                            placeholder="Tuliskan langkah yang benar-benar menyelesaikan masalah.",
                        )
                        kirim = st.form_submit_button("Simpan Solusi Pengguna")
                    if kirim:
                        if not teks_solusi.strip():
                            st.error("Tuliskan solusi terlebih dahulu sebelum menyimpan.")
                        else:
                            _terapkan_revise(
                                hasil,
                                indeks,
                                gejala_input,
                                berhasil=False,
                                solusi_baru=teks_solusi.strip(),
                            )

    st.write("")
    if st.button("Diagnosis Baru", width="stretch"):
        kembali_ke_input()
