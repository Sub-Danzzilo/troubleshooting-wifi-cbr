"""Data dan parameter sistem pakar CBR troubleshooting WiFi.

File ini HANYA berisi data dan konstanta: daftar gejala, pemetaan pilihan lampu
router, bobot gejala, parameter similarity/retain, dan case base awal. Tidak ada
logika inferensi di sini (tidak ada aturan IF-THEN yang memetakan gejala ke
kesimpulan).
"""

import os
from typing import TypedDict


class Kasus(TypedDict):
    """Struktur satu kasus pada basis pengetahuan CBR."""

    id: str
    nama_kasus: str
    gejala: list[str]
    solusi: list[str]
    kategori_solusi: str
    status: str
    jumlah_dipakai: int
    sumber: str


# ---------------------------------------------------------------------------
# 1. DAFTAR_GEJALA — 25 gejala boolean
#    Kelompok A: keluhan utama pengguna (checkbox)
#    Kelompok B: status lampu router (satu pilihan radio per lampu)
#    Kelompok C: informasi tambahan (checkbox)
# ---------------------------------------------------------------------------

DAFTAR_GEJALA: list[dict[str, str]] = [
    # --- Kelompok A: keluhan utama -----------------------------------------
    {"nama": "tidak_connect", "label": "Tidak bisa terhubung ke WiFi sama sekali", "kelompok": "A"},
    {"nama": "connect_tapi_tanpa_internet", "label": "Terhubung ke WiFi, tetapi tidak ada akses internet", "kelompok": "A"},
    {"nama": "internet_lambat", "label": "Internet lambat / loading lama", "kelompok": "A"},
    {"nama": "putus_nyambung", "label": "Koneksi sering putus lalu tersambung lagi", "kelompok": "A"},
    {"nama": "semua_perangkat", "label": "Gangguan dirasakan di semua perangkat", "kelompok": "A"},
    {"nama": "hanya_1_perangkat", "label": "Gangguan hanya pada satu perangkat", "kelompok": "A"},
    {"nama": "wifi_tidak_muncul", "label": "Nama WiFi tidak muncul di daftar jaringan", "kelompok": "A"},
    # --- Kelompok B: status lampu router -----------------------------------
    {"nama": "power_nyala", "label": "Lampu POWER menyala normal", "kelompok": "B"},
    {"nama": "power_mati", "label": "Lampu POWER mati", "kelompok": "B"},
    {"nama": "power_kedip", "label": "Lampu POWER berkedip", "kelompok": "B"},
    {"nama": "pon_nyala", "label": "Lampu PON menyala normal", "kelompok": "B"},
    {"nama": "pon_mati", "label": "Lampu PON mati", "kelompok": "B"},
    {"nama": "pon_kedip", "label": "Lampu PON berkedip", "kelompok": "B"},
    {"nama": "los_mati", "label": "Lampu LOS mati (normal)", "kelompok": "B"},
    {"nama": "los_merah", "label": "Lampu LOS menyala merah", "kelompok": "B"},
    {"nama": "los_kedip", "label": "Lampu LOS berkedip", "kelompok": "B"},
    {"nama": "internet_nyala", "label": "Lampu INTERNET menyala normal", "kelompok": "B"},
    {"nama": "internet_mati", "label": "Lampu INTERNET mati", "kelompok": "B"},
    {"nama": "wlan_nyala", "label": "Lampu WLAN menyala normal", "kelompok": "B"},
    {"nama": "wlan_mati", "label": "Lampu WLAN mati", "kelompok": "B"},
    {"nama": "lan_nyala", "label": "Lampu LAN menyala normal", "kelompok": "B"},
    {"nama": "lan_mati", "label": "Lampu LAN mati", "kelompok": "B"},
    # --- Kelompok C: informasi tambahan ------------------------------------
    # router_tidak_punya_indikator ikut Kelompok C, tetapi di UI ditampilkan di
    # bagian status lampu karena pilihannya menonaktifkan seluruh pilihan lampu.
    {"nama": "router_tidak_punya_indikator", "label": "Router tidak memiliki lampu indikator", "kelompok": "C"},
    {"nama": "password_ditolak", "label": "Pesan password salah muncul saat menyambung", "kelompok": "C"},
    {"nama": "sinyal_lemah", "label": "Sinyal lemah / perangkat jauh dari router / banyak dinding", "kelompok": "C"},
]

LABEL_GEJALA: dict[str, str] = {
    gejala["nama"]: gejala["label"] for gejala in DAFTAR_GEJALA
}

# ---------------------------------------------------------------------------
# 2. PILIHAN_LAMPU — satu lampu = satu radio di UI
#    Pasangan (label tombol, nama gejala boolean). None = tidak ada gejala
#    (dipakai untuk opsi "Tidak tahu").
# ---------------------------------------------------------------------------

PILIHAN_LAMPU: dict[str, list[tuple[str, str | None]]] = {
    "POWER": [
        ("Tidak tahu", None),
        ("Menyala", "power_nyala"),
        ("Mati", "power_mati"),
        ("Berkedip", "power_kedip"),
    ],
    "PON": [
        ("Tidak tahu", None),
        ("Menyala", "pon_nyala"),
        ("Mati", "pon_mati"),
        ("Berkedip", "pon_kedip"),
    ],
    "LOS": [
        ("Tidak tahu", None),
        ("Mati (normal)", "los_mati"),
        ("Merah", "los_merah"),
        ("Berkedip", "los_kedip"),
    ],
    "INTERNET": [
        ("Tidak tahu", None),
        ("Menyala", "internet_nyala"),
        ("Mati", "internet_mati"),
    ],
    "WLAN": [
        ("Tidak tahu", None),
        ("Menyala", "wlan_nyala"),
        ("Mati", "wlan_mati"),
    ],
    "LAN": [
        ("Tidak tahu", None),
        ("Menyala", "lan_nyala"),
        ("Mati", "lan_mati"),
    ],
}

# ---------------------------------------------------------------------------
# 3. BOBOT_GEJALA — parameter similarity (bukan aturan inferensi)
#    0.5 = kondisi normal yang muncul di banyak kasus, nilainya ditekan.
#    2.0 = gejala menyimpang dari kondisi normal, lebih membedakan kasus.
#    1.0 = keluhan/informasi umum.
# ---------------------------------------------------------------------------

BOBOT_GEJALA: dict[str, float] = {
    # Keluhan utama
    "tidak_connect": 1.0,
    "connect_tapi_tanpa_internet": 1.0,
    "internet_lambat": 1.0,
    "putus_nyambung": 1.0,
    "semua_perangkat": 1.0,
    "hanya_1_perangkat": 1.0,
    "wifi_tidak_muncul": 1.0,
    # Lampu POWER
    "power_nyala": 0.5,
    "power_mati": 2.0,
    "power_kedip": 2.0,
    # Lampu PON
    "pon_nyala": 0.5,
    "pon_mati": 2.0,
    "pon_kedip": 2.0,
    # Lampu LOS
    "los_mati": 0.5,
    "los_merah": 2.0,
    "los_kedip": 2.0,
    # Lampu INTERNET
    "internet_nyala": 0.5,
    "internet_mati": 2.0,
    # Lampu WLAN
    "wlan_nyala": 0.5,
    "wlan_mati": 2.0,
    # Lampu LAN
    "lan_nyala": 0.5,
    "lan_mati": 2.0,
    # Informasi tambahan
    "router_tidak_punya_indikator": 1.0,
    "password_ditolak": 1.0,
    "sinyal_lemah": 1.0,
}

# ---------------------------------------------------------------------------
# 4. PARAMETER SISTEM
#    AMBANG_MIN_SIMILARITY : skor terbaik di bawah nilai ini = "tidak ada kasus
#                            yang cukup mirip", sistem tidak memaksa diagnosis.
#    AMBANG_DUPLIKAT       : skor >= nilai ini = kasus baru dianggap duplikat,
#                            retain hanya menaikkan jumlah_dipakai.
#    TOP_K                 : jumlah kasus teratas yang ditampilkan di UI.
# ---------------------------------------------------------------------------

AMBANG_MIN_SIMILARITY = 0.30
AMBANG_DUPLIKAT = 1.0
TOP_K = 3

PATH_CASE_BASE_JSON: str = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "data",
    "case_base.json",
)

# ---------------------------------------------------------------------------
# 5. CASE_BASE_AWAL — 15 kasus awal (basis pengetahuan berbentuk KASUS)
#    Setiap kasus: id, nama_kasus, gejala, solusi, kategori_solusi, status,
#    jumlah_dipakai, sumber. Tiap kasus sengaja hanya memakai 4-6 gejala agar
#    similarity mudah dihitung manual di papan tulis.
# ---------------------------------------------------------------------------

CASE_BASE_AWAL: list[Kasus] = [
    # --- kabel_optik_bermasalah -------------------------------------------
    {
        "id": "K01",
        "nama_kasus": "LOS merah, internet mati total di semua perangkat",
        "gejala": [
            "tidak_connect",
            "semua_perangkat",
            "los_merah",
            "pon_mati",
            "internet_mati",
        ],
        "solusi": [
            "Pastikan kabel patch cord fiber di belakang router tidak tertekuk, terjepit, atau lepas.",
            "Cabut dan pasang kembali konektor fiber sampai terdengar klik, lalu tunggu 2-3 menit.",
            "Bersihkan ujung konektor fiber dengan kain bersih kering bila terlihat berdebu.",
            "Matikan router 30 detik lalu nyalakan lagi dan amati lampu LOS.",
            "Jika LOS tetap merah, laporkan gangguan kabel optik ke ISP karena perbaikan ada di sisi jaringan.",
        ],
        "kategori_solusi": "kabel_optik_bermasalah",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K02",
        "nama_kasus": "LOS merah dengan koneksi putus-nyambung",
        "gejala": [
            "tidak_connect",
            "semua_perangkat",
            "putus_nyambung",
            "internet_lambat",
            "los_merah",
            "pon_nyala",
        ],
        "solusi": [
            "Periksa tekukan atau sambungan liar pada kabel fiber di dalam rumah.",
            "Ganti patch cord fiber yang ujungnya longgar atau kotor.",
            "Pasang kembali konektor fiber pada port LOS/PON dan restart router.",
            "Catat waktu koneksi putus, lalu minta ISP memeriksa daya optik (redaman) di sisi pelanggan.",
        ],
        "kategori_solusi": "kabel_optik_bermasalah",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K03",
        "nama_kasus": "LOS berkedip, internet lambat dan tidak stabil",
        "gejala": [
            "internet_lambat",
            "putus_nyambung",
            "los_kedip",
            "pon_nyala",
            "semua_perangkat",
        ],
        "solusi": [
            "Kencangkan konektor fiber pada router dan pada roset dinding.",
            "Hindari menyambung kabel fiber dengan isolasi; gunakan patch cord utuh.",
            "Restart router dan tunggu lampu LOS berhenti berkedip.",
            "Jika LOS tetap berkedip, laporkan ke ISP untuk pengecekan fisik jaringan.",
        ],
        "kategori_solusi": "kabel_optik_bermasalah",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    # --- router_mati_daya --------------------------------------------------
    {
        "id": "K04",
        "nama_kasus": "Router mati total setelah listrik padam",
        "gejala": [
            "tidak_connect",
            "semua_perangkat",
            "wifi_tidak_muncul",
            "power_mati",
            "internet_mati",
        ],
        "solusi": [
            "Pastikan adaptor daya terpasang kuat pada router dan stopkontak.",
            "Coba colokan lain dan tekan tombol power router.",
            "Coba adaptor lain dengan voltase dan polaritas yang sama.",
            "Periksa MCB atau stavolt rumah bila perangkat lain juga mati.",
            "Jika adaptor sudah diganti tetapi router tetap mati, ganti unit router.",
        ],
        "kategori_solusi": "router_mati_daya",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K05",
        "nama_kasus": "Router tanpa lampu indikator tidak memancarkan WiFi",
        "gejala": [
            "tidak_connect",
            "semua_perangkat",
            "wifi_tidak_muncul",
            "router_tidak_punya_indikator",
        ],
        "solusi": [
            "Pastikan adaptor daya benar-benar terpasang dan kabel daya tidak longgar.",
            "Coba stopkontak lain dan tunggu 1 menit, lalu cari nama WiFi dari ponsel.",
            "Raba badan router; bila sangat panas, matikan 10 menit lalu coba nyalakan lagi.",
            "Ganti adaptor daya dengan spesifikasi yang sama.",
            "Jika tetap tidak ada WiFi maupun suara kipas, router kemungkinan rusak dan perlu diganti.",
        ],
        "kategori_solusi": "router_mati_daya",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    # --- gangguan_isp ------------------------------------------------------
    {
        "id": "K06",
        "nama_kasus": "Lampu PON normal tetapi internet mati total",
        "gejala": [
            "connect_tapi_tanpa_internet",
            "semua_perangkat",
            "internet_mati_total",
            "pon_nyala",
            "los_mati",
            "internet_mati",
        ],
        "solusi": [
            "Restart router dan tunggu 3 menit sampai lampu INTERNET menyala.",
            "Cek status gangguan jaringan lewat aplikasi atau situs resmi ISP.",
            "Pastikan tagihan internet sudah dibayar dan layanan tidak diblokir.",
            "Hubungi layanan pelanggan ISP dan minta pengecekan port pelanggan.",
        ],
        "kategori_solusi": "gangguan_isp",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K07",
        "nama_kasus": "Internet lambat pada jam sibuk di semua perangkat",
        "gejala": [
            "internet_lambat",
            "semua_perangkat",
            "connect_tapi_tanpa_internet",
            "pon_nyala",
            "internet_nyala",
        ],
        "solusi": [
            "Ukur kecepatan dengan kabel LAN, bandingkan dengan hasil tes lewat WiFi.",
            "Cek perangkat yang sedang mengunduh atau streaming, lalu batasi pemakaiannya.",
            "Ganti DNS ke DNS publik untuk mengurangi lambatnya pencarian alamat.",
            "Catat jam terjadinya lambat, lalu ajukan keluhan ke ISP atau pertimbangkan naik paket.",
        ],
        "kategori_solusi": "gangguan_isp",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    # --- wlan_nonaktif -----------------------------------------------------
    {
        "id": "K08",
        "nama_kasus": "Lampu WLAN mati sehingga nama WiFi tidak muncul",
        "gejala": [
            "wifi_tidak_muncul",
            "semua_perangkat",
            "wlan_mati",
            "power_nyala",
            "internet_nyala",
        ],
        "solusi": [
            "Tekan tombol WLAN di belakang router selama satu detik.",
            "Masuk ke halaman admin router dan aktifkan menu Wireless/WLAN.",
            "Pastikan opsi SSID Broadcast tidak dinonaktifkan.",
            "Restart router, lalu reset pabrik bila WLAN tetap mati.",
        ],
        "kategori_solusi": "wlan_nonaktif",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K09",
        "nama_kasus": "WiFi tidak terdeteksi di semua perangkat",
        "gejala": [
            "tidak_connect",
            "semua_perangkat",
            "wlan_mati",
            "power_nyala",
            "internet_nyala",
            "pon_nyala",
        ],
        "solusi": [
            "Periksa tombol WLAN pada router, pastikan tidak sengaja tertekan.",
            "Buka halaman admin router (misalnya 192.168.1.1) dan aktifkan wireless.",
            "Ganti channel WiFi ke channel yang lebih sepi, lalu simpan pengaturan.",
            "Restart router dan pindai jaringan dari beberapa perangkat.",
            "Jika WLAN tetap mati, lakukan reset pabrik lalu konfigurasi ulang.",
        ],
        "kategori_solusi": "wlan_nonaktif",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    # --- password_salah ----------------------------------------------------
    {
        "id": "K10",
        "nama_kasus": "Password WiFi ditolak di satu perangkat",
        "gejala": [
            "tidak_connect",
            "password_ditolak",
            "hanya_1_perangkat",
            "wlan_nyala",
            "power_nyala",
        ],
        "solusi": [
            "Pilih 'Lupakan jaringan' pada perangkat, lalu sambungkan ulang dari awal.",
            "Ketik ulang password dengan hati-hati dan perhatikan huruf besar-kecil.",
            "Cek keyboard atau fitur koreksi otomatis yang mungkin mengubah password.",
            "Coba sambungkan perangkat lain untuk memastikan password memang benar.",
            "Jika perlu, ubah password WiFi lewat halaman admin router.",
        ],
        "kategori_solusi": "password_salah",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K11",
        "nama_kasus": "Password WiFi berubah setelah router direset",
        "gejala": [
            "tidak_connect",
            "password_ditolak",
            "semua_perangkat",
            "wlan_nyala",
            "internet_nyala",
        ],
        "solusi": [
            "Lihat stiker bawaan router untuk password default setelah reset.",
            "Coba password default tersebut dari satu perangkat terlebih dahulu.",
            "Masuk ke halaman admin router dan atur ulang nama serta password WiFi.",
            "Sambungkan ulang semua perangkat dengan password baru.",
        ],
        "kategori_solusi": "password_salah",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    # --- masalah_perangkat_klien -------------------------------------------
    {
        "id": "K12",
        "nama_kasus": "Satu perangkat terhubung tetapi tidak ada internet",
        "gejala": [
            "connect_tapi_tanpa_internet",
            "hanya_1_perangkat",
            "internet_nyala",
            "wlan_nyala",
        ],
        "solusi": [
            "Restart perangkat yang bermasalah, lalu sambungkan ulang ke WiFi.",
            "Pilih 'Lupakan jaringan' agar pengaturan lama tidak dipakai lagi.",
            "Matikan VPN atau proxy, lalu cek pengaturan DNS perangkat.",
            "Matikan sementara data seluler agar perangkat benar-benar memakai WiFi.",
            "Reset pengaturan jaringan perangkat bila masalah tetap muncul.",
        ],
        "kategori_solusi": "masalah_perangkat_klien",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K13",
        "nama_kasus": "Koneksi putus-nyambung hanya di satu laptop",
        "gejala": [
            "putus_nyambung",
            "hanya_1_perangkat",
            "internet_lambat",
            "connect_tapi_tanpa_internet",
            "internet_nyala",
        ],
        "solusi": [
            "Perbarui driver adapter WiFi laptop dari situs resmi pabrikan.",
            "Matikan opsi hemat daya adapter WiFi di pengaturan daya.",
            "Lupakan jaringan lalu sambungkan ulang, coba juga band 5 GHz.",
            "Jalankan reset pengaturan jaringan Windows/macOS.",
        ],
        "kategori_solusi": "masalah_perangkat_klien",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    # --- sinyal_lemah_interferensi -----------------------------------------
    {
        "id": "K14",
        "nama_kasus": "Sinyal lemah di seluruh rumah",
        "gejala": [
            "internet_lambat",
            "sinyal_lemah",
            "semua_perangkat",
            "wlan_nyala",
        ],
        "solusi": [
            "Pindahkan router ke posisi tengah rumah dan tempat yang lebih tinggi.",
            "Jauhkan router dari microwave, telepon tanpa kabel, dan lemari logam.",
            "Ganti channel WiFi ke channel yang tidak padat.",
            "Tambahkan mesh atau repeater untuk area yang jauh dari router.",
            "Sambungkan perangkat tetap (TV, PC) dengan kabel LAN.",
        ],
        "kategori_solusi": "sinyal_lemah_interferensi",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
    {
        "id": "K15",
        "nama_kasus": "Sinyal lemah hanya di kamar belakang",
        "gejala": [
            "internet_lambat",
            "sinyal_lemah",
            "hanya_1_perangkat",
            "putus_nyambung",
            "wlan_nyala",
            "internet_nyala",
        ],
        "solusi": [
            "Dekatkan perangkat ke router saat menguji apakah masalahnya jangkauan.",
            "Gunakan band 5 GHz bila perangkat berada dekat router, 2,4 GHz untuk jarak jauh.",
            "Pasang repeater atau mesh di antara router dan kamar belakang.",
            "Arahkan antena router secara vertikal dan hindari dinding beton tebal.",
        ],
        "kategori_solusi": "sinyal_lemah_interferensi",
        "status": "berhasil",
        "jumlah_dipakai": 1,
        "sumber": "awal",
    },
]

