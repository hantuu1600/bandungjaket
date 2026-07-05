# Task Brief — BandungJaket Customer Segmentation Platform

**Untuk:** Agent Antigravity (Gemini 3.1 Pro)
**Mode yang disarankan:** Agent-assisted / Review-driven (bukan full Autopilot) — proyek ini adalah lampiran skripsi S1, setiap perubahan harus bisa dijelaskan ke penguji.
**Repo:** https://github.com/hantuu1600/bandungjaket.git (branch `main`)

---

## 1. Konteks proyek (baca dulu sebelum mulai)

Ini adalah implementasi web pendukung skripsi S1 tentang segmentasi pelanggan e-commerce menggunakan UMAP + HDBSCAN pada data RFM (Recency, Frequency, Monetary). Ada dua komponen yang **sudah live dan berjalan** — jangan dianggap belum ada:

| Komponen | Status | URL |
|---|---|---|
| Frontend (Astro, static) | ✅ Live | https://bandungjaket.vercel.app/ |
| Backend (FastAPI + model ML) | ✅ Live, tapi *sleeping* (normal, free tier) | https://huggingface.co/spaces/hantuu16/data-bandungjaket |

**Masalah utama yang harus diselesaikan:** frontend dan backend ini belum saling terhubung, dan repo GitHub belum sinkron dengan apa yang live. Tugas kamu adalah menyambungkan keduanya dengan benar, tanpa merusak apa yang sudah bekerja.

---

## 2. Struktur proyek yang sudah ada (JANGAN diasumsikan, ini fakta hasil pengecekan langsung)

```
bandungjaket/
├── src/
│   ├── pages/
│   │   ├── index.astro        # Halaman overview — SUDAH ADA, jangan diubah strukturnya
│   │   ├── dashboard.astro    # Analisis & sebaran segmen — SUDAH ADA
│   │   ├── tentang.astro      # SUDAH ADA
│   │   └── prediksi.astro     # ❌ TIDAK ADA DI REPO — meski live di Vercel menampilkan halaman
│   │                          #    ini ("Simulasi Segmen"). Kemungkinan besar file ini pernah
│   │                          #    dibuat lokal lalu di-deploy manual ke Vercel tanpa di-commit.
│   │                          #    JANGAN asumsikan isinya — buat ulang dari nol sesuai spesifikasi §4.
│   ├── components/
│   │   ├── dashboard/{KpiCards,DonutChart,BarChart,ScatterPlot,SegmentAccordion}.astro
│   │   ├── navigation/{TopNavbar,Sidebar,BottomTabs}.astro
│   │   │     → TopNavbar.astro SUDAH punya link <a href="/prediksi">Prediksi</a>,
│   │   │       jadi begitu file prediksi.astro dibuat, link ini otomatis akan berfungsi.
│   │   └── ui/{StatCard,MetricCard,StepCard}.astro
│   └── data/
│       ├── summary.json    # jangan diubah
│       ├── metrics.json    # jangan diubah
│       ├── scatter.json    # jangan diubah (132KB, data UMAP 2D)
│       └── segments.json   # PENTING — lihat §3, ini sumber kebenaran nama segmen
├── backend/
│   ├── main.py              # FastAPI app — lihat isi lengkap di §5, ada 1 bug kecil yang harus diperbaiki
│   ├── requirements.txt     # fastapi, uvicorn, python-multipart, pydantic, pandas, scikit-learn, umap-learn, hdbscan, joblib
│   ├── Dockerfile           # SUDAH BENAR untuk HF Spaces (port 7860) — JANGAN diubah
│   └── models/
│       ├── scaler.pkl         # PowerTransformer (Yeo-Johnson) — JANGAN diubah/regenerate
│       ├── umap_reducer.pkl   # JANGAN diubah/regenerate
│       └── hdbscan_model.pkl  # JANGAN diubah/regenerate
├── AGENTS.md   # sudah ada tapi isinya masih generic boilerplate Astro, boleh dilengkapi
└── CLAUDE.md   # sama seperti AGENTS.md
```

---

## 3. Sumber kebenaran: mapping cluster_id → nama segmen

Model HDBSCAN yang di-pickle mengembalikan **angka cluster_id (integer)**, bukan nama. Mapping yang SUDAH BENAR dan tervalidasi ada di `src/data/segments.json`:

| cluster_id | Nama segmen |
|---|---|
| 0 | Pelanggan Potensial |
| 1 | Pelanggan Dorman |
| 2 | Pelanggan Unggulan |
| 3 | Pelanggan Aktif |
| 4 | Pelanggan Berisiko Berhenti |
| 5 | Pelanggan Bernilai Terancam |
| **-1** | **Noise / outlier** — HDBSCAN bisa mengembalikan -1 kalau titik data tidak cukup mirip cluster manapun. **Ini BUKAN bug, ini perilaku normal HDBSCAN.** Harus ditangani secara eksplisit di UI (lihat §4), jangan biarkan `undefined`/crash. |

**Aturan wajib:** jangan hardcode ulang nama-nama segmen di tempat lain (misalnya di dalam `prediksi.astro` sebagai string terpisah). Selalu import dan baca dari `src/data/segments.json` supaya hanya ada SATU sumber kebenaran. Kalau nanti model di-retrain dan urutan cluster berubah, cukup update `segments.json` saja.

---

## 4. TASK LIST (kerjakan berurutan, jangan lompat)

### TASK 1 — Perbaiki CORS di backend (prioritas tinggi, low-risk)
File: `backend/main.py`, baris ±18.

Saat ini:
```python
allow_origins=["*"], # TODO: Restrict origins in production
```

Ubah menjadi:
```python
allow_origins=[
    "https://bandungjaket.vercel.app",
    "http://localhost:4321",   # default port dev server Astro
    "http://localhost:4323",   # port yang disebut di komentar asli, pertahankan untuk kompatibilitas
],
```
**Verifikasi:** setelah deploy ulang ke HF Space, pastikan request dari `https://bandungjaket.vercel.app` tetap berhasil (cek header `Access-Control-Allow-Origin` di response, atau test langsung dari browser console di halaman live).

---

### TASK 2 — Konfirmasi URL publik HF Space (WAJIB sebelum Task 3)
**Jangan menebak URL ini.** Cara memastikan:
1. Buka https://huggingface.co/spaces/hantuu16/data-bandungjaket
2. Klik tombol "Embed this Space" atau lihat address bar saat membuka tab "App" — salin URL persisnya (formatnya kemungkinan `https://hantuu16-data-bandungjaket.hf.space` tapi HARUS diverifikasi, jangan diasumsikan).
3. Test dengan `curl <URL>/` — harus mengembalikan JSON `{"message": "API Segmentasi BandungJaket Aktif!", ...}`. Kalau Space sedang sleeping, request pertama akan lambat (~30-60 detik) sebelum merespons — ini normal, jangan dianggap error dan jangan retry berlebihan dalam waktu singkat.
4. Simpan URL ini sebagai environment variable, JANGAN hardcode langsung di kode.

---

### TASK 3 — Buat halaman `src/pages/prediksi.astro`

**Spesifikasi fungsional:**
- Judul halaman: "Simulasi Segmen" (sesuai apa yang sudah live, agar konsisten dengan yang pernah ada)
- Gunakan layout yang sama dengan `dashboard.astro` (cek `src/layouts/` dan ikuti pola import yang sama — jangan buat layout baru)
- Form input dengan 3 field:
  - `recency` (integer, hari sejak transaksi terakhir) — beri label & placeholder yang jelas dalam Bahasa Indonesia
  - `frequency` (integer, jumlah transaksi)
  - `monetary` (float/number, total belanja dalam Rupiah)
- Validasi input di sisi client SEBELUM submit: semua field wajib diisi, harus angka positif. Jangan kirim request kalau validasi gagal.
- Saat submit: `POST {API_BASE_URL}/api/predict` dengan body JSON:
  ```json
  { "recency": <int>, "frequency": <int>, "monetary": <float> }
  ```
  Perhatikan: `recency` dan `frequency` harus dikirim sebagai integer, `monetary` sebagai number — backend pakai Pydantic dan akan menolak (`422 Unprocessable Entity`) kalau tipe salah (misalnya string kosong).
- **State loading wajib ada**, dengan pesan spesifik: *"Menghubungi server model... (jika baru pertama kali, ini bisa memakan waktu hingga 1 menit)"* — supaya pengguna tidak mengira aplikasi hang saat cold start HF Space.
- **Response handling:**
  - Ambil `cluster_id` dari response.
  - Cari entry dengan `id === cluster_id` di `src/data/segments.json` (import langsung, sudah bundled statis di frontend, tidak perlu fetch terpisah).
  - **Kalau `cluster_id === -1` ATAU tidak ditemukan entry yang cocok:** tampilkan pesan ramah, BUKAN error teknis. Contoh: *"Pola belanja ini belum cocok dengan segmen manapun yang teridentifikasi. Coba dengan nilai RFM yang lain."* Jangan biarkan halaman menampilkan `undefined` atau crash.
  - Kalau ditemukan: tampilkan `name`, `description`, dan `recommendations` (array) dari segments.json, plus badge warna sesuai field `badge`/`color_dot` supaya konsisten visual dengan `dashboard.astro`.
- **Error handling jaringan:** kalau fetch gagal total (network error, timeout, 500) — tampilkan pesan yang membedakan dua kemungkinan: (a) server sedang bangun dari sleep, sarankan coba lagi dalam 1 menit, (b) error lain, tampilkan pesan generik tanpa membocorkan stack trace ke pengguna.
- Reuse komponen UI yang ada (`StatCard`, `MetricCard`) untuk konsistensi visual — jangan membuat gaya/komponen baru dari nol.

---

### TASK 4 — Environment variable untuk API URL
Jangan hardcode URL HF Space langsung di dalam `.astro` file. Gunakan mekanisme environment variable Astro:
- Buat/update `.env` (dan `.env.example` untuk referensi, TANPA nilai asli di `.env.example` — isi dengan placeholder) dengan:
  ```
  PUBLIC_API_BASE_URL=https://<url-hasil-verifikasi-task-2>
  ```
- Akses di `prediksi.astro` lewat `import.meta.env.PUBLIC_API_BASE_URL`.
- Pastikan variable ini juga diset di Vercel project settings (kalau Antigravity punya akses; kalau tidak, tuliskan instruksi manual yang jelas untuk pengguna di akhir laporan pekerjaan).

---

### TASK 5 (opsional, prioritas rendah) — Endpoint tambahan di backend
Hanya kerjakan setelah Task 1-4 selesai dan diverifikasi. Tambahkan di `backend/main.py`:
```python
@app.get("/api/model-info")
def model_info():
    return {
        "r_mid_recency": 1481,
        "f_p75_frequency": 3,
        "m_p75_monetary": 233238,
        "n_clusters": 6,
        "algorithm": "UMAP + HDBSCAN (2-layer: repeat buyers only)"
    }
```
**Jangan** menambahkan endpoint yang di luar cakupan skripsi (lihat §6 — larangan eksplisit). Endpoint ini murni informatif, tidak mengubah pipeline prediksi yang sudah ada.

---

### TASK 6 — Sinkronisasi repo
Setelah semua di atas selesai dan **lolos verifikasi end-to-end** (lihat §7):
1. `git add` semua file yang berubah/baru (`src/pages/prediksi.astro`, `backend/main.py`, `.env.example`, dll — JANGAN commit `.env` asli berisi URL kalau dianggap sensitif, meski URL HF Space publik biasanya tidak masalah).
2. Commit dengan pesan yang jelas dan deskriptif, contoh: `feat: hubungkan halaman prediksi ke backend API, perbaiki CORS`.
3. Push ke `main` di https://github.com/hantuu1600/bandungjaket.git.
4. Tujuan akhir: **repo GitHub, live Vercel, dan live HF Space harus 100% konsisten** — tidak ada lagi file yang ada di live tapi tidak ada di repo.

---

## 5. Isi lengkap `backend/main.py` saat ini (referensi, jangan menebak isi file)

Baca langsung dari `backend/main.py` di repo hasil clone. Poin-poin yang PERLU diperhatikan:
- Endpoint `/api/predict` HANYA mengembalikan `{status, cluster_id, umap_x, umap_y}` — TIDAK ada nama segmen di response. Ini bukan bug yang perlu diperbaiki di backend; mapping nama segmen memang sengaja dilakukan di frontend (§3-4).
- Ada `@app.on_event("startup")` yang me-load 3 file model. Kalau load gagal, error message disimpan di `load_error_msg` dan bisa dilihat lewat `GET /`. Kalau saat verifikasi kamu menemukan `load_error_msg` tidak `null`, JANGAN mencoba memperbaiki file `.pkl` — laporkan ke pengguna, karena itu di luar scope tugas ini (kemungkinan besar masalah versi library, bukan file model yang rusak).
- `hdbscan.approximate_predict()` butuh model HDBSCAN yang dilatih dengan `prediction_data=True` — kalau ada error terkait ini saat testing, itu artinya `hdbscan_model.pkl` perlu di-regenerate dari notebook aslinya (di luar scope Antigravity, harus dikerjakan manual oleh mahasiswa di notebook Kaggle-nya, JANGAN mencoba regenerate model dari sini).

---

## 6. Larangan eksplisit (guardrails) — WAJIB DIPATUHI

Proyek ini adalah lampiran skripsi dengan **Batasan Masalah** yang sudah ditetapkan dan tidak boleh dilampaui tanpa persetujuan pembimbing. Jangan menambahkan:
- ❌ Fitur prediksi penjualan masa depan / forecasting
- ❌ Analisis kepuasan pelanggan
- ❌ Field data demografis atau psikografis pelanggan
- ❌ Sistem login/autentikasi pengguna (tidak diminta, di luar scope)
- ❌ Perubahan pada `backend/models/*.pkl` — file-file ini adalah hasil training resmi yang dirujuk di Bab IV skripsi; regenerasi model HANYA boleh dilakukan manual oleh mahasiswa dari notebook aslinya
- ❌ Perubahan pada `backend/Dockerfile` (port 7860 wajib untuk HF Spaces, sudah benar)
- ❌ Perubahan pada isi `src/data/*.json` — ini adalah hasil ekspor resmi dari notebook, mengubahnya berarti dashboard tidak lagi mencerminkan hasil penelitian yang sebenarnya
- ❌ Mengganti library/dependency yang sudah ada di `requirements.txt` atau `package.json` tanpa alasan kuat dan tanpa melaporkannya secara eksplisit

Kalau menemukan hal yang tampak seperti bug tapi di luar daftar task di atas, **laporkan dulu ke pengguna, jangan langsung memperbaiki sendiri.**

---

## 7. Verifikasi wajib sebelum menyatakan tugas selesai

Antigravity punya akses browser — gunakan untuk verifikasi nyata, bukan asumsi:
1. Jalankan dev server lokal (`astro dev --background`, sesuai `AGENTS.md`).
2. Buka `/prediksi` di browser terintegrasi.
3. Isi form dengan minimal 3 skenario:
   - Nilai yang kemungkinan menghasilkan cluster valid (contoh: recency=600, frequency=5, monetary=475000 — mendekati profil "Pelanggan Unggulan")
   - Nilai ekstrem yang berpotensi menghasilkan `cluster_id = -1` (contoh: recency=50, frequency=1, monetary=1000000)
   - Input kosong/invalid — pastikan validasi client-side mencegah submit
4. Screenshot hasil tiap skenario sebagai artifact.
5. Konfirmasi tidak ada error di browser console.
6. Baru setelah semua ini lolos, lanjut ke Task 6 (commit & push).

---

## 8. Ringkasan prioritas

1. Task 1 (CORS) — cepat, low-risk, kerjakan duluan
2. Task 2 (verifikasi URL HF Space) — wajib sebelum lanjut, jangan ditebak
3. Task 3 + 4 (halaman prediksi + env var) — inti pekerjaan
4. Verifikasi (§7) — jangan dilewati
5. Task 6 (commit & push)
6. Task 5 (endpoint tambahan) — opsional, hanya jika waktu masih ada
