"""
Operator-996 Cognitive OS Backend Tests
Comprehensive test coverage for FastAPI endpoints
"""

import pytest
import json
import io
from httpx import AsyncClient, ASGITransport
from backend_main import app, os_engine, BehavioralEvent


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture
def anyio_backend():
    return 'asyncio'


@pytest.fixture
async def client():
    """Create async test client"""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def sample_event_data():
    """Sample behavioral event data"""
    return {
        "event_type": "decision",
        "description": "Decided to use microservices architecture for new project",
        "timestamp": "2024-01-15T10:30:00Z",
        "outcome": "successful",
        "decision_logic": "Systematic analysis of scalability requirements",
        "tags": ["architecture", "decision"]
    }


@pytest.fixture
def sample_events_json():
    """Sample events JSON for import testing"""
    return [
        {
            "event_type": "project",
            "description": "Started AI integration project",
            "timestamp": "2024-01-10T09:00:00Z",
            "tags": ["ai", "project"]
        },
        {
            "event_type": "interaction",
            "description": "Team meeting on project planning",
            "timestamp": "2024-01-11T14:00:00Z",
            "tags": ["meeting", "team"]
        }
    ]


# ============================================================================
# HEALTH CHECK TESTS
# ============================================================================

class TestHealthCheck:
    """Tests for health check endpoint"""
    
    @pytest.mark.anyio
    async def test_health_returns_online_status(self, client):
        """Test /health returns correct status"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "online"
    
    @pytest.mark.anyio
    async def test_health_returns_operator_name(self, client):
        """Test /health returns correct operator name"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["operator"] == "Operator-996"
    
    @pytest.mark.anyio
    async def test_health_contains_timestamp(self, client):
        """Test /health response contains timestamp"""
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "timestamp" in data


# ============================================================================
# PROFILE MANAGEMENT TESTS
# ============================================================================

class TestProfileManagement:
    """Tests for profile management endpoints"""
    
    @pytest.mark.anyio
    async def test_profile_returns_valid_structure(self, client):
        """Test /profile returns valid cognitive profile structure"""
        response = await client.get("/profile")
        assert response.status_code == 200
        data = response.json()
        assert "profile" in data
        assert "timestamp" in data
    
    @pytest.mark.anyio
    async def test_profile_contains_cognitive_section(self, client):
        """Test profile contains cognitive attributes"""
        response = await client.get("/profile")
        data = response.json()
        profile = data["profile"]
        assert "cognitive" in profile
        assert isinstance(profile["cognitive"], dict)
    
    @pytest.mark.anyio
    async def test_profile_contains_behavioral_section(self, client):
        """Test profile contains behavioral attributes"""
        response = await client.get("/profile")
        data = response.json()
        profile = data["profile"]
        assert "behavioral" in profile
        assert isinstance(profile["behavioral"], dict)
    
    @pytest.mark.anyio
    async def test_profile_contains_communication_section(self, client):
        """Test profile contains communication attributes"""
        response = await client.get("/profile")
        data = response.json()
        profile = data["profile"]
        assert "communication" in profile
        assert isinstance(profile["communication"], dict)
    
    @pytest.mark.anyio
    async def test_profile_contains_shadow_section(self, client):
        """Test profile contains shadow attributes"""
        response = await client.get("/profile")
        data = response.json()
        profile = data["profile"]
        assert "shadow" in profile
        assert isinstance(profile["shadow"], dict)
    
    @pytest.mark.anyio
    async def test_profile_contains_domains_section(self, client):
        """Test profile contains domains section"""
        response = await client.get("/profile")
        data = response.json()
        profile = data["profile"]
        assert "domains" in profile
        assert isinstance(profile["domains"], dict)


# ============================================================================
# EVENT MANAGEMENT TESTS
# ============================================================================

class TestEventManagement:
    """Tests for event management endpoints"""
    
    @pytest.mark.anyio
    async def test_add_event_with_valid_data(self, client, sample_event_data):
        """Test POST /event/add with valid event data"""
        response = await client.post("/event/add", json=sample_event_data)
        assert response.status_code == 200
        data = response.json()
        assert "event_id" in data
        assert data["status"] == "logged"
        assert "timestamp" in data
    
    @pytest.mark.anyio
    async def test_add_decision_event(self, client):
        """Test adding decision event type"""
        event_data = {
            "event_type": "decision",
            "description": "Test decision event",
            "timestamp": "2024-01-15T10:00:00Z",
            "decision_logic": "Test logic",
            "tags": ["test"]
        }
        response = await client.post("/event/add", json=event_data)
        assert response.status_code == 200
    
    @pytest.mark.anyio
    async def test_add_project_event(self, client):
        """Test adding project event type"""
        event_data = {
            "event_type": "project",
            "description": "Test project event",
            "timestamp": "2024-01-15T10:00:00Z",
            "tags": ["project"]
        }
        response = await client.post("/event/add", json=event_data)
        assert response.status_code == 200
    
    @pytest.mark.anyio
    async def test_add_interaction_event(self, client):
        """Test adding interaction event type"""
        event_data = {
            "event_type": "interaction",
            "description": "Test interaction event",
            "timestamp": "2024-01-15T10:00:00Z",
            "tags": ["interaction"]
        }
        response = await client.post("/event/add", json=event_data)
        assert response.status_code == 200
    
    @pytest.mark.anyio
    async def test_add_communication_event(self, client):
        """Test adding communication event type"""
        event_data = {
            "event_type": "communication",
            "description": "Test communication event",
            "timestamp": "2024-01-15T10:00:00Z",
            "tags": ["communication"]
        }
        response = await client.post("/event/add", json=event_data)
        assert response.status_code == 200
    
    @pytest.mark.anyio
    async def test_get_events_returns_list(self, client):
        """Test GET /events returns events list"""
        response = await client.get("/events")
        assert response.status_code == 200
        data = response.json()
        assert "events" in data
        assert "count" in data
        assert isinstance(data["events"], list)
        assert isinstance(data["count"], int)


# ============================================================================
# PATTERN DETECTION TESTS
# ============================================================================

class TestPatternDetection:
    """Tests for pattern detection endpoint"""
    
    @pytest.mark.anyio
    async def test_detect_patterns_returns_patterns(self, client):
        """Test POST /patterns/detect returns patterns"""
        response = await client.post("/patterns/detect")
        assert response.status_code == 200
        data = response.json()
        assert "patterns" in data
        assert "count" in data
        assert isinstance(data["patterns"], list)
    
    @pytest.mark.anyio
    async def test_pattern_confidence_scores_valid(self, client, sample_event_data):
        """Test that confidence scores are between 0 and 1"""
        # Add multiple events to generate patterns
        for i in range(3):
            event = sample_event_data.copy()
            event["description"] = f"Decision {i}: {event['description']}"
            event["timestamp"] = f"2024-01-{15+i}T10:30:00Z"
            await client.post("/event/add", json=event)
        
        response = await client.post("/patterns/detect")
        data = response.json()
        
        for pattern in data["patterns"]:
            if "confidence" in pattern:
                assert 0 <= pattern["confidence"] <= 1, \
                    f"Confidence score {pattern['confidence']} out of range [0,1]"


# ============================================================================
# ANOMALY DETECTION TESTS
# ============================================================================

class TestAnomalyDetection:
    """Tests for anomaly detection endpoint"""
    
    @pytest.mark.anyio
    async def test_detect_anomalies_returns_anomalies(self, client):
        """Test POST /anomalies/detect returns anomalies"""
        response = await client.post("/anomalies/detect")
        assert response.status_code == 200
        data = response.json()
        assert "anomalies" in data
        assert "count" in data
        assert isinstance(data["anomalies"], list)
    
    @pytest.mark.anyio
    async def test_anomaly_severity_scores_valid(self, client):
        """Test that severity scores are valid (between 0 and 1)"""
        response = await client.post("/anomalies/detect")
        data = response.json()
        
        for anomaly in data["anomalies"]:
            if "severity" in anomaly:
                assert 0 <= anomaly["severity"] <= 1, \
                    f"Severity score {anomaly['severity']} out of range [0,1]"


# ============================================================================
# SCENARIO SIMULATION TESTS
# ============================================================================

class TestScenarioSimulation:
    """Tests for scenario simulation endpoint"""
    
    @pytest.mark.anyio
    async def test_simulate_scenario_with_valid_input(self, client):
        """Test POST /scenario/simulate with sample scenario"""
        scenario_data = {
            "scenario": "Should I invest in a new AI startup with high risk but high reward potential?"
        }
        response = await client.post("/scenario/simulate", json=scenario_data)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_decision" in data
        assert "confidence" in data
        assert "reasoning" in data
        assert "alternative_paths" in data
    
    @pytest.mark.anyio
    async def test_simulate_scenario_confidence_valid(self, client):
        """Test that simulation confidence is between 0 and 1"""
        scenario_data = {"scenario": "Test scenario for confidence validation"}
        response = await client.post("/scenario/simulate", json=scenario_data)
        data = response.json()
        assert 0 <= data["confidence"] <= 1
    
    @pytest.mark.anyio
    async def test_simulate_scenario_empty_fails(self, client):
        """Test POST /scenario/simulate with empty scenario fails"""
        scenario_data = {"scenario": ""}
        response = await client.post("/scenario/simulate", json=scenario_data)
        assert response.status_code == 400


# ============================================================================
# SEARCH FUNCTIONALITY TESTS
# ============================================================================

class TestSearchFunctionality:
    """Tests for search endpoint"""
    
    @pytest.mark.anyio
    async def test_search_returns_results(self, client):
        """Test GET /search?q=query returns results"""
        response = await client.get("/search?q=decision")
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert "count" in data
    
    @pytest.mark.anyio
    async def test_search_query_preserved(self, client):
        """Test that search query is preserved in response"""
        query = "pattern analysis"
        response = await client.get(f"/search?q={query}")
        data = response.json()
        assert data["query"] == query


# ============================================================================
# IMPORT/EXPORT TESTS
# ============================================================================

class TestImportExport:
    """Tests for import/export endpoints"""
    
    @pytest.mark.anyio
    async def test_export_full_returns_complete_profile(self, client):
        """Test GET /export/full returns complete profile"""
        response = await client.get("/export/full")
        assert response.status_code == 200
        data = response.json()
        assert "metadata" in data
        assert "profile" in data
        assert "behavioral_events" in data
        assert "patterns" in data
        assert "anomalies" in data
        assert "export_timestamp" in data
    
    @pytest.mark.anyio
    async def test_import_events_with_valid_json(self, client, sample_events_json):
        """Test POST /import/events with sample JSON file"""
        json_content = json.dumps(sample_events_json)
        files = {
            "file": ("events.json", io.BytesIO(json_content.encode()), "application/json")
        }
        response = await client.post("/import/events", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["imported"] == len(sample_events_json)


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

class TestErrorHandling:
    """Tests for error handling"""
    
    @pytest.mark.anyio
    async def test_invalid_endpoint_returns_404(self, client):
        """Test that invalid endpoints return 404"""
        response = await client.get("/invalid/endpoint")
        assert response.status_code == 404
    
    @pytest.mark.anyio
    async def test_add_event_missing_required_fields(self, client):
        """Test POST /event/add with missing required fields"""
        invalid_event = {
            "event_type": "decision"
            # Missing description and timestamp
        }
        response = await client.post("/event/add", json=invalid_event)
        assert response.status_code == 422  # Validation error
