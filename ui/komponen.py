"""Komponen tampilan dan navigasi yang dipakai lebih dari satu halaman.

Hanya urusan tampilan/state UI; tidak ada perhitungan similarity di sini.
"""

from pathlib import Path

import streamlit as st

from core.case_base import LABEL_GEJALA

LOGO_PATH = Path(__file__).resolve().parents[1] / "assets" / "logo.svg"


PILIHAN_TEMA = {"Gelap": "dark", "Terang": "light"}


def terapkan_gaya():
    """Gaya global seperlunya: lebar konten dan sembunyikan elemen non-aplikasi."""
    st.markdown(
        """
        <style>
          .block-container { max-width: 1080px; padding-top: 2.5rem; padding-bottom: 3rem; }
          [data-testid="stAppDeployButton"] { display: none; }
          footer { visibility: hidden; }
        </style>
        """,
        unsafe_allow_html=True,
    )


def sinkronkan_tema():
    """Catat tema yang sudah terpasang dan samakan pilihan pada sesi baru."""
    if "tema_terpasang" in st.session_state:
        return
    try:
        base = st._config.get_option("theme.base")
    except Exception:
        base = "dark"
    st.session_state["tema_terpasang"] = base
    st.session_state["tema_tampilan"] = "Terang" if base == "light" else "Gelap"


def atur_tema():
    """Terapkan pilihan tema sidebar ke konfigurasi Streamlit.

    Streamlit belum punya API publik untuk mengganti tema saat runtime, jadi
    dipakai helper konfigurasi internal yang sesuai dengan versi yang dipin di
    requirements.txt.
    """
    base = PILIHAN_TEMA.get(st.session_state.get("tema_tampilan"), "dark")
    try:
        st._config.set_option("theme.base", base)
    except Exception as kesalahan:  # pragma: no cover - hanya bila API internal berubah
        st.sidebar.warning(f"Tema tidak dapat diganti: {kesalahan}")


def tampilkan_header(judul, deskripsi=""):
    """Header halaman: logo di kiri, judul dan deskripsi di kanan."""
    kolom_logo, kolom_teks = st.columns([1, 14], vertical_alignment="center")
    with kolom_logo:
        st.image(str(LOGO_PATH), width=48, alt="Logo Sistem Pakar WiFi")
    with kolom_teks:
        st.title(judul)
        if deskripsi:
            st.caption(deskripsi)


def format_persen(skor):
    """Ubah skor 0.0-1.0 menjadi teks persen dengan satu angka desimal."""
    return f"{skor * 100:.1f}%"


def nama_mode_similarity(mode):
    """Nama tampilan mode similarity."""
    return "Weighted Jaccard" if mode == "weighted" else "Jaccard biasa"


def kembali_ke_input():
    """Kembali ke halaman input dan bersihkan form pada rerun berikutnya."""
    st.session_state["reset_form"] = True
    st.session_state["halaman"] = "input"
    st.session_state["gejala_input"] = []
    st.session_state["hasil_retrieve"] = None
    st.session_state["indeks_kandidat"] = 0
    st.session_state["info_retain"] = None
    st.session_state["status_feedback"] = "belum"
    st.rerun()


def _daftar_gejala(daftar, pesan_kosong):
    if not daftar:
        st.caption(pesan_kosong)
        return
    for nama in daftar:
        st.markdown(f"- {LABEL_GEJALA.get(nama, nama)} (`{nama}`)")


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
    """Tabel kasus dengan bar kemiripan dan kategori."""
    baris = [
        {
            "ID": kandidat["kasus"]["id"],
            "Nama Kasus": kandidat["kasus"]["nama_kasus"],
            "Similarity": float(kandidat["skor"]),
            "Kategori": kandidat["kasus"]["kategori_solusi"],
        }
        for kandidat in daftar_kandidat
    ]
    st.dataframe(
        baris,
        hide_index=True,
        column_config={
            "ID": st.column_config.TextColumn("ID", width="small"),
            "Nama Kasus": st.column_config.TextColumn("Nama Kasus", width="medium"),
            "Similarity": st.column_config.ProgressColumn(
                "Similarity",
                help="Skor similarity (0-1) dari mode yang dipilih",
                min_value=0.0,
                max_value=1.0,
                format="%.4f",
                width="small",
            ),
            "Kategori": st.column_config.TextColumn("Kategori", width="medium"),
        },
    )


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
