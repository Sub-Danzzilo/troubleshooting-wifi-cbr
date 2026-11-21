"""Siklus Case-Based Reasoning (CBR) 4R: Retrieve, Reuse, Revise, Retain.

Satu fungsi per tahap. Basis pengetahuan adalah kumpulan KASUS, bukan aturan.
Tidak ada pemetaan "gejala X -> kesimpulan Y" di file ini; keputusan diambil
dari kemiripan terhadap kasus lama.
"""

import copy

from core.case_base import (
    AMBANG_DUPLIKAT,
    AMBANG_MIN_SIMILARITY,
    BOBOT_GEJALA,
    TOP_K,
)
from core.similarity import (
    bandingkan_gejala,
    jaccard_similarity,
    weighted_jaccard_similarity,
)


def _skor_similarity(gejala_input, gejala_kasus, mode_similarity):
    """Hitung skor dengan fungsi similarity yang sama untuk semua tahap."""
    if mode_similarity == "weighted":
        return weighted_jaccard_similarity(gejala_input, gejala_kasus, BOBOT_GEJALA)
    return jaccard_similarity(gejala_input, gejala_kasus)


def retrieve(gejala_input, case_base, mode_similarity="jaccard", top_k=None):
    """Tahap RETRIEVE: cari kasus lama yang paling mirip dengan keluhan baru.

    Semua kasus dihitung skornya (kecuali status "belum_terselesaikan"), lalu
    diurutkan menurun. Daftar kandidat dikembalikan lengkap agar tahap Revise
    bisa menawarkan kandidat berikutnya; UI hanya menampilkan top_k pertama.

    Hasil berupa dict:
        kandidat        : list {kasus, skor, penjelasan} terurut menurun
        ada_kecocokan   : False bila skor tertinggi < AMBANG_MIN_SIMILARITY
        skor_tertinggi  : skor kandidat pertama (0.0 bila kosong)
        ambang_min      : nilai ambang yang dipakai
        mode_similarity : mode yang dipakai
        pesan           : keterangan singkat untuk UI
    """
    top_k = TOP_K if top_k is None else top_k
    kandidat = []
    for kasus in case_base:
        if kasus.get("status") == "belum_terselesaikan":
            continue
        skor = _skor_similarity(gejala_input, kasus["gejala"], mode_similarity)
        kandidat.append(
            {
                "kasus": kasus,
                "skor": skor,
                "penjelasan": bandingkan_gejala(gejala_input, kasus["gejala"]),
            }
        )

    # Urutan menurun; sort stabil sehingga skor sama mempertahankan urutan kasus.
    kandidat.sort(key=lambda item: item["skor"], reverse=True)
    skor_tertinggi = kandidat[0]["skor"] if kandidat else 0.0
    ada_kecocokan = bool(kandidat) and skor_tertinggi >= AMBANG_MIN_SIMILARITY

    if not kandidat:
        pesan = "Case base belum berisi kasus."
    elif ada_kecocokan:
        pesan = "Ditemukan kasus lama yang cukup mirip."
    else:
        pesan = "Tidak ada kasus yang cukup mirip."

    return {
        "kandidat": kandidat,
        "top_k": top_k,
        "ada_kecocokan": ada_kecocokan,
        "skor_tertinggi": skor_tertinggi,
        "ambang_min": AMBANG_MIN_SIMILARITY,
        "mode_similarity": mode_similarity,
        "pesan": pesan,
    }


def reuse(kasus_terpilih, gejala_input):
    """Tahap REUSE: pakai solusi kasus terpilih apa adanya.

    Tidak ada adaptasi if-then. Solusi disalin utuh, dan selisih gejala
    dikembalikan lewat "penjelasan" (cocok / hanya input / hanya kasus) sebagai
    hal yang perlu diverifikasi pengguna.
    """
    return {
        "kasus_id": kasus_terpilih["id"],
        "kategori_solusi": kasus_terpilih["kategori_solusi"],
        "solusi": list(kasus_terpilih["solusi"]),
        "penjelasan": bandingkan_gejala(gejala_input, kasus_terpilih["gejala"]),
    }


def revise(hasil_retrieve, indeks_sekarang, berhasil, solusi_baru=None):
    """Tahap REVISE: tangani umpan balik pengguna terhadap solusi.

    Parameter:
        hasil_retrieve : hasil fungsi retrieve().
        indeks_sekarang: posisi kandidat yang sedang dicoba (0 = terbaik).
        berhasil       : True bila solusi kandidat berhasil.
        solusi_baru    : solusi dari pengguna, dipakai bila semua kandidat habis.

    Keputusan yang dikembalikan:
        "retain"               : solusi berhasil, lanjut simpan kasus.
        "kandidat_berikutnya"  : solusi gagal, coba kandidat peringkat berikutnya.
        "solusi_baru"          : semua kandidat habis, pakai solusi dari pengguna.
        "tidak_ada_kandidat"   : semua kandidat habis dan tidak ada solusi baru.
    """
    kandidat = hasil_retrieve.get("kandidat", [])
    if not kandidat:
        return {
            "keputusan": "tidak_ada_kandidat",
            "indeks_kandidat": 0,
            "kasus_terpilih": None,
            "pesan": "Belum ada kandidat solusi untuk dinilai.",
        }

    # Indeks dari session_state bisa tertinggal setelah case base berubah.
    indeks_sekarang = min(max(0, int(indeks_sekarang)), len(kandidat) - 1)

    if berhasil:
        return {
            "keputusan": "retain",
            "indeks_kandidat": indeks_sekarang,
            "kasus_terpilih": kandidat[indeks_sekarang]["kasus"],
            "pesan": "Solusi berhasil; kasus siap disimpan ke basis kasus.",
        }

    indeks_berikut = indeks_sekarang + 1
    if indeks_berikut < len(kandidat):
        return {
            "keputusan": "kandidat_berikutnya",
            "indeks_kandidat": indeks_berikut,
            "kasus_terpilih": kandidat[indeks_berikut]["kasus"],
            "pesan": "Solusi belum berhasil; menampilkan kandidat berikutnya.",
        }

    if solusi_baru:
        return {
            "keputusan": "solusi_baru",
            "indeks_kandidat": indeks_sekarang,
            "kasus_terpilih": None,
            "solusi_baru": solusi_baru,
            "pesan": "Semua kandidat habis; solusi pengguna akan disimpan.",
        }

    return {
        "keputusan": "tidak_ada_kandidat",
        "indeks_kandidat": indeks_sekarang,
        "kasus_terpilih": None,
        "pesan": "Semua kandidat sudah dicoba dan belum ada solusi yang berhasil.",
    }


def buat_id_kasus_baru(case_base):
    """Buat id kasus berikutnya (K16, K17, ...) dari id yang sudah ada."""
    nomor_tertinggi = 0
    for kasus in case_base:
        id_kasus = str(kasus.get("id", ""))
        if id_kasus.upper().startswith("K") and id_kasus[1:].isdigit():
            nomor_tertinggi = max(nomor_tertinggi, int(id_kasus[1:]))
    return f"K{nomor_tertinggi + 1:02d}"


def retain(gejala_input, kasus_acuan, solusi, status, case_base):
    """Tahap RETAIN: simpan pengalaman baru ke basis kasus.

    Bila kasus baru identik dengan kasus lama (similarity >= AMBANG_DUPLIKAT),
    kasus TIDAK ditambahkan; hanya jumlah_dipakai kasus lama yang naik.
    Selain itu kasus baru ditambahkan dengan id otomatis.

    Mengembalikan (case_base_baru, info) tanpa mengubah list masukan.
    """
    if status not in ("berhasil", "belum_terselesaikan"):
        raise ValueError("Status kasus harus 'berhasil' atau 'belum_terselesaikan'.")
    if not solusi:
        raise ValueError("Solusi kasus baru tidak boleh kosong.")

    case_base_baru = copy.deepcopy(case_base)
    gejala_baru = sorted(set(gejala_input or []))
    if not gejala_baru:
        raise ValueError("Kasus baru harus memiliki minimal satu gejala.")

    kasus_duplikat = None
    skor_duplikat = 0.0
    for kasus in case_base_baru:
        # Kasus yang belum terselesaikan tidak boleh "menelan" kasus baru yang
        # gejalanya sama, karena kasus itu tidak dipakai saat retrieve.
        if kasus.get("status") == "belum_terselesaikan":
            continue
        skor = jaccard_similarity(gejala_baru, kasus["gejala"])
        if skor > skor_duplikat:
            skor_duplikat = skor
            kasus_duplikat = kasus

    if kasus_duplikat is not None and skor_duplikat >= AMBANG_DUPLIKAT:
        kasus_duplikat["jumlah_dipakai"] = int(kasus_duplikat.get("jumlah_dipakai", 0)) + 1
        info = {
            "aksi": "duplikat",
            "id_kasus": kasus_duplikat["id"],
            "nama_kasus": kasus_duplikat["nama_kasus"],
            "skor_duplikat": skor_duplikat,
            "jumlah_kasus": len(case_base_baru),
            "pesan": (
                f"Kasus baru identik dengan {kasus_duplikat['id']} "
                f"(similarity {skor_duplikat:.4f}). Kasus tidak ditambahkan, "
                f"jumlah_dipakai menjadi {kasus_duplikat['jumlah_dipakai']}."
            ),
        }
        return case_base_baru, info

    id_baru = buat_id_kasus_baru(case_base_baru)
    if kasus_acuan:
        nama_kasus = f"Variasi dari {kasus_acuan['nama_kasus']}"
        kategori_solusi = kasus_acuan.get("kategori_solusi", "baru")
    else:
        nama_kasus = "Kasus baru dari pengguna"
        kategori_solusi = "baru"

    kasus_baru = {
        "id": id_baru,
        "nama_kasus": nama_kasus,
        "gejala": gejala_baru,
        "solusi": list(solusi),
        "kategori_solusi": kategori_solusi,
        "status": status,
        "jumlah_dipakai": 1,
        "sumber": "retain",
    }
    case_base_baru.append(kasus_baru)
    info = {
        "aksi": "ditambahkan",
        "id_kasus": id_baru,
        "nama_kasus": nama_kasus,
        "skor_duplikat": skor_duplikat,
        "jumlah_kasus": len(case_base_baru),
        "pesan": f"Kasus baru {id_baru} ditambahkan. Jumlah kasus menjadi {len(case_base_baru)}.",
    }
    return case_base_baru, info
