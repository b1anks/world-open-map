import { useEffect, useMemo, useState } from 'react';
import MapView from './components/MapView';

const API_URL = import.meta.env.VITE_API_URL || '';
const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws/live';

function App() {
  const [overview, setOverview] = useState(null);
  const [items, setItems] = useState([]);
  const [selectedTypes, setSelectedTypes] = useState({ flight: true, satellite: true, camera: true, ground: true });
  const [selectedSources, setSelectedSources] = useState({});
  const [viewMode, setViewMode] = useState('map');

  useEffect(() => {
    fetch(`${API_URL}/api/overview`)
      .then((res) => res.json())
      .then((data) => setOverview(data));

    fetch(`${API_URL}/api/map/bounds?limit=200`)
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

  useEffect(() => {
    const sources = Array.from(new Set(items.map((item) => item.source).filter(Boolean))).sort();
    setSelectedSources((prev) => {
      const next = { ...prev };
      for (const source of sources) {
        if (!(source in next)) next[source] = true;
      }
      for (const source of Object.keys(next)) {
        if (!sources.includes(source)) delete next[source];
      }
      return next;
    });
  }, [items]);

  const toggleType = (layer) => {
    setSelectedTypes((prev) => ({ ...prev, [layer]: !prev[layer] }));
  };

  const toggleSource = (source) => {
    setSelectedSources((prev) => ({ ...prev, [source]: !prev[source] }));
  };

  const sources = useMemo(() => Array.from(new Set(items.map((item) => item.source).filter(Boolean))).sort(), [items]);

  const visibleItems = useMemo(() => {
    return items.filter((item) => {
      const typeMatches = selectedTypes[item.type];
      const sourceMatches = !item.source || (selectedSources[item.source] ?? true);
      return typeMatches && sourceMatches;
    });
  }, [items, selectedTypes, selectedSources]);

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

      <div className="content-grid">
        <aside className="sidebar">
          <section className="panel">
            <h2>Data layers</h2>
            {Object.entries(selectedTypes).map(([layer, enabled]) => (
              <label key={layer} className={`chip ${enabled ? 'active' : ''}`}>
                <input type="checkbox" checked={enabled} onChange={() => toggleType(layer)} />
                {layer}
              </label>
            ))}
          </section>

          <section className="panel">
            <h2>Sources</h2>
            {sources.map((source) => (
              <label key={source} className={`chip ${selectedSources[source] !== false ? 'active' : ''}`}>
                <input type="checkbox" checked={selectedSources[source] !== false} onChange={() => toggleSource(source)} />
                {source}
              </label>
            ))}
          </section>

          <section className="panel">
            <h2>View mode</h2>
            <div className="view-toggle">
              <button className={viewMode === 'map' ? 'active' : ''} onClick={() => setViewMode('map')}>2D map</button>
              <button className={viewMode === 'globe' ? 'active' : ''} onClick={() => setViewMode('globe')}>3D globe</button>
            </div>
          </section>
        </aside>

        <main className="map-panel">
          <MapView items={visibleItems} viewMode={viewMode} />
        </main>
      </div>
    </div>
  );
}

export default App;
