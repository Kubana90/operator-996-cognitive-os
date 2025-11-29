# 🚀 Advanced Deployment & Extension Guide

## Operator-996 Cognitive OS: Production Setup & Custom Features

---

## Phase 1: Production Deployment

### 1.1 Local Docker Deployment (Recommended for First-Time)

```bash
# Clone repository
git clone <repo-url>
cd operator-996-os

# Build and start
docker-compose up -d --build

# Verify services
docker-compose ps
# Expected output:
# operator996-backend   Up (Healthy)
# operator996-frontend  Up

# Access application
# Frontend:   http://localhost:3000
# Backend:    http://localhost:8000
# API Docs:   http://localhost:8000/docs (Swagger UI)
```

### 1.2 Environment Configuration

Create `.env` file in project root:

```bash
# BACKEND SETTINGS
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1

# FRONTEND SETTINGS
REACT_APP_API_BASE=http://localhost:8000
REACT_APP_ENVIRONMENT=development

# OPTIONAL: Database (PostgreSQL)
DATABASE_URL=postgresql://operator996:SecurePass123!@db:5432/cognitive_os
DATABASE_POOL_SIZE=10

# OPTIONAL: Redis Caching
REDIS_URL=redis://redis:6379/0
REDIS_EXPIRATION=3600

# API INTEGRATIONS (Future)
OPENAI_API_KEY=sk-...
PERPLEXITY_API_KEY=ppl-...
TWELVEDATA_API_KEY=...
```

Update `docker-compose.yml` to use environment file:

```yaml
services:
  backend:
    env_file: .env
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - REDIS_URL=${REDIS_URL}
```

### 1.3 Production Security Hardening

#### Update docker-compose.yml:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: operator996-backend
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
      - LOG_LEVEL=WARNING  # Reduce verbosity
    volumes:
      - ./backend:/app/backend
    networks:
      - operator996-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    # Add resource limits
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: operator996-frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - operator996-network
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M

networks:
  operator996-network:
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br_op996
```

### 1.4 SSL/HTTPS Setup (Let's Encrypt)

Create `nginx.conf` for HTTPS:

```nginx
events {
  worker_connections 1024;
}

http {
  upstream backend {
    server backend:8000;
  }

  # Redirect HTTP to HTTPS
  server {
    listen 80;
    server_name operator996.yourdomain.com;
    
    location /.well-known/acme-challenge/ {
      root /var/www/certbot;
    }
    
    location / {
      return 301 https://$host$request_uri;
    }
  }

  # HTTPS server
  server {
    listen 443 ssl http2;
    server_name operator996.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/operator996.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/operator996.yourdomain.com/privkey.pem;
    
    # Modern SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Frontend
    location / {
      root /usr/share/nginx/html;
      index index.html;
      try_files $uri $uri/ /index.html;
    }

    # Backend proxy
    location /api/ {
      proxy_pass http://backend;
      proxy_set_header Host $host;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto $scheme;
    }

    # WebSocket support
    location /ws {
      proxy_pass http://backend;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";
      proxy_set_header Host $host;
    }
  }
}
```

---

## Phase 2: Cloud Deployment

### 2.1 AWS ECS/Fargate Deployment

Create `ecs-task-definition.json`:

```json
{
  "family": "operator-996-cognitive-os",
  "containerDefinitions": [
    {
      "name": "operator996-backend",
      "image": "YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/operator996-backend:latest",
      "portMappings": [
        {
          "containerPort": 8000,
          "protocol": "tcp"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/operator-996-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      },
      "environment": [
        {
          "name": "LOG_LEVEL",
          "value": "INFO"
        }
      ],
      "essential": true
    },
    {
      "name": "operator996-frontend",
      "image": "YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/operator996-frontend:latest",
      "portMappings": [
        {
          "containerPort": 80,
          "protocol": "tcp"
        }
      ],
      "essential": true
    }
  ],
  "requiresCompatibilities": ["FARGATE"],
  "networkMode": "awsvpc",
  "cpu": "1024",
  "memory": "2048"
}
```

Deploy to AWS:

```bash
# Push images to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

docker build -t operator996-backend ./backend
docker tag operator996-backend:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/operator996-backend:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/operator996-backend:latest

# Register task definition
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create ECS service
aws ecs create-service \
  --cluster operator996-cluster \
  --service-name operator996-service \
  --task-definition operator-996-cognitive-os:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx]}
```

### 2.2 Google Cloud Run Deployment

```bash
# Build and push to GCR
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/operator996-backend ./backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/operator996-frontend ./frontend

# Deploy backend
gcloud run deploy operator996-backend \
  --image gcr.io/YOUR_PROJECT_ID/operator996-backend \
  --platform managed \
  --region us-central1 \
  --memory 2Gi \
  --cpu 2 \
  --allow-unauthenticated

# Deploy frontend
gcloud run deploy operator996-frontend \
  --image gcr.io/YOUR_PROJECT_ID/operator996-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 2.3 Azure Container Instances

```bash
# Create resource group
az group create --name operator996-rg --location eastus

# Create ACR
az acr create --resource-group operator996-rg \
  --name operator996acr \
  --sku Basic

# Push image
az acr build --registry operator996acr \
  --image operator996-backend:latest ./backend

# Deploy container
az container create \
  --resource-group operator996-rg \
  --name operator996-backend \
  --image operator996acr.azurecr.io/operator996-backend:latest \
  --ports 8000 \
  --environment-variables LOG_LEVEL=INFO
```

---

## Phase 3: Advanced Feature Extensions

### 3.1 PostgreSQL Integration

Edit `backend_main.py`:

```python
from sqlalchemy import create_engine, Column, String, Float, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./cognitive_os.db")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define models
class BehavioralEventDB(Base):
    __tablename__ = "behavioral_events"
    
    id = Column(String, primary_key=True)
    event_type = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    decision_logic = Column(String)
    outcome = Column(String)
    tags = Column(JSON)
    metadata = Column(JSON)

class PatternDB(Base):
    __tablename__ = "patterns"
    
    pattern_id = Column(String, primary_key=True)
    name = Column(String)
    confidence = Column(Float)
    events_count = Column(int)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Modify CognitiveOS to use database
class CognitiveOSDB(CognitiveOS):
    def __init__(self):
        super().__init__()
        self.db = SessionLocal()
    
    def add_behavioral_event_db(self, event: BehavioralEvent) -> str:
        event_id = super().add_behavioral_event(event)
        
        db_event = BehavioralEventDB(
            id=event_id,
            event_type=event.event_type,
            description=event.description,
            decision_logic=event.decision_logic,
            tags=event.tags
        )
        self.db.add(db_event)
        self.db.commit()
        
        return event_id
```

### 3.2 Redis Caching

```python
import redis
import json

redis_client = redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379/0"))

class CognitiveOSCached(CognitiveOS):
    def detect_patterns(self) -> List[Dict[str, Any]]:
        cache_key = "patterns:latest"
        
        # Check cache
        cached = redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Compute and cache
        patterns = super().detect_patterns()
        redis_client.setex(cache_key, 3600, json.dumps(patterns))
        
        return patterns
```

### 3.3 Perplexity AI Integration

```python
import aiohttp

class CognitiveOSAI(CognitiveOS):
    async def enhanced_scenario_simulation(self, scenario: str) -> Dict:
        perplexity_key = os.getenv("PERPLEXITY_API_KEY")
        
        if not perplexity_key:
            return await super().scenario_simulation(scenario)
        
        async with aiohttp.ClientSession() as session:
            headers = {"Authorization": f"Bearer {perplexity_key}"}
            payload = {
                "model": "pplx-7b-online",
                "messages": [{
                    "role": "user",
                    "content": f"""
Given this Operator-996 profile (IQ 140+, systems thinker, innovation-focused, 
high risk tolerance, perfectionist tendencies, control-optimization driven),
predict decision in scenario:

{scenario}

Provide:
1. Predicted decision
2. Reasoning based on profile
3. Alternative paths
4. Risk assessment
5. Confidence score (0-1)
"""
                }]
            }
            
            async with session.post(
                "https://api.perplexity.ai/chat/completions",
                json=payload,
                headers=headers
            ) as resp:
                data = await resp.json()
                response_text = data['choices'][0]['message']['content']
                
                return {
                    "scenario": scenario,
                    "ai_analysis": response_text,
                    "source": "perplexity"
                }
```

### 3.4 EEG/Biometric Integration (WebRTC)

```python
@app.websocket("/ws/biometric/stream")
async def biometric_stream(websocket: WebSocket):
    await websocket.accept()
    
    while True:
        try:
            data = await websocket.receive_json()
            
            sensor_type = data.get("type")  # "eeg", "hrv", "gsr"
            values = data.get("values", [])
            timestamp = data.get("timestamp", datetime.now().isoformat())
            
            # Create biometric event
            event = BehavioralEvent(
                event_type="biometric",
                description=f"{sensor_type}: {json.dumps(values)}",
                timestamp=timestamp,
                tags=[sensor_type, "physiological", "real-time"]
            )
            
            os_engine.add_behavioral_event(event)
            
            # Trigger anomaly detection if critical
            if sensor_type == "hrv" and any(v > 150 for v in values):
                anomalies = os_engine.detect_anomalies()
                await websocket.send_json({
                    "type": "cognitive_overload_warning",
                    "severity": 0.85,
                    "recommendation": "Take break, reduce cognitive load"
                })
            
        except Exception as e:
            logger.error(f"Biometric error: {e}")
            break
```

### 3.5 Advanced Visualization with Plotly

Add to `App.jsx`:

```javascript
import Plot from 'react-plotly.js';

const CognitiveProfileChart = ({ profile }) => {
  if (!profile) return null;

  const categories = [
    'IQ Percentile',
    'Pattern Recognition',
    'Systems Thinking',
    'Risk Tolerance',
    'Innovation Focus',
    'Complexity Comfort'
  ];

  const values = [
    profile.cognitive.iq_percentile * 100,
    profile.cognitive.pattern_recognition * 100,
    profile.cognitive.systems_thinking * 100,
    profile.behavioral.risk_tolerance * 100,
    profile.behavioral.innovation_focus * 100,
    profile.behavioral.complexity_comfort * 100
  ];

  return (
    <Plot
      data={[{
        r: values,
        theta: categories,
        fill: 'toself',
        type: 'scatterpolar'
      }]}
      layout={{
        polar: {
          radialaxis: {
            visible: true,
            range: [0, 100]
          }
        },
        title: 'Operator-996 Cognitive Profile'
      }}
    />
  );
};
```

---

## Phase 4: Monitoring & Observability

### 4.1 Prometheus Metrics

```python
from prometheus_client import Counter, Histogram, generate_latest

# Metrics
pattern_detections = Counter('pattern_detections_total', 'Total patterns detected')
anomaly_scans = Counter('anomaly_scans_total', 'Total anomaly scans')
api_request_duration = Histogram('api_request_duration_seconds', 'API request duration')

@app.get("/metrics")
async def metrics():
    return generate_latest()
```

### 4.2 Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

# File logging
file_handler = RotatingFileHandler('logs/operator996.log', maxBytes=10000000, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(file_handler)

# Console logging
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(console_handler)
```

---

## Phase 5: Troubleshooting & Optimization

### 5.1 Performance Tuning

```python
# Add caching decorator
from functools import lru_cache

@lru_cache(maxsize=128)
def get_profile_summary():
    """Cache profile summary for 5 minutes"""
    return os_engine.export_full_profile()

# Batch event processing
def batch_import_events(events: List[BehavioralEvent], batch_size=100):
    for i in range(0, len(events), batch_size):
        batch = events[i:i+batch_size]
        for event in batch:
            os_engine.add_behavioral_event(event)
        # Periodic pattern detection
        if i % 500 == 0:
            os_engine.detect_patterns()
```

### 5.2 Database Optimization

```sql
-- Create indexes for fast queries
CREATE INDEX idx_event_type ON behavioral_events(event_type);
CREATE INDEX idx_timestamp ON behavioral_events(timestamp);
CREATE INDEX idx_tags ON behavioral_events USING GIN(tags);

-- Partition events by month for large datasets
CREATE TABLE behavioral_events_2024_11 PARTITION OF behavioral_events
  FOR VALUES FROM ('2024-11-01') TO ('2024-12-01');
```

---

## Deployment Checklist

- [ ] Environment variables configured (.env file)
- [ ] Docker images built and tested locally
- [ ] SSL certificates (Let's Encrypt) configured
- [ ] Database migrations applied (if using PostgreSQL)
- [ ] Redis cache connected (if enabled)
- [ ] Monitoring/logging setup (Prometheus, ELK)
- [ ] Backup strategy in place (daily snapshots)
- [ ] Load balancer configured (if multi-instance)
- [ ] Rate limiting enabled on API
- [ ] CORS policies configured
- [ ] Documentation updated
- [ ] Disaster recovery plan documented

---

**Version**: 1.0.0
**Last Updated**: 2024-11-29
**Maintained By**: Operator-996 Development Team
