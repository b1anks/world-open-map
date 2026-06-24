import random
import time
from typing import Any

import requests

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

_cache: dict[str, tuple[float, Any]] = {}
_CACHE_TTL_SECONDS = 60


def _read_json(url: str) -> Any | None:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def _get_cached(key: str, loader: Any, ttl: int = _CACHE_TTL_SECONDS) -> Any:
    now = time.time()
    cached = _cache.get(key)
    if cached and now - cached[0] < ttl:
        return cached[1]
    value = loader()
    _cache[key] = (now, value)
    return value


def _build_flight_features() -> list[dict[str, Any]]:
    payload = _get_cached("flights", lambda: _read_json("https://opensky-network.org/api/states/all"))
    if not payload or not payload.get("states"):
        return [feature for feature in sample_features if feature["type"] == "flight"]

    features: list[dict[str, Any]] = []
    for state in payload["states"][:20]:
        icao24 = state[0] if len(state) > 0 else None
        callsign = (state[1] or "").strip() if len(state) > 1 else ""
        longitude = state[5] if len(state) > 5 else None
        latitude = state[6] if len(state) > 6 else None
        altitude = state[7] if len(state) > 7 else None
        on_ground = bool(state[8]) if len(state) > 8 else False
        velocity = state[9] if len(state) > 9 else None

        if not icao24 or latitude is None or longitude is None:
            continue

        features.append(
            {
                "id": f"flight-{icao24}",
                "type": "flight",
                "name": callsign or f"Flight {icao24}",
                "lat": latitude,
                "lng": longitude,
                "altitude": altitude,
                "velocity": velocity,
                "status": "On ground" if on_ground else "Cruising",
                "source": "OpenSky Network",
            }
        )

    return features or [feature for feature in sample_features if feature["type"] == "flight"]


def _build_satellite_features() -> list[dict[str, Any]]:
    payload = _get_cached("satellites", lambda: _read_json("https://api.wheretheiss.at/v1/satellites/25544"))
    if payload:
        return [
            {
                "id": "satellite-iss",
                "type": "satellite",
                "name": "ISS",
                "lat": payload.get("latitude"),
                "lng": payload.get("longitude"),
                "altitude": payload.get("altitude"),
                "velocity": payload.get("velocity"),
                "status": "Orbiting",
                "source": "Where the ISS at",
            }
        ]

    return [feature for feature in sample_features if feature["type"] == "satellite"]


def _build_camera_features() -> list[dict[str, Any]]:
    return [
        {
            "id": "camera-times-square",
            "type": "camera",
            "name": "Times Square Public Cam",
            "lat": 40.7580,
            "lng": -73.9855,
            "status": "Live",
            "camera_type": "city",
            "source": "public-webcam",
            "feed_url": "https://www.earthcam.com/usa/newyork/timessquare/",
        },
        {
            "id": "camera-sydney",
            "type": "camera",
            "name": "Sydney Harbor Cam",
            "lat": -33.8688,
            "lng": 151.2093,
            "status": "Live",
            "camera_type": "harbor",
            "source": "public-webcam",
            "feed_url": "https://www.earthcam.com/australia/sydney/",
        },
        {
            "id": "camera-london",
            "type": "camera",
            "name": "London Eye Cam",
            "lat": 51.5033,
            "lng": -0.1195,
            "status": "Live",
            "camera_type": "landmark",
            "source": "public-webcam",
            "feed_url": "https://www.earthcam.com/uk/london/londoneye/",
        },
    ]


def _build_ground_features() -> list[dict[str, Any]]:
    cities = [
        ("Seattle", 47.6062, -122.3321),
        ("Berlin", 52.5200, 13.4050),
        ("Sydney", -33.8688, 151.2093),
        ("Nairobi", -1.2921, 36.8219),
    ]
    features: list[dict[str, Any]] = []
    for name, lat, lng in cities:
        weather_payload = _get_cached(
            f"weather-{name}",
            lambda lat=lat, lng=lng: _read_json(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lng}&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
            ),
        )
        if weather_payload and weather_payload.get("current"):
            current = weather_payload["current"]
            temperature = current.get("temperature_2m")
            humidity = current.get("relative_humidity_2m")
            wind_speed = current.get("wind_speed_10m")
            features.append(
                {
                    "id": f"ground-{name.lower()}",
                    "type": "ground",
                    "name": f"{name} Weather",
                    "lat": lat,
                    "lng": lng,
                    "status": "Clear" if temperature is not None and temperature < 25 else "Active",
                    "temperature": temperature,
                    "humidity": humidity,
                    "wind_speed": wind_speed,
                    "source": "Open-Meteo",
                }
            )

    return features or [feature for feature in sample_features if feature["type"] == "ground"]


def get_live_map_features() -> list[dict[str, Any]]:
    return [
        * _build_flight_features(),
        * _build_satellite_features(),
        * _build_camera_features(),
        * _build_ground_features(),
    ]


def get_features_for_kind(kind: str) -> list[dict[str, Any]]:
    return [feature for feature in get_live_map_features() if feature["type"] == kind]


def get_map_features() -> list[dict[str, Any]]:
    return get_live_map_features()


def get_feature_summary() -> dict[str, Any]:
    features = get_live_map_features()
    counts = {"flight": 0, "satellite": 0, "camera": 0, "ground": 0}
    for feature in features:
        counts[feature["type"]] += 1
    return {"counts": counts, "updated": "now"}


def get_live_update() -> dict[str, Any]:
    features = get_live_map_features()
    feature = random.choice(features)
    update = dict(feature)
    update["lat"] = round(update["lat"] + random.uniform(-0.2, 0.2), 4)
    update["lng"] = round(update["lng"] + random.uniform(-0.2, 0.2), 4)
    return {"type": "update", "data": update}


def create_sample_features(kind: str) -> list[dict[str, Any]]:
    return [feature for feature in sample_features if feature["type"] == kind]
