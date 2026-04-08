# 🎴 Pokemon Stock Bot — KlikIndomaret

Bot Python untuk **mengecek stok Pokémon Card** di seluruh toko Indomaret Xpress secara otomatis via API KlikIndomaret.

---

## ✨ Fitur

- 🔍 **Cari Manual** — Cek stok berdasarkan nama kota/kecamatan yang kamu ketik sendiri
- 🚀 **Auto-Scan Wilayah** — Scan semua kecamatan di satu kota secara otomatis (Provinsi → Kota → Semua Kecamatan)
- 🛡️ **Anti Rate Limit** — Delay otomatis antar request untuk menghindari Cloudflare block
- 🔄 **Token Refresh** — Minta token baru otomatis jika token expired (401/403)
- 💾 **Simpan Hasil** — Hasil scan disimpan ke file `.txt` secara otomatis
- 🎨 **Tampilan Rich Terminal** — Output berwarna dan rapi menggunakan library `rich`

---

## 📋 Persyaratan

- Python **3.9+**
- Akun **KlikIndomaret** yang sudah login
- Browser (Chrome/Edge) untuk mengambil token

---

## ⚙️ Instalasi

### 1. Clone / Download Proyek

```bash
git clone https://github.com/onesyah05/domartCek.git
cd domartCek/pokemon-stock-bot
```

### 2. Buat Virtual Environment (Opsional tapi Disarankan)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

Paket yang akan diinstall:
| Paket | Fungsi |
|---|---|
| `curl_cffi` | HTTP request dengan impersonasi Chrome (bypass Cloudflare) |
| `rich` | Tampilan terminal berwarna |
| `python-dotenv` | Membaca file `.env` |
| `questionary` | Menu interaktif di terminal |
| `asyncio` | Async/await (built-in Python) |

---

## 🔑 Cara Mendapatkan Token

Bot ini memerlukan **2 token** yang diambil dari browser saat kamu login ke KlikIndomaret:

### Langkah-langkah:

1. Buka browser Chrome/Edge, lalu buka **https://www.klikindomaret.com**
2. Login dengan akun kamu
3. Tekan **F12** untuk membuka DevTools → pilih tab **Network**
4. Refresh halaman atau lakukan aktivitas apa saja (misal: klik produk)
5. Di kolom filter Network, ketik `api` atau `cart`
6. Klik salah satu request, lalu buka tab **Headers**
7. Salin nilai dari:
   - **`Authorization`** → ambil bagian setelah kata `Bearer ` → ini adalah **JWT Token** (diawali `eyJ...`)
   - **`x-aws-waf-token`** → ini adalah **AWS WAF Token**

> ⚠️ **Token bersifat sementara** dan akan expired dalam ~1 jam. Jika bot mendeteksi error 401/403, kamu akan diminta memasukkan token baru.

---

## 🚀 Cara Menjalankan Bot

```bash
python main.py
```

### Langkah 1 — Masukkan Token

Saat pertama kali dijalankan, bot akan meminta token:

```
--- UPDATE TOKEN MANUAL ---
Silakan ambil token dari browser (DevTools -> Network -> cari request apa saja).

Masukkan JWT Token (berawalan 'ey...'): eyJ0eXAiOiJKV1Qi...
Masukkan AWS WAF Token: 93bd1439-6b05-424e...
```

### Langkah 2 — Pilih Menu

Setelah token dimasukkan, akan muncul menu utama:

```
┌─────────────────────────────────────────────┐
│         Pokemon Stock Checker Bot           │
├─────────────────────────────────────────────┤
│  > Cari Berdasarkan Nama (Manual)           │
│    Auto-Scan Wilayah (Pilih Provinsi → ...) │
│    Keluar                                   │
└─────────────────────────────────────────────┘
```

---

## 📖 Panduan Penggunaan

### 🔍 Mode 1: Cari Berdasarkan Nama (Manual)

Gunakan mode ini untuk cek stok di satu kecamatan/kota tertentu.

1. Pilih **"Cari Berdasarkan Nama (Manual)"**
2. Ketik nama kota atau kecamatan, contoh: `Kemayoran`, `Gambir`, `Bekasi`
3. Bot akan mencari semua toko Indomaret Xpress di area tersebut
4. Setiap toko akan dicek stoknya satu per satu
5. Hasil akan ditampilkan dan disimpan ke file `.txt` di folder `hasil/`

**Contoh output:**
```
✅ Toko: KEMAYORAN 1 (Jl. Bungur Besar No. 71)
  📦 Pokemon Booster Pack Sv2d Letusan Tanah  → Ready (Stok: 3)
  📦 Pokemon Booster Pack Sv3s Kilau Hitam    → Habis
  📦 Pokemon Set Special Kilat Rasi Sv8s 2's  → Ready (Stok: 1)
```

---

### 🚀 Mode 2: Auto-Scan Wilayah

Gunakan mode ini untuk scan **seluruh kecamatan** dalam satu kota secara otomatis.

1. Pilih **"Auto-Scan Wilayah (Pilih Provinsi → Kota → Semua Kecamatan)"**
2. Pilih **Provinsi** dari daftar yang muncul
3. Pilih **Kota/Kabupaten**
4. Bot akan otomatis scan **semua kecamatan** di kota tersebut
5. Setiap kecamatan diberi delay **5 detik** untuk keamanan
6. Semua hasil disimpan ke file terpisah di folder `hasil/`

> ⏱️ **Perkiraan waktu:** 1 kota dengan ~10 kecamatan ≈ 5-15 menit (tergantung jumlah toko per kecamatan)

---

## ⚙️ Konfigurasi `config.py`

Kamu bisa mengubah daftar produk yang dicek di file `config.py`:

```python
POKEMON_PLUS = [
    "20129926", # Pokemon Booster Pack Sv2d Letusan Tanah
    "20129925", # Pokemon Booster Pack Sv1a Hantaman Triplet
    "20129927", # Pokemon Booster Pack Sv2p Mara Bahaya Salju
    # ... tambahkan PLU produk lainnya di sini
]
```

**Cara menambah produk baru:**
1. Buka KlikIndomaret di browser
2. Cari produk Pokémon yang ingin dilacak
3. Ambil kode PLU dari URL atau Network request
4. Tambahkan ke list `POKEMON_PLUS` di `config.py`

---

## 📁 Struktur Proyek

```
pokemon-stock-bot/
│
├── main.py              # File utama, entry point bot
├── config.py            # Konfigurasi: daftar PLU produk & API constants
├── requirements.txt     # Daftar dependensi Python
├── .env.example         # Contoh file environment variable
│
├── api/
│   ├── stock.py         # Fungsi cek stok via API add-to-cart
│   ├── cart.py          # Fungsi set mode pickup ke toko tertentu
│   ├── store.py         # Fungsi cari toko terdekat berdasarkan keyword
│   └── coverage.py      # Fungsi ambil data provinsi, kota, kecamatan
│
├── utils/
│   ├── display.py       # Tampilan terminal (banner, tabel, menu)
│   ├── headers.py       # Helper untuk membuat HTTP headers
│   └── output.py        # Fungsi simpan hasil ke file .txt
│
└── hasil/               # Folder output hasil scan (dibuat otomatis)
```

---

## ❓ Troubleshooting

| Masalah | Solusi |
|---|---|
| `Token expired atau diblokir WAF` | Ambil token baru dari browser, masukkan saat diminta |
| `Error 429 — Rate Limited` | Bot akan otomatis tunggu 10 detik, lalu lanjut |
| `Tidak ada toko ditemukan` | Coba kata kunci yang lebih spesifik, misal nama kecamatan |
| `ModuleNotFoundError` | Jalankan `pip install -r requirements.txt` |
| `RuntimeWarning event loop` | Sudah diatasi otomatis, abaikan pesan ini |

---

## ⚠️ Disclaimer

> Bot ini dibuat untuk **keperluan pribadi** dalam memantau stok Pokémon Card di toko fisik Indomaret.
> Penggunaan berlebihan dapat menyebabkan akun diblokir sementara oleh sistem Cloudflare.
> Gunakan dengan bijak dan bertanggung jawab.

---

## 📄 Lisensi

MIT License — bebas digunakan dan dimodifikasi untuk keperluan pribadi.
