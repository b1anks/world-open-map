import os
from datetime import datetime
import json

from sqlalchemy import create_engine, Column, String, Float, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./world_open_map.db")
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class MarkerRecord(Base):
    __tablename__ = "marker_records"

    id = Column(String, primary_key=True)
    type = Column(String, index=True, nullable=False)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    altitude = Column(Float, nullable=True)
    status = Column(String, nullable=True)
    source = Column(String, nullable=True)
    camera_type = Column(String, nullable=True)
    feed_url = Column(String, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed = Column(Float, nullable=True)
    extra_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self) -> dict[str, object]:
        data = {
            "id": self.id,
            "type": self.type,
            "name": self.name,
            "lat": self.lat,
            "lng": self.lng,
            "altitude": self.altitude,
            "status": self.status,
            "source": self.source,
            "camera_type": self.camera_type,
            "feed_url": self.feed_url,
            "temperature": self.temperature,
            "humidity": self.humidity,
            "wind_speed": self.wind_speed,
        }
        extra_payload = json.loads(self.extra_json or "{}")
        return {**data, **extra_payload}


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def upsert_markers(features: list[dict[str, object]]) -> None:
    if not features:
        return

    session = SessionLocal()
    try:
        for feature in features:
            record = session.get(MarkerRecord, str(feature["id"]))
            if record is None:
                record = MarkerRecord(id=str(feature["id"]))

            record.type = str(feature.get("type", "unknown"))
            record.name = str(feature.get("name", "Unnamed"))
            record.lat = float(feature.get("lat", 0))
            record.lng = float(feature.get("lng", 0))
            record.altitude = feature.get("altitude")
            record.status = feature.get("status")
            record.source = feature.get("source")
            record.camera_type = feature.get("camera_type")
            record.feed_url = feature.get("feed_url")
            record.temperature = feature.get("temperature")
            record.humidity = feature.get("humidity")
            record.wind_speed = feature.get("wind_speed")

            safe_keys = {
                "id",
                "type",
                "name",
                "lat",
                "lng",
                "altitude",
                "status",
                "source",
                "camera_type",
                "feed_url",
                "temperature",
                "humidity",
                "wind_speed",
            }
            extra_payload = {key: value for key, value in feature.items() if key not in safe_keys}
            record.extra_json = json.dumps(extra_payload, default=str)
            session.merge(record)

        session.commit()
    finally:
        session.close()


def list_markers(marker_type: str | None = None, source: str | None = None, limit: int = 200) -> list[dict[str, object]]:
    session = SessionLocal()
    try:
        query = session.query(MarkerRecord)
        if marker_type:
            query = query.filter(MarkerRecord.type == marker_type)
        if source:
            query = query.filter(MarkerRecord.source == source)
        records = query.order_by(MarkerRecord.updated_at.desc()).limit(limit).all()
        return [record.to_dict() for record in records]
    finally:
        session.close()
