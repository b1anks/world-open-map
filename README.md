# World Open Map

A comprehensive open-source platform for visualizing real-time global data on a unified map, including:

- Live flight tracking
- Satellite positions
- Public camera locations and feeds
- Ground sensor data (weather, air quality, seismic)
- Real-time WebSocket updates

## Features

- Interactive 2D map built with Leaflet
- FastAPI backend with REST and WebSocket APIs
- Docker-based local setup
- Sample and live-ready data adapters
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

## Project structure

```text
world-open-map/
├── backend/
├── frontend/
├── docker-compose.yml
└── README.md
```

## Next steps

- Add real API keys for OpenSky / OpenWeatherMap / WAQI
- Replace sample markers with live feeds
- Add filtering by source and time window
- Expand to 3D globe support with CesiumJS
