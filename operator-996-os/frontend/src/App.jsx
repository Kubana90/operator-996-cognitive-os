/**
 * Operator-996 Cognitive OS - Frontend React App
 * Complete Interactive Dashboard with Real-time Pattern Analysis
 */

import React, { useState, useEffect, useRef } from "react";
import "./App.css";


// ============================================================================
// COMPONENTS
// ============================================================================

const CognitiveOS = () => {
  const [apiBase, setApiBase] = useState('http://localhost:8000');
  const [profile, setProfile] = useState(null);
  const [events, setEvents] = useState([]);
  const [patterns, setPatterns] = useState([]);
  const [anomalies, setAnomalies] = useState([]);
  const [selectedTab, setSelectedTab] = useState('dashboard');
  const [searchQuery, setSearchQuery] = useState('');
  const [scenarioInput, setScenarioInput] = useState('');
  const [loading, setLoading] = useState(false);
  const websocketRef = useRef(null);

  // ========================================================================
  // LIFECYCLE
  // ========================================================================

  useEffect(() => {
    initializeOS();
    connectWebSocket();
    
    return () => {
      if (websocketRef.current) {
        websocketRef.current.close();
      }
    };
  }, []);

  // ========================================================================
  // API CALLS
  // ========================================================================

  const initializeOS = async () => {
    try {
      const profileRes = await fetch(`${apiBase}/profile`);
      const profileData = await profileRes.json();
      setProfile(profileData.profile);

      const eventsRes = await fetch(`${apiBase}/events`);
      const eventsData = await eventsRes.json();
      setEvents(eventsData.events || []);

      detectPatterns();
    } catch (err) {
      console.error('Failed to initialize:', err);
    }
  };

  const connectWebSocket = () => {
    try {
      const ws = new WebSocket(`ws://localhost:8000/ws/live`);
      
      ws.onopen = () => {
        console.log('✓ WebSocket connected');
        websocketRef.current = ws;
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        
        if (data.type === 'patterns') {
          setPatterns(data.data);
        } else if (data.type === 'anomalies') {
          setAnomalies(data.data);
        }
      };

      ws.onerror = (err) => console.error('WebSocket error:', err);
      ws.onclose = () => {
        console.log('WebSocket closed. Will retry...');
        setTimeout(connectWebSocket, 3000);
      };
    } catch (err) {
      console.error('WebSocket connection failed:', err);
    }
  };

  const detectPatterns = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${apiBase}/patterns/detect`, { method: 'POST' });
      const data = await res.json();
      setPatterns(data.patterns || []);
    } catch (err) {
      console.error('Pattern detection failed:', err);
    }
    setLoading(false);
  };

  const detectAnomalies = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${apiBase}/anomalies/detect`, { method: 'POST' });
      const data = await res.json();
      setAnomalies(data.anomalies || []);
    } catch (err) {
      console.error('Anomaly detection failed:', err);
    }
    setLoading(false);
  };

  const addBehavioralEvent = async (eventType, description, decisionLogic = '') => {
    try {
      const res = await fetch(`${apiBase}/event/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          event_type: eventType,
          description: description,
          decision_logic: decisionLogic,
          timestamp: new Date().toISOString(),
          tags: [eventType],
        }),
      });
      const data = await res.json();
      
      // Refresh events
      const eventsRes = await fetch(`${apiBase}/events`);
      const eventsData = await eventsRes.json();
      setEvents(eventsData.events || []);
      
      return data.event_id;
    } catch (err) {
      console.error('Failed to add event:', err);
    }
  };

  const performSemanticSearch = async () => {
    if (!searchQuery.trim()) return;
    
    try {
      const res = await fetch(`${apiBase}/search?q=${encodeURIComponent(searchQuery)}`);
      const data = await res.json();
      console.log('Search results:', data.results);
      alert(`Found ${data.count} results. Check console.`);
    } catch (err) {
      console.error('Search failed:', err);
    }
  };

  const runScenarioSimulation = async () => {
    if (!scenarioInput.trim()) return;
    
    try {
      const res = await fetch(`${apiBase}/scenario/simulate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ scenario: scenarioInput }),
      });
      const data = await res.json();
      console.log('Scenario simulation:', data);
      alert(`Predicted Decision:\n${data.predicted_decision}\n\nConfidence: ${(data.confidence * 100).toFixed(0)}%`);
    } catch (err) {
      console.error('Simulation failed:', err);
    }
  };

  const exportProfile = async () => {
    try {
      const res = await fetch(`${apiBase}/export/full`);
      const data = await res.json();
      
      const dataStr = JSON.stringify(data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `operator996_profile_${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Export failed:', err);
    }
  };

  // ========================================================================
  // RENDER COMPONENTS
  // ========================================================================

  const renderDashboard = () => (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>🧠 Operator-996 Cognitive OS</h1>
        <div className="status-bar">
          <span className="status-item">
            📊 Events: <strong>{events.length}</strong>
          </span>
          <span className="status-item">
            🔗 Patterns: <strong>{patterns.length}</strong>
          </span>
          <span className="status-item">
            ⚠️ Anomalies: <strong>{anomalies.length}</strong>
          </span>
          <span className="status-item">
            ✓ Backend: <strong>Online</strong>
          </span>
        </div>
      </div>

      {/* Cognitive Profile Grid */}
      {profile && (
        <section className="profile-section">
          <h2>📈 Cognitive Profile</h2>
          <div className="profile-grid">
            <ProfileCategory 
              name="Cognitive" 
              attributes={profile.cognitive}
            />
            <ProfileCategory 
              name="Behavioral" 
              attributes={profile.behavioral}
            />
            <ProfileCategory 
              name="Communication" 
              attributes={profile.communication}
            />
            <ProfileCategory 
              name="Shadow" 
              attributes={profile.shadow}
            />
          </div>

          <div className="domain-grid">
            <h3>💼 Domain Expertise</h3>
            <div className="skills-row">
              {Object.entries(profile.domains || {}).map(([domain, score]) => (
                <SkillBar key={domain} label={domain} value={score} />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* Behavioral Events Timeline */}
      {events.length > 0 && (
        <section className="events-section">
          <h2>📋 Behavioral Events Timeline</h2>
          <div className="events-list">
            {events.slice(-10).reverse().map((event, idx) => (
              <div key={idx} className="event-card">
                <div className="event-header">
                  <span className="event-type">{event.event_type.toUpperCase()}</span>
                  <span className="event-time">
                    {new Date(event.timestamp).toLocaleString()}
                  </span>
                </div>
                <p className="event-description">{event.description}</p>
                {event.decision_logic && (
                  <p className="event-logic">
                    <strong>Logic:</strong> {event.decision_logic}
                  </p>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Detected Patterns */}
      {patterns.length > 0 && (
        <section className="patterns-section">
          <h2>🔗 Detected Patterns</h2>
          <div className="patterns-list">
            {patterns.map((pattern, idx) => (
              <div key={idx} className="pattern-card">
                <h3>{pattern.name}</h3>
                <p>
                  <strong>Confidence:</strong>{' '}
                  <span className="confidence-badge">
                    {(pattern.confidence * 100).toFixed(0)}%
                  </span>
                </p>
                {pattern.themes && (
                  <p>
                    <strong>Themes:</strong> {pattern.themes.join(', ')}
                  </p>
                )}
                {pattern.domains && (
                  <p>
                    <strong>Domains:</strong> {Object.entries(pattern.domains)
                      .map(([d, c]) => `${d} (${c})`)
                      .join(', ')}
                  </p>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Anomalies & Bias Detection */}
      {anomalies.length > 0 && (
        <section className="anomalies-section">
          <h2>⚠️ Bias & Contradiction Scanner</h2>
          <div className="anomalies-list">
            {anomalies.map((anomaly, idx) => (
              <div key={idx} className="anomaly-card">
                <div className="anomaly-header">
                  <span className="anomaly-type">{anomaly.anomaly_type}</span>
                  <span className="severity-badge" style={{
                    backgroundColor: `hsl(${(1 - anomaly.severity) * 120}, 100%, 50%)`
                  }}>
                    {(anomaly.severity * 100).toFixed(0)}% severity
                  </span>
                </div>
                <p>{anomaly.explanation}</p>
                {anomaly.recommendation && (
                  <p className="recommendation">
                    💡 <strong>Recommendation:</strong> {anomaly.recommendation}
                  </p>
                )}
              </div>
            ))}
          </div>
        </section>
      )}
    </div>
  );

  const renderEventLogger = () => (
    <div className="event-logger">
      <h2>📝 Log Behavioral Event</h2>
      <form onSubmit={(e) => {
        e.preventDefault();
        const formData = new FormData(e.target);
        const eventType = formData.get('event_type');
        const description = formData.get('description');
        const decisionLogic = formData.get('decision_logic');
        
        addBehavioralEvent(eventType, description, decisionLogic);
        e.target.reset();
      }}>
        <div className="form-group">
          <label>Event Type:</label>
          <select name="event_type" required>
            <option value="">Select...</option>
            <option value="decision">Decision</option>
            <option value="project">Project</option>
            <option value="interaction">Interaction</option>
            <option value="communication">Communication</option>
          </select>
        </div>

        <div className="form-group">
          <label>Description:</label>
          <textarea name="description" required placeholder="Describe the event..."></textarea>
        </div>

        <div className="form-group">
          <label>Decision Logic (optional):</label>
          <textarea name="decision_logic" placeholder="Explain the reasoning..."></textarea>
        </div>

        <button type="submit" className="btn-primary">Log Event</button>
      </form>

      <div className="action-buttons">
        <button onClick={detectPatterns} disabled={loading} className="btn-secondary">
          🔍 Detect Patterns
        </button>
        <button onClick={detectAnomalies} disabled={loading} className="btn-secondary">
          🔎 Scan for Anomalies
        </button>
      </div>
    </div>
  );

  const renderAnalytics = () => (
    <div className="analytics">
      <h2>🎯 Scenario Simulation & Search</h2>

      <div className="scenario-box">
        <h3>Hypothetical Scenario Simulator</h3>
        <textarea
          value={scenarioInput}
          onChange={(e) => setScenarioInput(e.target.value)}
          placeholder="Describe a hypothetical scenario..."
          rows={4}
        ></textarea>
        <button onClick={runScenarioSimulation} className="btn-primary">
          🚀 Simulate Decision
        </button>
      </div>

      <div className="search-box">
        <h3>Semantic Search</h3>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search across profile and events..."
          onKeyPress={(e) => e.key === 'Enter' && performSemanticSearch()}
        />
        <button onClick={performSemanticSearch} className="btn-primary">
          🔍 Search
        </button>
      </div>

      <div className="export-section">
        <h3>Data Export</h3>
        <button onClick={exportProfile} className="btn-primary">
          📥 Export Full Profile (JSON)
        </button>
      </div>
    </div>
  );

  const renderSettings = () => (
    <div className="settings">
      <h2>⚙️ Configuration</h2>
      <div className="settings-group">
        <label>Backend API Base URL:</label>
        <input
          type="text"
          value={apiBase}
          onChange={(e) => setApiBase(e.target.value)}
          placeholder="http://localhost:8000"
        />
        <small>Change and refresh page if connecting to remote backend</small>
      </div>

      <div className="demo-section">
        <h3>🎮 Demo Mode</h3>
        <p>Load 50+ realistic behavioral events to see the system in action.</p>
        <button 
          onClick={async () => {
            try {
              setLoading(true);
              const response = await fetch(`${apiBase}/import/sample-data`, {method: 'POST'});
              if (response.ok) {
                const data = await response.json();
                alert(`✅ Sample data imported! ${data.imported} events loaded.\nRefresh to see the dashboard populated.`);
                window.location.reload();
              } else {
                alert('❌ Failed to import sample data. Check if backend is running.');
              }
            } catch (err) {
              alert('❌ Error importing sample data: ' + err.message);
            } finally {
              setLoading(false);
            }
          }}
          disabled={loading}
          style={{
            padding: '12px 24px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            border: 'none',
            borderRadius: '8px',
            cursor: loading ? 'not-allowed' : 'pointer',
            fontSize: '16px',
            fontWeight: 'bold',
            opacity: loading ? 0.7 : 1,
            marginTop: '10px'
          }}
        >
          {loading ? '⏳ Loading...' : '🎮 Load Demo Data (50+ Events)'}
        </button>
      </div>

      <div className="info-box">
        <h3>ℹ️ System Information</h3>
        <p><strong>Version:</strong> 1.0.0</p>
        <p><strong>Operator:</strong> Operator-996</p>
        <p><strong>Frontend:</strong> React</p>
        <p><strong>Backend:</strong> FastAPI</p>
        <p><strong>WebSocket:</strong> Live pattern detection enabled</p>
      </div>
    </div>
  );

  // ========================================================================
  // MAIN RENDER
  // ========================================================================

  return (
    <div className="operator-996-os">
      <nav className="navbar">
        <div className="nav-brand">🧠 OP-996</div>
        <div className="nav-tabs">
          <button 
            className={`nav-tab ${selectedTab === 'dashboard' ? 'active' : ''}`}
            onClick={() => setSelectedTab('dashboard')}
          >
            Dashboard
          </button>
          <button 
            className={`nav-tab ${selectedTab === 'logger' ? 'active' : ''}`}
            onClick={() => setSelectedTab('logger')}
          >
            Event Logger
          </button>
          <button 
            className={`nav-tab ${selectedTab === 'analytics' ? 'active' : ''}`}
            onClick={() => setSelectedTab('analytics')}
          >
            Analytics
          </button>
          <button 
            className={`nav-tab ${selectedTab === 'settings' ? 'active' : ''}`}
            onClick={() => setSelectedTab('settings')}
          >
            Settings
          </button>
        </div>
      </nav>

      <main className="main-content">
        {selectedTab === 'dashboard' && renderDashboard()}
        {selectedTab === 'logger' && renderEventLogger()}
        {selectedTab === 'analytics' && renderAnalytics()}
        {selectedTab === 'settings' && renderSettings()}
      </main>

      <footer className="footer">
        <p>Operator-996 Cognitive OS | Full-Stack Pattern Analysis | Real-time Behavioral Monitoring</p>
      </footer>
    </div>
  );
};

// ============================================================================
// SUB-COMPONENTS
// ============================================================================

const ProfileCategory = ({ name, attributes }) => (
  <div className="profile-category">
    <h3>{name}</h3>
    <div className="attributes-list">
      {Object.entries(attributes).map(([key, value]) => (
        <div key={key} className="attribute-row">
          <span className="attribute-label">{key.replace(/_/g, ' ')}</span>
          <div className="attribute-bar">
            <div 
              className="attribute-fill" 
              style={{ width: `${value * 100}%` }}
            ></div>
          </div>
          <span className="attribute-value">{(value * 100).toFixed(0)}%</span>
        </div>
      ))}
    </div>
  </div>
);

const SkillBar = ({ label, value }) => (
  <div className="skill-bar">
    <span className="skill-label">{label}</span>
    <div className="skill-meter">
      <div className="skill-fill" style={{ width: `${value * 100}%` }}></div>
    </div>
    <span className="skill-value">{(value * 100).toFixed(0)}%</span>
  </div>
);

export default CognitiveOS;
