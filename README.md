# World Open Map

A comprehensive open-source platform for visualizing real-time global data on a unified map, including:

- Live flight tracking from OpenSky
- Satellite positions from the ISS tracking endpoint
- Public camera metadata and public webcam locations
- Ground weather sensor data from Open-Meteo
- Real-time WebSocket updates
- A 2D map and a 3D globe view with source/type filtering
- SQLite-backed persistence for the latest loaded features

## Features

- Interactive 2D map built with Leaflet
- 3D globe view built with react-globe.gl
- FastAPI backend with REST and WebSocket APIs
- Docker-based local setup
- Live data adapters with graceful fallbacks to sample data and persisted markers
- Responsive UI with source and layer filtering

## Quick start

### With Docker Compose

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:3000
- Backend: http://localhost:8000/docs

### Local development

Backend:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

## API overview

- `GET /health`
- `GET /api/overview`
- `GET /api/flights`
- `GET /api/satellites`
- `GET /api/cameras`
- `GET /api/ground-sensors`
- `GET /api/map/bounds?marker_type=flight&source=OpenSky%20Network`
- `WS /ws/live`

## Notes

- The project uses live public endpoints where available and falls back to curated sample markers or persisted markers when a provider is unreachable.
- The latest loaded features are stored locally in SQLite to support quick reloads and simple persistence.
