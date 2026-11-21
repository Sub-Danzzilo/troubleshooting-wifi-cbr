"""Lima skenario uji baru untuk menguji retrieval (bukan kasus di CASE_BASE_AWAL).

Setiap skenario memakai kombinasi gejala yang berbeda dari kasus awal, tetapi
kategori yang diharapkan tetap jelas. Komentar menjelaskan alasan ground truth.
"""

SKENARIO_UJI = [
    {
        "id": "S1",
        "deskripsi": "Kabel fiber terganggu, semua perangkat tidak bisa internet",
        "gejala": [
            "tidak_connect",
            "semua_perangkat",
            "internet_mati_total",
            "los_merah",
            "pon_mati",
        ],
        # LOS merah dan PON mati menandakan gangguan jalur optik.
        "kategori_diharapkan": "kabel_optik_bermasalah",
    },
    {
        "id": "S2",
        "deskripsi": "Router tidak menyala setelah listrik padam",
        "gejala": [
            "tidak_connect",
            "semua_perangkat",
            "wifi_tidak_muncul",
            "power_mati",
        ],
        # Lampu POWER mati dan WiFi hilang mengarah ke masalah daya router.
        "kategori_diharapkan": "router_mati_daya",
    },
    {
        "id": "S3",
        "deskripsi": "Lampu PON normal tetapi tidak ada akses internet sama sekali",
        "gejala": [
            "connect_tapi_tanpa_internet",
            "semua_perangkat",
            "internet_mati_total",
            "pon_nyala",
            "internet_mati",
        ],
        # Jaringan optik normal (PON nyala, LOS mati) tetapi layanan internet mati.
        "kategori_diharapkan": "gangguan_isp",
    },
    {
        "id": "S4",
        "deskripsi": "Nama WiFi hilang karena lampu WLAN mati",
        "gejala": [
            "wifi_tidak_muncul",
            "semua_perangkat",
            "wlan_mati",
            "power_nyala",
        ],
        # Router menyala normal, hanya modul WLAN yang tidak aktif.
        "kategori_diharapkan": "wlan_nonaktif",
    },
    {
        "id": "S5",
        "deskripsi": "Password WiFi ditolak di semua perangkat setelah diganti",
        "gejala": [
            "tidak_connect",
            "password_ditolak",
            "semua_perangkat",
            "wlan_nyala",
            "power_nyala",
        ],
        # Pesan password salah muncul padahal WLAN dan POWER menyala normal.
        "kategori_diharapkan": "password_salah",
    },
]
