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

# Configure CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bandungjaket.vercel.app",
        "http://localhost:4321",
        "http://localhost:4323",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schemas
class CustomerData(BaseModel):
    recency: int
    frequency: int
    monetary: float

# ML Model instances
yeo_johnson = None
umap_model = None
hdbscan_model = None
load_error_msg = None

@app.on_event("startup")
def load_models():
    """Initialize ML models on application startup."""
    global yeo_johnson, umap_model, hdbscan_model
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(BASE_DIR, "models")
    
    try:
        yeo_johnson = joblib.load(os.path.join(models_dir, "scaler.pkl"))
        umap_model = joblib.load(os.path.join(models_dir, "umap_reducer.pkl"))
        hdbscan_model = joblib.load(os.path.join(models_dir, "hdbscan_model.pkl"))
        print("Models loaded successfully.")
    except Exception as e:
        global load_error_msg
        load_error_msg = str(e)
        import traceback
        
        # Append directory contents for debugging container environments
        try:
            files_in_dir = os.listdir(BASE_DIR)
            load_error_msg += f"\n\n[DEBUG] File yang ada di {BASE_DIR}: {files_in_dir}\n"
        except Exception as ex:
            load_error_msg += f"\n\n[DEBUG] Gagal membaca direktori: {ex}\n"
            
        load_error_msg += "\n" + traceback.format_exc()
        print(f"Failed to load models: {e}")
        print("Ensure scaler.pkl, umap_reducer.pkl, and hdbscan_model.pkl exist in the models directory.")

@app.get("/")
def read_root():
    return {
        "message": "API Segmentasi BandungJaket Aktif!",
        "load_error": load_error_msg
    }

@app.get("/api/model-info")
def model_info():
    return {
        "r_mid_recency": 1481,
        "f_p75_frequency": 3,
        "m_p75_monetary": 233238,
        "n_clusters": 6,
        "algorithm": "UMAP + HDBSCAN (2-layer: repeat buyers only)"
    }

@app.post("/api/predict")
def predict_segment(data: CustomerData):
    if not all([yeo_johnson, umap_model, hdbscan_model]):
        raise HTTPException(status_code=500, detail="Model belum siap/gagal diload.")
        
    try:
        # Convert to DataFrame
        df = pd.DataFrame([data.dict()])
        
        # Apply Yeo-Johnson transformation
        df_transformed = yeo_johnson.transform(df)
        
        # UMAP dimensionality reduction
        umap_coords = umap_model.transform(df_transformed)
        
        # HDBSCAN clustering prediction
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
    Batch predict endpoint handling raw Kaggle dataset. 
    Performs dynamic RFM calculation and clustering prediction.
    """
    if not yeo_johnson or not umap_model or not hdbscan_model:
        raise HTTPException(status_code=500, detail="Models are not loaded on server.")
        
    try:
        # Parse CSV
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content), low_memory=False)
        
        # Calculate RFM metrics
        if 'Waktu Pesanan Selesai' not in df.columns or 'Username (Pembeli)' not in df.columns:
            raise HTTPException(status_code=400, detail="Kolom Waktu Pesanan Selesai atau Username tidak ditemukan di CSV.")
            
        df['completion_date'] = pd.to_datetime(df['Waktu Pesanan Selesai'].dropna(), errors='coerce')
        df = df.dropna(subset=['completion_date'])
        
        acuan = df['completion_date'].max() + pd.Timedelta(days=1)
        
        # Determine monetary column
        monetary_col = 'Total Pembayaran' if 'Total Pembayaran' in df.columns else 'Total Harga Produk'
        if monetary_col not in df.columns:
            monetary_col = df.columns[-1] # Fallback mechanism
            
        rfm = df.groupby('Username (Pembeli)').agg(
            last_buy=('completion_date', 'max'),
            frequency=('No. Pesanan', 'nunique'),
            monetary=(monetary_col, 'sum'),
        ).reset_index()

        rfm['recency'] = (acuan - rfm['last_buy']).dt.days
        
        # Filter repeat buyers (frequency >= 2)
        repeat = rfm[rfm['frequency'] >= 2].copy()
        if len(repeat) == 0:
            raise HTTPException(status_code=400, detail="Tidak ada pelanggan dengan frekuensi >= 2 (repeat buyer) di dataset ini.")
            
        # Execute prediction pipeline
        fitur = ['recency', 'frequency', 'monetary']
        
        # Pipeline: PowerTransformer -> UMAP -> HDBSCAN
        X = yeo_johnson.transform(repeat[fitur].values)
        emb = umap_model.transform(X)
        labels, probabilities = hdbscan.approximate_predict(hdbscan_model, emb)
        
        # Format response data
        repeat['cluster_id'] = labels
        repeat['umap_x'] = emb[:, 0]
        repeat['umap_y'] = emb[:, 1]
        
        # Limit output to 5000 records to prevent memory overflow
        hasil = repeat[['Username (Pembeli)', 'recency', 'frequency', 'monetary', 'cluster_id', 'umap_x', 'umap_y']].head(5000).to_dict(orient='records')
        
        return {
            "message": "Berhasil memproses raw data!",
            "total_repeat_buyers": len(repeat),
            "data": hasil
        }
        
    except Exception as e:
        error_msg = f"{str(e)}\n{traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_msg)

