import { MapContainer, Marker, Popup, TileLayer } from 'react-leaflet';
import L from 'leaflet';

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

function MapView({ items }) {
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
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default MapView;
