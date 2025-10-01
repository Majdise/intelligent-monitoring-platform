import { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'http://localhost:8000';

function App() {
  const [services, setServices] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [realtimeAlerts, setRealtimeAlerts] = useState([]);
  const [isConnected, setIsConnected] = useState(false);

  // Fetch services
  useEffect(() => {
    const fetchServices = async () => {
      try {
        const response = await fetch(`${API_URL}/api/services`);
        const data = await response.json();
        setServices(data);
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    };

    fetchServices();
    const interval = setInterval(fetchServices, 5000);
    return () => clearInterval(interval);
  }, []);

  // Fetch alerts
  useEffect(() => {
    const fetchAlerts = async () => {
      try {
        const response = await fetch(`${API_URL}/api/alerts`);
        const data = await response.json();
        setAlerts(data);
      } catch (error) {
        console.error('Error fetching alerts:', error);
      }
    };

    fetchAlerts();
    const interval = setInterval(fetchAlerts, 5000);
    return () => clearInterval(interval);
  }, []);

  // WebSocket connection for real-time alerts
  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/ws/alerts');

    ws.onopen = () => {
      console.log('WebSocket connected');
      setIsConnected(true);
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'incident') {
        setRealtimeAlerts(prev => [data, ...prev].slice(0, 10));
      }
    };

    ws.onclose = () => {
      console.log('WebSocket disconnected');
      setIsConnected(false);
    };

    return () => ws.close();
  }, []);

  const simulateIncident = async (serviceName) => {
    try {
      await fetch(`${API_URL}/api/simulate-incident?service_name=${serviceName}`, {
        method: 'POST'
      });
    } catch (error) {
      console.error('Error simulating incident:', error);
    }
  };

  const getStatusColor = (status) => {
    return status === 'healthy' ? '#10b981' : '#ef4444';
  };

  const getSeverityColor = (severity) => {
    const colors = {
      critical: '#ef4444',
      warning: '#f59e0b',
      info: '#3b82f6'
    };
    return colors[severity] || '#6b7280';
  };

  return (
    <div className="app">
      <header className="header">
        <h1>🔍 Intelligent Monitoring Platform</h1>
        <div className="connection-status">
          <span className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></span>
          <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </header>

      <div className="container">
        {/* Services Section */}
        <section className="section">
          <h2>Services Status</h2>
          <div className="services-grid">
            {services.map(service => (
              <div key={service.id} className="service-card">
                <div className="service-header">
                  <h3>{service.name}</h3>
                  <span 
                    className="status-badge"
                    style={{ backgroundColor: getStatusColor(service.status) }}
                  >
                    {service.status}
                  </span>
                </div>
                <div className="service-info">
                  <p>Uptime: {service.uptime}%</p>
                  <p>Last Check: {new Date(service.last_check * 1000).toLocaleTimeString()}</p>
                </div>
                <button 
                  className="btn-simulate"
                  onClick={() => simulateIncident(service.name)}
                >
                  Simulate Incident
                </button>
              </div>
            ))}
          </div>
        </section>

        {/* Active Alerts Section */}
        <section className="section">
          <h2>Active Alerts</h2>
          <div className="alerts-list">
            {alerts.length === 0 ? (
              <p className="no-alerts">No active alerts</p>
            ) : (
              alerts.map(alert => (
                <div key={alert.id} className="alert-card">
                  <div 
                    className="alert-severity"
                    style={{ backgroundColor: getSeverityColor(alert.severity) }}
                  >
                    {alert.severity}
                  </div>
                  <div className="alert-content">
                    <h4>{alert.service}</h4>
                    <p>{alert.message}</p>
                    <small>{new Date(alert.timestamp * 1000).toLocaleString()}</small>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>

        {/* Real-time Incidents Section */}
        <section className="section">
          <h2>Real-time Incidents Stream</h2>
          <div className="incidents-stream">
            {realtimeAlerts.length === 0 ? (
              <p className="no-alerts">Waiting for incidents...</p>
            ) : (
              realtimeAlerts.map((incident, index) => (
                <div key={index} className="incident-item">
                  <span 
                    className="incident-badge"
                    style={{ backgroundColor: getSeverityColor(incident.severity) }}
                  >
                    {incident.severity}
                  </span>
                  <div className="incident-details">
                    <strong>{incident.service}</strong>
                    <span>{incident.message}</span>
                    <small>{new Date(incident.timestamp * 1000).toLocaleTimeString()}</small>
                  </div>
                </div>
              ))
            )}
          </div>
        </section>
      </div>
    </div>
  );
}

export default App;