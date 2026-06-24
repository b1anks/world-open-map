import asyncio
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from app.database import init_db
from app.services.data_service import get_feature_summary, get_features_for_kind, get_live_update, get_map_features

load_dotenv()

app = FastAPI(title="World Open Map", version="0.1.0")

origins = [origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()


@app.get("/health")
def health() -> dict[str, object]:
    return {"status": "ok", "service": "world-open-map"}


@app.get("/api/overview")
def overview() -> dict[str, object]:
    return get_feature_summary()


@app.get("/api/flights")
def flights(limit: int = 50) -> list[dict[str, object]]:
    return get_features_for_kind("flight")[:limit]


@app.get("/api/satellites")
def satellites(limit: int = 50) -> list[dict[str, object]]:
    return get_features_for_kind("satellite")[:limit]


@app.get("/api/cameras")
def cameras(limit: int = 50) -> list[dict[str, object]]:
    return get_features_for_kind("camera")[:limit]


@app.get("/api/ground-sensors")
def ground_sensors(limit: int = 50) -> list[dict[str, object]]:
    return get_features_for_kind("ground")[:limit]


@app.get("/api/map/bounds")
def map_bounds(
    marker_type: str | None = None,
    source: str | None = None,
    limit: int = Query(200, ge=1, le=500),
) -> list[dict[str, object]]:
    return get_map_features(marker_type=marker_type, source=source, limit=limit)


@app.websocket("/ws/live")
async def live_updates(websocket) -> None:
    await websocket.accept()
    try:
        while True:
            await websocket.send_json(get_live_update())
            await asyncio.sleep(5)
    except Exception:
        await websocket.close()
