import random
from typing import Any

sample_features: list[dict[str, Any]] = [
    {"id": "flight-1", "type": "flight", "name": "AAL 123", "lat": 40.7128, "lng": -74.0060, "altitude": 10800, "status": "Cruising"},
    {"id": "flight-2", "type": "flight", "name": "BAW 777", "lat": 51.5074, "lng": -0.1278, "altitude": 10668, "status": "Approaching"},
    {"id": "flight-3", "type": "flight", "name": "SWA 200", "lat": 34.0522, "lng": -118.2437, "altitude": 9753, "status": "Cruising"},
    {"id": "satellite-1", "type": "satellite", "name": "ISS", "lat": 39.0, "lng": -97.0, "altitude": 420, "status": "Orbiting"},
    {"id": "satellite-2", "type": "satellite", "name": "Starlink-56", "lat": 10.0, "lng": 20.0, "altitude": 550, "status": "Orbiting"},
    {"id": "camera-1", "type": "camera", "name": "Downtown CCTV", "lat": 47.6062, "lng": -122.3321, "altitude": 0, "status": "Live"},
    {"id": "camera-2", "type": "camera", "name": "Harbor Cam", "lat": 25.2048, "lng": 55.2708, "altitude": 0, "status": "Live"},
    {"id": "ground-1", "type": "ground", "name": "Seattle Weather", "lat": 47.6062, "lng": -122.3321, "altitude": 0, "status": "Clear"},
    {"id": "ground-2", "type": "ground", "name": "Air Quality Berlin", "lat": 52.5200, "lng": 13.4050, "altitude": 0, "status": "Moderate"},
]


def create_sample_features(kind: str) -> list[dict[str, object]]:
    return [feature for feature in sample_features if feature["type"] == kind]


def get_map_features() -> list[dict[str, object]]:
    return sample_features


def get_feature_summary() -> dict[str, object]:
    counts = {"flight": 0, "satellite": 0, "camera": 0, "ground": 0}
    for feature in sample_features:
        counts[feature["type"]] += 1
    return {"counts": counts, "updated": "now"}


def get_live_update() -> dict[str, object]:
    feature = random.choice(sample_features)
    feature = dict(feature)
    feature["lat"] = round(feature["lat"] + random.uniform(-0.5, 0.5), 4)
    feature["lng"] = round(feature["lng"] + random.uniform(-0.5, 0.5), 4)
    return {"type": "update", "data": feature}
