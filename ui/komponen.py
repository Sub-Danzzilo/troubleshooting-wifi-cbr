"""Komponen tampilan yang dipakai lebih dari satu halaman.

Hanya urusan tampilan; tidak ada perhitungan similarity di sini.
"""

import streamlit as st

from core.case_base import LABEL_GEJALA


def format_persen(skor):
    """Ubah skor 0.0-1.0 menjadi teks persen dengan satu angka desimal."""
    return f"{skor * 100:.1f}%"


def label_gejala(nama):
    """Label Bahasa Indonesia untuk sebuah nama gejala."""
    return LABEL_GEJALA.get(nama, nama)


def _daftar_gejala(daftar, pesan_kosong):
    if not daftar:
        st.caption(pesan_kosong)
        return
    for nama in daftar:
        st.markdown(f"- {label_gejala(nama)} (`{nama}`)")


def _angka(nilai):
    """Tampilkan angka tanpa desimal bila nilainya bulat (6.0 -> 6)."""
    if isinstance(nilai, float) and nilai.is_integer():
        return str(int(nilai))
    return f"{nilai:g}"


def _himpunan(daftar):
    if not daftar:
        return "∅"
    return "{" + ", ".join(daftar) + "}"


def tampilkan_tabel_kasus(daftar_kandidat):
    """Tabel kasus: ID, nama, similarity, kategori, dan ringkasan solusi."""
    baris = []
    for urutan, kandidat in enumerate(daftar_kandidat, start=1):
        kasus = kandidat["kasus"]
        langkah_pertama = kasus["solusi"][0] if kasus.get("solusi") else ""
        if len(langkah_pertama) > 70:
            langkah_pertama = langkah_pertama[:67] + "..."
        baris.append(
            {
                "#": urutan,
                "ID": kasus["id"],
                "Nama Kasus": kasus["nama_kasus"],
                "Similarity": f"{kandidat['skor']:.4f}",
                "Persen": format_persen(kandidat["skor"]),
                "Kategori": kasus["kategori_solusi"],
                "Ringkasan Solusi": langkah_pertama,
            }
        )
    st.dataframe(baris, hide_index=True)


def tampilkan_langkah_solusi(solusi):
    """Daftar bernomor langkah solusi."""
    for nomor, langkah in enumerate(solusi, start=1):
        st.markdown(f"**{nomor}.** {langkah}")


def tampilkan_penjelasan_gejala(penjelasan):
    """Tiga kelompok gejala: cocok, hanya di input, hanya di kasus."""
    kolom = st.columns(3)
    with kolom[0]:
        st.markdown(f"**Cocok (A ∩ B) — {len(penjelasan['cocok'])} gejala**")
        _daftar_gejala(penjelasan["cocok"], "Tidak ada gejala yang sama.")
    with kolom[1]:
        st.markdown(f"**Hanya di input (A − B) — {len(penjelasan['hanya_input'])} gejala**")
        _daftar_gejala(penjelasan["hanya_input"], "Tidak ada gejala tambahan.")
    with kolom[2]:
        st.markdown(f"**Hanya di kasus (B − A) — {len(penjelasan['hanya_kasus'])} gejala**")
        _daftar_gejala(penjelasan["hanya_kasus"], "Tidak ada gejala yang tidak dilaporkan.")


def tampilkan_perhitungan_rinci(rinci):
    """Tampilkan langkah hitung similarity yang bisa ditulis ulang di papan tulis."""
    st.markdown(f"**Rumus {rinci['mode']}**: `{rinci['rumus']}`")
    st.markdown(f"**A (input)** = `{_himpunan(rinci['himpunan_a'])}` → {rinci['jumlah_a']} anggota")
    st.markdown(f"**B (kasus)** = `{_himpunan(rinci['himpunan_b'])}` → {rinci['jumlah_b']} anggota")
    st.markdown(f"**A ∩ B** = `{_himpunan(rinci['irisan'])}` → {rinci['jumlah_irisan']} anggota")
    st.markdown(f"**A ∪ B** = `{_himpunan(rinci['gabungan'])}` → {rinci['jumlah_gabungan']} anggota")

    if rinci["mode"] == "jaccard":
        st.markdown(
            f"**Hasil** = {rinci['pembilang']} / {rinci['penyebut']} = "
            f"**{rinci['hasil']:.4f}**"
        )
    else:
        tabel = [
            {
                "Gejala": item["gejala"],
                "Label": item["label"],
                "Bobot": item["bobot"],
                "Ada di irisan": "ya" if item["gejala"] in rinci["irisan"] else "—",
            }
            for item in rinci["bobot_gabungan"]
        ]
        st.table(tabel)
        st.markdown(
            f"**Σ bobot irisan** = {_angka(rinci['pembilang'])} · "
            f"**Σ bobot gabungan** = {_angka(rinci['penyebut'])}"
        )
        st.markdown(
            f"**Hasil** = {_angka(rinci['pembilang'])} / {_angka(rinci['penyebut'])} = "
            f"**{rinci['hasil']:.4f}**"
        )
