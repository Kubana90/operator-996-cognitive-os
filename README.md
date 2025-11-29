[README.md](https://github.com/user-attachments/files/23832862/README.md)
# 🧠 Operator-996 Cognitive OS

**Full-Stack Behavioral Analysis & Real-time Pattern Recognition System**

A production-ready, self-hosted cognitive profiling platform built with **React + FastAPI + Docker** for advanced pattern detection, anomaly scanning, and decision simulation.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Usage Guide](#usage-guide)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Extension Guide](#extension-guide)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**Operator-996 Cognitive OS** is a behavioral analysis system designed for high-performer profiling. It:

1. **Seeds with known Operator-996 attributes** (IQ 140+, strategic thinking, pattern recognition, etc.)
2. **Logs behavioral events** (decisions, projects, communications, interactions)
3. **Detects recurring patterns** through multi-dimensional analysis
4. **Scans for anomalies** (bias detection, contradictions, consistency checks)
5. **Simulates hypothetical scenarios** using learned decision patterns
6. **Provides semantic search** across profile and behavioral history
7. **Exports complete profiles** as JSON for external analysis or backup

---

## ✨ Features

### Core Modules

#### 1. **Cognitive Profile Canvas**
- Visualizes 7 dimensions of cognitive attributes:
  - **Cognitive**: IQ, pattern recognition, systems thinking, strategic depth, abstraction, meta-cognition
  - **Behavioral**: Risk tolerance, experimentation, complexity comfort, control optimization, honesty, innovation
  - **Communication**: Directness, provocation tolerance, substance preference, manipulation sensitivity, depth-seeking
  - **Shadow**: Cognitive overload risk, perfectionism, control tendency, rumination, trust deficit, emotional volatility
  - **Domains**: AI integration, full-stack dev, EM research, trading analytics, 3D modeling, business strategy, psychology

#### 2. **Behavioral Event Logger**
- Import/log events of 4 types:
  - **Decision**: Strategic choices with reasoning
  - **Project**: Deliverables with domain tags
  - **Interaction**: Collaboration/conflict events
  - **Communication**: Direct/indirect exchanges
- Timestamp, decision logic, and outcome tracking
- Real-time event timeline visualization

#### 3. **Pattern Detection Engine**
- **Automatic pattern recognition**:
  - Decision logic consistency analysis
  - Project domain clustering
  - Communication signature detection
  - Emerging pattern identification
- Confidence scoring (0-1 scale)
- Supporting/contradicting events tracking

#### 4. **Bias & Contradiction Scanner**
- **Anomaly Detection Types**:
  - Logic contradictions between events
  - Perfectionism vs. completion rate analysis
  - Pattern violations
  - Cognitive overload signals
- Severity scoring
- Actionable recommendations

#### 5. **Scenario Simulation Engine**
- Predicts operator decision in hypothetical scenarios
- Based on documented behavioral patterns
- Confidence scoring
- Alternative path suggestions
- Cognitive load assessment
- Bias warnings

#### 6. **Semantic Search**
- Natural language queries across profile and events
- Powered by sentence-transformers embeddings
- Similarity scoring
- Multi-source results (events, patterns)

#### 7. **Real-time WebSocket Updates**
- Live pattern detection
- Anomaly alerts
- Bidirectional communication
- Zero-latency streaming

---

## 🏗️ Architecture

### System Diagram

```
┌─────────────────────────────────────────────────────┐
│        OPERATOR-996 COGNITIVE OS                    │
│  Full-Stack Behavioral Analysis Platform            │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │     React Frontend Dashboard                │   │
│  ├─────────────────────────────────────────────┤   │
│  │ • Profile Visualization                     │   │
│  │ • Event Logger & Timeline                   │   │
│  │ • Pattern Cards                             │   │
│  │ • Anomaly Reports                           │   │
│  │ • Scenario Simulator                        │   │
│  │ • Semantic Search                           │   │
│  │ • Settings & Export                         │   │
│  └─────────────────────────────────────────────┘   │
│                    ↕ (REST + WebSocket)            │
│  ┌─────────────────────────────────────────────┐   │
│  │     FastAPI Backend Engine                  │   │
│  ├─────────────────────────────────────────────┤   │
│  │ • CognitiveOS Core Class                    │   │
│  │ • Pattern Analysis ML                       │   │
│  │ • Anomaly Detection (IsolationForest)       │   │
│  │ • Semantic Embeddings                       │   │
│  │ • WebSocket Handler                         │   │
│  │ • Data Import/Export                        │   │
│  └─────────────────────────────────────────────┘   │
│                    ↕ (File I/O)                    │
│  ┌─────────────────────────────────────────────┐   │
│  │     Data Layer (In-Memory + Optional DB)    │   │
│  ├─────────────────────────────────────────────┤   │
│  │ • Seed Profile (Operator-996 attributes)    │   │
│  │ • Behavioral Events (JSON)                  │   │
│  │ • Pattern Cache                             │   │
│  │ • Anomaly Log                               │   │
│  │ • [Optional] PostgreSQL                     │   │
│  │ • [Optional] Redis Cache                    │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
├─────────────────────────────────────────────────────┤
│ Deployment: Docker Compose (Local/Cloud)          │
│ Frontend: port 3000 | Backend: port 8000          │
└─────────────────────────────────────────────────────┘
```

### Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | React 18+ | Interactive dashboard, real-time UI |
| **Backend** | FastAPI + Uvicorn | Async REST API, WebSocket server |
| **ML** | scikit-learn | Pattern detection, anomaly detection |
| **NLP** | sentence-transformers | Semantic embeddings, similarity search |
| **Container** | Docker + Docker Compose | Multi-container orchestration |
| **Data** | JSON (in-memory) | Event/pattern storage |
| **Optional** | PostgreSQL | Persistent analytics |
| **Optional** | Redis | Real-time caching |

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose (v20.10+)
- OR: Python 3.11+, Node.js 18+

### Option 1: Docker (Recommended)

```bash
# Clone or extract project
cd operator-996-os

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn backend_main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm start
```

---

## 🎮 Demo Mode (Quick Test)

Want to see the system in action immediately?

### Option 1: Auto-Import Sample Data (Recommended)

```bash
# Start the system
docker-compose up -d

# Import 50+ realistic behavioral events
cd operator-996-os/backend
python import_sample_data.py

# Open dashboard
open http://localhost:3000
```

### Option 2: Frontend Demo Button

1. Start the system: `docker-compose up -d`
2. Open http://localhost:3000
3. Go to **Settings** tab
4. Click **🎮 Load Demo Data (50+ Events)**
5. Dashboard will auto-refresh with populated data

### Option 3: Manual API Import

```bash
curl -X POST http://localhost:8000/import/sample-data
```

**What you'll see:**
- ✅ Populated dashboard with events timeline
- ✅ Detected patterns (decision frameworks, domain clusters)
- ✅ Anomaly reports (contradictions, perfectionism signals)
- ✅ Semantic search results
- ✅ Scenario simulation with learned behavior

**Sample Events Include:**
- Strategic AI/ML project decisions
- Full-stack development deliverables
- Trading algorithm implementations
- Technical debates and collaborations
- Direct communication patterns

---

## 📦 Installation

### File Structure

```
operator-996-os/
├── backend/
│   ├── backend_main.py          # FastAPI app & CognitiveOS engine
│   ├── requirements.txt          # Python dependencies
│   └── Dockerfile               # Backend container
├── frontend/
│   ├── App.jsx                  # Main React component
│   ├── App.css                  # Styles
│   ├── index.jsx                # React entry point
│   ├── package.json             # Node dependencies
│   └── Dockerfile               # Frontend build
├── docker-compose.yml           # Multi-container orchestration
├── README.md                    # This file
└── DEPLOYMENT.md                # Advanced deployment guide
```

### Dependencies

**Backend (Python 3.11+)**

```
fastapi==0.104.1
uvicorn==0.24.0
pydantic==2.4.0
numpy==1.26.0
scikit-learn==1.3.2
sentence-transformers==2.2.2
python-multipart==0.0.6
python-dotenv==1.0.0
```

**Frontend (Node 18+)**

```
react==18.2.0
react-dom==18.2.0
axios==1.6.0
```

---

## 📡 API Documentation

### Base URL
- **Local**: `http://localhost:8000`
- **Production**: Configure in `docker-compose.yml`

### Endpoints

#### Health Check
```
GET /health
Response: { "status": "online", "operator": "Operator-996", "timestamp": "..." }
```

#### Profile Management

```
GET /profile
→ Returns current cognitive profile snapshot

POST /event/add
Body: {
  "event_type": "decision|project|interaction|communication",
  "description": "Event description",
  "timestamp": "2024-11-29T12:58:00Z",
  "decision_logic": "Optional reasoning",
  "outcome": "Optional result",
  "tags": ["tag1", "tag2"]
}
Response: { "event_id": "abc123...", "status": "logged" }

GET /events
Response: { "count": N, "events": [...] }
```

#### Analysis

```
POST /patterns/detect
→ Analyzes behavioral events for recurring patterns
Response: { "patterns": [...], "count": N, "timestamp": "..." }

POST /anomalies/detect
→ Scans for bias, contradictions, consistency violations
Response: { "anomalies": [...], "count": N, "timestamp": "..." }

POST /scenario/simulate
Body: { "scenario": "Describe hypothetical situation..." }
Response: {
  "scenario": "...",
  "predicted_decision": "...",
  "reasoning": "...",
  "confidence": 0.85,
  "alternative_paths": [...],
  "cognitive_load_assessment": "...",
  "bias_check": "..."
}

GET /search?q=query
→ Semantic search across profile and events
Response: { "query": "...", "results": [...], "count": N }
```

#### Data Management

```
POST /import/events
Multipart form: { "file": <JSON file> }
→ Bulk import behavioral events
Response: { "status": "success", "imported": N, "timestamp": "..." }

GET /export/full
→ Export complete profile snapshot as JSON
Response: {
  "metadata": {...},
  "profile": {...},
  "behavioral_events": [...],
  "patterns": [...],
  "anomalies": [...]
}
```

#### WebSocket

```
WS ws://localhost:8000/ws/live
Messages:
  → "ping"       (heartbeat)
  → "patterns"   (request pattern update)
  → "anomalies"  (request anomaly scan)
```

---

## 🎮 Usage Guide

### 1. Dashboard Overview

On load, the dashboard displays:
- **Status bar**: Total events, patterns, anomalies
- **Cognitive profile**: 4 attribute categories + 7 domain skills
- **Recent events**: Last 10 behavioral entries
- **Detected patterns**: Recurring themes
- **Anomalies**: Bias/contradiction alerts

### 2. Logging Behavioral Events

1. Navigate to **Event Logger** tab
2. Select event type: Decision | Project | Interaction | Communication
3. Describe the event in **Description** field
4. (Optional) Add decision logic/reasoning
5. Click **Log Event** → Saved and timestamped
6. Click **Detect Patterns** to re-analyze

### 3. Pattern Analysis

1. Go to **Analytics** tab
2. Review **Detected Patterns** section on main dashboard
3. Each pattern shows:
   - Name and confidence score
   - Supporting themes/domains
   - Number of events contributing
4. Patterns update in real-time via WebSocket

### 4. Anomaly Scanning

1. In **Analytics**, click **🔎 Scan for Anomalies**
2. View anomaly cards with:
   - Type (contradiction, perfectionism_overreach, etc.)
   - Severity indicator (0-1)
   - Explanation
   - Recommended action

### 5. Scenario Simulation

1. Go to **Analytics** tab
2. In "Hypothetical Scenario Simulator" box:
   - Describe a scenario
   - Click **🚀 Simulate Decision**
3. Get prediction with:
   - Expected operator decision
   - Confidence score
   - Alternative paths
   - Cognitive load assessment
   - Bias warnings

### 6. Semantic Search

1. Go to **Analytics** tab
2. In "Semantic Search" box:
   - Enter natural language query (e.g., "decision related to AI")
   - Press Enter or click button
3. Results appear in browser console:
   - Source (event or pattern)
   - Content
   - Similarity score (0-1)

### 7. Data Export

1. Go to **Settings** tab
2. Click **📥 Export Full Profile (JSON)**
3. Browser downloads: `operator996_profile_YYYY-MM-DD.json`
4. Contains all events, patterns, anomalies, and metadata

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1

# Frontend
REACT_APP_API_BASE=http://localhost:8000

# Database (optional)
DATABASE_URL=postgresql://user:pass@db:5432/cognitive_os
REDIS_URL=redis://redis:6379/0

# API Keys (for future integrations)
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=ppl-...
```

### Customizing Profile Seed

Edit `backend_main.py`, function `_init_seed_profile()`:

```python
def _init_seed_profile(self):
    """Initialize with known Operator-996 attributes"""
    self.profile = {
        "cognitive": {
            "iq_percentile": 0.98,           # Customize here
            "pattern_recognition": 0.95,
            # ... etc
        },
        # ...
    }
```

---

## 🌐 Deployment

### Docker Production

```bash
# Build multi-stage image
docker-compose build

# Run in production mode
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Scale backend (if using multiple instances)
docker-compose up -d --scale backend=3
```

### Cloud Deployment (AWS, GCP, Azure)

1. **Build Docker images**:
   ```bash
   docker build -t operator996-backend ./backend
   docker build -t operator996-frontend ./frontend
   ```

2. **Push to registry** (Docker Hub, ECR, GCR):
   ```bash
   docker tag operator996-backend myregistry/operator996-backend:latest
   docker push myregistry/operator996-backend:latest
   ```

3. **Deploy with Kubernetes**:
   - Create `k8s/deployment.yaml` (see DEPLOYMENT.md)
   - `kubectl apply -f k8s/`

4. **Setup domain & SSL**:
   - Configure DNS for `operator996.yourdomain.com`
   - Enable HTTPS with Let's Encrypt

---

## 🔧 Extension Guide

### Adding New Pattern Detectors

In `backend_main.py`, `CognitiveOS.detect_patterns()`:

```python
def detect_patterns(self) -> List[Dict[str, Any]]:
    # ... existing patterns ...
    
    # NEW: Risk Appetite Pattern
    risky_decisions = [e for e in self.behavioral_events 
                       if 'risk' in e.get('tags', [])]
    if len(risky_decisions) >= 2:
        patterns_found.append({
            "name": "Risk Appetite Profile",
            "confidence": 0.88,
            "count": len(risky_decisions),
            "characteristics": ["high_risk_tolerance", "experimentation_bias"]
        })
    
    return patterns_found
```

### Custom Anomaly Detectors

```python
def detect_anomalies(self) -> List[Dict[str, Any]]:
    # NEW: Goal Abandonment Pattern
    if len(self.behavioral_events) > 10:
        projects = [e for e in self.behavioral_events 
                   if e['event_type'] == 'project']
        completed = [e for e in projects if e['outcome'] == 'completed']
        abandoned = len(projects) - len(completed)
        
        if abandoned / len(projects) > 0.5:
            anomalies.append({
                "timestamp": datetime.now().isoformat(),
                "anomaly_type": "goal_abandonment",
                "severity": 0.75,
                "explanation": f"High project abandonment rate: {abandoned}/{len(projects)}",
                "recommendation": "Implement milestone-based checkpoints"
            })
    
    return anomalies
```

### Integrating External APIs

**Example: Perplexity API for enhanced reasoning**

```python
import requests

class CognitiveOS:
    def __init__(self, perplexity_key=None):
        # ... existing init ...
        self.perplexity_key = perplexity_key
    
    async def enhanced_scenario_simulation(self, scenario: str) -> Dict:
        if not self.perplexity_key:
            return {"error": "Perplexity API key not configured"}
        
        # Call Perplexity for intelligent reasoning
        headers = {"Authorization": f"Bearer {self.perplexity_key}"}
        payload = {
            "model": "pplx-7b-online",
            "messages": [{
                "role": "user",
                "content": f"Given Operator-996 profile, predict decision: {scenario}"
            }]
        }
        
        response = requests.post(
            "https://api.perplexity.ai/chat/completions",
            json=payload,
            headers=headers
        )
        
        return response.json()
```

### Adding Hardware Integration (EEG/HRV)

```python
# WebRTC/BLE handler for biometric sensors
@app.websocket("/ws/biometric")
async def biometric_stream(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        data = await websocket.receive_json()
        
        # Parse sensor data
        sensor_type = data.get("type")  # "eeg", "hrv", "gsr"
        values = data.get("values")
        
        # Create biometric event
        os_engine.add_behavioral_event(BehavioralEvent(
            event_type="biometric",
            description=f"{sensor_type} reading: {values}",
            timestamp=datetime.now().isoformat(),
            tags=[sensor_type, "physiological"]
        ))
        
        # Trigger anomaly detection
        anomalies = os_engine.detect_anomalies()
        
        await websocket.send_json({
            "type": "biometric_processed",
            "anomalies": anomalies
        })
```

---

## 🐛 Troubleshooting

### Backend fails to start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
cd backend
pip install -r requirements.txt
```

**Error**: `Port 8000 already in use`

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000
# Kill it
kill -9 <PID>

# Or use different port in docker-compose.yml:
# ports:
#   - "8001:8000"
```

### Frontend can't connect to backend

**Error**: `WebSocket is closed before the connection is established`

**Solution**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check `REACT_APP_API_BASE` in frontend settings
3. If using Docker, ensure containers are on same network:
   ```bash
   docker-compose ps
   docker network inspect operator996-os_operator996-network
   ```

### Pattern detection returns empty

**Error**: No patterns detected even with events logged

**Cause**: Not enough events (minimum 2-3 per pattern type)

**Solution**:
1. Log more behavioral events
2. Ensure tags match pattern detection logic
3. Check backend logs:
   ```bash
   docker-compose logs backend | grep "Detected"
   ```

### Semantic search not working

**Error**: `AttributeError: module 'sentence_transformers' not found`

**Solution**:
```bash
pip install sentence-transformers torch
```

(First time download is ~500MB)

### WebSocket connection drops

**Cause**: Network timeout or backend crash

**Solution**:
1. Increase timeout in frontend:
   ```javascript
   const connectWebSocket = () => {
     const ws = new WebSocket(`${apiBase.replace(/^http/, 'ws')}/ws/live`);
     // Add reconnect logic
     ws.onclose = () => setTimeout(connectWebSocket, 5000);
   }
   ```

2. Monitor backend health:
   ```bash
   curl http://localhost:8000/health
   ```

---

## 📚 Additional Resources

- **API Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **OpenAPI Schema**: `http://localhost:8000/openapi.json`
- **React Component Docs**: See code comments in `App.jsx`
- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **scikit-learn ML**: https://scikit-learn.org/

---

## 📝 License & Notes

**Operator-996 Cognitive OS v1.0.0**

Built for advanced behavioral analysis with:
- ✅ No browser storage (privacy-first)
- ✅ Full export capability (data ownership)
- ✅ Modular architecture (extensible)
- ✅ Production-ready (Docker + API)
- ✅ Semantic AI integration (future-proof)

**Disclaimer**: This system provides analytical insights based on documented behavior. It is **NOT** a substitute for professional psychological evaluation or clinical assessment. Use responsibly.

---

**Next Steps**:
1. Run: `docker-compose up -d`
2. Open: http://localhost:3000
3. Log events in "Event Logger" tab
4. Review patterns and anomalies on Dashboard
5. Export profile when ready


