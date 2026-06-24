import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import L from 'leaflet';
import Globe from 'react-globe.gl';
import { useEffect, useMemo, useRef } from 'react';

const iconColors = {
  flight: '#38bdf8',
  satellite: '#f59e0b',
  camera: '#ef4444',
  ground: '#34d399',
};

function getIcon(color) {
  return L.divIcon({
    className: 'custom-marker',
    html: `<div style="background:${color};width:12px;height:12px;border-radius:999px;border:2px solid white"></div>`,
    iconSize: [12, 12],
    iconAnchor: [6, 6],
  });
}

function MapView({ items, viewMode }) {
  const globeRef = useRef(null);

  useEffect(() => {
    if (globeRef.current) {
      const controls = globeRef.current.controls();
      controls.autoRotate = true;
      controls.autoRotateSpeed = 0.3;
    }
  }, []);

  const globeData = useMemo(() => items.map((item) => ({ ...item, lat: item.lat, lng: item.lng })), [items]);

  if (viewMode === 'globe') {
    return (
      <div className="globe-shell">
        <Globe
          ref={globeRef}
          globeImageUrl="https://unpkg.com/three-globe/example/img/earth-night.jpg"
          backgroundColor="rgba(0,0,0,0)"
          pointsData={globeData}
          pointLat="lat"
          pointLng="lng"
          pointColor={(item) => iconColors[item.type] || '#ffffff'}
          pointAltitude={0.01}
          pointRadius={0.6}
          labelsData={globeData}
          labelLat="lat"
          labelLng="lng"
          labelText="name"
          labelSize={0.6}
          labelDotRadius={0.4}
          labelColor={() => '#f8fafc'}
        />
      </div>
    );
  }

  return (
    <MapContainer center={[20, 0]} zoom={2} scrollWheelZoom>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      {items.map((item) => (
        <Marker key={item.id} position={[item.lat, item.lng]} icon={getIcon(iconColors[item.type])}>
          <Popup>
            <strong>{item.name}</strong>
            <br />
            Type: {item.type}
            <br />
            Status: {item.status}
            {item.source ? <><br />Source: {item.source}</> : null}
            {item.temperature !== undefined ? <><br />Temp: {item.temperature}°C</> : null}
            {item.humidity !== undefined ? <><br />Humidity: {item.humidity}%</> : null}
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapView;
