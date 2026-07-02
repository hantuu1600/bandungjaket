# PRD: Website Segmentasi Pelanggan bandungjaket.com

**Versi**: 1.0 | **Stack**: Astro + DaisyUI + Tailwind CSS + TypeScript + Chart.js  
**Scope**: Build frontend 4 halaman — koneksi API backend belum termasuk

---

## PENTING: Yang Dikerjakan vs Tidak

### KERJAKAN
- Setup project structure lengkap
- 4 halaman: Overview (`/`), Dashboard (`/dashboard`), Prediksi (`/prediksi`), Tentang (`/tentang`)
- Semua komponen reusable sesuai spesifikasi di bawah
- Responsif: desktop (≥1024px) dan mobile (<1024px)
- Data dari file JSON statis — tidak ada fetch ke API manapun

### JANGAN DIKERJAKAN
- Koneksi ke FastAPI backend apapun
- Logic ML inference
- Scatter plot UMAP sungguhan — buat placeholder saja
- Handler upload CSV — buat UI-nya saja
- Submit prediksi yang benar-benar bekerja — tombol harus dalam state disabled

---

## TECH STACK (EXACT)

```
astro: ^4.x
@astrojs/tailwind: latest
daisyui: ^4.x
tailwindcss: ^3.x
typescript: strict mode
chart.js: ^4.x (via npm, bukan CDN)
```

Tidak perlu React, Vue, atau framework UI lainnya.  
Chart.js digunakan langsung via `<script>` tag dalam file `.astro`.

---

## STRUKTUR FOLDER

```
src/
├── data/
│   ├── segments.json
│   ├── summary.json
│   └── metrics.json
├── types/
│   └── index.ts
├── layouts/
│   ├── BaseLayout.astro       ← Untuk Dashboard, Prediksi, Tentang
│   └── LandingLayout.astro    ← Untuk Overview saja
├── components/
│   ├── ui/
│   │   ├── StatCard.astro
│   │   ├── MetricCard.astro
│   │   ├── SegmentBadge.astro
│   │   └── StepCard.astro
│   ├── navigation/
│   │   ├── Sidebar.astro
│   │   ├── TopNavbar.astro
│   │   └── BottomTabs.astro
│   ├── dashboard/
│   │   ├── KpiCards.astro
│   │   ├── SegmentAccordion.astro
│   │   ├── BarChart.astro
│   │   ├── DonutChart.astro
│   │   └── ScatterPlotPlaceholder.astro
│   ├── prediksi/
│   │   ├── InputForm.astro
│   │   ├── ResultCard.astro
│   │   └── CsvUpload.astro
│   └── tentang/
│       ├── MethodologySteps.astro
│       ├── EvaluationMetrics.astro
│       └── References.astro
└── pages/
    ├── index.astro
    ├── dashboard.astro
    ├── prediksi.astro
    └── tentang.astro
```

---

## DESIGN SYSTEM

### tailwind.config.mjs

```js
import daisyui from 'daisyui'

export default {
  content: ['./src/**/*.{astro,html,js,ts,jsx,tsx}'],
  plugins: [daisyui],
  daisyui: {
    themes: [
      {
        bandungjaket: {
          "primary":   "#1a1a1a",
          "secondary": "#374151",
          "accent":    "#f97316",
          "neutral":   "#6b7280",
          "base-100":  "#ffffff",
          "base-200":  "#f9fafb",
          "base-300":  "#f3f4f6",
          "info":      "#3b82f6",
          "success":   "#10b981",
          "warning":   "#f59e0b",
          "error":     "#ef4444",
        }
      }
    ],
    defaultTheme: "bandungjaket",
    logs: false,
  }
}
```

### Segment Color Mapping (gunakan KONSISTEN di semua halaman)

| Segmen                      | Badge DaisyUI   | Warna dot  |
|-----------------------------|-----------------|------------|
| Pelanggan Unggulan          | `badge-warning` | `#f59e0b`  |
| Pelanggan Dorman            | `badge-neutral` | `#6b7280`  |
| Pelanggan Aktif             | `badge-success` | `#10b981`  |
| Pelanggan Potensial         | `badge-info`    | `#3b82f6`  |
| Pelanggan Berisiko Berhenti | `badge-warning` | `#f97316`  |
| Pelanggan Bernilai Terancam | `badge-error`   | `#ef4444`  |

### Typography
- Hero headline: `text-3xl md:text-4xl font-bold`
- Section heading: `text-xl font-semibold`
- Card label muted: `text-sm text-base-content/60`
- Body text: `text-base text-base-content`
- Number large: `text-2xl md:text-3xl font-bold`

---

## DATA FILES — BUAT PERSIS INI

### src/data/segments.json

```json
{
  "segments": [
    {
      "id": 0,
      "name": "Pelanggan Unggulan",
      "count": 1259,
      "recency": 620,
      "frequency": 5,
      "monetary": 475691,
      "badge": "warning",
      "color_dot": "#f59e0b",
      "description": "Pelanggan paling aktif dan bernilai tinggi. Baru bertransaksi, sering belanja, dan total belanja terbesar.",
      "recommendations": [
        "Berikan loyalty reward atau voucher eksklusif",
        "Tawarkan produk premium atau bundle spesial",
        "Ajak bergabung ke referral program"
      ]
    },
    {
      "id": 1,
      "name": "Pelanggan Dorman",
      "count": 20780,
      "recency": 1567,
      "frequency": 2,
      "monetary": 116051,
      "badge": "neutral",
      "color_dot": "#6b7280",
      "description": "Kelompok terbesar repeat buyer. Sudah lama tidak bertransaksi dengan frekuensi rendah.",
      "recommendations": [
        "Kirim kampanye reaktivasi via Shopee Broadcast",
        "Tawarkan gratis ongkir atau diskon comeback",
        "Fokus pada produk terlaris sebagai daya tarik"
      ]
    },
    {
      "id": 2,
      "name": "Pelanggan Aktif",
      "count": 1400,
      "recency": 688,
      "frequency": 3,
      "monetary": 185045,
      "badge": "success",
      "color_dot": "#10b981",
      "description": "Pelanggan yang masih aktif dengan frekuensi dan nilai belanja yang cukup baik.",
      "recommendations": [
        "Pertahankan dengan flash sale dan notifikasi produk baru",
        "Dorong upsell ke produk kategori lebih tinggi",
        "Cross-sell untuk menaikkan nilai per transaksi"
      ]
    },
    {
      "id": 3,
      "name": "Pelanggan Potensial",
      "count": 8319,
      "recency": 703,
      "frequency": 2,
      "monetary": 118391,
      "badge": "info",
      "color_dot": "#3b82f6",
      "description": "Baru mulai bertransaksi ulang. Berpotensi menjadi pelanggan aktif dengan dorongan yang tepat.",
      "recommendations": [
        "Kirim penawaran follow-up setelah pembelian kedua",
        "Voucher untuk mendorong pembelian ketiga",
        "Tampilkan produk serupa berdasarkan riwayat pembelian"
      ]
    },
    {
      "id": 4,
      "name": "Pelanggan Berisiko Berhenti",
      "count": 5007,
      "recency": 1563,
      "frequency": 3,
      "monetary": 199245,
      "badge": "warning",
      "color_dot": "#f97316",
      "description": "Dulunya cukup aktif namun sudah lama tidak bertransaksi. Perlu intervensi segera.",
      "recommendations": [
        "Kampanye win-back dengan penawaran terbatas waktu",
        "Hubungi personal via Shopee Chat",
        "Diskon khusus berdasarkan produk terakhir dibeli"
      ]
    },
    {
      "id": 5,
      "name": "Pelanggan Bernilai Terancam",
      "count": 5483,
      "recency": 1539,
      "frequency": 5,
      "monetary": 458654,
      "badge": "error",
      "color_dot": "#ef4444",
      "description": "Bernilai sangat tinggi namun sudah lama tidak aktif. Kehilangan segmen ini berdampak besar pada pendapatan.",
      "recommendations": [
        "Prioritas tertinggi — hubungi langsung via Shopee Chat",
        "Penawaran eksklusif: diskon besar atau bundle premium",
        "Jadwalkan follow-up dalam 7 hari"
      ]
    }
  ]
}
```

### src/data/summary.json

```json
{
  "total_customers": 390167,
  "valid_transactions": 481682,
  "repeat_buyers": 42248,
  "one_time_buyers": 347919,
  "one_time_ratio": 89.2,
  "raw_data_rows": 742182,
  "period_start": "September 2020",
  "period_end": "Oktober 2025",
  "reference_date": "16 Oktober 2025",
  "platform": "Shopee",
  "store": "bandungjaket.com"
}
```

### src/data/metrics.json

```json
{
  "layer1": {
    "label": "Populasi Penuh",
    "description": "Seluruh 390.167 pelanggan unik",
    "n_clusters": 8,
    "noise_pct": 2.4,
    "dbcv": 0.0111,
    "silhouette_umap": -0.1878,
    "silhouette_rfm": -0.4587,
    "cluster_stability": 0.7469
  },
  "layer2": {
    "label": "Repeat Buyer",
    "description": "42.248 pelanggan dengan ≥2 transaksi",
    "n_clusters": 6,
    "noise_pct": 0.0,
    "dbcv": 0.796,
    "silhouette_umap": 0.326,
    "silhouette_rfm": 0.430,
    "cluster_stability": 0.98
  }
}
```

---

## TYPESCRIPT TYPES — src/types/index.ts

```typescript
export interface Segment {
  id: number
  name: string
  count: number
  recency: number
  frequency: number
  monetary: number
  badge: 'warning' | 'neutral' | 'success' | 'info' | 'error'
  color_dot: string
  description: string
  recommendations: string[]
}

export interface Summary {
  total_customers: number
  valid_transactions: number
  repeat_buyers: number
  one_time_buyers: number
  one_time_ratio: number
  raw_data_rows: number
  period_start: string
  period_end: string
  reference_date: string
  platform: string
  store: string
}

export interface LayerMetrics {
  label: string
  description: string
  n_clusters: number
  noise_pct: number
  dbcv: number
  silhouette_umap: number
  silhouette_rfm: number
  cluster_stability: number
}

export interface Metrics {
  layer1: LayerMetrics
  layer2: LayerMetrics
}
```

---

## NAVIGATION — ATURAN PENTING

### Desktop (≥1024px)
- Halaman `/` (Overview): pakai `LandingLayout.astro` → top navbar horizontal
- Halaman `/dashboard`, `/prediksi`, `/tentang`: pakai `BaseLayout.astro` → sidebar kiri 240px fixed, konten kanan mengisi sisa

### Mobile (<1024px)
- Semua halaman: bottom tab bar 4 item, posisi fixed bottom, selalu visible
- Sidebar TIDAK muncul di mobile
- Top area hanya berisi hamburger icon dan logo

### Bottom Tabs (urutan dan route)
```
Tab 1: "Overview"   ikon home      href="/"
Tab 2: "Dashboard"  ikon chart-bar href="/dashboard"
Tab 3: "Prediksi"   ikon cpu       href="/prediksi"
Tab 4: "Tentang"    ikon info      href="/tentang"
```
Tab aktif: `text-primary font-semibold` dengan garis bawah atau dot indikator.

---

## LAYOUTS

### layouts/BaseLayout.astro

```astro
---
interface Props {
  title: string
  activePage: 'dashboard' | 'prediksi' | 'tentang'
}
const { title, activePage } = Astro.props
---
<html lang="id" data-theme="bandungjaket">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — bandungjaket.com Segmentasi</title>
</head>
<body class="bg-base-200 min-h-screen">
  <div class="flex min-h-screen">
    <!-- Sidebar: visible desktop, hidden mobile -->
    <aside class="hidden lg:flex lg:flex-col lg:w-60 lg:min-h-screen bg-base-100 border-r border-base-300">
      <Sidebar activePage={activePage} />
    </aside>

    <!-- Konten utama -->
    <main class="flex-1 p-4 lg:p-8 pb-24 lg:pb-8 max-w-6xl">
      <slot />
    </main>
  </div>

  <!-- Bottom tabs: visible mobile, hidden desktop -->
  <nav class="lg:hidden fixed bottom-0 left-0 right-0 z-50 bg-base-100 border-t border-base-300 h-16 flex items-center">
    <BottomTabs activePage={activePage} />
  </nav>
</body>
</html>
```

### layouts/LandingLayout.astro

```astro
---
interface Props { title: string }
const { title } = Astro.props
---
<html lang="id" data-theme="bandungjaket">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} — bandungjaket.com Segmentasi</title>
</head>
<body class="bg-base-100">
  <TopNavbar />
  <main>
    <slot />
  </main>
</body>
</html>
```

---

## KOMPONEN

### components/navigation/Sidebar.astro

```
Props: { activePage: string }
DaisyUI: ul.menu.bg-base-100.w-60.min-h-screen.p-4

Struktur:
  Logo area (div.mb-6.px-2):
    p.text-xs.text-base-content/50  "bandungjaket.com"
    p.text-sm.font-semibold         "Segmentasi Pelanggan"

  ul.menu:
    li > a[href="/dashboard"]   kelas aktif jika activePage==="dashboard"   "Dashboard"
    li > a[href="/prediksi"]    kelas aktif jika activePage==="prediksi"    "Prediksi"
    li > a[href="/tentang"]     kelas aktif jika activePage==="tentang"     "Tentang"

  Link aktif: tambahkan class "active" pada <a> (DaisyUI menu active = bg-primary text-primary-content)
```

### components/navigation/BottomTabs.astro

```
Props: { activePage: string }
Render: div.flex.w-full

4 item (flex-1 each), setiap item:
  <a href="{route}" class="flex flex-col items-center justify-center gap-1 flex-1 py-2
     {isActive ? 'text-primary font-semibold' : 'text-base-content/50'}">
    <span class="text-xl">{icon}</span>
    <span class="text-[10px]">{label}</span>
  </a>

Items:
  href="/"           label="Overview"   icon pakai SVG atau unicode
  href="/dashboard"  label="Dashboard"
  href="/prediksi"   label="Prediksi"
  href="/tentang"    label="Tentang"
```

### components/navigation/TopNavbar.astro

```
DaisyUI: navbar.bg-base-100.border-b.border-base-300.sticky.top-0.z-50

Left: logo text "bandungjaket.com" + label kecil "Segmentasi Pelanggan"
Right (desktop): nav links → Overview (active, font-bold underline) | Dashboard | Prediksi | Tentang
Right (mobile): hamburger button (tidak perlu fungsional — cukup render ikonnya)
```

### components/ui/StatCard.astro

```
Props: { label: string, value: string, subtitle?: string }

<div class="card card-bordered bg-base-100 shadow-sm">
  <div class="card-body p-4 gap-1">
    <p class="text-sm text-base-content/60">{label}</p>
    <p class="text-2xl font-bold text-primary">{value}</p>
    {subtitle && <p class="text-xs text-base-content/40">{subtitle}</p>}
  </div>
</div>
```

### components/ui/MetricCard.astro

```
Props: { label: string, value: string, description: string, highlight?: boolean }

<div class="card bg-base-100 border {highlight ? 'border-primary border-2' : 'border-base-300'}">
  <div class="card-body p-4 gap-1">
    <p class="text-xs text-base-content/60 uppercase tracking-wide">{label}</p>
    <p class="text-3xl font-bold {highlight ? 'text-primary' : 'text-base-content'}">{value}</p>
    <p class="text-xs text-base-content/50">{description}</p>
  </div>
</div>
```

### components/ui/StepCard.astro

```
Props: { step: number, title: string, description: string }

<div class="card bg-base-100 border border-base-300">
  <div class="card-body p-4 gap-2">
    <span class="text-xs text-base-content/40 font-medium">Tahap {step}</span>
    <h3 class="font-semibold text-sm">{title}</h3>
    <p class="text-xs text-base-content/60">{description}</p>
  </div>
</div>
```

### components/dashboard/KpiCards.astro

```
Import summary.json.
Render 3 StatCard dalam grid:
  class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8"

Card 1: label="Total Pelanggan"          value="390.167"   subtitle="Pelanggan unik Sep 2020 – Okt 2025"
Card 2: label="Repeat Buyer"             value="42.248"    subtitle="10,8% dari total pelanggan"
Card 3: label="Kualitas Model (DBCV)"    value="0.796"     subtitle="Layer 2 — 1.0 = sempurna"
```

### components/dashboard/SegmentAccordion.astro

```
Import segments.json.
DaisyUI: table.table.table-zebra dalam div.overflow-x-auto.rounded-lg.border.border-base-300

THEAD columns:
  Segmen | Jumlah | Recency (hari) | Frequency | Monetary (Rp) | [Rekomendasi — hidden di mobile]

TBODY:
  Setiap segment dirender dengan <details> HTML native:
  
  Baris utama (<summary> sebagai baris):
    - Colored circle dot (background: color_dot, diameter 10px)
    - Nama segmen + badge DaisyUI sesuai badge field
    - Jumlah: count.toLocaleString('id-ID')
    - Recency: recency + " hari"
    - Frequency: frequency + "×"
    - Monetary: "Rp " + monetary.toLocaleString('id-ID')
    - Kolom rekomendasi: hidden di mobile (class="hidden lg:table-cell")

  Baris detail (saat expanded):
    <tr class="bg-base-200">
      <td colspan="6" class="p-4">
        <p class="text-sm mb-2">{description}</p>
        <ul class="list-disc list-inside text-sm text-base-content/70 space-y-1">
          {recommendations.map(r => <li>{r}</li>)}
        </ul>
      </td>
    </tr>

DEFAULT STATE: segment id=5 (Pelanggan Bernilai Terancam) harus open by default.
Gunakan atribut `open` pada <details> untuk segment id=5.
```

### components/dashboard/BarChart.astro

```
Render canvas + script Chart.js.

<div class="card bg-base-100 border border-base-300">
  <div class="card-body p-4">
    <h3 class="font-semibold text-sm mb-3">Distribusi Segmen Pelanggan</h3>
    <canvas id="barChart" height="200"></canvas>
  </div>
</div>

<script>
  import { Chart } from 'chart.js/auto'
  import segmentsData from '../data/segments.json'

  const segments = segmentsData.segments
  new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
      labels: segments.map(s => s.name.replace('Pelanggan ', '')),
      datasets: [{
        label: 'Jumlah Pelanggan',
        data: segments.map(s => s.count),
        backgroundColor: segments.map(s => s.color_dot + 'CC'),
        borderColor: segments.map(s => s.color_dot),
        borderWidth: 1,
        borderRadius: 4,
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { y: { beginAtZero: true } }
    }
  })
</script>
```

### components/dashboard/DonutChart.astro

```
<div class="card bg-base-100 border border-base-300">
  <div class="card-body p-4">
    <h3 class="font-semibold text-sm mb-3">Proporsi Segmen</h3>
    <canvas id="donutChart" height="200"></canvas>
  </div>
</div>

<script>
  import { Chart } from 'chart.js/auto'
  import segmentsData from '../data/segments.json'

  const segments = segmentsData.segments
  new Chart(document.getElementById('donutChart'), {
    type: 'doughnut',
    data: {
      labels: segments.map(s => s.name.replace('Pelanggan ', '')),
      datasets: [{
        data: segments.map(s => s.count),
        backgroundColor: segments.map(s => s.color_dot + 'CC'),
        borderColor: segments.map(s => s.color_dot),
        borderWidth: 1,
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } }
      }
    }
  })
</script>
```

### components/dashboard/ScatterPlotPlaceholder.astro

```
BUKAN scatter plot sungguhan. Render placeholder informatif.

<div class="card bg-base-100 border border-base-300">
  <div class="card-body p-4">
    <h3 class="font-semibold text-sm mb-3">Visualisasi Klaster (UMAP 2D)</h3>
    <div class="border-2 border-dashed border-base-300 rounded-lg h-64
                flex flex-col items-center justify-center gap-3">
      <div class="loading loading-spinner loading-md text-base-content/20"></div>
      <p class="text-sm text-base-content/40">Visualisasi UMAP</p>
      <p class="text-xs text-base-content/30">
        Data koordinat akan tersedia setelah ekspor model selesai
      </p>
    </div>
  </div>
</div>
```

### components/prediksi/InputForm.astro

```
<div class="card bg-base-100 border border-base-300">
  <div class="card-body p-6">
    <h3 class="font-semibold mb-4">Data Pelanggan</h3>

    <div class="form-control mb-4">
      <label class="label">
        <span class="label-text">Hari sejak pembelian terakhir (Recency)</span>
      </label>
      <input id="input-recency" type="number" min="1"
             placeholder="Contoh: 30"
             class="input input-bordered w-full" />
    </div>

    <div class="form-control mb-4">
      <label class="label">
        <span class="label-text">Jumlah pembelian (Frequency)</span>
      </label>
      <input id="input-frequency" type="number" min="1"
             placeholder="Contoh: 3"
             class="input input-bordered w-full" />
      <!-- Warning muncul di sini via JS jika frequency = 1 -->
      <div id="freq-warning" class="alert alert-warning mt-2 text-sm hidden">
        <span>⚠ Pelanggan dengan 1× pembelian adalah one-time buyer dan tidak termasuk
              dalam segmen repeat buyer.</span>
      </div>
    </div>

    <div class="form-control mb-6">
      <label class="label">
        <span class="label-text">Total nilai belanja (Monetary) dalam Rp</span>
      </label>
      <input id="input-monetary" type="number" min="1000"
             placeholder="Contoh: 150000"
             class="input input-bordered w-full" />
    </div>

    <div class="tooltip tooltip-top w-full"
         data-tip="Backend API belum tersedia — akan aktif setelah model selesai diekspor">
      <button class="btn btn-primary btn-block" disabled>
        Prediksi Segmen
      </button>
    </div>
  </div>
</div>

<script>
  const freqInput = document.getElementById('input-frequency')
  const warning   = document.getElementById('freq-warning')
  freqInput?.addEventListener('input', () => {
    const val = parseInt((freqInput as HTMLInputElement).value)
    warning?.classList.toggle('hidden', val !== 1)
  })
</script>
```

### components/prediksi/ResultCard.astro

```
Tampilkan empty state. Konten hasil akan diisi JS setelah API tersedia (belum perlu).

<div class="card bg-base-200 border border-base-300">
  <div class="card-body items-center justify-center py-16 text-center">
    <div class="text-4xl mb-3 opacity-20">🎯</div>
    <p class="text-sm text-base-content/40">Hasil segmen akan muncul di sini</p>
    <p class="text-xs text-base-content/30 mt-1">
      Masukkan data pelanggan dan klik Prediksi Segmen
    </p>
  </div>
</div>
```

### components/prediksi/CsvUpload.astro

```
UI placeholder, tidak perlu handler fungsional.

<div class="card bg-base-100 border border-base-300">
  <div class="card-body p-6">

    <!-- Drag-drop area -->
    <div class="border-2 border-dashed border-base-300 rounded-lg p-8 text-center mb-4">
      <div class="text-3xl mb-2 opacity-30">↑</div>
      <p class="text-sm text-base-content/60">Drag & drop file CSV di sini</p>
      <p class="text-xs text-base-content/40 mt-2">
        Format kolom: <code class="bg-base-200 px-1 rounded">username, recency, frequency, monetary</code>
      </p>
      <button class="btn btn-sm btn-outline mt-4 gap-2" disabled>
        Pilih File
        <span class="badge badge-sm badge-neutral">Segera Hadir</span>
      </button>
    </div>

    <!-- Batch result placeholder -->
    <div class="text-center py-8 border border-dashed border-base-300 rounded-lg">
      <p class="text-sm text-base-content/40">
        Hasil prediksi batch akan muncul di sini
      </p>
    </div>

  </div>
</div>
```

---

## HALAMAN

### pages/index.astro (Overview)

```astro
---
import LandingLayout from '../layouts/LandingLayout.astro'
import StatCard from '../components/ui/StatCard.astro'
import summary from '../data/summary.json'
---
<LandingLayout title="Overview">

  <!-- HERO -->
  <section class="min-h-[60vh] flex flex-col justify-center px-6 md:px-20 py-16 max-w-5xl">
    <p class="text-xs text-base-content/50 uppercase tracking-widest mb-4">
      Penelitian Tugas Akhir — Universitas Widyatama 2025
    </p>
    <h1 class="text-3xl md:text-5xl font-bold leading-tight mb-4">
      390.167 Pelanggan<br />bandungjaket.com<br />
      <span class="text-base-content/40">— Siapa Mereka?</span>
    </h1>
    <p class="text-base text-base-content/60 max-w-xl mb-8">
      Segmentasi pelanggan berbasis perilaku belanja menggunakan UMAP dan HDBSCAN
      pada data transaksi Shopee periode 2020–2025.
    </p>
    <div class="flex flex-col sm:flex-row gap-3">
      <a href="/dashboard" class="btn btn-primary btn-lg">Lihat Segmentasi →</a>
      <a href="/prediksi"  class="btn btn-outline btn-lg">Coba Prediksi Pelanggan</a>
    </div>
  </section>

  <!-- STAT CARDS -->
  <section class="px-6 md:px-20 pb-16">
    <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
      <StatCard label="Pelanggan Unik"       value="390.167"  subtitle="Sep 2020 – Okt 2025" />
      <StatCard label="Transaksi Valid"       value="481.682"  subtitle="Setelah preprocessing" />
      <StatCard label="Klaster Segmen"        value="6 Segmen" subtitle="Layer 2 repeat buyer" />
      <StatCard label="Repeat Buyer"          value="10,8%"    subtitle="42.248 dari total" />
    </div>
  </section>

  <!-- INFO CARDS -->
  <section class="px-6 md:px-20 pb-24">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

      <div class="card bg-base-100 border border-base-300">
        <div class="card-body p-6">
          <h2 class="card-title text-base">Ringkasan Penelitian</h2>
          <p class="text-sm text-base-content/70">
            Penelitian ini menganalisis 742.182 baris transaksi toko online bandungjaket.com di Shopee
            untuk mengidentifikasi pola perilaku belanja pelanggan menggunakan pendekatan machine learning
            tanpa supervisi. Metode UMAP digunakan untuk reduksi dimensi dan HDBSCAN untuk klasterisasi
            berbasis kepadatan.
          </p>
        </div>
      </div>

      <div class="card bg-base-100 border border-base-300">
        <div class="card-body p-6">
          <h2 class="card-title text-base">Tujuan & Manfaat</h2>
          <p class="text-sm text-base-content/70">
            Mengelompokkan pelanggan berdasarkan pola belanja (Recency, Frequency, Monetary) untuk membantu
            pengelola toko merancang strategi pemasaran yang tepat sasaran, meningkatkan retensi pelanggan
            bernilai tinggi, dan mengidentifikasi pelanggan yang berisiko berhenti bertransaksi.
          </p>
        </div>
      </div>

      <div class="card bg-base-100 border border-base-300">
        <div class="card-body p-6">
          <h2 class="card-title text-base">Metode Penelitian</h2>
          <p class="text-sm text-base-content/70">
            Menggunakan pendekatan two-layer clustering: Layer 1 untuk seluruh populasi dan Layer 2 khusus
            repeat buyer (frekuensi ≥ 2). Pipeline: RFM → Normalisasi Yeo-Johnson → Reduksi UMAP (3D→2D)
            → Klasterisasi HDBSCAN. Evaluasi: DBCV, Silhouette Score, dan Cluster Stability Index.
          </p>
        </div>
      </div>

    </div>
  </section>

</LandingLayout>
```

### pages/dashboard.astro

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro'
import KpiCards from '../components/dashboard/KpiCards.astro'
import SegmentAccordion from '../components/dashboard/SegmentAccordion.astro'
import BarChart from '../components/dashboard/BarChart.astro'
import DonutChart from '../components/dashboard/DonutChart.astro'
import ScatterPlotPlaceholder from '../components/dashboard/ScatterPlotPlaceholder.astro'
---
<BaseLayout title="Dashboard" activePage="dashboard">

  <div class="mb-6">
    <h1 class="text-2xl font-bold">Dashboard Segmentasi</h1>
    <p class="text-sm text-base-content/60 mt-1">
      Hasil segmentasi pelanggan bandungjaket.com · Periode Sep 2020 – Okt 2025
    </p>
  </div>

  <KpiCards />

  <div class="mt-8 mb-3">
    <h2 class="text-lg font-semibold">Profil Segmen & Rekomendasi Strategi</h2>
  </div>
  <SegmentAccordion />

  <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-8">
    <BarChart />
    <DonutChart />
  </div>

  <div class="mt-8 mb-3">
    <h2 class="text-lg font-semibold">Visualisasi Klaster (UMAP 2D)</h2>
  </div>
  <ScatterPlotPlaceholder />

  <!-- Quality badge: fixed bottom-right -->
  <!-- bottom-20 di mobile (di atas bottom tabs), bottom-6 di desktop -->
  <div class="fixed bottom-20 right-4 lg:bottom-6 lg:right-6 z-40">
    <div class="badge badge-success badge-lg gap-2 shadow-md py-3 px-4">
      ✓ Model Tervalidasi
    </div>
  </div>

</BaseLayout>
```

### pages/prediksi.astro

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro'
import InputForm from '../components/prediksi/InputForm.astro'
import ResultCard from '../components/prediksi/ResultCard.astro'
import CsvUpload from '../components/prediksi/CsvUpload.astro'
---
<BaseLayout title="Prediksi" activePage="prediksi">

  <div class="mb-6">
    <h1 class="text-2xl font-bold">Prediksi Segmen Pelanggan</h1>
    <p class="text-sm text-base-content/60 mt-1">
      Masukkan nilai RFM pelanggan untuk melihat segmen yang sesuai
    </p>
  </div>

  <!-- Mode toggle tabs -->
  <div role="tablist" class="tabs tabs-boxed mb-6 w-fit">
    <button id="tab-manual" role="tab" class="tab tab-active" onclick="switchTab('manual')">
      Input Manual
    </button>
    <button id="tab-csv" role="tab" class="tab" onclick="switchTab('csv')">
      Upload CSV
    </button>
  </div>

  <!-- Panel Input Manual -->
  <div id="panel-manual">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <InputForm />
      <ResultCard />
    </div>
  </div>

  <!-- Panel CSV (hidden by default) -->
  <div id="panel-csv" class="hidden">
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <CsvUpload />
      <div class="card bg-base-100 border border-base-300">
        <div class="card-body items-center justify-center py-16 text-center">
          <p class="text-sm text-base-content/40">Hasil prediksi batch akan muncul di sini</p>
        </div>
      </div>
    </div>
  </div>

</BaseLayout>

<script>
  function switchTab(tab: string) {
    const manual = document.getElementById('panel-manual')!
    const csv    = document.getElementById('panel-csv')!
    const tabManual = document.getElementById('tab-manual')!
    const tabCsv    = document.getElementById('tab-csv')!

    if (tab === 'manual') {
      manual.classList.remove('hidden')
      csv.classList.add('hidden')
      tabManual.classList.add('tab-active')
      tabCsv.classList.remove('tab-active')
    } else {
      csv.classList.remove('hidden')
      manual.classList.add('hidden')
      tabCsv.classList.add('tab-active')
      tabManual.classList.remove('tab-active')
    }
  }

  (window as any).switchTab = switchTab
</script>
```

### pages/tentang.astro

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro'
import MetricCard from '../components/ui/MetricCard.astro'
import StepCard from '../components/ui/StepCard.astro'
import metrics from '../data/metrics.json'
---
<BaseLayout title="Tentang" activePage="tentang">

  <div class="mb-6">
    <h1 class="text-2xl font-bold">Tentang Penelitian</h1>
    <p class="text-sm text-base-content/60 mt-1">
      Metodologi, evaluasi model, dan informasi penelitian
    </p>
    <hr class="mt-4 border-base-300" />
  </div>

  <!-- BAGAIMANA SEGMENTASI INI DIBUAT -->
  <div class="card bg-base-100 border border-base-300 mb-6">
    <div class="card-body p-6">
      <h2 class="text-lg font-semibold mb-3">Bagaimana Segmentasi Ini Dibuat?</h2>
      <p class="text-sm text-base-content/70 mb-3">
        Penelitian ini menggunakan pendekatan <strong>two-layer clustering</strong> untuk mengatasi
        ketidakseimbangan data. Dari 390.167 pelanggan unik, 89,2% hanya melakukan satu kali pembelian
        (one-time buyer). Jika klasterisasi dilakukan pada seluruh populasi (Layer 1), hasilnya didominasi
        oleh satu klaster besar yang menampung 96% pelanggan — tidak memberikan informasi yang bermakna.
      </p>
      <p class="text-sm text-base-content/70">
        Untuk mendapatkan segmentasi yang lebih bermakna, klasterisasi Layer 2 difokuskan pada 42.248
        pelanggan repeat buyer (frekuensi ≥ 2). Pada subset ini, ketiga fitur RFM memiliki variasi yang
        cukup untuk membentuk 6 klaster yang terpisah dengan baik, menghasilkan DBCV = 0.796 dan
        Cluster Stability Index = 0.98.
      </p>
    </div>
  </div>

  <!-- SUMBER DATA -->
  <div class="card bg-base-100 border border-base-300 mb-6">
    <div class="card-body p-6">
      <h2 class="text-lg font-semibold mb-3">Sumber Data</h2>
      <p class="text-sm text-base-content/70 mb-4">
        Data transaksi diperoleh dari Shopee Seller Center milik toko bandungjaket.com dalam format Excel,
        mencakup periode September 2020 hingga Oktober 2025. Total data mentah 742.182 baris, yang setelah
        preprocessing menghasilkan 481.682 transaksi bersih dari 390.167 pelanggan unik.
      </p>
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="stat bg-base-200 rounded-lg p-3">
          <div class="stat-value text-lg">742.182</div>
          <div class="stat-desc">Baris data mentah</div>
        </div>
        <div class="stat bg-base-200 rounded-lg p-3">
          <div class="stat-value text-lg">481.682</div>
          <div class="stat-desc">Transaksi valid</div>
        </div>
        <div class="stat bg-base-200 rounded-lg p-3">
          <div class="stat-value text-lg">390.167</div>
          <div class="stat-desc">Pelanggan unik</div>
        </div>
        <div class="stat bg-base-200 rounded-lg p-3">
          <div class="stat-value text-lg">5 tahun</div>
          <div class="stat-desc">Periode data</div>
        </div>
      </div>
    </div>
  </div>

  <!-- METODOLOGI + METRIK (collapsible) -->
  <div class="collapse collapse-arrow bg-base-100 border border-base-300 mb-6">
    <input type="checkbox" checked />
    <div class="collapse-title text-base font-semibold">
      Detail Metodologi & Evaluasi Model
    </div>
    <div class="collapse-content">

      <!-- 4-step methodology -->
      <h3 class="text-sm font-semibold uppercase tracking-wide text-base-content/50 mb-3 mt-2">
        Diagram Metodologi Penelitian
      </h3>
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <StepCard step={1} title="RFM Analysis"
          description="Pembentukan fitur Recency, Frequency, dan Monetary per pelanggan dari data transaksi" />
        <StepCard step={2} title="Yeo-Johnson"
          description="Normalisasi PowerTransformer untuk menyeragamkan skala dan distribusi ketiga fitur" />
        <StepCard step={3} title="UMAP"
          description="Reduksi dimensi 3D ke 2D untuk mempertahankan struktur data dan memudahkan klasterisasi" />
        <StepCard step={4} title="HDBSCAN"
          description="Klasterisasi berbasis kepadatan tanpa perlu menentukan jumlah klaster di awal" />
      </div>

      <!-- Evaluation metrics -->
      <h3 class="text-sm font-semibold uppercase tracking-wide text-base-content/50 mb-3">
        Metrik Evaluasi Model (Layer 2)
      </h3>
      <div class="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-6">
        <MetricCard label="DBCV" value="0.796"
          description="Kualitas pemisahan klaster berbasis kepadatan — 0 hingga 1"
          highlight={true} />
        <MetricCard label="Silhouette Score" value="0.430"
          description="Kualitas pemisahan dalam ruang RFM ternormalisasi" />
        <MetricCard label="Cluster Stability" value="0.98"
          description="Konsistensi klaster terhadap variasi data — mendekati 1 = sangat stabil"
          highlight={true} />
        <MetricCard label="Noise Rate" value="0%"
          description="Proporsi data yang tidak masuk klaster mana pun pada Layer 2" />
      </div>

      <!-- Referensi -->
      <h3 class="text-sm font-semibold uppercase tracking-wide text-base-content/50 mb-3">
        Referensi Utama
      </h3>
      <div class="card bg-base-200 border border-base-300 mb-4">
        <div class="card-body p-4">
          <ul class="space-y-2 text-xs text-base-content/70">
            <li>Blessy et al. (2023). Customer Segmentation Using UMAP and HDBSCAN. <em>IJMRT</em>, 5(7), 117–136.</li>
            <li>Campello et al. (2015). Hierarchical density estimates for data clustering. <em>ACM TKDD</em>, 10(1).</li>
            <li>McInnes et al. (2020). UMAP: Uniform Manifold Approximation and Projection. <em>arXiv:1802.03426</em>.</li>
            <li>Díaz-Pérez & Miralles-Pechuán (2022). Customer segmentation for e-commerce. <em>Expert Systems with Applications</em>, 203.</li>
            <li>Ma (2022). E-commerce Customer Segmentation Based on RFM Model. <em>LNEE</em>, 926–931.</li>
          </ul>
        </div>
      </div>

      <!-- Info Pembuat -->
      <h3 class="text-sm font-semibold uppercase tracking-wide text-base-content/50 mb-3">
        Info Pembuat
      </h3>
      <div class="card bg-base-200 border border-base-300">
        <div class="card-body p-4">
          <p class="font-semibold text-base">Farhan Ramadhany</p>
          <div class="text-sm text-base-content/60 space-y-1 mt-1">
            <p>NPM: 40622100101</p>
            <p>Program Studi: Teknik Informatika — Konsentrasi Database</p>
            <p>Universitas Widyatama, Bandung</p>
            <p>Tahun: 2025</p>
          </div>
        </div>
      </div>

    </div>
  </div>

</BaseLayout>
```

---

## URUTAN BUILD — IKUTI PERSIS

```
1.  src/data/segments.json          ← salin dari PRD ini
2.  src/data/summary.json           ← salin dari PRD ini
3.  src/data/metrics.json           ← salin dari PRD ini
4.  src/types/index.ts              ← salin dari PRD ini
5.  tailwind.config.mjs             ← tambahkan DaisyUI theme dari PRD ini
6.  layouts/BaseLayout.astro        ← scaffold dulu, bisa disempurnakan nanti
7.  layouts/LandingLayout.astro
8.  components/navigation/Sidebar.astro
9.  components/navigation/BottomTabs.astro
10. components/navigation/TopNavbar.astro
11. components/ui/StatCard.astro
12. components/ui/MetricCard.astro
13. components/ui/StepCard.astro
14. pages/index.astro               ← verifikasi LandingLayout OK
15. pages/tentang.astro             ← verifikasi komponen UI OK
16. components/dashboard/KpiCards.astro
17. components/dashboard/SegmentAccordion.astro
18. components/dashboard/BarChart.astro
19. components/dashboard/DonutChart.astro
20. components/dashboard/ScatterPlotPlaceholder.astro
21. pages/dashboard.astro           ← verifikasi semua chart render
22. components/prediksi/InputForm.astro
23. components/prediksi/ResultCard.astro
24. components/prediksi/CsvUpload.astro
25. pages/prediksi.astro            ← verifikasi tab toggle OK
```

---

## CATATAN IMPLEMENTASI

- **Import JSON di Astro**: `import data from '../data/segments.json'` — langsung tanpa fetch
- **Chart.js**: install dulu `npm install chart.js`, lalu `import { Chart } from 'chart.js/auto'` di `<script>` tag
- **Format angka Indonesia**: `(390167).toLocaleString('id-ID')` → "390.167"
- **Format Rupiah**: `new Intl.NumberFormat('id-ID', { style: 'currency', currency: 'IDR', minimumFractionDigits: 0 }).format(475691)` → "Rp 475.691"
- **Accordion default open**: gunakan atribut `open` pada `<details>` untuk segment id=5
- **Active page navigation**: setiap `pages/*.astro` pass prop `activePage` ke `BaseLayout`
- **Chart.js di Astro**: `<script>` tag di dalam `.astro` diproses Vite — bisa import NPM packages langsung

---

## ACCEPTANCE CRITERIA

- [ ] `npm run dev` berjalan tanpa error atau warning kritis
- [ ] Semua 4 route accessible: `/`, `/dashboard`, `/prediksi`, `/tentang`
- [ ] Mobile 375px: bottom tabs terlihat, tidak ada horizontal scroll, sidebar tersembunyi
- [ ] Desktop 1440px: sidebar terlihat, bottom tabs tersembunyi, layout 2-kolom aktif
- [ ] SegmentAccordion: klik baris bisa expand/collapse, default expand segment "Bernilai Terancam"
- [ ] BarChart dan DonutChart render dengan data dari segments.json
- [ ] Prediksi — input frequency=1 menampilkan alert-warning DaisyUI
- [ ] Prediksi — submit button dalam state disabled dengan tooltip
- [ ] Badge "Model Tervalidasi" muncul fixed bottom-right di halaman Dashboard
- [ ] Scatter plot menampilkan placeholder (bukan error)
- [ ] `npm run build` selesai tanpa error TypeScript

---

## SDLC — METODE WATERFALL

Model SDLC yang digunakan adalah **Waterfall**, dipilih karena seluruh kebutuhan sistem sudah terdefinisi dengan jelas melalui penelitian, wireframe, dan PRD ini. Tidak ada perubahan requirements yang diantisipasi di tengah proses pengembangan.

### Fase dan Status

**Fase 1: Analisis Kebutuhan ✓ SELESAI**
- Input: Proposal tugas akhir, dataset Shopee, hasil ML pipeline (notebook)
- Output: PRD (dokumen ini), functional requirements, user requirements
- Deliverable: Daftar 4 halaman, komponen, struktur data JSON, user persona

**Fase 2: Perancangan Sistem ✓ SELESAI**
- Input: Requirements dari Fase 1
- Output: Wireframe 8 gambar (desktop + mobile), arsitektur informasi, DFD Level 0 dan Level 1
- Deliverable: Struktur folder, component tree, design system (DaisyUI theme), routing

**Fase 3: Implementasi → IN PROGRESS**
Dibagi tiga sub-fase berurutan:
- 3a — Frontend Static (Sprint 1-3): halaman Overview, Dashboard, Tentang
- 3b — Backend FastAPI (Sprint 4): ekspor model pkl, endpoint /api/predict, CORS
- 3c — Integrasi Prediksi (Sprint 5): halaman Prediksi + koneksi API

**Fase 4: Pengujian → UPCOMING**
- Unit testing: setiap komponen berdiri sendiri
- Integration testing: form Prediksi → API endpoint → model inference → response
- Functional testing: semua halaman sesuai acceptance criteria
- Responsiveness testing: mobile 375px, tablet 768px, desktop 1440px
- Edge case testing: frequency=1, hasil HDBSCAN=-1, CSV format salah

**Fase 5: Deployment → UPCOMING**
- Frontend (static pages): Vercel atau Netlify (free tier)
- Backend (FastAPI): Railway.app atau Render.com (free tier)
- Environment: set VITE_API_URL ke URL backend yang sudah dideploy
- Domain: opsional custom domain untuk keperluan sidang

**Fase 6: Pemeliharaan → FUTURE**
- Update model pkl jika ada penambahan data transaksi baru
- Bug fixes pasca sidang
- Dokumentasi kode untuk arsip skripsi

---

## DFD — DATA FLOW DIAGRAM

### Konvensi Notasi

| Simbol | Representasi dalam Diagram |
|--------|---------------------------|
| Persegi panjang (double border) | Entitas Eksternal |
| Oval | Proses (Level 0) |
| Kotak rounded | Proses (Level 1) |
| Dua garis horizontal terbuka | Data Store |
| Panah | Aliran Data |

### Context Diagram (Level 0)

Satu entitas eksternal: **Pengelola Toko** bandungjaket.com.

Aliran data:
- **Input ke sistem**: akses halaman web dan input nilai RFM (untuk halaman Prediksi)
- **Output dari sistem**: visualisasi segmentasi, informasi segmen, dan rekomendasi strategi pemasaran

### Level 1 DFD

**Daftar Proses:**

| ID | Nama Proses | Halaman | Tipe |
|----|-------------|---------|------|
| 1.0 | Tampil Overview | `/` | Static (SSG) |
| 2.0 | Tampil Dashboard | `/dashboard` | Static (SSG) |
| 3.0 | Prediksi Segmen | `/prediksi` | Dinamis (butuh API) |
| 4.0 | Tampil Metodologi | `/tentang` | Static (SSG) |

**Daftar Data Store:**

| ID | Nama | Sumber | Dibaca oleh |
|----|------|--------|-------------|
| D1 | Data Segmen | `src/data/segments.json` | 1.0, 2.0, 3.0 |
| D2 | Data Ringkasan | `src/data/summary.json` | 1.0, 2.0 |
| D3 | Data Metrik Evaluasi | `src/data/metrics.json` | 2.0, 4.0 |
| D4 | Model ML | FastAPI Backend (.pkl files) | 3.0 |

**Aliran data primer yang divisualisasikan (1:1 mapping):**
- D2 → Proses 1.0 (data ringkasan untuk stat cards Overview)
- D1 → Proses 2.0 (data segmen untuk accordion table dan charts Dashboard)
- D4 → Proses 3.0 (model ML via FastAPI untuk inference Prediksi)
- D3 → Proses 4.0 (data metrik untuk evaluation cards Tentang)

Seluruh proses bersifat **read-only** terhadap data store — tidak ada proses yang menulis balik ke data store dalam sistem ini.
