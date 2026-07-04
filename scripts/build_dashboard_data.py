"""
Mengonversi hasil_segmentasi.csv (data riil dari Kaggle)
menjadi file JSON untuk Dashboard website.
"""
import pandas as pd
import json
import random

df = pd.read_csv('hasil_segmentasi.csv')
print(f"Total data: {len(df)} baris")

sample_frames = []
for cid in sorted(df['cluster'].unique()):
    cluster_df = df[df['cluster'] == cid]
    # Ambil proporsional, minimal 50 titik per cluster
    n_sample = max(50, int(len(cluster_df) / len(df) * 3000))
    n_sample = min(n_sample, len(cluster_df))
    sample_frames.append(cluster_df.sample(n=n_sample, random_state=42))

sample = pd.concat(sample_frames)
print(f"Sample untuk scatter plot: {len(sample)} titik")

scatter_data = []
for _, row in sample.iterrows():
    scatter_data.append({
        "x": round(float(row['umap_x']), 3),
        "y": round(float(row['umap_y']), 3),
        "cluster_id": int(row['cluster']),
    })

with open('src/data/scatter.json', 'w') as f:
    json.dump(scatter_data, f)
print(f"[OK] scatter.json: {len(scatter_data)} titik data RIIL")

segment_names = {
    0: "Pelanggan Potensial",
    1: "Pelanggan Dorman",
    2: "Pelanggan Unggulan",
    3: "Pelanggan Aktif",
    4: "Pelanggan Berisiko Berhenti",
    5: "Pelanggan Bernilai Terancam"
}

badges = {0: "info", 1: "neutral", 2: "warning", 3: "success", 4: "warning", 5: "error"}
colors = {0: "#3b82f6", 1: "#6b7280", 2: "#f59e0b", 3: "#10b981", 4: "#f97316", 5: "#ef4444"}

descriptions = {
    0: "Baru mulai bertransaksi ulang. Berpotensi menjadi pelanggan aktif dengan dorongan yang tepat.",
    1: "Kelompok terbesar repeat buyer. Sudah lama tidak bertransaksi dengan frekuensi rendah.",
    2: "Pelanggan paling aktif dan bernilai tinggi. Baru bertransaksi, sering belanja, dan total belanja terbesar.",
    3: "Pelanggan yang masih aktif dengan frekuensi dan nilai belanja yang cukup baik.",
    4: "Dulunya cukup aktif namun sudah lama tidak bertransaksi. Perlu intervensi segera.",
    5: "Bernilai sangat tinggi namun sudah lama tidak aktif. Kehilangan segmen ini berdampak besar pada pendapatan."
}

recommendations = {
    0: ["Kirim penawaran follow-up setelah pembelian kedua", "Voucher untuk mendorong pembelian ketiga", "Tampilkan produk serupa berdasarkan riwayat pembelian"],
    1: ["Kirim kampanye reaktivasi via Shopee Broadcast", "Tawarkan gratis ongkir atau diskon comeback", "Fokus pada produk terlaris sebagai daya tarik"],
    2: ["Berikan loyalty reward atau voucher eksklusif", "Tawarkan produk premium atau bundle spesial", "Ajak bergabung ke referral program"],
    3: ["Pertahankan dengan flash sale dan notifikasi produk baru", "Dorong upsell ke produk kategori lebih tinggi", "Cross-sell untuk menaikkan nilai per transaksi"],
    4: ["Kampanye win-back dengan penawaran terbatas waktu", "Hubungi personal via Shopee Chat", "Diskon khusus berdasarkan produk terakhir dibeli"],
    5: ["Prioritas tertinggi — hubungi langsung via Shopee Chat", "Penawaran eksklusif: diskon besar atau bundle premium", "Jadwalkan follow-up dalam 7 hari"]
}

segments = []
for cid in sorted(df['cluster'].unique()):
    cluster_data = df[df['cluster'] == cid]
    segments.append({
        "id": int(cid),
        "name": segment_names[cid],
        "count": int(len(cluster_data)),
        "recency": float(cluster_data['recency'].median()),
        "frequency": float(cluster_data['frequency'].median()),
        "monetary": float(cluster_data['monetary'].median()),
        "badge": badges[cid],
        "color_dot": colors[cid],
        "description": descriptions[cid],
        "recommendations": recommendations[cid]
    })

segments_json = {"segments": segments}
with open('src/data/segments.json', 'w', encoding='utf-8') as f:
    json.dump(segments_json, f, ensure_ascii=False, indent=2)
print("[OK] segments.json: statistik riil dari 42.248 pelanggan")

# Tampilkan ringkasan
for s in segments:
    print(f"  Cluster {s['id']}: {s['name']} — {s['count']} pelanggan (R={s['recency']}, F={s['frequency']}, M={s['monetary']})")
