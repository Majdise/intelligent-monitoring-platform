from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from fastapi.responses import Response
import time
import asyncio
from typing import List
import json

# Create FastAPI app
app = FastAPI(
    title="Intelligent Monitoring Platform",
    description="AI-powered monitoring and incident response system",
    version="1.0.0"
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

ACTIVE_ALERTS = Gauge(
    'active_alerts_total',
    'Number of active alerts'
)

SERVICE_HEALTH = Gauge(
    'service_health_status',
    'Service health status (1=healthy, 0=unhealthy)',
    ['service_name']
)

# WebSocket connection manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

# Middleware to track metrics
@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()
    
    REQUEST_DURATION.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)
    
    return response

# Routes
@app.get("/")
async def root():
    return {
        "message": "Intelligent Monitoring Platform API",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "metrics": "/metrics",
            "alerts": "/api/alerts",
            "services": "/api/services"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": time.time()
    }

@app.get("/metrics")
async def metrics():
    """Prometheus metrics endpoint"""
    return Response(
        content=generate_latest(),
        media_type="text/plain"
    )

@app.get("/api/services")
async def get_services():
    """Get list of monitored services"""
    services = [
        {
            "id": 1,
            "name": "payment-api",
            "status": "healthy",
            "uptime": 99.9,
            "last_check": time.time()
        },
        {
            "id": 2,
            "name": "user-service",
            "status": "healthy",
            "uptime": 99.5,
            "last_check": time.time()
        },
        {
            "id": 3,
            "name": "database",
            "status": "healthy",
            "uptime": 100.0,
            "last_check": time.time()
        }
    ]
    
    # Update Prometheus metrics
    for service in services:
        health_value = 1 if service["status"] == "healthy" else 0
        SERVICE_HEALTH.labels(service_name=service["name"]).set(health_value)
    
    return services

@app.get("/api/alerts")
async def get_alerts():
    """Get active alerts"""
    alerts = [
        {
            "id": 1,
            "severity": "warning",
            "service": "payment-api",
            "message": "High response time detected",
            "timestamp": time.time() - 300,
            "status": "active"
        }
    ]
    
    ACTIVE_ALERTS.set(len(alerts))
    return alerts

@app.post("/api/simulate-incident")
async def simulate_incident(service_name: str):
    """Simulate a service incident"""
    incident = {
        "type": "incident",
        "service": service_name,
        "severity": "critical",
        "message": f"{service_name} is experiencing issues",
        "timestamp": time.time()
    }
    
    # Broadcast to WebSocket clients
    await manager.broadcast(incident)
    
    # Update metrics
    SERVICE_HEALTH.labels(service_name=service_name).set(0)
    ACTIVE_ALERTS.inc()
    
    return incident

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time alerts"""
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and send periodic updates
            await asyncio.sleep(5)
            await websocket.send_json({
                "type": "heartbeat",
                "timestamp": time.time()
            })
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)