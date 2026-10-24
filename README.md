# 🗄️ Tiered Storage Cache (tieredcache)

### Multi-Tier (SSD + HDD) LRU Storage Cache with I/O Backpressure Prioritization

[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg?logo=python&logoColor=white)](https://python.org)
[![Storage](https://img.shields.io/badge/Architecture-Tiered%20Storage%20(SSD%20%2B%20HDD)-blue.svg)](https://github.com/Kaio-Comk/Tiered-Storage-Cache)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Maximize storage efficiency on low-cost media servers.**  
*Combines blazing-fast NVMe/SSD hot caching with mass-capacity cold HDDs, automated LRU demotion, and live I/O backpressure throttling.*

---

## 🏗️ Architecture

```mermaid
flowchart TD
    Req["🎬 Stream Request"] --> Hot{"Item in Hot Tier (Fast NVMe)?"}
    Hot -->|Hit| ServeHot["⚡ Immediate Low-Latency Playback"]
    Hot -->|Miss| Cold{"Item in Cold Tier (Bulk HDD)?"}
    Cold -->|Hit| ServeCold["💾 Stream from Mass Storage"]
    Cold -->|Miss| Ingest["📥 Fetch from Network / Upstream"]
    
    Ingest --> StoreHot["🔥 Store to Hot SSD"]
    StoreHot --> Overquota{"Hot Tier Exceeds Max Quota?"}
    Overquota -->|Yes| Demote["📉 Demote Least Recently Used (LRU) to Cold HDD"]
    
    ServeHot & ServeCold --> Backpressure["🛑 Signal Backpressure Controller"]
    Backpressure --> PauseWorkers["⏸️ Pause Background Bulk Downloaders"]
```

---

## 📦 Installation

```bash
pip install git+https://github.com/Kaio-Comk/Tiered-Storage-Cache.git
```
