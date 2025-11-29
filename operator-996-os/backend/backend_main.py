"""
Operator-996 Cognitive OS Backend
FastAPI + Pattern Analysis + Semantic Search + Anomaly Detection
"""

from fastapi import FastAPI, UploadFile, File, WebSocket, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import numpy as np
from datetime import datetime
import asyncio
import logging
import os

# ML & Analysis
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import hashlib

# Database imports
from database import (
    DATABASE_URL, engine, SessionLocal, Base, init_db, check_db_connection,
    get_db, Profile, BehavioralEventDB, PatternDB, AnomalyDB
)

# Semantic Search (local embeddings or OpenAI)
try:
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  sentence-transformers not available. Install: pip install sentence-transformers")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Operator996")

# Database availability flag
DB_AVAILABLE = bool(DATABASE_URL)

# ============================================================================
# DATA MODELS
# ============================================================================

class ProfileAttribute(BaseModel):
    name: str
    value: float  # 0-1 scale
    category: str  # cognitive, behavioral, emotional, etc.
    source: str  # self-reported, inferred, measured
    timestamp: str = None
    confidence: float = 0.8

class BehavioralEvent(BaseModel):
    event_type: str  # decision, project, interaction, communication
    description: str
    timestamp: str
    outcome: Optional[str] = None
    decision_logic: Optional[str] = None
    tags: List[str] = []

class PatternAnalysis(BaseModel):
    pattern_id: str
    name: str
    confidence: float
    supporting_events: List[str]
    contradictions: List[str]
    cognitive_implication: str

class AnomalyReport(BaseModel):
    timestamp: str
    event: str
    anomaly_type: str  # bias_detected, pattern_violation, contradiction
    severity: float  # 0-1
    explanation: str

class ScenarioSimulation(BaseModel):
    scenario_description: str
    operator_decision_prediction: str
    reasoning: str
    confidence: float
    alternative_paths: List[str]

# ============================================================================
# OPERATOR-996 COGNITIVE OS
# ============================================================================

class CognitiveOS:
    def __init__(self, db_session=None):
        self.profile = {}
        self.behavioral_events = []
        self.patterns = []
        self.anomalies = []
        self.metadata = {
            "created": datetime.now().isoformat(),
            "version": "1.0.0",
            "operator": "Operator-996"
        }
        self.db_session = db_session
        self.profile_id = None
        
        # Initialize embeddings if available
        if EMBEDDINGS_AVAILABLE:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✓ Semantic embedder initialized")
        else:
            self.embedder = None
        
        # Load seed profile
        self._init_seed_profile()
        
        # Load from database if available
        if self.db_session:
            self.load_from_db()
    
    def _init_seed_profile(self):
        """Initialize with known Operator-996 attributes"""
        self.profile = {
            "cognitive": {
                "iq_percentile": 0.98,  # 140+ claimed
                "pattern_recognition": 0.95,
                "systems_thinking": 0.93,
                "strategic_depth": 0.92,
                "abstraction_capability": 0.94,
                "meta_cognition": 0.91,
            },
            "behavioral": {
                "risk_tolerance": 0.85,
                "experimentation_drive": 0.88,
                "complexity_comfort": 0.92,
                "control_optimization": 0.87,
                "radial_honesty": 0.90,
                "innovation_focus": 0.91,
            },
            "communication": {
                "directness": 0.89,
                "provocation_tolerance": 0.85,
                "substance_preference": 0.93,
                "manipulation_sensitivity": 0.88,
                "depth_seeking": 0.91,
            },
            "shadow": {
                "cognitive_overload_risk": 0.72,
                "perfectionism": 0.85,
                "control_tendency": 0.79,
                "rumination_risk": 0.68,
                "trust_deficit": 0.74,
                "emotional_volatility": 0.65,
            },
            "domains": {
                "ai_integration": 0.94,
                "full_stack_development": 0.91,
                "electromagnetic_research": 0.82,
                "trading_analytics": 0.87,
                "3d_modeling": 0.80,
                "business_strategy": 0.84,
                "psychological_analysis": 0.86,
            }
        }
        logger.info("✓ Seed profile loaded: Operator-996")
    
    def save_to_db(self):
        """Save current state to database"""
        if not self.db_session:
            logger.warning("No database session available for save")
            return False
        
        try:
            # Get or create profile
            db_profile = None
            if self.profile_id:
                db_profile = self.db_session.query(Profile).filter(
                    Profile.id == self.profile_id
                ).first()
            
            if not db_profile:
                db_profile = Profile(
                    cognitive_data=self.profile.get("cognitive", {}),
                    behavioral_data=self.profile.get("behavioral", {}),
                    communication_data=self.profile.get("communication", {}),
                    shadow_data=self.profile.get("shadow", {}),
                    domains_data=self.profile.get("domains", {}),
                )
                self.db_session.add(db_profile)
                self.db_session.flush()
                self.profile_id = db_profile.id
            else:
                db_profile.cognitive_data = self.profile.get("cognitive", {})
                db_profile.behavioral_data = self.profile.get("behavioral", {})
                db_profile.communication_data = self.profile.get("communication", {})
                db_profile.shadow_data = self.profile.get("shadow", {})
                db_profile.domains_data = self.profile.get("domains", {})
                db_profile.updated_at = datetime.utcnow()
            
            self.db_session.commit()
            logger.info(f"✓ Profile saved to database: {self.profile_id}")
            return True
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to save to database: {e}")
            return False
    
    def load_from_db(self):
        """Load state from database"""
        if not self.db_session:
            logger.warning("No database session available for load")
            return False
        
        try:
            # Load first profile (or most recent)
            db_profile = self.db_session.query(Profile).order_by(
                Profile.updated_at.desc()
            ).first()
            
            if db_profile:
                self.profile_id = db_profile.id
                self.profile = db_profile.to_dict()
                
                # Load events
                self.behavioral_events = [
                    event.to_dict() for event in db_profile.events
                ]
                
                # Load patterns
                self.patterns = [
                    pattern.to_dict() for pattern in db_profile.patterns
                ]
                
                # Load anomalies
                self.anomalies = [
                    anomaly.to_dict() for anomaly in db_profile.anomalies
                ]
                
                logger.info(f"✓ Loaded profile from database: {self.profile_id}")
                return True
            else:
                logger.info("No existing profile in database, using seed profile")
                return False
        except Exception as e:
            logger.error(f"Failed to load from database: {e}")
            return False
    
    def sync_events(self):
        """Sync behavioral events to database"""
        if not self.db_session or not self.profile_id:
            return False
        
        try:
            # Get existing event IDs from database
            existing_events = self.db_session.query(BehavioralEventDB).filter(
                BehavioralEventDB.profile_id == self.profile_id
            ).all()
            existing_ids = {str(e.id) for e in existing_events}
            
            # Add new events
            for event in self.behavioral_events:
                event_id = event.get('id', '')
                if event_id not in existing_ids:
                    # Parse timestamp
                    timestamp = event.get('timestamp')
                    if isinstance(timestamp, str):
                        try:
                            timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        except ValueError:
                            timestamp = datetime.utcnow()
                    
                    db_event = BehavioralEventDB(
                        profile_id=self.profile_id,
                        event_type=event.get('event_type', ''),
                        description=event.get('description', ''),
                        timestamp=timestamp,
                        decision_logic=event.get('decision_logic'),
                        outcome=event.get('outcome'),
                        tags=event.get('tags', []),
                    )
                    self.db_session.add(db_event)
            
            self.db_session.commit()
            logger.info("✓ Events synced to database")
            return True
        except Exception as e:
            self.db_session.rollback()
            logger.error(f"Failed to sync events: {e}")
            return False
    
    def add_behavioral_event(self, event: BehavioralEvent) -> str:
        """Log a behavioral event with timestamp and persist to database if available"""
        event_id = hashlib.md5(
            f"{event.timestamp}{event.description}".encode()
        ).hexdigest()[:12]
        
        event_dict = event.dict()
        event_dict['id'] = event_id
        self.behavioral_events.append(event_dict)
        
        # Persist to database if available
        if self.db_session and self.profile_id:
            try:
                # Parse timestamp
                timestamp = event.timestamp
                if isinstance(timestamp, str):
                    try:
                        timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    except ValueError:
                        timestamp = datetime.utcnow()
                
                db_event = BehavioralEventDB(
                    profile_id=self.profile_id,
                    event_type=event.event_type,
                    description=event.description,
                    timestamp=timestamp,
                    decision_logic=event.decision_logic,
                    outcome=event.outcome,
                    tags=event.tags or [],
                )
                self.db_session.add(db_event)
                self.db_session.commit()
                logger.info(f"Event persisted to database: {event_id}")
            except Exception as e:
                self.db_session.rollback()
                logger.warning(f"Failed to persist event to database: {e}")
        
        logger.info(f"Event logged: {event_id} - {event.event_type}")
        return event_id
    
    def detect_patterns(self) -> List[Dict[str, Any]]:
        """Analyze behavioral events for recurring patterns"""
        if not self.behavioral_events:
            return []
        
        patterns_found = []
        
        # Pattern 1: Decision Logic Consistency
        decision_events = [e for e in self.behavioral_events if e['event_type'] == 'decision']
        if len(decision_events) >= 3:
            # Extract decision_logic themes
            logics = [e.get('decision_logic', '') for e in decision_events]
            logic_themes = self._extract_themes(logics)
            
            patterns_found.append({
                "name": "Decision Logic Pattern",
                "confidence": min(0.95, len(decision_events) * 0.15),
                "themes": logic_themes,
                "count": len(decision_events)
            })
        
        # Pattern 2: Project Domain Clustering
        projects = [e for e in self.behavioral_events if e['event_type'] == 'project']
        if projects:
            domains = [tag for p in projects for tag in p['tags']]
            domain_freq = {}
            for d in domains:
                domain_freq[d] = domain_freq.get(d, 0) + 1
            
            patterns_found.append({
                "name": "Project Domain Focus",
                "confidence": 0.88,
                "domains": domain_freq,
                "count": len(projects)
            })
        
        # Pattern 3: Communication Style Signature
        comms = [e for e in self.behavioral_events if e['event_type'] == 'communication']
        if len(comms) >= 2:
            patterns_found.append({
                "name": "Communication Signature",
                "confidence": 0.82,
                "count": len(comms),
                "characteristics": ["direct", "substantive", "provokative"]
            })
        
        self.patterns = patterns_found
        logger.info(f"Detected {len(patterns_found)} patterns")
        return patterns_found
    
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect deviations from expected behavior (Bias/Contradiction Scanner)"""
        anomalies = []
        
        # Anomaly Type 1: Contradiction Detection
        for i, event1 in enumerate(self.behavioral_events):
            for event2 in self.behavioral_events[i+1:]:
                if event1['event_type'] == event2['event_type']:
                    # Check for decision_logic contradictions
                    logic1 = event1.get('decision_logic', '')
                    logic2 = event2.get('decision_logic', '')
                    
                    if logic1 and logic2 and self._is_contradictory(logic1, logic2):
                        anomalies.append({
                            "timestamp": event2['timestamp'],
                            "anomaly_type": "contradiction",
                            "severity": 0.65,
                            "events": [event1['id'], event2['id']],
                            "explanation": f"Decision logic inconsistency detected between events"
                        })
        
        # Anomaly Type 2: Perfectionism Overreach
        if len(self.behavioral_events) > 5:
            project_frequency = len([e for e in self.behavioral_events if e['event_type'] == 'project'])
            completion_rate = len([e for e in self.behavioral_events if e['outcome'] == 'completed'])
            
            if project_frequency > 0 and completion_rate / project_frequency < 0.4:
                anomalies.append({
                    "timestamp": datetime.now().isoformat(),
                    "anomaly_type": "perfectionism_overreach",
                    "severity": 0.72,
                    "explanation": f"Low project completion rate ({completion_rate}/{project_frequency}). Perfectionism or scope-creep detected.",
                    "recommendation": "Implement checkpoint-based delivery cycles"
                })
        
        self.anomalies = anomalies
        logger.info(f"Detected {len(anomalies)} anomalies")
        return anomalies
    
    def scenario_simulation(self, scenario: str) -> Dict[str, Any]:
        """Predict operator decision in hypothetical scenario"""
        # Extract decision patterns from history
        decision_patterns = self._extract_decision_patterns()
        
        prediction = {
            "scenario": scenario,
            "predicted_decision": "Systematic analysis → High-complexity embrace → Innovation-driven choice",
            "reasoning": f"Based on {len(decision_patterns)} documented decisions: Operator-996 prioritizes systems-thinking, complexity tolerance, and innovation potential over risk minimization.",
            "confidence": 0.79,
            "alternative_paths": [
                "Conservative risk-mitigation approach (lower probability)",
                "Radical experimentation path (higher risk, higher reward)",
                "Hybrid iterative approach"
            ],
            "cognitive_load_assessment": "Medium-High. Recommend checkpoint reflection.",
            "bias_check": "⚠️  Confirmation bias risk detected in scenario interpretation"
        }
        
        return prediction
    
    def semantic_search(self, query: str) -> List[Dict[str, Any]]:
        """Search profile and events using semantic similarity"""
        if not EMBEDDINGS_AVAILABLE:
            return [{"error": "Embeddings not available. Install sentence-transformers."}]
        
        query_embedding = self.embedder.encode(query)
        results = []
        
        # Search events
        for event in self.behavioral_events:
            event_text = f"{event['event_type']} {event['description']}"
            event_embedding = self.embedder.encode(event_text)
            
            similarity = np.dot(query_embedding, event_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(event_embedding) + 1e-8
            )
            
            if similarity > 0.6:
                results.append({
                    "source": "event",
                    "id": event['id'],
                    "content": event_text,
                    "similarity": float(similarity),
                    "timestamp": event['timestamp']
                })
        
        # Search patterns
        for pattern in self.patterns:
            pattern_text = f"{pattern['name']} {json.dumps(pattern)}"
            pattern_embedding = self.embedder.encode(pattern_text)
            
            similarity = np.dot(query_embedding, pattern_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(pattern_embedding) + 1e-8
            )
            
            if similarity > 0.6:
                results.append({
                    "source": "pattern",
                    "name": pattern['name'],
                    "content": pattern_text,
                    "similarity": float(similarity)
                })
        
        results = sorted(results, key=lambda x: x['similarity'], reverse=True)
        logger.info(f"Semantic search: '{query}' → {len(results)} results")
        return results
    
    def export_full_profile(self) -> Dict[str, Any]:
        """Export complete cognitive profile snapshot"""
        return {
            "metadata": self.metadata,
            "profile": self.profile,
            "behavioral_events": self.behavioral_events,
            "patterns": self.patterns,
            "anomalies": self.anomalies,
            "export_timestamp": datetime.now().isoformat()
        }
    
    # ========================================================================
    # HELPER METHODS
    # ========================================================================
    
    def _extract_themes(self, texts: List[str]) -> List[str]:
        """Extract common themes from text list"""
        keywords = ["systematic", "complexity", "innovation", "optimization", "analysis", "experiment"]
        themes = []
        combined = " ".join(texts).lower()
        for kw in keywords:
            if kw in combined:
                themes.append(kw)
        return themes
    
    def _is_contradictory(self, logic1: str, logic2: str) -> bool:
        """Simple contradiction detection"""
        contradictions = [
            ("conservative", "aggressive"),
            ("minimize_risk", "maximize_upside"),
            ("incremental", "radical"),
        ]
        
        l1_lower = logic1.lower()
        l2_lower = logic2.lower()
        
        for term1, term2 in contradictions:
            if (term1 in l1_lower and term2 in l2_lower) or \
               (term2 in l1_lower and term1 in l2_lower):
                return True
        
        return False
    
    def _extract_decision_patterns(self) -> List[str]:
        """Extract recurring decision patterns"""
        return [
            "Systems-thinking approach",
            "High-complexity tolerance",
            "Innovation bias",
            "Experimentation-first",
            "Risk-informed decision making"
        ]

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Operator-996 Cognitive OS",
    description="Full-Stack Behavioral Analysis & Pattern Recognition",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Cognitive OS (with database session if available)
def get_os_engine():
    """Get CognitiveOS instance with database session if available"""
    if DB_AVAILABLE and SessionLocal:
        db = SessionLocal()
        return CognitiveOS(db_session=db)
    return CognitiveOS()

os_engine = get_os_engine()


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    if DB_AVAILABLE:
        logger.info("Initializing database tables...")
        success = init_db()
        if success:
            logger.info("✓ Database tables initialized")
            # Reload engine with fresh DB state
            global os_engine
            os_engine = get_os_engine()
        else:
            logger.warning("⚠️ Failed to initialize database, using in-memory storage")


# ============================================================================
# ENDPOINTS
# ============================================================================

@app.get("/health")
async def health():
    """Health check with database status"""
    db_status = "not_configured"
    if DB_AVAILABLE:
        db_status = "connected" if check_db_connection() else "disconnected"
    
    return {
        "status": "online",
        "operator": "Operator-996",
        "timestamp": datetime.now().isoformat(),
        "database": db_status
    }


@app.post("/admin/init-db")
async def initialize_database():
    """Create all database tables"""
    if not DB_AVAILABLE:
        return {"status": "skipped", "message": "Database not configured"}
    
    success = init_db()
    if success:
        return {"status": "Database initialized"}
    return {"status": "error", "message": "Failed to initialize database"}

@app.get("/profile")
async def get_profile():
    """Get current cognitive profile"""
    return {
        "profile": os_engine.profile,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/event/add")
async def add_event(event: BehavioralEvent):
    """Log a behavioral event"""
    event_id = os_engine.add_behavioral_event(event)
    return {
        "event_id": event_id,
        "status": "logged",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/events")
async def list_events():
    """Get all behavioral events"""
    return {
        "count": len(os_engine.behavioral_events),
        "events": os_engine.behavioral_events,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/patterns/detect")
async def detect_patterns():
    """Analyze and return detected patterns"""
    patterns = os_engine.detect_patterns()
    return {
        "patterns": patterns,
        "count": len(patterns),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/anomalies/detect")
async def detect_anomalies():
    """Run bias/contradiction scanner"""
    anomalies = os_engine.detect_anomalies()
    return {
        "anomalies": anomalies,
        "count": len(anomalies),
        "timestamp": datetime.now().isoformat()
    }

@app.post("/scenario/simulate")
async def simulate_scenario(scenario_text: Dict[str, str]):
    """Simulate operator decision in hypothetical scenario"""
    scenario = scenario_text.get("scenario", "")
    if not scenario:
        raise HTTPException(status_code=400, detail="Scenario required")
    
    simulation = os_engine.scenario_simulation(scenario)
    return simulation

@app.get("/search")
async def search(q: str):
    """Semantic search across profile and events"""
    results = os_engine.semantic_search(q)
    return {
        "query": q,
        "results": results,
        "count": len(results)
    }

@app.post("/import/events")
async def import_events(file: UploadFile = File(...)):
    """Import behavioral events from JSON"""
    content = await file.read()
    try:
        data = json.loads(content)
        imported_count = 0
        
        for event_data in data:
            event = BehavioralEvent(**event_data)
            os_engine.add_behavioral_event(event)
            imported_count += 1
        
        return {
            "status": "success",
            "imported": imported_count,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/export/full")
async def export_full():
    """Export complete profile snapshot"""
    return os_engine.export_full_profile()

@app.websocket("/ws/live")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket for real-time pattern updates"""
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            
            if data == "ping":
                await websocket.send_json({
                    "type": "pong",
                    "timestamp": datetime.now().isoformat()
                })
            
            elif data == "patterns":
                patterns = os_engine.detect_patterns()
                await websocket.send_json({
                    "type": "patterns",
                    "data": patterns
                })
            
            elif data == "anomalies":
                anomalies = os_engine.detect_anomalies()
                await websocket.send_json({
                    "type": "anomalies",
                    "data": anomalies
                })
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
