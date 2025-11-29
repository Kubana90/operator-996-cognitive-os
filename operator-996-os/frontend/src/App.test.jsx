/**
 * Operator-996 Cognitive OS - Frontend Tests
 * React Testing Library + Jest
 */

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import CognitiveOS from './App';

// ============================================================================
// MOCKS
// ============================================================================

// Mock fetch API
global.fetch = jest.fn();

// Mock WebSocket
class MockWebSocket {
  constructor(url) {
    this.url = url;
    this.onopen = null;
    this.onmessage = null;
    this.onerror = null;
    this.onclose = null;
    setTimeout(() => {
      if (this.onopen) this.onopen();
    }, 0);
  }
  send(data) {}
  close() {}
}

global.WebSocket = MockWebSocket;

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

const mockProfileResponse = {
  profile: {
    cognitive: {
      iq_percentile: 0.98,
      pattern_recognition: 0.95,
      systems_thinking: 0.93,
    },
    behavioral: {
      risk_tolerance: 0.85,
      experimentation_drive: 0.88,
    },
    communication: {
      directness: 0.89,
      depth_seeking: 0.91,
    },
    shadow: {
      cognitive_overload_risk: 0.72,
      perfectionism: 0.85,
    },
    domains: {
      ai_integration: 0.94,
      full_stack_development: 0.91,
    },
  },
  timestamp: new Date().toISOString(),
};

const mockEventsResponse = {
  count: 2,
  events: [
    {
      id: 'abc123',
      event_type: 'decision',
      description: 'Test decision event',
      timestamp: '2024-01-15T10:30:00Z',
      tags: ['test'],
    },
    {
      id: 'def456',
      event_type: 'project',
      description: 'Test project event',
      timestamp: '2024-01-16T14:00:00Z',
      tags: ['project'],
    },
  ],
  timestamp: new Date().toISOString(),
};

const mockPatternsResponse = {
  patterns: [],
  count: 0,
  timestamp: new Date().toISOString(),
};

const setupMocks = () => {
  fetch.mockImplementation((url) => {
    if (url.includes('/profile')) {
      return Promise.resolve({
        json: () => Promise.resolve(mockProfileResponse),
      });
    }
    if (url.includes('/events')) {
      return Promise.resolve({
        json: () => Promise.resolve(mockEventsResponse),
      });
    }
    if (url.includes('/patterns/detect')) {
      return Promise.resolve({
        json: () => Promise.resolve(mockPatternsResponse),
      });
    }
    if (url.includes('/event/add')) {
      return Promise.resolve({
        json: () => Promise.resolve({ event_id: 'new123', status: 'logged' }),
      });
    }
    return Promise.resolve({
      json: () => Promise.resolve({}),
    });
  });
};

// ============================================================================
// COMPONENT RENDERING TESTS
// ============================================================================

describe('Component Rendering', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    setupMocks();
  });

  test('App component renders without crashing', async () => {
    render(<CognitiveOS />);
    
    // Should render the main heading (use getAllByText since the text appears multiple times)
    const elements = screen.getAllByText(/Operator-996 Cognitive OS/i);
    expect(elements.length).toBeGreaterThan(0);
  });

  test('dashboard displays status bar', async () => {
    render(<CognitiveOS />);
    
    // Wait for the component to load
    await waitFor(() => {
      expect(screen.getByText(/Events:/i)).toBeInTheDocument();
    });
    
    expect(screen.getByText(/Patterns:/i)).toBeInTheDocument();
    expect(screen.getByText(/Anomalies:/i)).toBeInTheDocument();
    expect(screen.getByText(/Backend:/i)).toBeInTheDocument();
  });

  test('navigation tabs are rendered', () => {
    render(<CognitiveOS />);
    
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Event Logger')).toBeInTheDocument();
    expect(screen.getByText('Analytics')).toBeInTheDocument();
    expect(screen.getByText('Settings')).toBeInTheDocument();
  });

  test('footer is rendered', () => {
    render(<CognitiveOS />);
    
    expect(screen.getByText(/Full-Stack Pattern Analysis/i)).toBeInTheDocument();
  });
});

// ============================================================================
// API INTEGRATION TESTS
// ============================================================================

describe('API Integration', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    setupMocks();
  });

  test('profile data is fetched on mount', async () => {
    render(<CognitiveOS />);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/profile'));
    });
  });

  test('events data is fetched on mount', async () => {
    render(<CognitiveOS />);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(expect.stringContaining('/events'));
    });
  });

  test('patterns detection is triggered', async () => {
    render(<CognitiveOS />);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/patterns/detect'),
        expect.objectContaining({ method: 'POST' })
      );
    });
  });

  test('profile displays cognitive attributes after loading', async () => {
    render(<CognitiveOS />);
    
    await waitFor(() => {
      expect(screen.getByText('Cognitive')).toBeInTheDocument();
    });
    
    expect(screen.getByText('Behavioral')).toBeInTheDocument();
    expect(screen.getByText('Communication')).toBeInTheDocument();
    expect(screen.getByText('Shadow')).toBeInTheDocument();
  });
});

// ============================================================================
// USER INTERACTION TESTS
// ============================================================================

describe('User Interactions', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    setupMocks();
  });

  test('clicking Event Logger tab shows event logger form', async () => {
    render(<CognitiveOS />);
    
    const loggerTab = screen.getByText('Event Logger');
    fireEvent.click(loggerTab);
    
    await waitFor(() => {
      expect(screen.getByText(/Log Behavioral Event/i)).toBeInTheDocument();
    });
  });

  test('event type selection is available in form', async () => {
    render(<CognitiveOS />);
    
    const loggerTab = screen.getByText('Event Logger');
    fireEvent.click(loggerTab);
    
    await waitFor(() => {
      const select = screen.getByRole('combobox');
      expect(select).toBeInTheDocument();
    });
    
    // Verify event type options are available (text content in options)
    const selectElement = screen.getByRole('combobox');
    expect(selectElement).toHaveTextContent('Decision');
    expect(selectElement).toHaveTextContent('Project');
    expect(selectElement).toHaveTextContent('Interaction');
    expect(selectElement).toHaveTextContent('Communication');
  });

  test('form submission triggers API call', async () => {
    render(<CognitiveOS />);
    
    const loggerTab = screen.getByText('Event Logger');
    fireEvent.click(loggerTab);
    
    await waitFor(() => {
      expect(screen.getByText(/Log Behavioral Event/i)).toBeInTheDocument();
    });
    
    // Fill the form
    const select = screen.getByRole('combobox');
    fireEvent.change(select, { target: { value: 'decision' } });
    
    const descriptionTextarea = screen.getByPlaceholderText('Describe the event...');
    fireEvent.change(descriptionTextarea, { target: { value: 'Test event description' } });
    
    // Submit the form
    const submitButton = screen.getByText('Log Event');
    fireEvent.click(submitButton);
    
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        expect.stringContaining('/event/add'),
        expect.objectContaining({ method: 'POST' })
      );
    });
  });

  test('clicking Analytics tab shows scenario simulation', async () => {
    render(<CognitiveOS />);
    
    const analyticsTab = screen.getByText('Analytics');
    fireEvent.click(analyticsTab);
    
    await waitFor(() => {
      expect(screen.getByText(/Scenario Simulation/i)).toBeInTheDocument();
    });
    
    expect(screen.getByText(/Hypothetical Scenario Simulator/i)).toBeInTheDocument();
    expect(screen.getByText(/Semantic Search/i)).toBeInTheDocument();
  });

  test('clicking Settings tab shows configuration', async () => {
    render(<CognitiveOS />);
    
    const settingsTab = screen.getByText('Settings');
    fireEvent.click(settingsTab);
    
    await waitFor(() => {
      expect(screen.getByText(/Configuration/i)).toBeInTheDocument();
    });
    
    expect(screen.getByText(/Backend API Base URL/i)).toBeInTheDocument();
    expect(screen.getByText(/System Information/i)).toBeInTheDocument();
  });

  test('detect patterns button is clickable', async () => {
    render(<CognitiveOS />);
    
    const loggerTab = screen.getByText('Event Logger');
    fireEvent.click(loggerTab);
    
    await waitFor(() => {
      const detectButton = screen.getByText(/Detect Patterns/i);
      expect(detectButton).toBeInTheDocument();
      fireEvent.click(detectButton);
    });
    
    // Verify the API was called
    await waitFor(() => {
      const patternCalls = fetch.mock.calls.filter(call => 
        call[0].includes('/patterns/detect')
      );
      expect(patternCalls.length).toBeGreaterThan(0);
    });
  });
});

// ============================================================================
// DASHBOARD CONTENT TESTS
// ============================================================================

describe('Dashboard Content', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    setupMocks();
  });

  test('domain expertise section renders', async () => {
    render(<CognitiveOS />);
    
    await waitFor(() => {
      expect(screen.getByText(/Domain Expertise/i)).toBeInTheDocument();
    });
  });

  test('nav brand shows correct text', () => {
    render(<CognitiveOS />);
    
    expect(screen.getByText(/OP-996/i)).toBeInTheDocument();
  });
});
