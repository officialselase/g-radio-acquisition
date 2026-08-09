# G-Radio Acquisition Framework (GRAF) - Operational Guide

**Project**: Rob-GhanaRadio  
**Dataset**: G-Radio  
**Specification**: G-Radio Metadata Specification (GRMS-1.0)  
**Author**: Selase K. Agbai  

---

## 1. Introduction & Overview

The **G-Radio Acquisition Framework (GRAF)** is a research-grade data acquisition and processing framework built to harvest, validate, annotate, and process high-interference Ghanaian live radio broadcasts.

GRAF powers the **G-Radio dataset** and is designed to seamlessly evolve into the production audio recognition pipeline powering **Zamio**.

---

## 2. Quick Start & Setup Verification

### Check System & Station Registry Status
Display framework configuration, storage directory hierarchy, detected FFmpeg binaries, and registered Ghanaian radio stations:
```bash
python3 cli.py info
```

### List & Filter Ghanaian Radio Stations
```bash
# List all 8 pre-configured Ghanaian stations
python3 cli.py stations

# Filter by broadcast language (e.g. Twi, English)
python3 cli.py stations --language Twi

# Filter by city (e.g. Accra, Kumasi)
python3 cli.py stations --city Accra
```

---

## 3. Step-by-Step Dataset Acquisition Workflow

### Step 1: Run a Test Recording (Single Segment Sanity Check)
Always run a short test recording to verify stream connectivity, FFprobe properties, SHA256 provenance hashing, and GRMS-1.0 metadata output:

```bash
python3 cli.py test-record --station-id peace_fm --duration 30
```

**What GRAF does during test recording:**
1. Connects to **Peace FM 104.3 FM** live stream.
2. Captures 30 seconds directly without re-encoding (`-c copy`) to preserve raw stream fidelity.
3. Saves raw audio to `storage/raw/peace_fm_YYYYMMDD_HHMMSS.mp3`.
4. Probes stream properties via `ffprobe` (codec, sample rate, bit rate, channels).
5. Computes SHA256 and MD5 cryptographic checksums for data provenance.
6. Generates matching **GRMS-1.0 JSON metadata** in `storage/metadata/peace_fm_YYYYMMDD_HHMMSS.json`.
7. Runs automated QA validation on the segment.

---

### Step 2: Launch Continuous Multi-Station Dataset Acquisition

GRAF records continuously, automatically splitting audio into **10-minute segments** (600s) with exponential backoff reconnect loops if network interruptions occur.

#### Option A: Record All Active Stations Simultaneously
```bash
python3 cli.py record
```

#### Option B: Record Specific Stations
```bash
python3 cli.py record --stations peace_fm,citi_fm,joy_fm
```

#### Option C: 24/7 Long-Running Background Recording
For continuous multi-day dataset acquisition, run GRAF as a background daemon using `nohup` or `tmux`:

```bash
# Launch background acquisition daemon
nohup python3 cli.py record > storage/logs/graf_daemon.log 2>&1 &

# Verify background process is running
ps aux | grep cli.py

# Monitor live acquisition logs
tail -f storage/logs/capture.log
```

To stop background acquisition:
```bash
kill $(pgrep -f "cli.py record")
```

---

### Step 3: Automated Quality Assurance & Segment Validation

Run batch QA validation across all raw audio segments in `storage/raw/`:

```bash
python3 cli.py validate
```

**Validation Checks Performed:**
- **Non-zero byte check**: Ensures files are non-empty.
- **FFprobe stream syntax**: Validates audio stream header integrity.
- **SHA256 checksum matching**: Verifies data provenance.
- **Auto-Quarantine**: Any corrupted or incomplete segment is automatically moved to `storage/failed/` to prevent contamination of research models.

---

### Step 4: Execute Downstream Machine Learning Pipeline

Once raw audio segments pass QA validation, run the ML processing pipeline to compute annotations, source separation, and neural fingerprint embeddings:

```bash
python3 cli.py pipeline
```

**Pipeline Stages Executed:**
1. **Music Detection Stage**: Computes Speech-to-Music Ratio (SMR) and flags music vs speech content.
2. **Source Separation Stage**: Separates presenter voice/jingles from background music stems.
3. **Neural Fingerprinting Stage**: Generates 128-dimensional continuous neural audio embeddings.
4. **Benchmarking Stage**: Evaluates retrieval accuracy and logs metrics into GRMS metadata.

All outputs update the matching `GRMS-1.0` JSON record in `storage/metadata/`.

---

## 4. Cloud Model Training & Deployment Workflow (Kaggle & Hugging Face)

Once dataset segments pass QA validation in Step 3, model training (Demucs-v4 source separation and contrastive neural fingerprint encoder) can be offloaded to cloud GPU infrastructure (Kaggle, Hugging Face, or Colab).

```
   Local Acquisition           Dataset Hub                 Cloud GPU Cluster               Local Pipeline
+--------------------+     +------------------+     +----------------------------+     +------------------+
| GRAF `storage/raw` | ──► | Hugging Face /   | ──► | Kaggle / Colab (NVIDIA T4) | ──► | `cli.py pipeline`|
| GRMS Metadata      |     | Kaggle Datasets  |     | PyTorch Model Training     |     | Model Weights    |
+--------------------+     +------------------+     +----------------------------+     +------------------+
```

### 4.1 Exporting Dataset to Kaggle Datasets

1. Install and configure Kaggle CLI:
   ```bash
   pip install kaggle
   # Ensure ~/.kaggle/kaggle.json contains your API token
   ```

2. Package validated raw audio and GRMS-1.0 metadata sidecars:
   ```bash
   # Initialize Kaggle dataset metadata in storage directory
   kaggle datasets init -p storage/
   ```

3. Create and upload dataset to Kaggle:
   ```bash
   kaggle datasets create -p storage/ --public
   ```

4. Attach the uploaded dataset to a Kaggle GPU Notebook (30 hours/week free NVIDIA T4/P100 GPUs) to train Demucs-v4 or the 128-D Neural Audio Fingerprint Encoder.

### 4.2 Publishing & Streaming via Hugging Face Hub

1. Log into Hugging Face CLI:
   ```bash
   huggingface-cli login
   ```

2. Stream or push raw audio & GRMS-1.0 metadata using Python:
   ```python
   from datasets import Dataset, Audio
   from pathlib import Path
   import json

   raw_dir = Path("storage/raw")
   meta_dir = Path("storage/metadata")

   records = []
   for mp3 in raw_dir.glob("*.mp3"):
       sidecar = meta_dir / f"{mp3.stem}.json"
       if sidecar.exists():
           with open(sidecar) as f:
               meta = json.load(f)
           records.append({
               "audio": str(mp3.absolute()),
               "station_id": meta["station"]["id"],
               "speech_music_ratio": meta["machine_learning"].get("speech_music_ratio", 1.0),
               "sha256": meta["file"]["sha256"]
           })

   ds = Dataset.from_list(records).cast_column("audio", Audio(sampling_rate=44100))
   ds.push_to_hub("username/ghana-radio-dataset")
   ```

### 4.3 Downloading Trained Checkpoints back to GRAF

After fine-tuning Demucs-v4 or training the neural fingerprint encoder on Kaggle or Hugging Face:
1. Download trained checkpoint weights (`.pt` or `.safetensors`) into `graf/pipeline/models/`.
2. Run local downstream inference and evaluation:
   ```bash
   python3 cli.py pipeline
   ```

---

## 5. Directory Hierarchy & Dataset Storage Structure

```
g-radio-acquisition/
├── OPERATIONAL_GUIDE.md # This operational guide
├── RESEARCH_PAPER.md    # Academic research paper draft
├── cli.py               # Main Command Line Interface
├── main.py              # Entrypoint wrapper script
├── config.py            # Top-level configuration wrapper
├── logger.py            # Logging module wrapper
├── metadata.py          # GRMS-1.0 metadata wrapper
├── stations/
│   └── ghana_stations.json # Active Ghanaian radio station registry
├── graf/                # Core GRAF Python package
│   ├── config.py        # Typed dataclass config & env overrides
│   ├── logger.py        # Rotating file & console logger
│   ├── metadata/        # GRMS-1.0 models, builder & schema
│   ├── acquisition/     # Stream recorder & multi-station manager
│   ├── validation/      # Segment QA validator & quarantine engine
│   ├── pipeline/        # ML pipeline stages (VAD, Separation, Fingerprinting)
│   └── utils/           # System profiler & audio utilities
├── tests/               # Pytest & unittest test suite
└── storage/             # Dataset storage hierarchy (.gitignore guarded)
    ├── raw/             # Raw audio segments ({station_id}_{YYYYMMDD}_{HHMMSS}.mp3)
    ├── metadata/        # GRMS-1.0 JSON records ({station_id}_{YYYYMMDD}_{HHMMSS}.json)
    ├── logs/            # Daily execution logs (capture.log, errors.log)
    ├── failed/          # Quarantined corrupt audio segments
    ├── reports/         # Dataset summary manifests & statistics
    ├── annotations/     # Ground-truth human annotations
    └── temp/            # Temporary scratch files
```

---

## 6. Adding Custom Radio Stations

To add new Ghanaian radio streams to the framework, open `stations/ghana_stations.json` and append a new station configuration object:

```json
{
  "id": "omutu_fm",
  "name": "Omutu FM",
  "frequency": "98.1 FM",
  "city": "Accra",
  "region": "Greater Accra",
  "country": "Ghana",
  "stream_url": "https://stream.example.com/live",
  "fallback_urls": [],
  "broadcast_type": "FM",
  "languages": ["Twi", "Ga"],
  "genre": "Highlife / Talk",
  "owner": "Independent",
  "active": true
}
```

---

## 7. Advanced Configuration via Environment Variables

All parameters can be overridden at runtime without code changes:

```bash
# Record in 30-minute (1800s) segments
GRAF_SEGMENT_DURATION=1800 python3 cli.py record

# Custom FFmpeg binary path
GRAF_FFMPEG_BINARY=/usr/local/bin/ffmpeg python3 cli.py record

# Custom audio bit rate
GRAF_BIT_RATE=192000 python3 cli.py record
```

---

## 8. Running Unit Tests

Run the complete automated test suite to ensure system integrity:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

