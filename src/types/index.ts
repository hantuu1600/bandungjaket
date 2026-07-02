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
