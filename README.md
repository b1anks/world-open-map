# World Open Map

A comprehensive open-source platform for visualizing real-time global data on a unified map, including:

- Live flight tracking from OpenSky
- Satellite positions from the ISS tracking endpoint
- Public camera metadata and public webcam locations
- Ground weather sensor data from Open-Meteo
- Real-time WebSocket updates

## Features

- Interactive 2D map built with Leaflet
- FastAPI backend with REST and WebSocket APIs
- Docker-based local setup
- Live data adapters with graceful fallbacks to sample data
- Responsive UI for desktop and mobile

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
- `GET /api/map/bounds`
- `WS /ws/live`

## Notes

- The project now uses live public endpoints where available and falls back to curated sample markers whenever the upstream services are unreachable.
- If you want to add richer camera or satellite data, you can plug in additional provider APIs or a database-backed catalog.
