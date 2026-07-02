from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import os
import io
import traceback
import hdbscan

app = FastAPI(title="BandungJaket Segmentasi API")

# Setup CORS agar Frontend Astro (localhost:4323) bisa memanggil API ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Dalam production sebaiknya diganti spesifik URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Struktur data dari Frontend
class CustomerData(BaseModel):
    recency: int
    frequency: int
    monetary: float

# Global variables untuk model
yeo_johnson = None
umap_model = None
hdbscan_model = None
load_error_msg = None

@app.on_event("startup")
def load_models():
    """Meload model .pkl saat server pertama kali menyala."""
    global yeo_johnson, umap_model, hdbscan_model
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(BASE_DIR, "models")
    
    try:
        yeo_johnson = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        umap_model = joblib.load(os.path.join(models_dir, "umap_reducer.pkl"))
        hdbscan_model = joblib.load(os.path.join(models_dir, "hdbscan_model.pkl"))
        print("✅ Semua model berhasil di-load!")
    except Exception as e:
        global load_error_msg
        load_error_msg = str(e)
        import traceback
        
        # Tambahkan informasi daftar file yang ada di dalam Docker!
        try:
            files_in_dir = os.listdir(BASE_DIR)
            load_error_msg += f"\n\n[DEBUG] File yang ada di {BASE_DIR}: {files_in_dir}\n"
        except Exception as ex:
            load_error_msg += f"\n\n[DEBUG] Gagal membaca direktori: {ex}\n"
            
        load_error_msg += "\n" + traceback.format_exc()
        print(f"⚠️ Peringatan: Gagal meload model. Error: {e}")
        print("Pastikan file scaler.pkl, umap_reducer.pkl, dan hdbscan_model.pkl ada sejajar dengan main.py")

@app.get("/")
def read_root():
    return {
        "message": "API Segmentasi BandungJaket Aktif!",
        "load_error": load_error_msg
    }

@app.post("/api/predict")
def predict_segment(data: CustomerData):
    if not all([yeo_johnson, umap_model, hdbscan_model]):
        raise HTTPException(status_code=500, detail="Model belum siap/gagal diload.")
        
    try:
        # 1. Jadikan DataFrame
        df = pd.DataFrame([data.dict()])
        
        # 2. Transformasi Yeo-Johnson
        df_transformed = yeo_johnson.transform(df)
        
        # 3. Reduksi UMAP
        umap_coords = umap_model.transform(df_transformed)
        
        # 4. Prediksi Cluster
        labels, probabilities = hdbscan.approximate_predict(hdbscan_model, umap_coords)
        cluster_id = int(labels[0])
        
        return {
            "status": "success",
            "cluster_id": cluster_id,
            "umap_x": float(umap_coords[0][0]),
            "umap_y": float(umap_coords[0][1])
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/predict_batch_raw")
async def predict_batch_raw(file: UploadFile = File(...)):
    """
    Endpoint untuk menerima RAW DATASET (seperti dari Kaggle), menghitung RFM secara dinamis, 
    dan melakukan prediksi klaster. (Hanya untuk demonstrasi, tidak disarankan untuk file > 50MB)
    """
    if not yeo_johnson or not umap_model or not hdbscan_model:
        raise HTTPException(status_code=500, detail="Models are not loaded on server.")
        
    try:
        # 1. Baca CSV Raw
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content), low_memory=False)
        
        # 2. Proses RFM (Logic dari Notebook)
        if 'Waktu Pesanan Selesai' not in df.columns or 'Username (Pembeli)' not in df.columns:
            raise HTTPException(status_code=400, detail="Kolom Waktu Pesanan Selesai atau Username tidak ditemukan di CSV.")
            
        df['completion_date'] = pd.to_datetime(df['Waktu Pesanan Selesai'].dropna(), errors='coerce')
        df = df.dropna(subset=['completion_date'])
        
        acuan = df['completion_date'].max() + pd.Timedelta(days=1)
        
        # Gunakan 'Total Pembayaran' atau 'Total Harga Produk' untuk Monetary
        monetary_col = 'Total Pembayaran' if 'Total Pembayaran' in df.columns else 'Total Harga Produk'
        if monetary_col not in df.columns:
            monetary_col = df.columns[-1] # fallback
            
        rfm = df.groupby('Username (Pembeli)').agg(
            last_buy=('completion_date', 'max'),
            frequency=('No. Pesanan', 'nunique'),
            monetary=(monetary_col, 'sum'),
        ).reset_index()

        rfm['recency'] = (acuan - rfm['last_buy']).dt.days
        
        # 3. Filter Repeat Buyers
        repeat = rfm[rfm['frequency'] >= 2].copy()
        if len(repeat) == 0:
            raise HTTPException(status_code=400, detail="Tidak ada pelanggan dengan frekuensi >= 2 (repeat buyer) di dataset ini.")
            
        # 4. Prediksi
        fitur = ['recency', 'frequency', 'monetary']
        
        # Karena kita pakai Pipeline: PowerTransformer -> UMAP -> HDBSCAN
        X = yeo_johnson.transform(repeat[fitur].values)
        emb = umap_model.transform(X)
        labels, probabilities = hdbscan.approximate_predict(hdbscan_model, emb)
        
        # 5. Format Output
        repeat['cluster_id'] = labels
        repeat['umap_x'] = emb[:, 0]
        repeat['umap_y'] = emb[:, 1]
        
        # Kembalikan maksimal 5000 baris agar JSON tidak crash
        hasil = repeat[['Username (Pembeli)', 'recency', 'frequency', 'monetary', 'cluster_id', 'umap_x', 'umap_y']].head(5000).to_dict(orient='records')
        
        return {
            "message": "Berhasil memproses raw data!",
            "total_repeat_buyers": len(repeat),
            "data": hasil
        }
        
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_msg)

