import { useEffect, useState } from 'react';
import MapView from './components/MapView';

const API_URL = import.meta.env.VITE_API_URL || '';
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/live';

function App() {
  const [overview, setOverview] = useState(null);
  const [items, setItems] = useState([]);
  const [selectedLayers, setSelectedLayers] = useState({ flight: true, satellite: true, camera: true, ground: true });

  useEffect(() => {
    fetch(`${API_URL}/api/overview`)
      .then((res) => res.json())
      .then((data) => setOverview(data));

    fetch(`${API_URL}/api/map/bounds`)
      .then((res) => res.json())
      .then((data) => setItems(data));
  }, []);

  useEffect(() => {
    const socket = new WebSocket(WS_URL);
    socket.onmessage = (event) => {
      const payload = JSON.parse(event.data);
      if (payload?.data) {
        setItems((prev) => {
          const next = prev.filter((item) => item.id !== payload.data.id);
          return [...next, payload.data];
        });
      }
    };

    return () => socket.close();
  }, []);

  const toggleLayer = (layer) => {
    setSelectedLayers((prev) => ({ ...prev, [layer]: !prev[layer] }));
  };

  const visibleItems = items.filter((item) => selectedLayers[item.type]);

  return (
    <div className="app-shell">
      <header className="topbar">
        <div>
          <h1>World Open Map</h1>
          <p>Unified view of live flight, satellite, camera and ground data</p>
        </div>
        <div className="stats">
          <div className="stat-card">Flights <strong>{overview?.counts?.flight ?? 0}</strong></div>
          <div className="stat-card">Satellites <strong>{overview?.counts?.satellite ?? 0}</strong></div>
          <div className="stat-card">Cameras <strong>{overview?.counts?.camera ?? 0}</strong></div>
          <div className="stat-card">Ground <strong>{overview?.counts?.ground ?? 0}</strong></div>
        </div>
      </header>

      <section className="controls">
        {Object.entries(selectedLayers).map(([layer, enabled]) => (
          <label key={layer} className={`chip ${enabled ? 'active' : ''}`}>
            <input type="checkbox" checked={enabled} onChange={() => toggleLayer(layer)} />
            {layer}
          </label>
        ))}
      </section>

      <MapView items={visibleItems} />
    </div>
  );
}

export default App;
