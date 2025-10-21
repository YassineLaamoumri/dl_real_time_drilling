# **DL Real-Time Drilling**

## **🔵 0) Cover & Metadata**
- **Project**: Real-time drilling analytics and deep learning
- **Domain**: Drilling telemetry (Volve WITSML → CSV time/depth)
- **Primary outcomes**: Real-time anomaly detection, ROP optimization, parameter recommendations, post-run evaluation
- **Tech**: Python 3.12, PyTorch Lightning, ONNX Runtime, FastAPI, MLflow (tracking + registry), Prometheus
- **Data**: Volve real-time CSVs (time + depth) [license: CC BY-NC-SA 4.0]
- **Ownership**: Application team; ML ops via MLflow; infra optional: S3/MinIO + Postgres for registry

## **🔵 1) Executive Summary (One-Pager)**
We build an end-to-end pipeline to learn from historical Volve real-time drilling logs and deploy an online inference service capable of sub-second decisions on streaming telemetry. Training logs experiments and artifacts in MLflow, promotes models via the registry, exports ONNX for low-latency serving, and exposes a FastAPI endpoint (/infer) and optional streaming pipeline. Depth-aligned data supports evaluation and root-cause analysis; time-indexed logs power real-time features.

### **🟢 1.1 Technical Overview**
- **Offline**: feature engineering (windowed statistics, deltas, frequency features), supervised learning for targets like ROP prediction, stick-slip/bit-bounce detection; MLflow tracking + model registry; ONNX export.
- **Online**: minimal featurizer + ONNXRuntime session; FastAPI endpoint; optional async stream processor; metrics to Prometheus; structured JSON logging with emojis; config typed; secrets via env only.
- **Data provenance**: dataset URIs and hashes logged as MLflow inputs; raw and curated stored in versioned object-store paths.

## **🔵 2) System Overview (Visuals)**

### **🟣 2.1 High-Level Architecture (Flowchart)**
Data source (Volve CSV time/depth) → Offline feature pipeline → Train (Lightning) → MLflow (metrics, artifacts) → ONNX export → Model Registry (Staging/Prod) → Online Service (FastAPI + ONNXRuntime) → Metrics/Logs → Dashboard.

### **🟣 2.2 Request Lifecycle (Sequence)**
Client sends JSON payload or stream event → featurizer forms input tensor → ONNXRuntime predicts → thresholds/post-processing → response + logs + metrics.

### **🟣 2.3 Data Flow (Pipeline)**
Raw CSVs → cleaning/standardization → feature generation → train/val/test splits (by wells/time) → model training → evaluation reports → registration → online inference.

### **🟣 2.4 Entity-Relationship (Core Data Model)**
- Entities: `Well`, `Run/Section`, `TimeLog`, `DepthLog`, `FeatureWindow`, `Prediction`, `Alert`.
- Relations: `Well` 1—N `Run`; each `Run` maps to many `TimeLog` rows; `FeatureWindow` derives from time slices; `Prediction` references input window and model version.

## **🔵 3) Scope & Requirements**

### **🟢 3.1 Functional Requirements**
- Ingest Volve time-based CSVs; optionally depth-based for alignment.
- Build offline features (windowed stats, lags, gradients, spectral proxies).
- Train and evaluate models; log to MLflow; export ONNX and register.
- Serve predictions via REST `/infer` and optional streaming pipeline.
- Monitor latency, throughput, error rate; log inputs/outputs with request IDs.
- Post-run analytics: depth joins, confusion metrics, ROP deltas, event reports.

### **🟢 3.2 Non-Functional Requirements (NFRs)**
- Latency per request: target 100–300 ms; P95 < 500 ms.
- Availability: 99.9% for serving; graceful degradation.
- Observability: structured logs, Prometheus metrics.
- Reproducibility: versioned datasets by URI; MLflow runs pinned with inputs.
- Security: env-only secrets; principle of least privilege for object store.

### **🟢 3.3 Constraints & Assumptions**
- Training and serving on CPU acceptable initially; GPU optional.
- Volve data is noisy and heterogeneous; robust cleaning needed.
- Real-time labels may be delayed; use proxy targets or semi-supervised flags.

## **🔵 4) Detailed Design**

### **🟣 4.1 Component Breakdown**
- `app.settings`: Pydantic Settings for secrets (MLflow URIs/tokens via env only).
- `app.logging`: JSON emoji `LOGGER`.
- `data.sources`: loaders for Volve CSVs (time/depth), schema normalization.
- `data.transforms`: feature generation, scaling, train-time pipelines.
- `models.*`: Lightning modules; ONNX export utilities; MLflow autolog hooks.
- `training.train_mlflow`: main trainer that logs runs and registers models.
- `serving.inference_mlflow`: model artifact loader via MLflow + ONNXRuntime.
- `serving.api`: FastAPI app exposing `/infer` and `/health`, `/metrics`.
- `pipelines.stream`: optional asyncio loop for windowed streaming inference.

### **🟣 4.2 API Contracts**
- POST `/infer`: `{ "input": number[][] }` → `{ "output": number[][] }`
- GET `/health`: `{"status":"ok"}`
- GET `/metrics`: Prometheus text format

### **🟣 4.3 Data Schemas**
- Time CSV columns typical: `timestamp, hookload, rpm, torque, flow, spm, standpipe_pressure, wob, bit_depth, hole_depth, rop`, etc.
- Depth CSV columns typical: `md, tvd, rop, wob, rpm, torque, spp, flow`, etc.
- Internal normalized schema documented in `data/README.md`.

### **🟣 4.4 Algorithms / Heuristics**
- Baseline regressors/classifiers: MLP for ROP/regression; classifier for dysfunctions.
- Feature windows: rolling stats (mean, std, min, max), lags/deltas, EWMA; optional STFT energy bands for vibration proxies; categorical encodings for BHA/bit if available.
- Thresholding + hysteresis for alert stability; smoothing for noisy signals.

### **🟣 4.5 Trade-offs & Alternatives**
- ONNXRuntime vs. TorchScript: ONNX for portability and non-PyTorch serving; TorchScript simpler but less portable.
- Full stream processor (Bytewax/Kafka) vs. simple asyncio: start simple; scale if needed.
- LakeFS/Delta for data versioning vs. MLflow-only provenance: MLflow-only is lighter; add LakeFS later if auditability requires it.

## **🔵 5) Delivery Plan**

### **🟢 5.1 Milestones & Deliverables**
1. Scaffold repo, logging, settings, deps; mock training loop; `/health`.
2. CSV loaders + basic features; MLflow tracking; baseline model; ONNX export.
3. FastAPI `/infer` + ONNXRuntime; Prometheus metrics; latency tests.
4. Stream pipeline (async) with sliding windows; basic alerts.
5. Offline evaluation with depth alignment; dashboards/reports; model registry promotion to Staging → Prod.

## **🔵 7) Observability & Operations**

### **🟢 7.1 Monitoring & Alerts**
- Metrics: request count, latency (p50/p95/p99), errors, input drift scores, output range checks.
- Logs: JSON with request_id, model_version, durations, emojis.
- Alerts: high error rate, high latency, drift beyond threshold.

### **🟢 7.2 Cost & Capacity**
- Storage: full Volve CSV compressed ~2.7 GB; expanded ~8–12 GB.
- Compute: CPU-only feasible; scale workers behind Uvicorn; batch predictions if needed.
- Artifact store: S3/MinIO (~100s MB per model with reports); Postgres for registry metadata.

## **🔵 8) Risks, Dependencies & Compliance**

### **🟠 8.1 Risk Register**
- Data quality gaps; misaligned time/depth channels → mitigated by cleaning and validation checks.
- Label uncertainty (real-time vs. post-hoc labels) → use proxy targets and human-in-loop review.
- Concept drift across wells/sections → monitor drift, schedule retrains.

### **🟠 8.2 Dependencies**
- MLflow server + backend store (e.g., Postgres) + artifact store (S3/MinIO).
- Python libs: PyTorch, Lightning, ONNX, ONNXRuntime, FastAPI, Prometheus client.

## **🔵 10) Open Questions & Decisions**

### **🟢 10.1 Open Questions**
- Primary online task: anomaly flags vs. ROP optimization vs. advisory?
- Target latency budget and deployment environment?
- Need for edge deployment or only cloud service?

### **🟢 10.2 Decision Log**
- Use MLflow, not DVC, for experiment tracking and registry.
- Serve ONNX models with ONNXRuntime for low latency.
- Secrets stay in env; non-secret config in repo.

---

### References
- Volve drilling data (CSV, real-time): `https://www.ux.uis.no/~atunkiel/file_list.html?utm_source=chatgpt.com`
- MLflow docs: `https://mlflow.org`
- ONNX Runtime: `https://onnxruntime.ai/docs`
- FastAPI: `https://fastapi.tiangolo.com`

