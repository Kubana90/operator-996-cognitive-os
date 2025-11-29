"""
Database Configuration and Models for Operator-996 Cognitive OS
PostgreSQL integration with SQLAlchemy ORM
"""

from sqlalchemy import create_engine, Column, String, Float, DateTime, Text, ForeignKey, TypeDecorator
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, JSONB
from sqlalchemy import text, JSON
import uuid
from datetime import datetime
import os

# Database URL from environment or fallback to SQLite for development
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Create engine only if DATABASE_URL is configured
engine = None
SessionLocal = None

if DATABASE_URL:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Custom UUID type that works with both PostgreSQL and SQLite
class GUID(TypeDecorator):
    """Platform-independent GUID type.
    Uses PostgreSQL's UUID type when available, otherwise stores as String(36).
    """
    impl = String(36)
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(String(36))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return value
        else:
            if isinstance(value, uuid.UUID):
                return str(value)
            return value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        if isinstance(value, uuid.UUID):
            return value
        return uuid.UUID(value)


# Custom JSON type that uses JSONB on PostgreSQL and JSON on others
class JSONType(TypeDecorator):
    """Platform-independent JSON type.
    Uses PostgreSQL's JSONB type when available, otherwise uses standard JSON.
    """
    impl = JSON
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(JSONB())
        else:
            return dialect.type_descriptor(JSON())


def get_db():
    """Dependency to get database session"""
    if SessionLocal is None:
        return None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables"""
    if engine is not None:
        Base.metadata.create_all(bind=engine)
        return True
    return False


def check_db_connection():
    """Check database connectivity"""
    if engine is None:
        return False
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False


# ============================================================================
# DATABASE MODELS
# ============================================================================

class Profile(Base):
    """Cognitive profile data"""
    __tablename__ = "profiles"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    cognitive_data = Column(JSONType, default=dict)
    behavioral_data = Column(JSONType, default=dict)
    communication_data = Column(JSONType, default=dict)
    shadow_data = Column(JSONType, default=dict)
    domains_data = Column(JSONType, default=dict)

    # Relationships
    events = relationship("BehavioralEventDB", back_populates="profile", cascade="all, delete-orphan")
    patterns = relationship("PatternDB", back_populates="profile", cascade="all, delete-orphan")
    anomalies = relationship("AnomalyDB", back_populates="profile", cascade="all, delete-orphan")

    def to_dict(self):
        """Convert to dictionary format compatible with existing code"""
        return {
            "cognitive": self.cognitive_data or {},
            "behavioral": self.behavioral_data or {},
            "communication": self.communication_data or {},
            "shadow": self.shadow_data or {},
            "domains": self.domains_data or {},
        }


class BehavioralEventDB(Base):
    """Behavioral event logs"""
    __tablename__ = "behavioral_events"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    profile_id = Column(GUID(), ForeignKey("profiles.id"), nullable=False)
    event_type = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    timestamp = Column(DateTime, nullable=False)
    decision_logic = Column(Text, nullable=True)
    outcome = Column(Text, nullable=True)
    tags = Column(JSONType, default=list)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    profile = relationship("Profile", back_populates="events")

    def to_dict(self):
        """Convert to dictionary format compatible with existing code"""
        return {
            "id": str(self.id),
            "event_type": self.event_type,
            "description": self.description,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None,
            "decision_logic": self.decision_logic,
            "outcome": self.outcome,
            "tags": self.tags or [],
        }


class PatternDB(Base):
    """Detected patterns"""
    __tablename__ = "patterns"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    profile_id = Column(GUID(), ForeignKey("profiles.id"), nullable=False)
    name = Column(String(255), nullable=False)
    confidence = Column(Float, nullable=False)
    characteristics = Column(JSONType, default=list)
    supporting_events = Column(JSONType, default=list)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    profile = relationship("Profile", back_populates="patterns")

    def to_dict(self):
        """Convert to dictionary format compatible with existing code"""
        return {
            "id": str(self.id),
            "name": self.name,
            "confidence": self.confidence,
            "characteristics": self.characteristics or [],
            "supporting_events": self.supporting_events or [],
            "detected_at": self.detected_at.isoformat() if self.detected_at else None,
        }


class AnomalyDB(Base):
    """Detected anomalies"""
    __tablename__ = "anomalies"

    id = Column(GUID(), primary_key=True, default=uuid.uuid4)
    profile_id = Column(GUID(), ForeignKey("profiles.id"), nullable=False)
    anomaly_type = Column(String(100), nullable=False)
    severity = Column(Float, nullable=False)
    explanation = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    detected_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    profile = relationship("Profile", back_populates="anomalies")

    def to_dict(self):
        """Convert to dictionary format compatible with existing code"""
        return {
            "id": str(self.id),
            "anomaly_type": self.anomaly_type,
            "severity": self.severity,
            "explanation": self.explanation,
            "recommendation": self.recommendation,
            "detected_at": self.detected_at.isoformat() if self.detected_at else None,
        }
