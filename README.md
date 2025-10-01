# 🔍 Intelligent Monitoring Platform

AI-powered monitoring and incident response system built with FastAPI, React, Prometheus, and Grafana.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![React](https://img.shields.io/badge/React-18.2-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📋 Overview

A production-grade observability platform that combines modern monitoring tools with AI-powered incident analysis. The system demonstrates full-stack development, real-time communication, and DevOps best practices suitable for enterprise environments.

### Key Features

- **Real-time Monitoring**: Track service health and performance metrics using Prometheus
- **Live Dashboard**: React-based UI with WebSocket integration for instant updates
- **AI Analysis**: Claude API integration for intelligent incident analysis and recommendations
- **Alert Management**: Configurable alerting with Alertmanager
- **Visual Analytics**: Grafana dashboards for metrics visualization
- **Automated Response**: Python automation scripts for incident remediation
- **Containerized**: Complete Docker Compose setup for easy deployment

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   React     │────▶│   FastAPI    │────▶│ Prometheus  │
│  Frontend   │     │   Backend    │     │   Metrics   │
└─────────────┘     └──────────────┘     └─────────────┘
       │                    │                     │
       │                    │                     ▼
       │                    │             ┌─────────────┐
       │                    │             │   Grafana   │
       │                    │             │ Dashboards  │
       │                    │             └─────────────┘
       │                    ▼
       │            ┌──────────────┐
       └───────────▶│ PostgreSQL   │
       WebSocket    │   Database   │
                    └──────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker Desktop
- Git
- Claude API key (optional for AI features)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Majdise/intelligent-monitoring-platform.git
   cd intelligent-monitoring-platform
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your Claude API key
   ```

3. **Start all services**
   ```bash
   docker-compose up --build
   ```

4. **Access the applications**
   - Frontend Dashboard: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

## 📊 Usage

### Simulating Incidents

1. Open the dashboard at http://localhost:5173
2. Click "Simulate Incident" on any service
3. Watch real-time incident updates in the stream
4. Check Prometheus for metric changes
5. View alerts in Grafana

### Running Tests

```bash
# Enter the backend container
docker exec -it monitoring_backend bash

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database interactions
- **Prometheus Client**: Metrics collection
- **Anthropic Claude API**: AI-powered analysis
- **Pytest**: Testing framework

### Frontend
- **React 18**: UI library
- **WebSocket**: Real-time communication
- **Vite**: Build tool and dev server

### Infrastructure
- **Docker & Docker Compose**: Containerization
- **Prometheus**: Metrics and monitoring
- **Grafana**: Visualization and dashboards
- **Alertmanager**: Alert routing and management
- **PostgreSQL**: Persistent storage
- **Redis**: Caching layer

## 📁 Project Structure

```
intelligent-monitoring-platform/
├── backend/
│   ├── app/
│   │   └── main.py              # FastAPI application
│   ├── tests/
│   │   └── test_api.py          # API tests
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── App.css              # Styling
│   │   └── main.jsx             # Entry point
│   ├── Dockerfile
│   ├── package.json
│   └── index.html
├── monitoring/
│   ├── prometheus/
│   │   ├── prometheus.yml       # Prometheus config
│   │   └── alert_rules.yml      # Alert definitions
│   ├── grafana/
│   │   └── dashboards/          # Dashboard configs
│   └── alertmanager/
│       └── alertmanager.yml     # Alert routing
├── docker-compose.yml
├── .env.example
└── README.md
```

## 🔧 Configuration

### Environment Variables

```bash
# Claude API (optional)
CLAUDE_API_KEY=your_api_key_here

# Database
DATABASE_URL=postgresql://admin:admin123@localhost:5432/monitoring

# Redis
REDIS_URL=redis://localhost:6379
```

### Custom Metrics

Add custom metrics in `backend/app/main.py`:

```python
from prometheus_client import Counter, Histogram, Gauge

CUSTOM_METRIC = Counter(
    'custom_metric_total',
    'Description of metric',
    ['label1', 'label2']
)
```

## 📈 Monitoring

### Available Metrics

- `http_requests_total`: Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds`: Request latency histogram
- `active_alerts_total`: Number of active alerts
- `service_health_status`: Service health (1=healthy, 0=unhealthy)

### Prometheus Queries

```promql
# Request rate
rate(http_requests_total[5m])

# 95th percentile latency
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

## 🧪 Testing

The project includes comprehensive tests for all API endpoints:

- Health checks
- Metrics collection
- Service status
- Incident simulation
- WebSocket connections

Run tests with:
```bash
docker exec -it monitoring_backend pytest -v
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request


## 🙏 Acknowledgments

- Built as a portfolio project demonstrating modern DevOps practices
- Inspired by production monitoring systems
- Uses industry-standard open-source tools

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [React Documentation](https://react.dev/)
- [Docker Documentation](https://docs.docker.com/)

## 🐛 Known Issues

- Database connection attempts may show harmless errors in logs during startup
- First Docker build may take 5-10 minutes to download all images

## 🔮 Future Enhancements

- [ ] Add authentication and user management
- [ ] Implement advanced AI-powered root cause analysis
- [ ] Add email/Slack notification integrations
- [ ] Create automated remediation workflows
- [ ] Add historical incident tracking and analytics
- [ ] Implement distributed tracing with OpenTelemetry
- [ ] Add support for Kubernetes deployment
- [ ] Create mobile-responsive dashboard views

---

**⭐ If you find this project useful, please consider giving it a star on GitHub!**