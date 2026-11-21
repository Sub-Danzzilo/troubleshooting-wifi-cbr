"""Halaman 2: hasil diagnosis, perhitungan rinci, dan umpan balik (Revise)."""

import streamlit as st

from core import cbr_engine, storage
from core.case_base import BOBOT_GEJALA, TOP_K
from core.similarity import hitung_rinci
from ui.komponen import (
    format_persen,
    kembali_ke_input,
    nama_mode_similarity,
    tampilkan_langkah_solusi,
    tampilkan_penjelasan_gejala,
    tampilkan_perhitungan_rinci,
    tampilkan_tabel_kasus,
)


def _simpan_retain(gejala_input, kasus_acuan, solusi):
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


def _terapkan_revise(hasil, indeks, gejala_input, berhasil, solusi_baru=None):
    """Jalankan tahap Revise, lalu Retain bila keputusannya menyimpan kasus."""
    keputusan = cbr_engine.revise(hasil, indeks, berhasil, solusi_baru=solusi_baru)
    if keputusan["keputusan"] == "retain":
        kasus_acuan = keputusan["kasus_terpilih"]
        _simpan_retain(gejala_input, kasus_acuan, kasus_acuan["solusi"])
    elif keputusan["keputusan"] == "solusi_baru":
        _simpan_retain(gejala_input, None, [keputusan["solusi_baru"]])


def render():
    st.title("Hasil Diagnosis")
    gejala_input = st.session_state.get("gejala_input") or []
    if not gejala_input:
        st.info("Belum ada diagnosis. Silakan isi gejala terlebih dahulu.")
        if st.button("⬅️ Kembali ke halaman input"):
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
        st.error("Case base kosong. Gunakan tombol Reset Case Base di sidebar.")
        return

    indeks = max(0, int(st.session_state.get("indeks_kandidat", 0)))
    indeks = min(indeks, len(kandidat) - 1)
    st.session_state["indeks_kandidat"] = indeks

    st.caption(
        f"Mode similarity: **{nama_mode_similarity(mode)}** · Ambang minimum: "
        f"{format_persen(hasil['ambang_min'])} · Gejala terpilih: {len(gejala_input)}"
    )

    if hasil["ada_kecocokan"]:
        teratas = kandidat[0]
        st.success(
            f"Kasus paling mirip: **{teratas['kasus']['id']} — {teratas['kasus']['nama_kasus']}** "
            f"(similarity {format_persen(teratas['skor'])})"
        )
    else:
        st.warning(
            f"Tidak ada kasus yang cukup mirip: skor tertinggi "
            f"{format_persen(hasil['skor_tertinggi'])} di bawah ambang "
            f"{format_persen(hasil['ambang_min'])}. Kasus terdekat tetap ditampilkan "
            "sebagai rujukan, tetapi solusinya belum tentu tepat."
        )

    st.subheader(f"Top-{min(TOP_K, len(kandidat))} Kasus Paling Mirip")
    tampilkan_tabel_kasus(kandidat[:TOP_K])

    for urutan, item in enumerate(kandidat[:TOP_K], start=1):
        judul = (
            f"Lihat perhitungan rinci — {urutan}. {item['kasus']['id']} "
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

    st.divider()
    pilihan = kandidat[indeks]
    kasus = pilihan["kasus"]
    reuse = cbr_engine.reuse(kasus, gejala_input)

    st.subheader(f"Rekomendasi Solusi (kandidat {indeks + 1} dari {len(kandidat)})")
    st.markdown(
        f"**{kasus['id']} — {kasus['nama_kasus']}**  \n"
        f"Kategori: `{kasus['kategori_solusi']}` · Sumber: {kasus['sumber']} · "
        f"Sudah dipakai {kasus['jumlah_dipakai']}x"
    )
    st.progress(
        max(0.0, min(1.0, pilihan["skor"])),
        text=f"Similarity {pilihan['skor']:.4f} ({format_persen(pilihan['skor'])})",
    )
    tampilkan_langkah_solusi(reuse["solusi"])

    st.markdown("**Penjelasan gejala**")
    tampilkan_penjelasan_gejala(reuse["penjelasan"])

    st.divider()
    st.subheader("Umpan Balik (Revise)")
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
            if st.button("💾 Simpan ke Basis Kasus (Retain)", type="primary"):
                _terapkan_revise(hasil, indeks, gejala_input, berhasil=True)

        elif jawaban == "Tidak berhasil":
            hasil_revise = cbr_engine.revise(hasil, indeks, False)
            if hasil_revise["keputusan"] == "kandidat_berikutnya":
                st.info(hasil_revise["pesan"])
                if st.button("➡️ Coba Kandidat Berikutnya", type="primary"):
                    st.session_state["indeks_kandidat"] = hasil_revise["indeks_kandidat"]
                    st.rerun()
            else:
                st.warning(hasil_revise["pesan"])
                with st.form("form_solusi_pengguna"):
                    teks_solusi = st.text_area(
                        "Solusi yang akhirnya berhasil (opsional)",
                        placeholder="Tuliskan langkah yang benar-benar menyelesaikan masalah.",
                    )
                    kirim = st.form_submit_button("Simpan Solusi Pengguna (Retain)")
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

    st.divider()
    if st.button("🔄 Diagnosis Baru"):
        kembali_ke_input()
